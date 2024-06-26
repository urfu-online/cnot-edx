import logging

from common.djangoapps.student.models import (
    CourseEnrollment
)
from django.contrib.auth import get_user_model

from .models import LikedCourse

log = logging.getLogger(__name__)


def get_course_enrollments(username, include_inactive=False):
    enrollments = []
    qset = CourseEnrollment.objects.filter(
        user__username=username,
    ).order_by('created')

    if not include_inactive:
        qset = qset.filter(is_active=True)

    for enrollment in qset:
        cnot_course = enrollment.course.cnot_course.first()
        enrollments.append({
            "id": cnot_course.id if cnot_course else None,
            'course_id': enrollment.course.id,
            'display_name': enrollment.course.display_name,
            'start_date': enrollment.course.start_date,
            'end_date': enrollment.course.end_date,
        })

    return enrollments


def get_liked_courses(username):
    return LikedCourse.objects.filter(
        user=get_user_model().objects.get(username=username)).values_list('course__id',
                                                                          flat=True)
