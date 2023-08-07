"""
Copyright 2023 nMachine.io
"""
from __future__ import annotations

import json
import logging
import os
import subprocess
import tempfile
from typing import Any, List, Optional, Tuple

import yaml

HELM_BIN_SEARCH_PATHS = ("./helm", "/usr/bin/helm", "/usr/local/bin/helm")


class HelmException(Exception):
    """Exception raised for errors returned by Helm.

    Attributes:
        code - exit code from Helm
        message - output from the command or error message
    """

    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(self.message)


class Configuration:
    """Configuration for HelmClient"""

    def __init__(
        self,
        token: Optional[str] = None,
        api_server: Optional[str] = None,
        ca_cert: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        kubeconfig_path: Optional[str] = None,
        cache_path: Optional[str] = None,
        helm_bin: Optional[str] = None,
    ):
        """Configuration for the class HelmClient.

        Args:
            token(str): Bearer token
            api_server(str): address to API server
            ca_cert(str): cluster's certificate authority
            verify_ssl(bool): option to ignore server cert, ignored if ca_cert is passed

            kubeconfig_path(str): path to Kube Config file

            cache_path(str): path to repository cache, random temp dir if None
            helm_bin(str): path to helm binary otherwise it tries to find it
        """

        self.api_server = api_server
        self.token = token
        self.verify_ssl = None
        self.ca_cert = ca_cert
        self.ca_cert_file = None
        self.verify_ssl = verify_ssl
        self.kubeconfig_path = None
        self.cache_path = cache_path
        self.helm_bin = helm_bin

        if not self.cache_path:
            self.cache_path = tempfile.mkdtemp()

        if ca_cert:
            self.ca_cert_file = os.path.join(self.cache_path, "ca.crt")
            with open(self.ca_cert_file, "w", encoding="utf8") as fh:
                fh.write(ca_cert)
            self.verify_ssl = True

        if kubeconfig_path:
            self.kubeconfig_path = kubeconfig_path

        if self.helm_bin is None:
            for path in HELM_BIN_SEARCH_PATHS[1:]:
                if os.path.exists(path):
                    self.helm_bin = path
                    break
            else:
                raise HelmException(-1, "Binary helm not found")

    def to_helm_args(self) -> List[str]:
        """Converts configuration to Helm CLI switches"""
        args: List[str] = []

        def _append(args: List[str], value: Optional[str], arg_name: str) -> None:
            if value:
                args.append(f"{arg_name}={value}")

        _append(args, self.token, "--kube-token")
        _append(args, self.kubeconfig_path, "--kubeconfig")
        _append(args, self.api_server, "--kube-apiserver")
        _append(args, self.cache_path, "--repository-cache")
        if self.cache_path:
            _append(
                args,
                os.path.join(self.cache_path, "repositories.yaml"),
                "--repository-config",
            )

        if self.ca_cert:
            _append(args, self.ca_cert_file, "--kube-ca-file")

        if self.verify_ssl is not None and not self.verify_ssl:
            args.append("--kube-insecure-skip-tls-verify")

        return args


class HelmClient:
    """The client class for Helm. It provides methods to get
    variables for Chart, install and check state.
    """

    def __init__(self, configuration: Configuration):
        """HelmClient constructor, it requires Configuration
        with connection parameters.

        Args:
            configuration (Configuration): configuration for Helm
        """
        self.helm_bin = configuration.helm_bin
        self.helm_args = configuration.to_helm_args()
        self.repositories: dict[str, str] = {}

    def _add_repository(
        self,
        repo_url: str,
        repo_username: Optional[str] = None,
        repo_password: Optional[str] = None,
    ) -> str:
        if repo_url in self.repositories:
            return self.repositories[repo_url]

        auth_repo: List[str] = []
        if repo_password:
            auth_repo.extend(["--password", repo_password])
        if repo_username:
            auth_repo.extend(["--username", repo_username])

        repo_name = f"repo{len(self.repositories)}"

        logging.debug("Adding repo %s as %s", repo_url, repo_name)

        code, result = self.call(["repo", "add", repo_name, repo_url] + auth_repo)
        if code != 0:
            raise HelmException(code, result)

        self.repositories[repo_url] = repo_name
        return repo_name

    def show_values(
        self,
        repo_url: str,
        chart: str,
        repo_username: Optional[str] = None,
        repo_password: Optional[str] = None,
    ) -> Any:
        """Calls 'helm show values' and returns response as
        python structure (it's usually a dict).

        Args:
            repo_url(str): chart repository
            chart (str): chart name
            repo_username(str): chart repository username
            repo_password(str): chart repository password

        Returns:
            chart values
        """

        repo = self._add_repository(repo_url, repo_username, repo_password)

        code, result = self.call(["show", "values", f"{repo}/{chart}"])
        if code != 0:
            raise HelmException(code, result)

        values = yaml.safe_load(result)
        return values

    def is_deployed(self, release_name: str) -> dict:
        """Calls helm status and returns response as a dict
        with status and run-time informations.

        Args:
            release_name (str): release name

        Returns:
            release status
        """

        code, result = self.call(["status", release_name, "--output", "json"])
        if code != 0:
            if "release: not found" in result:
                raise HelmException(code, f"Release {release_name} not found")
            raise HelmException(code, result)
        status = json.loads(result)
        return status

    def install(
        self,
        release_name: str,
        repo_url: str,
        chart: str,
        variables: Optional[dict] = None,
        repo_username: Optional[str] = None,
        repo_password: Optional[str] = None,
    ) -> None:
        """Calls helm install to deploy chart.

        Args:
            release_name (str): release name
            repo_url(str): chart repository
            chart (str): chart name
            repo_username(str): chart repository username
            repo_password(str): chart repository password
        """

        set_arg = []
        if variables:
            arr_vars = [f"{name}={value}" for name, value in variables.items()]
            set_arg = ["--set", ",".join(arr_vars)]

        repo = self._add_repository(repo_url, repo_username, repo_password)

        code, result = self.call(["install", release_name, f"{repo}/{chart}"] + set_arg)
        if code != 0:
            raise HelmException(code, result)

    def call(self, command: List[str]) -> Tuple[int, str]:
        """Calls helm command with arguments, returns exit code and output.

        Args:
            command (List[str]): command with args

        Returns:
            exit_code, message

        """
        command_to_exe = (
            [
                self.helm_bin,
            ]
            + command
            + self.helm_args
        )
        logging.debug("Call %s", command_to_exe)
        with subprocess.Popen(
            command_to_exe,  # type: ignore
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            errors="replace",
            shell=False,
        ) as process:
            outputs = []
            if process.stdout is not None:
                while True:
                    output = process.stdout.readline()
                    if output == "" and process.poll() is not None:
                        break
                    outputs.append(output)
            exit_code = process.poll()
            if exit_code is None:
                exit_code = 0
            return exit_code, "".join(outputs)
