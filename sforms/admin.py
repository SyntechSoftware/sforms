from django.contrib import admin

from .models import SForm, SFormRow, SFormResult, SFormResultAttach


class SFormRowInlineAdmin(admin.StackedInline):
    model = SFormRow


@admin.register(SForm)
class SFormAdmin(admin.ModelAdmin):
    model = SForm
    list_display = (
        'code',
        'name',
        'label',
    )
    inlines = (SFormRowInlineAdmin, )

    class Media:
        js = ["admin/sforms/widget_hidder.js"]



class SFormResultAttachInlineAdmin(admin.TabularInline):
    model = SFormResultAttach
    readonly_fields=['field', 'value']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(SFormResult)
class SFormResultAdmin(admin.ModelAdmin):
    can_delete = False
    readonly_fields=['form_code', 'timestamp', 'meta', 'values']
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    
    model = SFormResult
    list_display = (
        'form_code',
        'timestamp',
    )
    inlines = (SFormResultAttachInlineAdmin, )

