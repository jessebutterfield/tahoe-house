from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Night(models.Model):
    night = models.DateField()
    attendees = models.ManyToManyField(User,through='Attending')
    notcoming = models.ManyToManyField(User,related_name='unnights')
    
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.night)
    
class Attending(models.Model):
    member = models.ForeignKey(User)
    plusOne = models.BooleanField(default=False)
    night = models.ForeignKey(Night)
    parkingRequests = models.IntegerField(default=0)
    createdOn = models.DateTimeField(auto_now_add=True)
    
class Guest(models.Model):
    name = models.CharField(max_length=200)
    attend = models.ForeignKey(Attending)
    paid = models.BooleanField(default=False)
        
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField()
    night = models.ForeignKey(Night)
    poster = models.ForeignKey(User)
        
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    
class UserAttributes(models.Model):
    user = models.OneToOneField(User)
    sigMember = models.OneToOneField(User,related_name='dater',blank=True,null=True)
    