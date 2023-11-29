import uuid
from django.db import models
from account.models import Account
from django.utils.translation import gettext as _
from main.models import BaseModel
#from base_models.models import BaseModel



#Create your models here.

class Student(BaseModel):
    WORKING_TYPE =(
        ("Placement",'Placement'),
        ("Internship",'Internship')
    )
    account = models.ForeignKey(Account,related_name='student_account',on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.TextField(null=True,blank=True)
    dob = models.CharField(max_length=30, null=True,blank=True)
    profilepic = models.ImageField(upload_to='Profile_pic' ,null= True,blank=True)
    cv = models.FileField(upload_to ='cv',null=True,blank=True)
    cover_letter = models.FileField(upload_to ='cv',null=True,blank=True)
    cover_letter_two = models.FileField(upload_to ='cv',null=True,blank=True)
    linkedin_profile = models.FileField(upload_to ='cv',null=True,blank=True)
    company_cv = models.FileField(upload_to ='company_cv',null=True,blank=True)
    company_cv_two = models.FileField(upload_to ='company_cv_two',null=True,blank=True)
    linkedin_username = models.CharField(max_length=30, null=True,blank=True)
    linkedin_password = models.CharField(max_length=30, null=True,blank=True)
    university = models.CharField(max_length=140,null=True,blank=True)
    university_dead_line = models.CharField(max_length=140,null=True,blank=True)
    course_campus = models.CharField(max_length=140,null=True,blank=True)
    course_title = models.CharField(max_length=140,null=True,blank=True)
    course_start_date = models.CharField(max_length=30,null=True,blank=True)
    course_end_date = models.CharField(max_length=30,null=True,blank=True)
    company_name = models.CharField(max_length=140,null=True,blank=True)
    designation = models.CharField(max_length=140,null=True,blank=True)
    first_preferred_location = models.CharField(max_length=140,null=True,blank=True)
    second_preferred_location = models.CharField(max_length=140,null=True,blank=True)
    third_preferred_location = models.CharField(max_length=140,null=True,blank=True)
    forth_preferred_location = models.CharField(max_length=140,null=True,blank=True)
    working_type = models.CharField(max_length=80,choices= WORKING_TYPE,null=True,blank=True)
    is_no_internship = models.BooleanField(default=False)
    is_internship_interested = models.BooleanField(default=False)
    work_start_date = models.CharField(max_length=80,null=True,blank=True)
    work_end_date = models.CharField(max_length=80,null=True,blank=True)
    work_duration = models.CharField(max_length=50,null=True,blank=True)
    contract_submit_date = models.DateField(null=True,blank=True)
    expr_certi_submit_date = models.DateField(null=True,blank=True)
    first_job_sector = models.CharField(max_length=50,null=True,blank=True)
    second_job_sector = models.CharField(max_length=50,null=True,blank=True)
    third_job_sector = models.CharField(max_length=50,null=True,blank=True)
    forth_job_sector = models.CharField(max_length=50,null=True,blank=True)
    first_job_role = models.CharField(max_length=50,null=True,blank=True)
    second_job_role = models.CharField(max_length=50,null=True,blank=True)
    third_job_role = models.CharField(max_length=50,null=True,blank=True)
    forth_job_role = models.CharField(max_length=50,null=True,blank=True)
    course_duration = models.CharField(max_length=50,null=True,blank=True)
    visa_start_date =  models.CharField(max_length=50,null=True,blank=True)
    visa_end_date =  models.CharField(max_length=50,null=True,blank=True)
    fees_paid = models.BooleanField(default=False)
    application_submitted = models.BooleanField(default=False)

    current_location = models.TextField(null=True,blank=True)
    is_previous_experience = models.BooleanField(default=False)
    is_work_experience = models.BooleanField(default=False)
    is_confident_workplace_skills = models.BooleanField(default=False)
    has_academic_projects = models.BooleanField(default=False)
    is_include_work_project = models.BooleanField(default=False)
    has_internship_experience = models.BooleanField(default=False)

    class Meta:
        db_table = 'student'
        verbose_name = ('Student')
        verbose_name_plural = _('Student')
        ordering = ('-date_added',)

    def __str__(self):
        return str(self.account.full_name)
   
 
class Specialization(BaseModel):

    STATUS_CHOICES= [
        ("Passed",'Passed'),
        ("Not_assigned_yet",'Not Assigned yet'),
        ("Ongoing",'Ongoing'),
        ("Failed",'Failed'),
        ("Submitted","Submitted"),
        ("Not_selected",'Not selected')]


    title = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=30,choices=STATUS_CHOICES, null=True,blank=True)
    description = models.CharField(max_length=140,null=True,blank=True)
    student = models.ForeignKey(Student,related_name='specializations',on_delete=models.CASCADE)

    class Meta:
        db_table = 'specilizations'
        verbose_name =  _('specilizations')
        verbose_name_plural = _('specilizations')
        ordering = ('-date_added',)


    def __str__(self):
        return self.title
    


class JobApplication(BaseModel):
    STAGE_CHOICES= [
        ('applied','Applied'),
        ('declined','Decline'),
        ('pending','Pending'),]
    # student = models.ForeignKey(Student,related_name='job_applications', on_delete=models.CASCADE)
    date = models.CharField(max_length=140,null=True,blank=True)
    company = models.CharField(max_length=140,null=False,blank=False)
    position = models.CharField(max_length=140,null=False,blank=False)
    job_description = models.CharField(max_length=140,null=False,blank=False)
    last_date =  models.CharField(max_length=140,null=True,blank=True)
    country =  models.CharField(max_length=140,null=True,blank=True)
    category =  models.CharField(max_length=140,null=True,blank=True,default="others")
    job_link =  models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'job_applications'
        verbose_name =  _('job_application')
        verbose_name_plural = _('job_applications')
        ordering = ('-date_added',)

    def __str__(self):
        return "{} - {}".format(self.company,self.student.account.full_name)


class StudentNote(BaseModel):
    student = models.ForeignKey(Student,related_name='student',on_delete=models.CASCADE)
    title = models.CharField(max_length=150,null=True,blank=True)
    note = models.TextField(null=True,blank=True)
    date = models.DateTimeField(null=True,blank=True,auto_now_add=True)

    class Meta:
        db_table = 'student_note'
        verbose_name = ('Student_Note')
        verbose_name_plural = _('Student_Note')
        ordering = ('-date_added',)


    def __str__(self):
        return str(self.title)
        




