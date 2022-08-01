from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def update_rating(self, rate):
        rate += self.user.post_rating*3
        rate += self.user.comment_rating
        return rate


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    news = 'NE'
    article = 'AR'
    NEWS_OR_ARTICLE = [
        (news, 'News'),
        (article, 'Article')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    n_or_a = models.CharField(max_length=2, choices=NEWS_OR_ARTICLE)
    create_date = models.DateTimeField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    body = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        if self.post_rating:
            self.post_rating -= 1
        self.save()

    def preview(self):
        return self.body[:124]+'....'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500, default='Comment: ')
    create_date = models.DateTimeField(auto_now_add=True)
    create_time = models.TimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        if self.comment_rating:
            self.comment_rating -= 1
        self.save()

    def get_username(self):
        return self.user.username