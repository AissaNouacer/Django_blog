from django.urls import path, re_path
from .feed import LatestPostsFeed
from . import views


app_name = "blog"


urlpatterns = [

    #post views
    #  path('', views.posts_list, name="posts_list"),
    path('', views.PostListView.as_view(), name='posts_list'),
    #path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.PostDetailView.as_view(), name="posts_detail"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.posts_detail, name="posts_detail"),
    path('<int:post_id>/share/', views.post_share, name="post_share"),
    path('feed/',LatestPostsFeed(),name='post_feed'),
    path('search/',views.post_search,name='post_search'),
]
