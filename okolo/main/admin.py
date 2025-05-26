from django.contrib import admin
from .models import Ad, ExchangeProposal

class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at', 'category', 'condition')
    list_filter = ('category', 'condition', 'created_at')
    search_fields = ('title', 'description', 'contact_info')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'image')
        }),
        ('Дополнительная информация', {
            'fields': ('category', 'condition', 'contact_info', 'created_at')
        }),
    )

admin.site.register(Ad, AdAdmin)
admin.site.register(ExchangeProposal)
