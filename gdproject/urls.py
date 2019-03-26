from django.contrib import admin
from django.conf.urls import url, include


urlpatterns = [
    url('', include('plc.urls')),
    url('admin/', admin.site.urls),
]

# 바뀌나 test
