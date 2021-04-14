from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as django_auth_views
from django.urls import path

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from apps.auth_content import views as auth_content_views
from apps.health_alerts import views as health_alert_views
from apps.hip import views as hip_views
from apps.search import views as search_views


urlpatterns = [
    path("search/", search_views.search, name="search"),
    path(
        "closed-pod/closedpod-contact-information/",
        auth_content_views.closedpod_contact_information,
        name="closedpod_contact_information",
    ),
    path(
        "closed-pod/closedpod-contact-information-edit/",
        auth_content_views.closedpod_contact_information_edit,
        name="closedpod_contact_information_edit",
    ),
    path(
        "health-alerts-subscriber-signup/",
        health_alert_views.subscribe,
        name="health_alert_subscriber",
    ),
    path("admin/", admin.site.urls),
]

# Authentication-related views
urlpatterns += [
    path("accounts/login/", hip_views.HIPLoginView.as_view(), name="login"),
    path("accounts/logout/", django_auth_views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/password_reset/",
        django_auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "accounts/password_reset/done/",
        django_auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        django_auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        django_auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "accounts/router/", hip_views.authenticated_view_router, name="auth_view_router"
    ),
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
