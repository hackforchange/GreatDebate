from django.contrib import admin
from greatdebate.apps.activists import Activist, ActivistResponse

class ActivistAdmin(admin.ModelAdmin):
  fields = ('first_name', 'last_name', 'email', 'address', 'city', 'zip')
  list_display = ('first_name', 'last_name', 'email', 'address', 'city', 'zip')
admin.site.register(Activist, ActivistAdmin)

class ActivistResponseAdmin(admin.ModelAdmin):
  fields = ('campaign', 'activist', 'message')
  list_display = ('campaign', 'activist', 'message')
admin.site.register(ActivistResponse, ActivistResponseAdmin)

