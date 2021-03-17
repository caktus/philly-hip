from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from apps.health_alerts import views as health_alert_views
from apps.search import views as search_views


urlpatterns = [
    path("search/", search_views.search, name="search"),
    path(
        "health-alerts-subscriber-signup",
        health_alert_views.subscribe,
        name="health_alert_subscriber",
    ),
    path("admin/", admin.site.urls),
]


urlpatterns += [
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
