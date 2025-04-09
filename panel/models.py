from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.text import slugify

class TimeSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_clients = models.PositiveIntegerField(default=1)  # New field
    booked_clients = models.PositiveIntegerField(default=0)  # New field

    def is_available(self):
        return self.booked_clients < self.max_clients

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
    location = models.CharField(max_length=255)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)       
    service_type = models.CharField(max_length=10, choices=SERVICE_CHOICES) 
    def __str__(self):
        return f"Appointment with {self.name} on {self.time_slot.date} at {self.time_slot.start_time}"

# Auto-update `is_booked` status when an appointment is created or deleted
# @receiver(post_save, sender=Appointment)
# def mark_slot_as_booked(sender, instance, **kwargs):
#     instance.time_slot.is_booked = True
#     instance.time_slot.save()

# @receiver(post_delete, sender=Appointment)
# def mark_slot_as_available(sender, instance, **kwargs):
#     instance.time_slot.is_booked = False
#     instance.time_slot.save()

@receiver(post_save, sender=Appointment)
def update_booked_clients(sender, instance, created, **kwargs):
    if created:  # Only increment when a new appointment is created
        time_slot = instance.time_slot
        time_slot.booked_clients += 1
        time_slot.save()

@receiver(post_delete, sender=Appointment)
def update_booked_clients_on_delete(sender, instance, **kwargs):
    time_slot = instance.time_slot
    time_slot.booked_clients -= 1
    time_slot.save()
    
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='authors/')

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='blogs/')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    reading_time = models.PositiveIntegerField(help_text="Reading time in minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class BlogSection(models.Model):
    blog = models.ForeignKey(Blog, related_name='sections', on_delete=models.CASCADE)
    heading = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"{self.blog.title} - {self.heading}"

class Inquiry(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Inquiry from {self.name} - {self.email}"
