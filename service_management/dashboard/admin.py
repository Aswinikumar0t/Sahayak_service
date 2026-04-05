from django.contrib import admin
from .models import Category, SubCategory, RatePlan, ServicePartner

# Register Category
admin.site.register(Category)

# Register SubCategory
admin.site.register(SubCategory)

# Register RatePlan
admin.site.register(RatePlan)

# Register ServicePartner (if it exists)
admin.site.register(ServicePartner)