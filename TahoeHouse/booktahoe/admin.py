from django.contrib import admin
from booktahoe.models import Night,Guest,Comment,UserAttributes,Attending

# Register your models here.
admin.site.register(Night)
admin.site.register(Guest)
admin.site.register(Comment)
admin.site.register(UserAttributes)
admin.site.register(Attending)