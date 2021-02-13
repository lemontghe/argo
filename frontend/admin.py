from django.contrib import admin
from .models import Profile, Ad, PlansPlan


admin.site.register(Profile)
admin.site.register(Ad)
#  admin.site.register(AdsPlan)
admin.site.register(PlansPlan)
