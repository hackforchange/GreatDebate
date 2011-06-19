from django.contrib import admin
from greatdebate.apps.campaigns.models import Campaign

class CampaignAdmin(admin.ModelAdmin):
  list_display = ('organizer', 'campaign_url',)
  fields = ('organizer', 'decision_maker', 'campaign_url',)
admin.site.register(Campaign, CampaignAdmin)
