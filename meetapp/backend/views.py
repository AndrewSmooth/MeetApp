from django.shortcuts import render

from .forms import CreateProfileForm

from .models import Profile

from django.urls import reverse_lazy

from django.views.generic.edit import CreateView

class CreateProfileView(CreateView):
    model = Profile
    template_name = 'profile/register_user.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy('profile:create')

def main(request):
    return render(request, 'layout/basic.html')
