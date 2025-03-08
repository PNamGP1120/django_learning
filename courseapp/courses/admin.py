from django.contrib import admin
from courses.models import Category, Course, Lesson, Tag, MyUser, UserLessonView, CVOnline, Like, Comment
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.template.response import TemplateResponse
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseAppAdminSite(admin.AdminSite):
    site_header = 'Course App Admin'
    site_title = 'Course App Admin'
    index_title = 'Course App Admin'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('course-stats/', self.stats_view)
        ]
        return custom_urls + urls
    def stats_view(self, request):
        count = Course.objects.filter(active = True).count()
        stats = Course.objects.annotate(lesson_count = Count('lessons')).values('subject', 'lesson_count')
        print(stats)
        return TemplateResponse(request, 'admin/course-stats.html', {'course_count': count, 'course_stats': stats})

admin_site = CourseAppAdminSite(name='courseappadmin')
admin_site.register(Category)


class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    fk_name = 'course'

class CourseAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Course
        fields = '__all__'

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ('subject', 'category', 'created_date', 'updated_date')
    list_filter = ('category', 'created_date', 'updated_date')
    search_fields = ('subject', 'description')
    inlines = [LessonInlineAdmin]

    readonly_fields = ['image_view']

    def image_view(self, obj):
        if obj:
            return mark_safe(f'<img src="/static/{obj.image.name}" width="100" />')
    class Media:
        css = {
            'all': ('css/admin.css',)
        }
        js = ('js/admin.js',)
admin_site.register(Course, CourseAdmin)




admin_site.register(Lesson)
admin_site.register(Tag)
admin_site.register(MyUser)
admin_site.register(UserLessonView)
admin_site.register(CVOnline)
admin_site.register(Like)
admin_site.register(Comment)
