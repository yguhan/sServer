from django.contrib import admin

# Register your models here.
from .models import Document

class DocumentAdmin(admin.ModelAdmin):
	list_filter = ['id']
	search_fields = ['id']

admin.site.register(Document, DocumentAdmin)
