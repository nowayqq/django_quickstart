from django.contrib import admin
from tutorial.quickstart.models import Tweet, Followers

# Register your models here.
admin.site.register(Tweet)
admin.site.register(Followers)
