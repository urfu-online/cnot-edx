from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .core.models import (
    Organization,
    ProgramCourse,
    OrganizationCourse,
    Direction,
    Project,
    Program,
    TextBlock
)
from .courses.models import (Course)
from .learners.models import (ProgramEnrollment)
from .profiles.models import (Profile, Reflection, Question, Answer)


class UMNOCAdminSite(admin.AdminSite):
    site_header = _('UMNOC administration')


umnoc_admin_site = UMNOCAdminSite(name='umnoc_admin')


# inlines
class OrganizationCourseInline(admin.TabularInline):
    model = OrganizationCourse
    extra = 1
    autocomplete_fields = ['course']


class ProgramCourseInline(admin.TabularInline):
    model = ProgramCourse
    extra = 1
    autocomplete_fields = ['course']


# modeladmins

@admin.register(Course, site=umnoc_admin_site)
class CourseAdmin(admin.ModelAdmin):
    autocomplete_fields = ['course_overview__display_name']
    search_fields = ['course_overview__display_name']


@admin.register(Program, site=umnoc_admin_site)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'logo', 'active', 'owner')
    list_filter = ('active', 'owner')
    ordering = ('title',)
    search_fields = ('title', 'short_name', 'slug')
    inlines = [ProgramCourseInline]


@admin.register(Organization, site=umnoc_admin_site)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_name', 'logo', 'active',)
    list_filter = ('active',)
    ordering = ('title', 'short_name',)
    search_fields = ('title', 'short_name', 'slug')
    inlines = [OrganizationCourseInline]
