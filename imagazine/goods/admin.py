from django.contrib import admin
from imagazine.goods.models import *

# Register your models here.


class GalleryInlineC(admin.TabularInline):
    fk_name = 'good'
    model = GalleryConsole


@admin.register(Console)
class ConsoleAdmin(admin.ModelAdmin):
    inlines = [GalleryInlineC,]
    
class GalleryInlineG(admin.TabularInline):
    fk_name = 'good'
    model = GalleryGame


@admin.register(Game)
class ConsoleAdmin(admin.ModelAdmin):
    inlines = [GalleryInlineG,]