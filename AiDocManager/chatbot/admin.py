from django.contrib import admin
from .models import File, KeyEntity

# Register your models here.

class KeyEntityInline(admin.TabularInline):  # or use admin.StackedInline for a different layout
    model = KeyEntity
    extra = 1  # Number of empty KeyEntity forms shown

# Register the File model with inline KeyEntity
@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "file", "uploaded_at", "document_type")
    search_fields = ("user__username", "document_type")
    list_filter = ("uploaded_at", "document_type")
    inlines = [KeyEntityInline]  # Attach KeyEntity to File admin
