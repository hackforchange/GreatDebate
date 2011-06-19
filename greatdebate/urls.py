from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'greatdebate.views.home', name='home'),
    # url(r'^greatdebate/', include('greatdebate.foo.urls')),
    # Campaigns
    url(r'^create_campaign/', 'greatdebate.apps.campaigns.views.create_campaign_template'),
    url(r'^save_campaign/', 'greatdebate.apps.campaigns.views.save_campaign'),
    url(r'^button/', 'greatdebate.apps.campaigns.views.button_html'),
    # Activists
    url(r'^takeaction/', 'greatdebate.apps.activists.views.take_action_template'),
    url(r'^process_takeaction/', 'greatdebate.apps.activists.views.process_takeaction'),
    url(r'^button/$', 'greatdebate.apps.campaigns.views.button_html'),
    # Decision Makers
    url(r'^respond/', 'greatdebate.apps.decisionMakers.views.response_template'),
    url(r'^dm_lookup/', 'greatdebate.apps.decisionMakers.views.decision_maker_lookup'),
    url(r'^post_response/', 'greatdebate.apps.decisionMakers.views.post_response'),
    # Organizers
    url(r'^$', 'greatdebate.apps.organizers.views.home'),
    
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

if settings.SERVE_MEDIA:
  urlpatterns += patterns("", url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True,}),)
