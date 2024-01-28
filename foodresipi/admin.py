from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

@admin.register(models.Resipi)
class ResipiAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['title']
    }
    #actions = ['clear_inventory']
    #inlines = [ProductImageInline]
    list_display = ['title', 'category_title']
    #list_editable = ['unit_price']
    list_filter = ['category', 'last_update']
    list_per_page = 10
    list_select_related = ['category']
    search_fields = ['title']

    def category_title(self, recipi):
        return recipi.category.title

    # @admin.display(ordering='inventory')
    # def inventory_status(self, product):
    #     if product.inventory < 10:
    #         return 'Low'
    #     return 'OK'

    # @admin.action(description='Clear inventory')
    # def clear_inventory(self, request, queryset):
    #     updated_count = queryset.update(inventory=0)
    #     self.message_user(
    #         request,
    #         f'{updated_count} products were successfully updated.',
    #         messages.ERROR
    #     )
    class Media:
        css = {
            'all': ['foodresipi/styles.css']
        }

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    #autocomplete_fields = ['title']
    list_display = ['title', 'resipis_count']
    search_fields = ['title']

    @admin.display(ordering='resipis_count')
    def resipis_count(self, category):
        url = (
            reverse('admin:foodresipi_resipi_changelist')
            + '?'
            + urlencode({
                'category__id': str(category.id)
            }))
        return format_html('<a href="{}">{} Resipis</a>', url, category.resipis_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            resipis_count=Count('resipis')
        )


@admin.register(models.Chef)
class ChefrAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',  'membership']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
