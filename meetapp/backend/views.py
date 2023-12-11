from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .forms import CreateProfileForm, ChangeProfileForm, LikeForm

from .models import Profile, Match, AdvUser

from django.urls import reverse_lazy

from django.views.generic.edit import CreateView, UpdateView

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

#request, slug, model_class=Event, form_class=RSVPForm,
#                template_name='rsvp/event_view.html'

# def CreateProfileView(request, model_class=Profile, form_class = CreateProfileForm, ):
#     template_name = 'profile/create_profile.html'
#     success_url = reverse_lazy('backend:start')


# class CreateProfileView(CreateView):
#     model = Profile
#     template_name = 'profile/profile_create.html'
#     form_class = CreateProfileForm
#     success_url = reverse_lazy('backend:start')

def create_profile(request):
    canCreate = True
    if Profile.objects.get(advUser = request.user):
        canCreate = False

    if request.method == 'POST':
        data = request.POST.copy()
        data.update({'advuser': request.user})
        print('ЧЕК')
        form = CreateProfileForm(data)
        if form.is_valid():
            form.advuser = request.user
            form.save()
            return render(request, 'layout/basic.html')
        
    else:
        form = CreateProfileForm
        return render(request, 'profile/profile_create.html', {'form': form, 'canCreate': canCreate})
    
def view_profile(request, username):
    message = ''
    user2 = get_object_or_404(AdvUser, username=username)
    if request.method == 'POST':
        form = LikeForm
        try: 
            Match.objects.get(giveLikeUser = request.user, getLikeUser = user2)
            message = 'Вы уже поставили лайк этому пользователю'
        except:
            Match.objects.create(giveLikeUser = request.user, getLikeUser = user2)
            return render(request, 'profile/profile_liked.html', {'user': user2})
            
    else:
        form = LikeForm
    return render(request, 'profile/profile_view.html', {'user': user2, 'form': form, 'message': message})



class ChangeProfileView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile/profile_change.html'
    form_class = ChangeProfileForm
    success_url = reverse_lazy ('backend:start')
    success_message = 'Анкета изменена'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)
    
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


def main(request):
    profiles = Profile.objects.all()
    return render(request, 'layout/basic.html', {'profiles': profiles})
