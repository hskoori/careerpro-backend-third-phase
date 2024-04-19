import json
from urllib import request

from django.http import HttpResponse
from main.functions import password_generater, send_common_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate,logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.viewsets import  ModelViewSet
from rest_framework import generics, permissions
from account.serializers import  AccountPropertiesSerializer, RegistrationSerializer, ChangePasswordSerializer,AdminSerializer , AccountSerializer
from account.models import Account
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser,FormParser, MultiPartParser,FileUploadParser
from rest_framework.decorators import parser_classes
from account.models import OtpVerification
from django.contrib.sessions.backends.db import SessionStore
import random


@api_view(['POST',])
@permission_classes((AllowAny, ))
@parser_classes([JSONParser,FormParser, MultiPartParser,FileUploadParser])
def registration_view(request):
    status_code=status.HTTP_400_BAD_REQUEST
    if request.method == 'POST':
        data = {}
        # print(request.data['email'])
        email = request.data.get('email', '0').lower()
        print(email)
        # if validate_email(email) != None:
        #     data['error_message'] = 'That email is already in use.'
        #     data['response'] = 'Error'
        #     return Response(data)

        # username = request.data.get('username', '0')
        # if validate_username(username) != None:
        #     data['response'] = 'Error'
        #     return Response(data)
        request_data = request.data.copy()
        # request_data['role'] = 'student'
        # request_data['creator'] = request.user



        serializer = RegistrationSerializer(data=request_data)
        if serializer.is_valid():
        #     user = serializer.save()
        #     data['response'] = 'successfully registered new user.'
        #     data['email'] = user.email
        #     data['username'] = user.username
        #     data['pk'] = user.pk
        #     data['role'] = user.role

        #     token = Token.objects.get(user=user).key
        #     data['token'] = token
            status_code=status.HTTP_200_OK
            data= serializer.data
            otp = random.randint(1000,9999)

            to_email = request.data.get('email')
            subject = "OTP verification"
            html_context = {
                "title":"OTP verification",
                "data":[
                    {
                        "label":"Your OTP is : ",
                        "value":otp
                    }
                ]
            }
            text_content = str(html_context)
            send_common_mail(html_context,to_email,subject)

            my_session = SessionStore()
            my_session['email'] = request.data.get('email')
            # my_session['username'] = request.data.get('username')
            my_session['password'] = request.data.get('password')
            my_session['phone'] = request.data.get('phone')
            my_session['full_name'] = request.data.get('full_name')
            my_session['login_otp'] = otp
            my_session['login_otp_count'] = 5
            my_session.create()
            data['session_key'] = my_session.session_key
            print(my_session['login_otp'])
        else:
            data = serializer.errors
            status_code=status.HTTP_400_BAD_REQUEST


        return Response(data,status=status_code)




def validate_email(email):
    user = None
    try:
        user = Account.objects.get(email=email)
        # print(user)
    except Account.DoesNotExist:
        return None
    if user != None:
        return email

# def validate_username(username):
#     user = None
#     try:
#         user = Account.objects.get(username=username)
#     except Account.DoesNotExist:
#         return None
#     if user != None:
#         return username
# # =====================================================

class EmailVerification(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request):
        session_key = request.data.get('session_key')
        my_session = SessionStore(session_key=session_key)

        data = {}
        otp = request.data['otp']
        otp_verification = my_session['login_otp']
        if ((int(otp) == int(otp_verification)) and (my_session['login_otp_count'] > 0)):

            request_data = request.data.copy()
            request_data['role'] = 'student'
            # request_data['username'] = my_session['username']
            request_data['email'] = my_session['email']
            request_data['password'] = my_session['password']
            request_data['full_name'] = my_session['full_name']
            request_data['phone'] = my_session['phone']

            serializer = RegistrationSerializer(data=request_data)
            if serializer.is_valid():
                user = serializer.save()
                data['response'] = 'successfully registered new user.'
                data['email'] = user.email
                # data['username'] = user.username
                data['pk'] = user.pk
                data['role'] = user.role

                token = Token.objects.get(user=user).key
                data['token'] = token
                data['response'] = "Email Verfied Successfully"
                status_code=status.HTTP_200_OK
            else:
                data = serializer.errors
                status_code=status.HTTP_400_BAD_REQUEST
            return Response(data,status=status_code)

        else:
            if(my_session['login_otp_count'] > 0):
                my_session['login_otp_count'] -= 1
                data['error_message'] = "invalid OTP"
            else:
                my_session.delete()
                data['error_message'] = "Limit Exceeded, Register again"

            status_code=status.HTTP_400_BAD_REQUEST
        return Response(data,status=status_code)




        
# def resend_otp(request):
#     response_data = {}
#     email = request.GET.get('email')
#     if(OtpVerification.objects.filter(user__email=email).exists()):
#         otp_verification = OtpVerification.objects.filter(user__email=email).first()
#         user = otp_verification.user
#         subject = "Please Verify Your Email Address"
#         text_content = "Dear <b>{}</b>,</br><p>We need to verify that {} is your email address so that it can be used with your careerpro account.<br>OTP : <b>{}</b></p>".format(user.full_name,email,otp_verification.otp)
#         send_mail(text_content,email,subject)

#         response_data['response'] = 'OTP is sent to your email'
#         response_data['email'] = user.email
#         response_data['otp_verification'] = str(otp_verification.id)
#         response_data['status']="true"
#         status_code = status.HTTP_200_OK

#     else:
#         response_data['status']="false"
#         response_data['response'] = 'Invalid Email.'
#         status_code = status.HTTP_400_BAD_REQUEST

#     return HttpResponse(json.dumps(response_data),content_type='application/javascript',status=status_code)


@api_view(['POST',])
@permission_classes((AllowAny, ))
@parser_classes([JSONParser,FormParser, MultiPartParser,FileUploadParser])
def resend_otp(request):
    status_code=status.HTTP_400_BAD_REQUEST
    if request.method == 'POST':
        data = {}
        session_key = request.data.get('session_key')
        my_session = SessionStore(session_key=session_key)
        status_code=status.HTTP_200_OK

        to_email = my_session['email']
        subject = "OTP verification"
        html_context = {
            "title":"OTP verification",
            "data":[
                {
                    "label":"Your OTP is : ",
                    "value":my_session['login_otp']
                }
            ]
        }
        send_common_mail(html_context,to_email,subject)
        data['session_key'] = my_session.session_key
        print(my_session['login_otp'])
    else:
        data = {"error":"somthing went wrong !"}
        status_code=status.HTTP_400_BAD_REQUEST
    return Response(data,status=status_code)
    

# ==============================================

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def account_properties_view(request):
    try:
        user = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(user)
        return Response(serializer.data)


@api_view(['POST',])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):
    try:
        user = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'POST':

        serializer = AccountPropertiesSerializer(user, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'User update success'
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@permission_classes((AllowAny, ))
@parser_classes([JSONParser,FormParser, MultiPartParser,FileUploadParser])
def login_view(request):

    context = {}
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email,password=password)
    # print("user //")
    # print(user)

    if user:
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)

        context['response'] = 'Successfully authenticated.'
        context['pk'] = user.pk
        context['email'] = email.lower()
        context['token'] = token.key
        context['role'] = user.role
    else:
        context['response'] = 'Error'
        context['error_message'] = 'The email or password is incorrect'
    return Response(context)


@api_view(['POST',])
@permission_classes((AllowAny, ))
@parser_classes([JSONParser,FormParser, MultiPartParser,FileUploadParser])
def logout_view(request):
    context = {}
    try:
        request.user.auth_token.delete()
        # logout(request)
        context['response'] = 'LogOut Successful.'
        status_code=status.HTTP_200_OK
    except:
        context['response'] = 'Error'
        context['error_message'] = 'Invalid Token'
        status_code=status.HTTP_400_BAD_REQUEST
        
    return Response(context,status=status_code)

# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# @parser_classes([JSONParser, FormParser, MultiPartParser, FileUploadParser])
# def delete_user_account(request):
#     user = request.user
#     instance = get_object_or_404(Account, id=request.data.get('account_id'))  
#     if user.is_admin or instance.student.account == user:
#         instance.delete()
#         data = {"response": "Successfully deleted"}
#         return Response(data, status=status.HTTP_204_NO_CONTENT)
#     else:
#         data = {"response": "Access denied"}
#         return Response(data, status=status.HTTP_403_FORBIDDEN)

class DeleteAccount(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        user=self.request.user
        user.delete()
        return Response({"result":"Account delete"},status=status.HTTP_204_NO_CONTENT)

    
@api_view(['GET','POST'])
@permission_classes((IsAuthenticated, ))
@parser_classes([JSONParser,FormParser, MultiPartParser,FileUploadParser])
def profile_view(request):
    status_code=status.HTTP_400_BAD_REQUEST
    context = {}
    if(Account.objects.filter(pk=request.user.pk).exists()):
        user = Account.objects.get(pk=request.user.pk)
        context["email"] = user.email
        context["phone"] = user.phone
        context["full_name"] = user.full_name

        status_code=status.HTTP_200_OK
    return Response(context,status=status_code)





@api_view(['GET', ])
@permission_classes([])
@authentication_classes([])
def does_account_exist_view(request):
    if request.method == 'GET':
        email = request.GET['email'].lower()
        data = {}
        try:
            user = Account.objects.get(email=email)
            data['response'] = email
        except Account.DoesNotExist:
            data['response'] = "User does not exist"
        return Response(data)


@permission_classes((AllowAny, ))
class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = Account
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            # confirm the new passwords match
            new_password = serializer.data.get("new_password")
            confirm_new_password = serializer.data.get("confirm_new_password")
            if new_password != confirm_new_password:
                return Response({"new_password": ["New passwords must match"]}, status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            # print("-----------------",self.object)
            self.object.save()
            return Response({"response":"successfully changed password"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
@permission_classes((AllowAny, ))
def forgot_password(request):
    # Check old password
    data = {}
    if Account.objects.filter(email=request.data.get('email')).exists():
        password = password_generater(8)

        user = Account.objects.get(email=request.data.get('email'))
        user.set_password(password)
        user.save()
        token = Token.objects.get(user=user).key
        # from_email = "mail.osperb@gmail.com"
        to_email = user.email
        subject = "Reset your password"
        html_context = {
            "title":"Reset your password",
            "data":[

                {
                    "label":"Click the link to reset your password :",
                    "value":"https://careerpro.uk/password/reset/" + token,
                    "type":"url",
                    "title":">> Click here <<"
                }
            ]
        }

        text_content = str(html_context)
        send_common_mail(html_context,to_email,subject)
        data['response'] = "Your new password has been sent to your email"
        
    else:
        data['response'] = "Email does not exist"

    return Response(data, status=status.HTTP_200_OK)



@api_view(['POST','GET'])
@permission_classes((AllowAny, ))
def new_password(request,token_id):
    # Check old password
    token = Token.objects.get(key=token_id)
    data = {}
    if(request.data.get('newPassword')==request.data.get('confirmPassword')):
        user = token.user
        user.set_password(request.data.get('newPassword'))
        user.save()
        token = Token.objects.get(user=user).key
        # from_email = "mail.osperb@gmail.com"
        to_email = user.email
        subject = "Password changed Successfully"
        html_context = {
            "title":"Password changed Successfully",
            "data":[
                {
                    "label":"email",
                    "value":user.email
                },
                {
                    "label":"Your New Password",
                    "value":request.data.get('newPassword')
                },
            ]
        }
        send_common_mail(html_context,to_email,subject)
        data['response'] = "Your new password has been sent to your email"
    else:
        data['response'] = "Validation error !"
    return Response(data, status=status.HTTP_200_OK)




# # ============================================================================================


class AdminViewSet(ModelViewSet):

    queryset = Account.objects.filter(role ='admin',is_active = True)
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        data = {}
        if serializer.is_valid(): 

            serializer.save()
            data = serializer.data
            return Response(data=data)
        else:
            data = serializer.errors
            data['response'] = 'Error'
            data['error_message'] = 'Data Not Valid'
        return Response(data = data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        # self.object = self.get_object()
        serializer = self.get_serializer(self.get_object(),data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response(data=data)
        else:
            data = serializer.errors
            data['response'] = 'Error'
            data['error_message'] = 'Data Not Valid'
        return Response(data = data, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.id
        Account.objects.filter(id=id).update(is_active = False)
        data = {"response":"Successfully deleted"}
        return Response(data,status=status.HTTP_204_NO_CONTENT)



def send_mail(html_context,to_email,subject):
    r = request.post('https://mail-sender.vingb.com/custom-mail/edf554f6-c207-4ec7-a657-9285913a9a35', data={
        "to_email": to_email,
        "subject": subject,
        "html_data": html_context
    })





