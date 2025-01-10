from django import template
from django.utils.translation import get_language

register = template.Library()


@register.inclusion_tag('includes/setlang.html', takes_context=True)
def setlang(context):
    LANGUAGES = {
        'en': '🇺🇸',
        'es': '🇪🇸',
    }

    current_lang = get_language()
    current_flag = LANGUAGES.pop(current_lang)
    next = context['request'].path
    return {
        'current_lang': current_lang,
        'current_flag': current_flag,
        'languages': LANGUAGES,
        'next': next,
    }
