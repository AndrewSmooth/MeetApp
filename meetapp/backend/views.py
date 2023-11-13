from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .forms import CreateProfileForm

from .models import Profile

from django.urls import reverse_lazy

from django.views.generic.edit import CreateView

class CreateProfileView(CreateView):
    model = Profile
    template_name = 'profile/create_profile.html'
    form_class = CreateProfileForm
    success_url = reverse_lazy('backend:start')

def main(request):
    return render(request, 'layout/basic.html')
