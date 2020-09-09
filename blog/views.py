from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import Post, Comment, ImagePost
from django.views.generic import ListView,DetailView
# for paginating data (posts)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
#  importing count from db to count something from db , it's aggregation
from django.db.models import Count
# SearchVecor for(search multiple fields), SearchQuery object to filter
# results, SearchRank it's for ranking the results.
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

#############################################################

def post_share(request, post_id):
    '''
    This post_share is about sharing post via email
    if form of the send mail is valid clean data and
    get post_url by using request.build_absolute_uri(passed arg
    post.get_abloste_url() method )
    construncting the mail
    subject, message at last send_mail().
    using sent variable to use it later to redirecte and verified the mail was sent
    '''

    # retrieving publised post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form field passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = '{} ({}) recommends you reading"{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read {} at {} \n\n {}\n s coments: {}'.format(post.title, post_url, cd["name"], cd ["comments"])
            send_mail(subject, message, 'aissanouacer@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post':post, 'form':form, 'sent':sent})

##################end share post by mail ####################


############################################################
class PostListView(ListView):
    '''
    It's list view of all posts extentiate class ListView
    using django paginator , paginate_by , querset = Post.publised.all()
    "publised is custom manager for publised posts"
    here multiple context  posts and 3 recent posts
    "def get_context_data" with rendering template
    '''
    queryset = Post.published.all()
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 5
####################### end of PostListView ##############

# this function doing the same as PostLisView

#  def posts_list(request):
    #  posts = Post.published.all()
    #  recent = posts[0:3]
    #  r1=recent[0]
    #  r2=recent[1]
    #  r3=recent[2]
    #  paginator = Paginator(posts,5) # 5 post on each page
    #  page = request.GET.get('page')
    #  try:
        #  posts =paginator.page(page)
    #  except PageNotAnInteger:
        #  posts =paginator.page(1)
    #  except EmptyPage:
        #  posts =paginator.page( paginator.num_pages)
    #  return render(request, 'blog/post/list.html', {'page':page,
                                                   #  'posts':posts,
                                                   #  'r1':r1,
                                                   #  'r2':r2,
                                                   #  'r3':r3
                                                   #  })

#################################################################
#  class PostDetailView(DetailView):
    #  '''
    #  It's Detail View posts , extentiate the class DetailView
    #  selecting model post with template & the context
    #  has function get_object(self): returning with lookup
    #  of publish__year=year, publish__month=month,publish__day=day
    #  for selecting the variables with kwargs.get() method.
    #  exp: post = self.kwargs.get("post")

    #  '''
    #  model = Post
    #  template_name = 'blog/post/detail.html'
    #  context_object_name = 'posts'
    #  def get_object(self):
        #  post = self.kwargs.get("post")
        #  year = self.kwargs.get("year")
        #  month = self.kwargs.get("month")
        #  day = self.kwargs.get("day")
        #  return get_object_or_404(Post, slug=post,
                                 #  publish__year=year,
                                 #  publish__month=month,
                                 #  publish__day=day)

###################### End of DetailView ##########################

#this def function view select spec post
#doing the same thing with PostDetailView
def posts_detail(request, year, month, day, post):
    posts = get_object_or_404(Post, slug = post,
                        publish__year = year,
                        publish__month = month,
                        publish__day = day)
 #List of active comments for this post
    comments = posts.comments.filter(active = True)
    new_comment = None
    if request.method == 'POST':
            # A comment was posted
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.posts = posts
                # Save the comment to the database
                new_comment.save()
    else:
        comment_form = CommentForm()
    # list of similar posts
    post_tags_id = posts.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=posts.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    photos = ImagePost.objects.filter(post=posts.id)
    return render(request, 'blog/post/detail.html',
                  {'posts':posts,
                   'comments':comments,
                   'new_comment':new_comment,
                   'comment_form':comment_form,
                   'similar_posts':similar_posts,
                   'photos' : photos })

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            search_query = SearchQuery(query)
            search_vector = SearchVector('title','body')
            results=Post.objects.annotate(
                search = search_vector,
                rank = SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
    return render(request,
                  'blog/post/search.html',
                  {'form':form,
                   'query':query,
                   'results':results})




