from rest_framework import serializers
# from careerpro import student
from account.models import Account
from chat.models import Chat,ChatMember
from account.serializers import AccountSerializer, RegistrationSerializer
from main.functions import get_auto_id, password_generater, send_common_mail
from student.models import Specialization, Student,JobApplication, StudentNote
from django.db import transaction

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = [
            'id',
            'title',
            'status',
            'description',
            'student'
        ]

        extra_kwargs = {
            'auto_id':{'read_only': True},
            'student':{'read_only': True},
            
        }
    def create(self, validated_data):
        print(validated_data)
        specialization = Specialization.objects.create(
            **validated_data,
            auto_id = get_auto_id(Specialization),
            # creator = self.context['request'].user
        )
        return specialization
       


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id','company','position','job_description','last_date','job_link','country','category']

        extra_kwargs = {
                'id': {'read_only': True},
        }	


    def create(self,validated_data):
        job_application = JobApplication.objects.create(
            **validated_data,
            auto_id = get_auto_id(JobApplication)
        )

        return job_application

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email', 'phone','full_name','role']

    def create(self, validated_data):
        password = password_generater(8)
        validated_data["password"] = password
        validated_data["password2"] = password

        account_serializer = RegistrationSerializer(data=validated_data)
        if account_serializer.is_valid():
            account = account_serializer.save()

        return account



      

# class StudentSerializer2(serializers.ModelSerializer):
#     # queryset = Student.objects.filter(is_deleted=False).order_by("-auto_id") 
#     # username = serializers.CharField(write_only=True)
#     # phone = serializers.CharField(write_only=True)
#     # email = serializers.CharField(write_only=True)
#     # full_name = serializers.CharField(write_only=True)
#     account = AccountSerializer()
#     specializations = SpecializationSerializer(many=True)
#     class Meta:
#         model = Student
#         fields =  [
#             'id',
#             'account',
#             'address',
#             'dob',
#             'profilepic',
#             'cv',
#             'cover_letter',
#             'cover_letter_two',
#             'linkedin_profile',
#             'company_cv',
#             'company_cv_two',
#             'linkedin_username',
#             'linkedin_password',
#             'university',
#             'university_dead_line',
#             'course_campus',
#             'course_title',
#             'course_start_date',
#             'course_end_date',
#             'company_name',
#             'designation',
#             'first_preferred_location',
#             'second_preferred_location',
#             'third_preferred_location',
#             'forth_preferred_location',
#             'working_type',
#             'work_start_date',
#             'work_end_date',
#             'work_duration',
#             'contract_submit_date',
#             'expr_certi_submit_date',
#             'first_job_sector',
#             'second_job_sector',
#             'third_job_sector',
#             'forth_job_sector',
#             'first_job_role',
#             'second_job_role',
#             'third_job_role',
#             'forth_job_role',
#             'course_duration',
#             'visa_start_date',
#             'visa_end_date',
#             'fees_paid',
#             'application_submitted',
#             'specializations',
#             'job_applications'
#             ]
#         extra_kwargs = {
#             # 'balance':{'read_only': True},
#             'job_applications':{'read_only': True},
#         }

#     def create(self, validated_data):
#         print("create ///.")
#         account_serializer = AccountSerializer(data=validated_data["account"])
#         specializations = validated_data["specializations"]

#         try:
#             with transaction.atomic():
#                 if(account_serializer.is_valid()):
#                     validated_data["account"] = account_serializer.save()
#                     validated_data.pop("specializations")
#                     student = Student.objects.create(
#                         **validated_data,
#                         auto_id = get_auto_id(Student),
#                     )
#                     for item in specializations:
#                         item.update({'student':student})

#                         print(item)

#                         specialization_serializer = SpecializationSerializer(data = item)
#                         if(specialization_serializer.is_valid()):
#                             Specialization.objects.create(
#                                 auto_id = get_auto_id(Specialization),
#                                 **item
#                             )
#                         else:
#                             raise serializers.ValidationError({'error_message': 'Form vaidation error !'})
#                     return student
#         except:
#             raise serializers.ValidationError({'error_message': 'Form vaidation error !'})



 

class StudentSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    specializations = SpecializationSerializer(many=True)

    class Meta:
        model = Student
        fields =  [
            'id',
            'account',
            'address',
            'dob',
            'profilepic',
            'cv',
            'cover_letter',
            'cover_letter_two',
            'linkedin_profile',
            'company_cv',
            'company_cv_two',
            'linkedin_username',
            'linkedin_password',
            'university',
            'university_dead_line',
            'course_campus',
            'course_title',
            'course_start_date',
            'course_end_date',
            'company_name',
            'designation',
            'first_preferred_location',
            'second_preferred_location',
            'third_preferred_location',
            'forth_preferred_location',
            'working_type',
            'work_start_date',
            'work_end_date',
            'work_duration',
            'contract_submit_date',
            'expr_certi_submit_date',
            'first_job_sector',
            'second_job_sector',
            'third_job_sector',
            'forth_job_sector',
            'first_job_role',
            'second_job_role',
            'third_job_role',
            'forth_job_role',
            'course_duration',
            'visa_start_date',
            'visa_end_date',
            'fees_paid',
            'application_submitted',
            'specializations',
            'is_no_internship',
            'is_internship_interested',
            'current_location',
            'is_previous_experience',
            'is_work_experience',
            'is_confident_workplace_skills',
            'has_academic_projects',
            'is_include_work_project',
            'has_internship_experience',
            ]
        extra_kwargs = {
        'balance':{'read_only': True},
        'cv':{'read_only': True},
        'cover_letter':{'read_only': True},
        'cover_letter_two':{'read_only': True},
        'linkedin_profile':{'read_only': True},
        'company_cv':{'read_only': True},
        'company_cv_two':{'read_only': True},

        }

    def create(self, validated_data):
        account_serializer = AccountSerializer(data=validated_data["account"])
        specializations = validated_data["specializations"]

        with transaction.atomic():
            if(account_serializer.is_valid()):
                validated_data["account"] = account_serializer.save()
                validated_data.pop("specializations")
                student = Student.objects.create(
                    **validated_data,
                    auto_id = get_auto_id(Student),
                )
                for item in specializations:
                    item.update({'student':student})
                    specialization_serializer = SpecializationSerializer(data = item)
                    if(specialization_serializer.is_valid()):
                        Specialization.objects.create(
                            auto_id = get_auto_id(Specialization),
                            **item
                        )
                    else:
                        raise serializers.ValidationError({'error_message': 'Form vaidation error !'})

                    chat = Chat.objects.create(
                        name = validated_data["account"].full_name,
                        email = validated_data["account"].email
                    )
                    ChatMember.objects.create(
                        chat = chat,
                        account = validated_data["account"]
                    )
                    admins = Account.objects.filter(is_admin=True)
                    for admin in admins:
                        ChatMember.objects.create(
                        chat = chat,
                        account = admin
                    )
                    
                return student
            else:
                raise serializers.ValidationError({'error_message': 'Form vaidation error !'})

            


class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields =  [
            'id',
            # 'account',
            'address',
            'dob',
            # 'profilepic',
            # 'cv',
            # 'cover_letter',
            # 'cover_letter_two',
            'linkedin_profile',
            # 'company_cv',
            # 'company_cv_two',
            'linkedin_username',
            'linkedin_password',
            'university',
            'university_dead_line',
            'course_campus',
            'course_title',
            'course_start_date',
            'course_end_date',
            'company_name',
            'designation',
            'first_preferred_location',
            'second_preferred_location',
            'third_preferred_location',
            'forth_preferred_location',
            'working_type',
            'work_start_date',
            'work_end_date',
            'work_duration',
            'contract_submit_date',
            'expr_certi_submit_date',
            'first_job_sector',
            'second_job_sector',
            'third_job_sector',
            'forth_job_sector',
            'first_job_role',
            'second_job_role',
            'third_job_role',
            'forth_job_role',
            'course_duration',
            'visa_start_date',
            'visa_end_date',
            'fees_paid',
            'application_submitted',
            'is_no_internship',
            'is_internship_interested',
            'current_location',
            'is_previous_experience',
            'is_work_experience',
            'is_confident_workplace_skills',
            'has_academic_projects',
            'is_include_work_project',
            'has_internship_experience',
            ]
        extra_kwargs = {
        'balance':{'read_only': True},
        }



class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id','company','position','job_description','last_date','job_link','country','category']
        extra_kwargs = {
                'id': {'read_only': True},
        }	


    def create(self,validated_data):
        job_application = JobApplication.objects.create(
            **validated_data,
            auto_id = get_auto_id(JobApplication)
        )

        # student = validated_data['student']
        # email = student.account.email

        # from_email = "careerportal.in <ecolumsmarketing@gmail.com>"
        # subject = "New job Alert"
        # try:
        # text_content = ""
        # html_context = {
        #     "position" : job_application.position,
        #     "company":job_application.company,
        #     "student_name":student.account.username,
        #     "last_date":job_application.last_date,
        #     "website":"https://careerpro.uk"
        # }
        # html_content = render_to_string('email/jobalert_email.html', html_context)
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()

        


        return job_application



 

class StudentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields =  [
            'profilepic',
            'cv',
            'cover_letter',
            'cover_letter_two',
            'linkedin_profile',
            'company_cv',
            'company_cv_two',
            ]

class StudentNoteSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.account.full_name',read_only = True)
    class Meta:
        model = StudentNote
        fields = ['id','student','student_name','title','note','date']

        extra_kwargs = {
                'auto_id': {'read_only': True},
        }	


    def create(self,validated_data):
        studentNote = StudentNote.objects.create(
            **validated_data,
            auto_id = get_auto_id(StudentNote),
            creator = self.context['request'].user
        )
        return studentNote
