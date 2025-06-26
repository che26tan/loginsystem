from django.contrib import admin
# from admin_panel.models import AdminPanel, OfferCode, TemplateCategory
from admin_panel.models import AdminPanel, OfferCode


@admin.register(AdminPanel)
class AdminPanelAdmin(admin.ModelAdmin):
    search_fields = []
    list_display = []

@admin.register(OfferCode)
class OfferCodeAdmin(admin.ModelAdmin):
    search_fields = ['code_id', 'code_name',]
    list_display = ['code_id', 'code_name', 'value', 'created_at', 'expire_value', 'expire_unit', 'validation_date', 'valid']


# @admin.register(TemplateCategory)
# class TemplateCategoryAdmin(admin.ModelAdmin):
#     search_fields = ['template_num',]
#     list_display = ['template_num',]