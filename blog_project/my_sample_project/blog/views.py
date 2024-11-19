from django.views.generic.list import ListView
from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import UpdateView, CreateView
from .models import Post
from django.urls import reverse_lazy
from .forms import *
from django.views.decorators.http import require_POST

from django.utils.text import slugify
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


# def post_list(request):
#     # Отримуємо параметр сортування (за замовчуванням від найновіших до старіших)
#     sort_order = request.GET.get('sort_order', 'desc')  # 'desc' для від найновіших до старіших, 'asc' - навпаки
#
#     # Запит для постів
#     posts = Post.objects.all()
#
#     # Якщо потрібно, сортуємо за датою публікації
#     if sort_order == 'asc':
#         posts = posts.order_by('published_at')  # Від старих до нових
#     else:
#         posts = posts.order_by('-published_at')  # Від нових до старих
#
#     # Пагінація
#     paginator = Paginator(posts, 10)  # 10 постів на сторінку
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     return render(request, 'blog/post_list.html', {
#         'page_obj': page_obj,
#         'sort_order': sort_order,  # Передаємо параметр сортування до шаблону
#     })


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # ,status=BlogPost.PublicationStatus.PUBLISHED
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()

    return render(request,
                  'blog/comment.html',
                  {
                      'post': post,
                      'form': form,
                      'comment': comment
                  }
                  )

class PostView(ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return Post.published_objects.all()

class PostDetailView(DetailView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
        return ctx


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy("blog:posts")

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()
        if post.author != request.user:
            return HttpResponseForbidden("You are not allowed to delete this post.")
        return super().dispatch(request, *args, **kwargs)


class MyPostsListView(ListView):
    model = Post
    paginate_by = 5

    def get_queryset(self):
        return Post.published_objects.filter(author=self.request.user)


class DraftPostsListView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'blog/draft_posts_list.html'

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user,
            status=Post.PublicationStatus.DRAFT
        )


# class PostDeleteView(DeleteView):
#     model = Post
#     success_url = reverse_lazy("blog:posts")
#
#     def get_queryset(self, **kwargs):
#         queryset = super().get_queryset(**kwargs)
#         queryset = queryset.filter(author=self.request.user)
#         return queryset


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "content", "status"]
    success_url = reverse_lazy('blog:posts')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(author=self.request.user)
        return queryset


class PostCreateView(CreateView):
    model = Post
    fields = ["title", "content", "status"]
    success_url = reverse_lazy('blog:posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
