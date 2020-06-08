from modeltranslation.translator import register, TranslationOptions
from .models import Food


@register(Food)

class CategoryTranslationOptions(TranslationOptions):
	fields = ('name', 'composition', 'description')