from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .models import ExternalPlatform


class GetExternalCourses(View):
    """
    Редиректит на поддомен edu
    """

    def get(self, request, *args, **kwargs):
        context = {}
        sources = ExternalPlatform.objects.all()
        context['sources'] = sources
        return render(request, template_name='cnot_edx/staff/external_courses.html', context=context)

    def post(self, request, *args, **kwargs):
        external_course_id = request.POST.get("external_course_id", None)
        external_platform_id = request.POST.get("external_platform_id", None)
        external_platform = ExternalPlatform.objects.get(pk=external_platform_id)
        external_course = external_platform.get_course(external_course_id)

        return HttpResponse(external_platform.assimilate(external_course))
