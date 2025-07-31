from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
import environ
env = environ.Env()
environ.Env.read_env()
DEBUG = env.bool('DEBUG', default=False)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('', include("core.urls")),
    path('', include("my_routine.urls")),

]

# if DEBUG:
#     urlpatterns += [
#         path("__reload__/", include("django_browser_reload.urls")),
#     ]


# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {
        'document_root': settings.STATIC_ROOT,
    }),
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]