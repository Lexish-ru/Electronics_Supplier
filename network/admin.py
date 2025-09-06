from django.contrib import admin
from django.utils.html import format_html
from .models import NetworkNode, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админ-панель для продуктов."""
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt_action(modeladmin, request, queryset):
    """Админ-действие: обнулить задолженность выбранных объектов."""
    for obj in queryset:
        obj.clear_debt()


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    """Админ-панель для узлов сети."""
    list_display = ("name", "kind", "country", "city", "supplier_link", "debt_to_supplier", "level_display", "created_at")
    list_filter = ("city", "country", "kind")
    search_fields = ("name", "email", "city", "country", "street", "house_number")
    readonly_fields = ("created_at", "level_display", "supplier_link")
    actions = [clear_debt_action]
    filter_horizontal = ("products",)

    fieldsets = (
        (None, {
            "fields": ("name", "kind", "supplier", "supplier_link", "level_display")
        }),
        ("Контакты", {
            "fields": ("email", "country", "city", "street", "house_number")
        }),
        ("Продукты", {
            "fields": ("products",)
        }),
        ("Финансы и системное", {
            "fields": ("debt_to_supplier", "created_at")
        }),
    )

    def level_display(self, obj):
        """Отображает уровень объекта."""
        return obj.level
    level_display.short_description = "Уровень"

    def supplier_link(self, obj):
        """Ссылка на страницу поставщика."""
        if not obj.supplier_id:
            return "—"
        url = f"/admin/network/networknode/{obj.supplier_id}/change/"
        return format_html('<a href="{}">{}</a>', url, obj.supplier)
    supplier_link.short_description = "Поставщик (ссылка)"
