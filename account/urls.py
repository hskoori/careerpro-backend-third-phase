from django.urls import path,include
from rest_framework import routers
from . import views 


from account.views import(
    AdminViewSet,
    forgot_password,
    new_password,
    registration_view,
    account_properties_view,
    update_account_view,
    does_account_exist_view,
    ChangePasswordView,
    DeleteAccount,
    login_view,
    logout_view,
    profile_view,
    validate_email,
    EmailVerification,resend_otp
)
# from rest_framework.authtoken.views import obtain_auth_token

app_name = 'account'
router = routers.DefaultRouter()
router.register('admin',AdminViewSet, basename='admin')


urlpatterns = [
    path('check_if_account_exists/', does_account_exist_view, name="check_if_account_exists"),
    path('change_password/', ChangePasswordView.as_view(), name="change_password"),
    path('forgot_password/', forgot_password, name="forgot_password"),
    path('new_password/<token_id>', new_password, name="new_password"),
    path('properties', account_properties_view, name="properties"),
    path('properties/update', update_account_view, name="update"),
    path('login', login_view, name="login"), 
    path('delete-account/',DeleteAccount.as_view(),name='delete_account'),
    path('logout', logout_view, name="logout"), 
    path('profile', profile_view, name="profile"), 
    path('register', registration_view, name="register"),
    path('validate-email', validate_email, name="register"),
    path('email-verification/', EmailVerification.as_view(), name="email_verification"),
    path('resend_otp/', resend_otp, name="resend_otp"),

]

urlpatterns += router.urls

