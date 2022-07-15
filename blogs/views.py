from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import PostModel


class BlogsView(ListView):
    template_name = 'blog.html'

    def get_queryset(self):
        qs = PostModel.objects.order_by('-id')
        tag = self.request.GET.get('tag')
        if tag:
            qs = qs.filter(tag__name=tag)
        return qs


class BlogDetailView(DetailView):
    model = PostModel
    template_name = 'blog-details.html'
