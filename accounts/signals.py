from django.db.models.signals import post_save # a way to do signals; see documentation
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group


# instance will be our user
# the parameters have to be the exact names put in; otherwise won't work
def customerProfile(sender, instance, created, **kwargs):
    if created:
        #group = Group.objects.get(name='customer')
        group, created = Group.objects.get_or_create(name='customer')
        instance.groups.add(group)
        Customer.objects.create(
            user=instance,
            name=instance.username,
            )
# this will actually create the user
post_save.connect(customerProfile, sender=User)
