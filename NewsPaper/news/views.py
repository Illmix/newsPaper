from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from django.core.paginator import Paginator
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostList(ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    ordering = ['-create_date']
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = "flatpages/post_detail.html"
    context_object_name = "post"


class PostFilters(ListView):
    model = Post
    template_name = "search.html"
    context_object_name = "search"
    queryset = Post.objects.order_by('-create_date')

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data
        # у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostCreate(CreateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm


class PostUpdate(UpdateView):
    template_name = 'flatpages/post_create.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset,
    # чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'flatpages/post_delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'
