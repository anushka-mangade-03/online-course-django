```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from models import Course, Enrollment, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    context = {
        'course': course
    }

    return render(
        request,
        'onlinecourse/course_details_bootstrap.html',
        context
    )


@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    if request.method == 'POST':
        submission = Submission.objects.create(
            enrollment=enrollment
        )

        for question in course.questions.all():
            selected_choices = request.POST.getlist(
                'choice_' + str(question.id)
            )

            for choice_id in selected_choices:
                choice = get_object_or_404(
                    Choice,
                    pk=choice_id
                )

                submission.choices.add(choice)

        submission.save()

        return redirect(
            'onlinecourse:show_exam_result',
            course_id=course.id,
            submission_id=submission.id
        )

    return redirect(
        'onlinecourse:course_details',
        course_id=course.id
    )


@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(
        Course,
        pk=course_id
    )

    submission = get_object_or_404(
        Submission,
        pk=submission_id
    )

    questions = course.questions.all()

    score = 0
    total_score = 0
    exam_results = []

    for question in questions:
        total_score += question.grade

        correct_choices = set(
            question.choices.filter(
                is_correct=True
            ).values_list(
                'id',
                flat=True
            )
        )

        selected_choices = set(
            submission.choices.filter(
                question=question
            ).values_list(
                'id',
                flat=True
            )
        )

        is_correct = (
            selected_choices == correct_choices
        )

        if is_correct:
            score += question.grade

        exam_results.append({
            'question': question,

            'selected_choices':
                submission.choices.filter(
                    question=question
                ),

            'correct_choices':
                question.choices.filter(
                    is_correct=True
                ),

            'is_correct': is_correct
        })

    percentage = 0

    if total_score > 0:
        percentage = (
            score / total_score
        ) * 100

    passed = percentage >= 70

    context = {
        'course': course,
        'submission': submission,
        'score': score,
        'total_score': total_score,
        'percentage': percentage,
        'passed': passed,
        'exam_results': exam_results
    }

    return render(
        request,
        'onlinecourse/exam_result.html',
        context
    )
```
