from django.shortcuts import render,get_object_or_404
from .models import User, AgProfile
from .forms import ProfileForm
from apps.oinfo import oinfo
from apps.feeder.models import SiteFeeder

def select_subscribes(user):
    profile_subscribes = AgProfile.objects.get(user=user.id).subscribe_to.values() # выбираем значения по полю subscribe_to 
    return {x['name']:x['active'] for x in profile_subscribes} #словарь с активными подписками


def get_profile(request,username):

    user = User.objects.get(username=username)
    profile_subscribes = select_subscribes(user)

    #oinfo (profile_subscribes)
    if request.method == 'POST':

        form = ProfileForm(request.POST)
        if form.is_valid():

            subscribe_to = [SiteFeeder.objects.get(name=key) for key,value in form.cleaned_data.items() if value == True] #выбыраем поля с True
            #instance = AgProfile.objects.get(user=user) # таким способом нужно
            instance = get_object_or_404(AgProfile, user=user)
            instance.subscribe_to.set(subscribe_to) # сохранять в базу many2many field

            profile_subscribes = select_subscribes(user) # снова делаем выборку подписок юэера
    else:
        form = ProfileForm()

    #print ("-render agprofile/profile.html-")
    return render(request,'agprofile/profile.html', {'user':user, 'form':form,'profile_subscribes':profile_subscribes})