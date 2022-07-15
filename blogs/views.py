from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import PostModel


class BlogsView(ListView):
    queryset = PostModel.objects.order_by('-id')
    template_name = 'blog.html'


class BlogDetailView(DetailView):
    model = PostModel
    template_name = 'blog-details.html'
