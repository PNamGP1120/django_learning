from rest_framework import serializers
from .models import Course, Category, Lesson, Comment, Tag
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class CourseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    def get_image(self, obj):
        request = self.context['request']
        if obj.image.name.startswith('static'):
            path = '/%s' % obj.image.name
        else:
            path = '/static/%s' % obj.image
        return request.build_absolute_uri(path)
    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'category', 'pre_course']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'course', 'tags', 'viewers']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'lesson', 'rate']
        extra_kwargs = {
            'rate': {
                'error_messages': {
                    'required': 'content is required',
                    'blank': 'Blank comments are not allowed'
                }
            }
        }
    
    def validate_content(self, value):
        import re
        if re.match(r'\d+', value):
            raise serializers.ValidationError('Content must not contain numbers')
        return value
    
    