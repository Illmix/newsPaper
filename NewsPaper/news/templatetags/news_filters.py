from django import template

register = template.Library()


@register.filter(
    name='censor'
)
def censor(value):
    bad_words = ['fuck', 'bitch', 'bastard']
    if isinstance(value, str):
        for word in bad_words:
            if word in str(value):
                length = len(word)
                return str(value.replace(word, '*'*length))
            return str(value)
