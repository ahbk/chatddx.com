from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path(
        settings.APP_ROOT,
        include(
            [
                path("admin/", admin.site.urls),
                path("", include("api.urls")),
            ]
        ),
    )
] + staticfiles_urlpatterns()
