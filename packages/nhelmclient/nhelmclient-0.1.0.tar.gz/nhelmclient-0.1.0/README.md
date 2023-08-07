nHelmClient
===========

The Helm Client Library.

Features:
* get values from charts (helm show values)
* check deployment (helm status)
* install (helm install)
* call other Helm commands


Example
-------

```
from nhelmclient import Configuration, HelmClient

configuration = Configuration()
helm = HelmClient(configuration)
helm.install(release_name, repo_url, chart)
```
