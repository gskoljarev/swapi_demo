from django.contrib import admin

from .models import DatasetMetadata


@admin.register(DatasetMetadata)
class DatasetMetadataAdmin(admin.ModelAdmin):
    pass