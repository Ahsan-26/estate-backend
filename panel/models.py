from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} - {self.start_time} to {self.end_time}"


class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('buy', 'Buy Property'),
        ('sell', 'Sell Property'), 
        ('manage', 'Manage Property'),
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    query = models.TextField()
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES) 
    def __str__(self):
        return f"Appointment with {self.name} on {self.time_slot.date} at {self.time_slot.start_time}"

# Auto-update `is_booked` status when an appointment is created or deleted
@receiver(post_save, sender=Appointment)
def mark_slot_as_booked(sender, instance, **kwargs):
    instance.time_slot.is_booked = True
    instance.time_slot.save()

@receiver(post_delete, sender=Appointment)
def mark_slot_as_available(sender, instance, **kwargs):
    instance.time_slot.is_booked = False
    instance.time_slot.save()
    
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    author_image = models.ImageField(upload_to='authors/', blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name} - {self.email}"
