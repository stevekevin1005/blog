from django.db import models
from django.utils import timezone

class User(models.Model):

    class Meta:
        db_table = "user_tab"

    account = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    sex = models.BooleanField(default = 0) # 0: M, 1: F
    create_date = models.DateTimeField(default = timezone.now)
    update_date = models.DateTimeField(default = timezone.now)

class Post(models.Model):

    class Meta:
        db_table = "post_tab"

    title = models.CharField(max_length = 200)
    description = models.CharField(max_length = 200)
    text = models.TextField()
    location = models.CharField(max_length = 200)
    user_id = models.IntegerField()
    date = models.DateField()
    create_date = models.DateTimeField(default = timezone.now)
    update_date = models.DateTimeField(default = timezone.now)

class Photo(models.Model):
    
    class Meta:
        db_table = "photo_tab"

    url = models.TextField()
    post_id = models.IntegerField();
    create_date = models.DateTimeField(default = timezone.now)
    update_date = models.DateTimeField(default = timezone.now)
        

class Comment(models.Model):
    
    class Meta:
        db_table = "comment_tab"

    text = models.TextField()
    post_id = models.IntegerField();
    create_date = models.DateTimeField(default = timezone.now)
    update_date = models.DateTimeField(default = timezone.now)

class Like(models.Model):
    
    class Meta:
        db_table = "like_tab"

    post_id = models.IntegerField()
    user_id = models.IntegerField();
    create_date = models.DateTimeField(default = timezone.now)
    update_date = models.DateTimeField(default = timezone.now)

class Participate(models.Model):

    class Meta:
        db_table = "participate_tab"

    post_id = models.IntegerField()
    user_id = models.IntegerField();
    create_date = models.DateTimeField(default = timezone.now)
    update_date = models.DateTimeField(default = timezone.now)
        