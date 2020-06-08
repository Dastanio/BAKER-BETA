from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import Food, Comment, Rating, RatingStar
from ckeditor_uploader.widgets import CKEditorUploadingWidget

admin.site.register(Comment)
admin.site.register(RatingStar)
admin.site.register(Rating)




@admin.register(Food)
class FoodAdmin(TranslationAdmin):
    """Food"""
    list_display = ("name" , "description", "composition")