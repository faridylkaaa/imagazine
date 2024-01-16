from django.contrib import admin
from imagazine.goods.models import *

# Register your models here.


class GalleryInlineC(admin.TabularInline):
    fk_name = 'good'
    model = Gallery


@admin.register(Game)
class GoodsAdmin(admin.ModelAdmin):
    inlines = [GalleryInlineC,]
    
    
@admin.register(Console)
class GoodsAdmin(admin.ModelAdmin):
    inlines = [GalleryInlineC,]