from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user_rating = models.SmallIntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def update_rating(self):
        post_r = self.post_set.all().aggregate(postRating=Sum('post_rating'))
        p_rat = 0
        p_rat += post_r.get('postRating')
        comment_r = self.user.comment_set.all().aggregate(commentRating=Sum('comment_rating'))
        c_rat = 0
        c_rat += comment_r.get('commentRating')
        self.user_rating = p_rat * 3 + c_rat
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    news = 'NE'
    article = 'AR'
    NEWS_OR_ARTICLE = [
        (news, 'News'),
        (article, 'Article')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=news)
    n_or_a = models.CharField(max_length=2, choices=NEWS_OR_ARTICLE)
    create_date = models.DateTimeField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=120)
    body = models.TextField()
    post_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        if self.post_rating:
            self.post_rating -= 1
        self.save()

    def preview(self):
        if len(self.body) >= 124:
            return self.body[:124]+'....'
        else:
            return self.body


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, default='Comment: ')
    create_date = models.DateTimeField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        if self.comment_rating:
            self.comment_rating -= 1
        self.save()

    def __str__(self):
        return self.user.username