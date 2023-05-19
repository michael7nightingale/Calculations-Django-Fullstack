from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("users.urls")),
    path('', include("main.urls")),
    path('science/', include("science.urls")),
    path("search/", include("search.urls")),

]


handler404 = "main.views.error404"
handler500 = "main.views.error500"
handler403 = "main.views.error403"


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
