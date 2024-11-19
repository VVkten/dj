from django.urls import path, include
from . import views


app_name="blog"

urlpatterns = [
    path('my_posts/', views.MyPostsListView.as_view(), name="my_posts"),
    path('drafts/', views.DraftPostsListView.as_view(), name='drafts'),
    path('posts/', views.PostView.as_view(), name='posts'),
    # path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post'),
    path('delete_post/<int:pk>', views.PostDeleteView.as_view(), name='delete_post'),
    path('update_post/<int:pk>', views.PostUpdateView.as_view(), name='update_post'),
    path('create_post/', views.PostCreateView.as_view(), name='create_post'),
    # path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post_comment/<int:post_id>', views.post_comment, name="post_comment")

]