from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('auth/', include('authentication.urls')),
    path('dashboard/', include('prompt_engine.urls')),
    path('analytics/', include('analytics.urls')),
    path('custom-admin/', include('custom_admin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom admin header
admin.site.site_header = "HalluciGuard Admin"
admin.site.site_title = "HalluciGuard"
admin.site.index_title = "AI Hallucination Platform"
