![Bitbucket Pipelines](https://img.shields.io/bitbucket/pipelines/hespul/django-reverse-proxy-send-file/master?style=flat-square)
![license](https://img.shields.io/pypi/l/django-reverse-proxy-send-file?style=flat-square)
![status](https://img.shields.io/pypi/status/django-reverse-proxy-send-file?style=flat-square)
![version](https://img.shields.io/pypi/v/django-reverse-proxy-send-file?style=flat-square)
![pyversion](https://img.shields.io/pypi/pyversions/django-reverse-proxy-send-file?style=flat-square)

# django-reverse-proxy-send-file

## Sumary

This package help writing views which use the `X-Accel-Redirect` header to have `nginx` serving files but still allow a permission check at django's side

## Intro

The `storage.ReverseProxySendFileFileSystemStorage` class is a drop-in replacement of django's `FileSystemStorage` which make FileField (or ImageField) url to use the `REVERSE_PROXY_SENDFILE_MEDIA_URL` settings base url instead of MEDIA_URL

The `storage.ReverseProxySendFileStorageMixin` allow you to apply the overriden `base_url` on any storage class

The `ReverseProxySendFileView` class handle GET request and return an empty response with nginx's `X-Accel-Redirect` header to order nginx to return the file at given path. The `REVERSE_PROXY_SENDFILE_MEDIA_ROOT` setting must be defined in the nginx context si it can find the file

The `ReverseProxySendFileView` can be overrided to implement a custom `check_permission` method which verify is the current user is allowed to download the resource.

## Installation

Install the `django-reverse-proxy-send-file` pypi package.
ex:

- `poetry add django-reverse-proxy-send-file`
- `pip install django-reverse-proxy-send-file`

## Usage

See example section bellow

## Settings

| Name                                        | Default     | Description                                                                                                                             |
| ------------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| REVERSE_PROXY_SENDFILE_MEDIA_ROOT           | MEDIA_ROOT  | Base path in django's context where to store media files when uploaded (used by Storage class)                                          |
| REVERSE_PROXY_SENDFILE_MEDIA_URL            | `"smedia/"` | URL that handle the resources that should be served by the reverse proxy.                                                               |
| REVERSE_PROXY_SENDFILE_REVERSE_PROXY_ROOT   | `"smedia/"` | Base path in reverse-proxy's context which is sent back to reverse-proxy in header so it can find the file                              |
| REVERSE_PROXY_SENDFILE_MODE                 | `"nginx"`   | Possible values: `"nginx"` or `"apache"`. <br> `nginx` mode will use `X-Accel-Redirect` header.<br> `apache` mode will use `X-Sendfile` |
| REVERSE_PROXY_SENDFILE_HEADER_NAME          | `None`      | A custom header name. If set this header will be used regardless `REVERSE_PROXY_SENDFILE_MODE` setting.                                 |
| REVERSE_PROXY_SENDFILE_DEBUG_SERVE_RESOURCE | `True`      | In django's `DEBUG` mode, the resource is directly served by the dev server.                                                            |

## Exemple

### `settings.py`

```python
...
REVERSE_PROXY_SENDFILE_MEDIA_URL = "smedia/"
REVERSE_PROXY_SENDFILE_MEDIA_ROOT = "/django_path/to/smedia/"
REVERSE_PROXY_SENDFILE_REVERSE_PROXY_ROOT = "/nginx_path/to/smedia/"
...
```

### `models.py`

```python
from django.contrib.auth.models import User

from reverse_proxy_send_file.storage import ReverseProxySendFileFileSystemStorage

class MyModel(models.Model):
    ...
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_file = models.FileField(
        "My file",
        upload_to="my_files/",
        storage=ReverseProxySendFileFileSystemStorage(),
    )
    ...
```

### `views.py`

```python
from django.http import Http404

from reverse_proxy_send_file.views import ReverseProxySendFileView

class ReverseProxySendFileMyFileView(ReverseProxySendFileView):
    def check_permission(self, request, resource_url, *args, **kwargs):
        obj_qs = MyModel.objects.filter(my_file=resource_url)
        if not obj_qs.exists():
            raise Http404()
        return obj_qs.filter(user=request.user).exists()
```

### `urls.py`

```python
from django.conf import settings
from views import ReverseProxySendFileMyFileView

urlpatterns = [
    ...
    re_path(
        settings.REVERSE_PROXY_SENDFILE_MEDIA_URL + "(?P<resource_url>my_files/.*)$",
        views.ReverseProxySendFileMyFileView.as_view(),
        name="reverse_proxy_send_file",
    ),
    ...
]
```

1. User upload file. The file is stored in `/django_path/to/smedia/my_files/blop.pdf`
1. User access `/smedia/my_files/blop.pdf`
1. A django request is performed and it check file access permission for current user (in check_permission).
1. - If the user is allowed return a HTTP response with header : `X-Accel-Redirect=/nginx_path/to/smedia/my_files/blop.pdf` (Nginx will use it to send the file to the client)
   - If the file os not found return a `404 note found`.
   - If the user id forbidden, return a `403 response forbidden`

## Setup dev environnement

```bash
# install dev dependencies
poetry install --no-root
# install git pre-commit
pre-commit install
```

## Run tests

Use `tox` command to run all tests on all supported python versions
Examples:

```bash
tox
tox -e py38-django40
tox -f py39
```

## Build package and publish on PyPI

Change version number in `pyproject.toml`

```bash
poetry build
poetry publish
```
