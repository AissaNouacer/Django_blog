from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor.fields import RichTextField


#### Published Post Manager ##################################################
####################################################################
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status="published",publish__lte=timezone.now())

#### Post Model ##################################################
####################################################################

# model post
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=250,
                            unique_for_date = 'publish')
    author = models.ForeignKey(User, on_delete = models.CASCADE,
                               related_name = 'blog_posts')
    #  body = models.TextField()
    body = RichTextField(blank=True, null=True)
    publish = models.DateTimeField(default = timezone.now)
    himage = models.ImageField(default= "default.png")
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=10, choices = STATUS_CHOICES,
                              default = 'draft')
    is_featured = models.BooleanField(default=False)
    objects = models.Manager() # default manager
    published = PublishedManager() # Our custom manager.
    tags = TaggableManager()
    def get_absolute_url(self):
        return reverse('blog:posts_detail',
                      args=[self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug])

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # this for using canonical URLs (using names urls) def get_absolute_url(self):
        return reverse(
            'blog:posts_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
####ImagePost Model ##################################################
####################################################################
class ImagePost(models.Model):
    '''
    it's linked to post model for multiple uploads
    multiple images upload
    '''
    post = models.ForeignKey(Post,default=None,
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    def  __str__(self):
        return self.post.title


####Comment Model ##################################################
####################################################################
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
##########################################################################
