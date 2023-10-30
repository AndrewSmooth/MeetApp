from django.urls import path, include
from .views import main
from users import views as user_views
from .views import CreateProfileView

app_name = "backend"

urlpatterns = [  
    #users
    path('accounts/profile/create/', CreateProfileView.as_view(), name='profile_create'),
    path('accounts/profile/delete/', user_views.DeleteUserView.as_view(), name='profile_delete'),
    path ('accounts/profile/change/', user_views.ChangeUserlnfoView.as_view(), name='profile_change'),
    path('accounts/logout', user_views.UserLogoutView.as_view(), name='logout' ),
    path ('accounts/passwords/change/', user_views.UserPasswordChangeView.as_view(), name='password_change'),
    path ('password-reset/', user_views.send_instruction, name='password_reset'),
    path('password-reset/<str:sign>/', user_views.SetNewPasswordView, name='set_new_password'),
    path('accounts/register/activate/<str:sign>/', user_views.user_activate, name='register_activate'),
    path ('accounts/register/done/', user_views.RegisterDoneView.as_view(), name='register_done'),
    path ('accounts/register/', user_views.RegisterUserView.as_view(), name='register'),
    path('accounts/login', user_views.UserLoginView.as_view(), name='login' ),
    #meetApp
    path('accounts/start', main, name='start'),  
    path('', main, name='start'),  
]