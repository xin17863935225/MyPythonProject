from django.conf.urls import url, include
from django.contrib import admin

from app import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^axf/', include("app.urls", namespace="axf")),
    url(r'', views.home),

]
