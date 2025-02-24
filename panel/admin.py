from django.contrib import admin
from .models import TimeSlot, Appointment
from .models import Blog, Inquiry

admin.site.register(Blog)
admin.site.register(TimeSlot)
admin.site.register(Appointment)
admin.site.register(Inquiry)
