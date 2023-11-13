from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .forms import ChangeUserlnfoForm

from backend.models import AdvUser

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .forms import RegisterUserForm, ResetUserPasswordForm, SetPasswordForm

from django.core.signing import BadSignature
from .utilities import signer, send_password_reset_instruction

from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages

from django.core.mail import send_mail

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'users/delete_user.html'
    success_url = reverse_lazy('backend:start')
                               
    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)
    

    def get_object(self , queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'users/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'users/user_is_activated.html'
    else:
        template = 'users/activation_done.html'
    user.is_active = True
    user.is_activated = True
    user.save()
    return render(request, template)

def SetNewPasswordView(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'users/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user:
        if request.method == 'POST':
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                password1 = form.cleaned_data['password1']
                if password1:
                    password_validation.validate_password(password1)
                password2 = form.cleaned_data['password2']
                if password1 and password2 and password1 != password2:
                    errors = {'password2': ValidationError ('Введенные пароли не совпадают', code='password_mismatch')}
                    raise ValidationError(errors)
                else:
                    user.set_password(form.cleaned_data['password1'])
                    user.save()
                    return render(request, 'users/password_reset_confirm.html')
        else:
            form = SetPasswordForm()
            return render(request, 'users/set_password.html', {'form': form})


class RegisterDoneView(TemplateView):
    template_name = 'users/register_done.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'users/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('backend:register_done')


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('backend:start')
    success_message = 'Пароль пользователя изменен'

def send_instruction(request):
    if request.method == 'POST':
        form = ResetUserPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            user = get_object_or_404(AdvUser, username=username)
            if user:
                letter = send_password_reset_instruction(user)
                subject, body = letter[0], letter[1]

                send_mail(subject, body, 'gladkiy.a2004@gmail.com', [email,])
                return render(request, 'users/password_reset_done.html')
    else:
        form = ResetUserPasswordForm
        return render(request, 'users/password_reset.html', {'form': form})

class ChangeUserlnfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'users/change_user_info.html'
    form_class = ChangeUserlnfoForm
    success_url = reverse_lazy ('backend:start')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'users/logout.html'


class UserLoginView(LoginView):
    template_name = 'users/login.html'