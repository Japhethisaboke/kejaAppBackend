from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import *


# Register your models here.
admin.site.register(House, LeafletGeoAdmin)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(HouseImages)
admin.site.register(Review)
admin.site.register(Report)
