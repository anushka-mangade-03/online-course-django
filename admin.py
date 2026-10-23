```python
from django.contrib import admin

from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Enrollment,
    Question,
    Choice
)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ['question_text', 'course', 'grade']


class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'course']


admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
```
