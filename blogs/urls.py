from django.urls import path
from .views import BlogsView, BlogDetailView, CommentCreateView

app_name = 'blogs'

urlpatterns = [
    path('', BlogsView.as_view(), name='posts'),
    path('<int:pk>/post/', BlogDetailView.as_view(), name='detail'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='comment')
]