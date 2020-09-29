from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from apps.feeder.models import SiteFeeder

class AgProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,unique=True) # id of user
    subscribe_to = models.ManyToManyField(SiteFeeder,blank=True)

    def __str__(self):
    	return f"{self.user}"

########    Signals создание профайла при создании юзера    ##########
def create_profile(sender,**kwargs ):
    if kwargs['created']:
        user_profile=AgProfile.objects.create(user=kwargs['instance'])
post_save.connect(create_profile,sender=User)
#######################################################################

#User.agprofile = property(lambda u:AgProfile.objects.get_or_create(user=u)[0])
