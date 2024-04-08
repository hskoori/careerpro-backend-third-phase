from urllib import response
from django.shortcuts import get_object_or_404, render
# from main.permissions import IsUser
from student.serializers import SpecializationSerializer, StudentNoteSerializer, StudentSerializer,UpdateStudentSerializer,JobApplicationSerializer,StudentFileSerializer
from .models import *
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from  rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from main.functions import get_auto_id
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from chat.models import Chat,ChatMember


# Create your views here.


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page'
    max_page_size = 1000

# class FooViewSet(viewsets.ModelViewSet):
#     pagination_class = StandardResultsSetPagination


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.filter(is_deleted = False)
    filter_backends = [SearchFilter]
    search_fields = ['account__email','account__full_name']
    permission_classes = [IsAuthenticated]
    # pagination_class = StandardResultsSetPagination

    def retrieve(self, request, pk=None):
        item = get_object_or_404(self.queryset, pk=pk)
        serializer = StudentSerializer(item, context={'request': self.request})
        return Response(serializer.data,status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        instance = self.get_object()
        account_data = request.data['account']

        if(request.user.is_admin or (instance.account == request.user)):

            if((not Account.objects.filter(email=account_data["email"]).exists()) or Account.objects.filter(pk = instance.account.pk ,email=account_data["email"]).exists()):
                if((not Account.objects.filter(email=account_data["email"]).exists()) or Account.objects.filter(pk = instance.account.pk ,email=account_data["email"]).exists()):
                    account = Account.objects.get(pk=instance.account.pk)
                    account.full_name = account_data.get('full_name', account.full_name)
                    account.email = account_data.get('email', account.full_name)
                    account.phone = account_data.get('phone', account.phone)
                    account.save()

            if(not request.user.is_admin):
                request.data["fees_paid"] = instance.fees_paid 
            data=request.data.copy()
            serializer = UpdateStudentSerializer(instance=instance,data=data)
            if(serializer.is_valid()):
                serializer.save()
                Specialization.objects.filter(student=instance).delete()
                for item in request.data['specializations']:
                    item["student"] = instance
                    Specialization.objects.create(
                         auto_id = get_auto_id(Specialization),
                         **item
                    )
                instance = Student.objects.get(pk=instance.pk)
                instance.application_submitted = True
                instance.save()
                data = StudentSerializer(instance=instance).data
                status_code=status.HTTP_200_OK

            else:
                data = serializer.errors
                status_code=status.HTTP_400_BAD_REQUEST

        else:
            data = {"error_message":"Access deneid !"}
            status_code=status.HTTP_401_UNAUTHORIZED
        return Response(data,status=status_code)

    def destroy(self, request, *args, pk=None, **kwargs ):
        # try:
            user = self.request.user
            instance = self.get_object()
            if(user.is_admin or (instance.student.account == user)):
                Account.objects.filter(id=instance.account.id).delete()
                data = {"response":"Successfully deleted"}
                return Response(data, status=status.HTTP_204_NO_CONTENT)

            else:
                data = {"response":"Access denied"}

            return Response(data,status=status.HTTP_204_NO_CONTENT)
    
    
    # def destroy(self, request, *args, pk=None, **kwargs):
    #     user = self.request.user
    #     instance = self.get_object()

    #     if instance.student.account == user.account:
    #         Account.objects.filter(id=instance.account.id).delete()
    #         data = {"response": "Successfully deleted"}
    #         return Response(data, status=status.HTTP_204_NO_CONTENT)
    #     else:
    #         data = {"response": "Access denied"}
    #         return Response(data, status=status.HTTP_403_FORBIDDEN)

    
    # def retrieve(self, request, pk=None, *args, **kwargs):
    #     queryset = Student.objects.get(pk=pk)
    #     serializer = StudentSerializer(queryset)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    def list(self, request):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        if(request.user.is_admin):
            fees_paid = self.request.query_params.get('fees_paid')
            if(fees_paid=="true" or fees_paid==True):
                queryset = queryset.filter(is_deleted = False,fees_paid=True)
            elif(fees_paid=="false" or fees_paid==False):
                queryset = queryset.filter(is_deleted = False,fees_paid=False)
            else:
                queryset = queryset.filter(is_deleted = False)
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response({"detail":"Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)



class SpecializationViewSet(ModelViewSet):
   
    queryset = Specialization.objects.all() 
    serializer_class = SpecializationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['student__user__email','student__user__first_name','student__user__last_name']

    def destroy(self, request, *args, **kwargs):
        try:
            user = self.request.user
            instance = self.get_object()
            if(user.is_admin or (instance.student.account == user)):
                instance.delete()
                data = {"response":"Successfully deleted"}
            else:
                data = {"response":"Access denied"}        
            return Response(data,status=status.HTTP_200_OK)
        except:
            data = {"Not found !"}
            return Response(data,status=status.HTTP_403_FORBIDDEN)  



class StudentFileViewSet(ModelViewSet):
    serializer_class = StudentFileSerializer
    queryset = Student.objects.filter(is_deleted = False)
    filter_backends = [SearchFilter]
    search_fields = ['account__email','account__full_name']
    permission_classes = [IsAuthenticated]
    
    # pagination_class = StandardResultsSetPagination
    # def get_queryset(self):
    #     user = self.request.user
    #     if(user.is_admin):
    #         queryset = Student.objects.filter(student=student).order_by('auto_id')
    #     else:
    #         queryset = Student.objects.all().order_by('auto_id')
    #     return queryset


class JobApplicationViewSet(ModelViewSet):
    serializer_class = JobApplicationSerializer
    queryset = JobApplication.objects.all()
    # permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['company',"country","category","job_description","position"]

    def get_queryset(self):
        queryset = JobApplication.objects.all().order_by('auto_id')
        country = self.request.query_params.get('country')
        category = self.request.query_params.get('category')
        if((country) and (country!="all")):
            queryset = queryset.filter(country=country).order_by('auto_id')
        if((category) and (category!="all")):
            queryset = queryset.filter(category=category).order_by('auto_id')
        return queryset
    
    


class StudentNoteViewSet(ModelViewSet):
    serializer_class = StudentNoteSerializer
    queryset = StudentNote.objects.all()
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter]
    search_fields = ['title','date','note']
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        student = self.request.query_params.get('student')
        if(student):
            queryset = StudentNote.objects.filter(student=student).order_by('auto_id')
        else:
            queryset = StudentNote.objects.all().order_by('auto_id')
        return queryset


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def dashboard(request):
    data = {
        "students_count":0,
        "paid_students_count":0,
        "unpaid_students_count":0,
        "job_application_count":0,
        "applied_job_application_count":0,
        "declined_job_application_count":0,
    }
    

    if(request.user.is_admin):
        students_count = Student.objects.filter(is_deleted=False).count()
        paid_students_count = Student.objects.filter(fees_paid=True,is_deleted=False).count()
        unpaid_students_count = Student.objects.filter(fees_paid=False,is_deleted=False).count()
        job_application = JobApplication.objects.filter(is_deleted=False)
        data["students_count"]=students_count
        data["paid_students_count"]=paid_students_count
        data["unpaid_students_count"]=unpaid_students_count
        

    elif(request.user.role == 'student'):
        student = Student.objects.filter(account = request.user).first()
        job_application = JobApplication.objects.filter(student=student)
    else:
        return Response(data,status=status.HTTP_200_OK)   
    job_application_count = job_application.filter().count()
    # applied_job_application_count = job_application.filter(stage='applied').count()
    # pending_job_application_count = job_application.filter(stage='pending').count()
    # declined_job_application_count = job_application_count - pending_job_application_count
    data["job_application_count"]=job_application_count
    # data["applied_job_application_count"]=applied_job_application_count
    # data["declined_job_application_count"]=declined_job_application_count

    return Response(data,status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def my_profile(request):
    if(Student.objects.filter(account=request.user).exists()):
        student = Student.objects.filter(account=request.user).first()
    else:
        student = Student.objects.create(
            account=request.user,
            auto_id=get_auto_id(Student)
        )

        chat = Chat.objects.create(
            name = request.user.full_name,
            email = request.user.email
        )
        ChatMember.objects.create(
            chat = chat,
            account = request.user
        )
        admins = Account.objects.filter(is_admin=True)
        for admin in admins:
            ChatMember.objects.create(
            chat = chat,
            account = admin
        )

    serializer = StudentSerializer(student)
    return Response(serializer.data,status=status.HTTP_200_OK)



@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def students_list(request):
    students = Student.objects.filter(is_deleted=False).values("id","account__full_name")
    return Response(students,status=status.HTTP_200_OK)
