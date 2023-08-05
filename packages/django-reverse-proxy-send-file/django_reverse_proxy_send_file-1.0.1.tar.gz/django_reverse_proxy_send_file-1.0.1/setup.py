# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['reverse_proxy_send_file']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-reverse-proxy-send-file',
    'version': '1.0.1',
    'description': 'Storage and View to send X-Accel-Redirect (or X-Sendfile) header to nginx (or apache) reverse-proxy',
    'long_description': '![license](https://img.shields.io/pypi/l/django-reverse-proxy-send-file?style=flat-square)\n![status](https://img.shields.io/pypi/status/django-reverse-proxy-send-file?style=flat-square)\n![version](https://img.shields.io/pypi/v/django-reverse-proxy-send-file?style=flat-square)\n![pyversion](https://img.shields.io/pypi/pyversions/django-reverse-proxy-send-file?style=flat-square)\n\n# django-reverse-proxy-send-file\n\n## Sumary\n\nThis package help writing views which use the `X-Accel-Redirect` header to have `nginx` serving files but still allow a permission check at django\'s side\n\n## Intro\n\nThe `storage.ReverseProxySendFileStorageFileSystemStorage` class is a drop-in replacement of django\'s `FileSystemStorage` which make FileField (or ImageField) url to use the `REVERSE_PROXY_SENDFILE_MEDIA_URL` settings base url instead of MEDIA_URL\n\nThe `storage.ReverseProxySendFileStorageMixin` allow you to apply the overriden `base_url` on any storage class\n\nThe `ReverseProxySendFileView` class handle GET request and return an empty response with nginx\'s `X-Accel-Redirect` header to order nginx to return the file at given path. The `REVERSE_PROXY_SENDFILE_MEDIA_ROOT` setting must be defined in the nginx context si it can find the file\n\nThe `ReverseProxySendFileView` can be overrided to implement a custom `check_permission` method which verify is the current user is allowed to download the resource.\n\n## Installation\n\nInstall the `django-reverse-proxy-send-file` pypi package.\nex:\n* `poetry add django-reverse-proxy-send-file`\n* `pip install django-reverse-proxy-send-file`\n\n## Usage\n\nSee example section bellow\n\n## Settings\n\n### REVERSE_PROXY_SENDFILE_MEDIA_ROOT\n\nDefault to django\'s `MEDIA_ROOT`\n\nBase path in django\'s context where to store media files when uploaded (used by Storage class)\n\n### REVERSE_PROXY_SENDFILE_MEDIA_URL\n\nDefault to `"smedia/"`\n\nURL that handle the resources that should be served by the reverse proxy.\n\n### REVERSE_PROXY_SENDFILE_REVERSE_PROXY_ROOT\n\nDefault to `"smedia/"`\n\nBase path in reverse-proxy\'s context which is sent back to reverse-proxy in header so it can find the file\n\n### REVERSE_PROXY_SENDFILE_MODE\n\nDefault to `"nginx"`\n\nPossible values: `"nginx"` or `"apache"`\n\n`nginx` mode will use `X-Accel-Redirect` header whereas `apache` mode will use `X-Sendfile`\n\n### REVERSE_PROXY_SENDFILE_HEADER_NAME\n\nDefault to `None`\n\nEnter a custom header name. If set this header will be used regardless `REVERSE_PROXY_SENDFILE_MODE` setting.\n\n### REVERSE_PROXY_SENDFILE_DEBUG_SERVE_RESOURCE\n\nDefault to `True`\n\nIn django\'s `DEBUG` mode, the resource is directly served by the dev server.\n\n## Exemple\n\n### `settings.py`\n\n```python\n...\nREVERSE_PROXY_SENDFILE_MEDIA_URL = "smedia/"\nREVERSE_PROXY_SENDFILE_MEDIA_ROOT = "/django_path/to/smedia/"\nREVERSE_PROXY_SENDFILE_REVERSE_PROXY_ROOT = "/nginx_path/to/smedia/"\n...\n```\n\n### `models.py`\n\n```python\nfrom django.contrib.auth.models import User\n\nfrom reverse_proxy_send_file.storage import ReverseProxySendFileStorageFileSystemStorage\n\nclass MyModel(models.Model):\n    ...\n    user = models.ForeignKey(User, on_delete=models.CASCADE)\n    my_file = models.FileField(\n        "My file",\n        upload_to="my_files/",\n        storage=ReverseProxySendFileStorageFileSystemStorage(),\n    )\n    ...\n```\n\n### `views.py`\n\n```python\nfrom django.http import Http404\n\nfrom reverse_proxy_send_file.views import ReverseProxySendFileView\n\nclass ReverseProxySendFileMyFileView(ReverseProxySendFileView):\n    def check_permission(self, request, resource_url, *args, **kwargs):\n        obj_qs = MyModel.objects.filter(my_file=resource_url)\n        if not obj_qs.exists():\n            raise Http404()\n        return obj_qs.filter(user=request.user).exists()\n```\n\n### `urls.py`\n\n```python\nfrom django.conf import settings\nfrom views import ReverseProxySendFileMyFileView\n\nurlpatterns = [\n    ...\n    re_path(\n        settings.REVERSE_PROXY_SENDFILE_MEDIA_URL + "(?P<resource_url>my_files/.*)$",\n        views.ReverseProxySendFileMyFileView.as_view(),\n        name="reverse_proxy_send_file",\n    ),\n    ...\n]\n```\n1. User upload file. The file is stored in `/django_path/to/smedia/my_files/blop.pdf`\n1. User access `/smedia/my_files/blop.pdf`\n2. A django request is performed and it check file access permission for current user (in check_permission).\n3. - If the user is allowed return a HTTP response with header : `X-Accel-Redirect=/nginx_path/to/smedia/my_files/blop.pdf` (Nginx will use it to send the file to the client)\n   - If the file os not found return a `404 note found`.\n   - If the user id forbidden, return a `403 response forbidden`\n\n\n## Setup dev environnement\n\n```bash\n# install dev dependencies\npoetry install --no-root\n# install git pre-commit\npre-commit install\n```\n\n## Run tests\n\nUse `tox` command to run all tests on all supported python versions \nExamples:\n\n```bash\ntox\ntox -e py38-django40\ntox -f py39\n```\n## Build package and publish on PyPI\n\nChange version number in `pyproject.toml`\n\n```bash\npoetry build\npoetry publish\n```\n',
    'author': 'Fabs',
    'author_email': 'fabien.michel@hespul.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://bitbucket.org/hespul/django-reverse-proxy-send-file',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
