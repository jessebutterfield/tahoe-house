from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Night(models.Model):
    night = models.DateField()
    members = models.ManyToManyField(User)
    
    def __unicode__(self):  # Python 3: def __str__(self):
        return unicode(self.night)
    
class Guest(models.Model):
    name = models.CharField(max_length=200)
    night = models.ForeignKey(Night)
    host = models.ForeignKey(User)
        
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

class Comment(models.Model):
    text = models.TextField()
    night = models.ForeignKey(Night)
    poster = models.ForeignKey(User)
        
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name