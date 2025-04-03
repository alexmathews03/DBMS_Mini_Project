from django.contrib import admin
from .models import Donor, Receiver

admin.site.register(Donor)
admin.site.register(Receiver)