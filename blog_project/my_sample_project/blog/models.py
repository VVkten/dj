from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager

class PublishedPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.PublicationStatus.PUBLISHED)


class Post(models.Model):
    class Meta:
        ordering = ['-published_at']

    class PublicationStatus(models.TextChoices):
        DRAFT = "D", _("Draft")
        PUBLISHED = "P", _("Published")

    status = models.CharField(
        max_length=1,
        choices=PublicationStatus,
        default=PublicationStatus.PUBLISHED,
    )

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=70, unique_for_date='created_at', blank=False)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    tags = TaggableManager()

    objects = models.Manager()
    published_objects = PublishedPostsManager()

    def save(self, *args, **kwargs):
        if self.pk:
            previous = Post.objects.get(pk=self.pk)
            if previous.status == Post.PublicationStatus.DRAFT and \
                    self.status == Post.PublicationStatus.PUBLISHED:
                self.published_at = timezone.now()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title + " by " + self.author.username

    def get_absolute_url(self):
        return reverse('blog:post', args=[
            self.created_at.year,
            self.created_at.month,
            self.created_at.day,
            self.slug
        ])


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)