from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class MyUser(User):
    avatar = models.ImageField(upload_to='users/%Y/%m/', null=True, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class TimeStampedModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']

class Course(TimeStampedModel):
    subject = models.CharField(max_length=100, unique=True)
    description = RichTextField()
    image = models.ImageField(upload_to='courses/%Y/%m/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pre_course = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.subject
    
class Lesson(TimeStampedModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', related_query_name='lessons')
    tags = models.ManyToManyField('Tag', blank=True, related_name='lessons', related_query_name='lessons')
    viewers = models.ManyToManyField(MyUser, through='UserLessonView')

    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ['title', 'course']

class UserLessonView(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    counter = models.PositiveIntegerField(default=0)
    reading_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'lesson']

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class CVOnline(models.Model):
    intro = models.TextField()
    from_salary = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    to_salary = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)


    
class ActionModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        unique_together = ['user', 'lesson']

class Like(ActionModel):
    active = models.BooleanField(default=False)

class Comment(ActionModel):
    rate = models.SmallIntegerField(default=0)