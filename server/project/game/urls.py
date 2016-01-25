from django.conf.urls import patterns, include, url

urlpatterns = patterns('game.views',
    url(r'^$', 'control_game', name='control_game'),
    url(r'control_game/switch_for_arduino/$', 'switch_for_arduino', name='switch_for_arduino'),

)