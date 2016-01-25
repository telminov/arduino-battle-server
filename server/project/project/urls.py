from django.conf.urls import include, url
from django.contrib import admin
import game.urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^game/', include(game.urls))
]
