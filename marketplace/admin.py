from django.contrib import admin
from .models import UserProfile, Crop, Contract   # 🔥 ADD Contract

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter = ('role',)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'price', 'quantity', 'created_at')
    search_fields = ('name', 'variety')

# 🔥 ADD THIS
@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('crop', 'buyer', 'farmer', 'offered_price', 'status', 'created_at')
    list_filter = ('status',)