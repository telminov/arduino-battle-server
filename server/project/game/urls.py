from django.conf.urls import patterns, include, url

urlpatterns = patterns('game.views',
    url(r'^$', 'control_game', name='control_game'),
    url(r'control_game/ajax_switch_for_arduino/$', 'ajax_switch_for_arduino', name='ajax_switch_for_arduino'),
    url(r'control_game/ajax_get_from_arduino/$', 'ajax_get_data_from_arduino', name='ajax_get_from_arduino'),

)