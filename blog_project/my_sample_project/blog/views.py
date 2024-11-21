from django.views.generic.list import ListView
from django.views.generic import DetailView, DeleteView
from django.views.generic.edit import UpdateView, CreateView
from .models import Post
from django.urls import reverse_lazy
from .forms import *
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail


def share_by_email(request, post_id):
    form = None
    if request.method == "POST":
        form = EmailForm(request.POST)
        if (form.is_valid()):
            email_to = form.cleaned_data["email_to"]
            subject = form.cleaned_data["subject"]
            text = form.cleaned_data["text"]

            send_mail(
                subject,
                text,
                from_email=None,
                recipient_list=[email_to],
                fail_silently=False,
            )
    else:
        form = EmailForm()

    ctx = {"form": form}

    return render(request, "blog/share_post.html", ctx)

def posts_by_tag(request, tag):
    posts = Post.objects.filter(tags__name=tag)
    return render(request, 'blog/posts_by_tag.html', {'posts': posts, 'tag': tag})


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
    template_name = "blog/post_list.html"

    def get_queryset(self):
        queryset = Post.published_objects.all()
        query = self.request.GET.get('q')  # Отримуємо параметр для пошуку

        if query:
            if "#" in query:  # Якщо в запиті є '#', шукаємо за тегами
                tag = query.lstrip('#')  # Видаляємо '#' для пошуку по тегах
                queryset = queryset.filter(tags__name__icontains=tag)
            else:  # Якщо '#' немає, шукаємо за назвою постів
                queryset = queryset.filter(title__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')  # Передаємо введений текст для пошуку
        return context


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
    fields = ["title", "content", "status", "tags"]
    success_url = reverse_lazy('blog:posts')

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset = queryset.filter(author=self.request.user)
        return queryset


class PostCreateView(CreateView):
    model = Post
    fields = ["title", "content", "status", "tags"]
    success_url = reverse_lazy('blog:posts')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
