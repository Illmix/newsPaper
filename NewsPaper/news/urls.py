from django.urls import path
from .views import PostList, PostDetail, PostFilters, PostCreate, PostUpdate, PostDelete
urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', PostFilters.as_view(), name='post_search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete')
]
