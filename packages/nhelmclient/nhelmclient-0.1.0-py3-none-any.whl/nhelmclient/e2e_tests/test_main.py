"""
Copyright 2023 nMachine.io
"""
import unittest

from nhelmclient import Configuration, HelmClient, HelmException


class TestHelmClient(unittest.TestCase):
    """E2E tests for Broker, Configuration"""

    def test_show_values(self) -> None:
        """Tests showing default values."""
        client = HelmClient(Configuration())
        values = client.show_values(
            "https://prometheus-community.github.io/helm-charts", "prometheus"
        )

        # dict with values is huge, so check only
        # if some keys exists
        self.assertTrue("rbac" in values)
        self.assertTrue("serviceAccounts" in values)

    def test_install(self) -> None:
        """Install prometheus."""
        client = HelmClient(Configuration())
        release_name = "e2e-test-prometheus"
        try:
            ret = client.is_deployed(release_name)
            self.skipTest(
                "e2e-test-prometheus already installed, delete it or use empty cluster"
            )
        except HelmException as ex:
            if ex.message != f"Release {release_name} not found":
                raise

        client.install(
            release_name,
            "https://prometheus-community.github.io/helm-charts",
            "prometheus",
        )
        ret = client.is_deployed(release_name)
        self.assertEqual(ret["info"]["status"], "deployed")
