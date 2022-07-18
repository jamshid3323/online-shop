from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import PostModel
from .forms import CommentModelForm


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


class CommentCreateView(CreateView):
    form_class = CommentModelForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(PostModel, pk=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blogs:detail', kwargs={'pk': self.kwargs.get('pk')})
