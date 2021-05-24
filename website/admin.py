from django.contrib import admin
from django.contrib.admin import AdminSite

from website.models import (BidClientLot, BidCompanyLot, Category, Client,
                            ClientLot, ClientReview, Company, CompanyLot,
                            CompanyReview, LotPhoto)

def duplicate_event(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.url = None
        object.save()
duplicate_event.short_description = "Дублювати"

class LotPhotoInline(admin.TabularInline):
    model = LotPhoto

class CompanyLotAdmin(admin.ModelAdmin):
    actions = [duplicate_event,]
    list_display_links = ['name']
    list_display = ['is_active', 'owner', 'name', 'category', 'price', 'current_price', 'price_gap', 'date_created', 'date_end',]
    inlines = [
        LotPhotoInline,
    ]

admin.site.register(Client)
admin.site.register(ClientLot)
admin.site.register(BidClientLot)
admin.site.register(ClientReview)

admin.site.register(Company)
admin.site.register(CompanyLot, CompanyLotAdmin)
admin.site.register(BidCompanyLot)
admin.site.register(CompanyReview)

admin.site.register(Category)
admin.site.register(LotPhoto)

# admin.site.register()

AdminSite.site_header = 'Аукціон'
AdminSite.site_title = 'Адміністрування'
AdminSite.index_title = 'Аукціон Адміністрування'
