```python
from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    content = models.TextField()

    def __str__(self):
        return self.title


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_time = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + self.course.name


class Question(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class Submission(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE
    )
    choices = models.ManyToManyField(Choice)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Submission " + str(self.id)
```
