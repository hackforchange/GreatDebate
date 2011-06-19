from django.contrib import admin
from greatdebate.apps.decisionMakers.models import DecisionMaker, DecisionMakerResponse

class DecisionMakerAdmin(admin.ModelAdmin):
  fields = ('name','title')
  list_display = ('name','title')
admin.site.register(DecisionMaker,DecisionMakerAdmin)

class DecisionMakerResponseAdmin(admin.ModelAdmin):
  fields = ('decision_maker', 'campaign', 'response_url')
  list_display = ('decision_maker', 'response_url')
admin.site.register(DecisionMakerResponse, DecisionMakerResponseAdmin)
