from django.forms import ModelForm, BooleanField
from .models import Post


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно,
    # надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с
    # фильтрами.
    check_box = BooleanField(label='Confirm!')

    class Meta:
        model = Post
        fields = ['author', 'n_or_a', 'category', 'title', 'body']
