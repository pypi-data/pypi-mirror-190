from http import HTTPStatus

from django.conf import settings as django_settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views import View
from django.views.static import serve

from reverse_proxy_send_file import settings as rpr_settings


class ReverseProxySendFileView(View):
    def get(self, request, resource_url, *args, **kwargs):
        if not self.check_permission(request, resource_url):
            return HttpResponseForbidden()

        if rpr_settings.get_debug_serve_resource() and django_settings.DEBUG:
            return serve(request, resource_url, document_root=rpr_settings.get_media_root())

        response = HttpResponse(status=HTTPStatus.OK)
        response["Content-Type"] = ""

        reverse_proxy_resource_path = self.get_reverse_proxy_path(request, resource_url)
        header = rpr_settings.get_header_name()
        if not header:
            if rpr_settings.get_mode() == "apache":
                header = "X-Sendfile"
            else:  # nginx
                header = "X-Accel-Redirect"

        response[header] = reverse_proxy_resource_path

        return response

    def get_reverse_proxy_path(self, request, resource_url):
        reverse_proxy_send_file_root = rpr_settings.get_reverse_proxy_root()
        if not reverse_proxy_send_file_root.endswith("/"):
            reverse_proxy_send_file_root += "/"
        return reverse_proxy_send_file_root + resource_url

    def check_permission(self, request, resource_url):
        return True
