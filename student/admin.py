from django.contrib import admin

from student.models import Specialization, Student,JobApplication,StudentNote


class Admin(admin.ModelAdmin):
    list_display = ('user','fees_paid','date_added')

# admin.site.register(Student,Admin)
# admin.site.register(Specialization)


class StudentAdmin(admin.ModelAdmin):
    list_display = (
    'auto_id',
    
    )
admin.site.register(Student,StudentAdmin)

class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('auto_id','title')
admin.site.register(Specialization,SpecializationAdmin)


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('auto_id','student','company')
admin.site.register(JobApplication,JobApplicationAdmin)


class StudentNoteAdmin(admin.ModelAdmin):
    list_display = ('auto_id','student','title')
admin.site.register(StudentNote,StudentNoteAdmin)