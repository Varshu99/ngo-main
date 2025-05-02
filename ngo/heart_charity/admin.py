
from django.contrib import admin
from .models import Volunteer, Contact, Cause, Donate
from .models import Event

# Register your models here.
admin.site.register(Volunteer)
admin.site.register(Contact)
admin.site.register(Cause)
admin.site.register(Donate)
admin.site.register(Event)
