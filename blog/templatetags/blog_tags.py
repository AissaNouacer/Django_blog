from django import template
from ..models import Post
from ..views import SearchForm
from django.contrib.postgres.search import SearchVector

register = template.Library()

#  @register.inclusion_tag('blog/post/latest_posts.html')
#  def r():
    #  return Post.published.all()[:3]
# i call it left cuz the column that i use , just to distinguish
@register.inclusion_tag("blog/post/latest_posts.html")
def recent_left():
    form = Post.published.filter(is_featured=True)
    if form != None:
        f1 = form[0]
        return {'f1': f1,}
    else:
        return None

# i call it right cuz the column that i use , just to distinguish
@register.inclusion_tag("blog/post/latest_wposts.html")
def recent_right():
    form = Post.published.filter(is_featured=True)[:3]
    if form != None:
        f2 = form[1]
        f3 = form[2]
        return {'f2': f2, 'f3': f3}
    else:
        return None

@register.inclusion_tag("blog/post/latest.html")
def latests():
    latest = Post.published.all()
    if latest != None:
        latest = latest[:3]
        return {'latest':latest}
    else:
        return None

