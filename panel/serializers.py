from rest_framework import serializers
from .models import TimeSlot, Appointment
from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

class TimeSlotSerializer(serializers.ModelSerializer):
    formatted_start_time = serializers.SerializerMethodField()
    formatted_end_time = serializers.SerializerMethodField()

    class Meta:
        model = TimeSlot
        fields = ['id', 'date', 'start_time', 'end_time', 'is_booked', 'formatted_start_time', 'formatted_end_time']

    def get_formatted_start_time(self, obj):
        timezone = self.context.get('timezone', 'Asia/Kolkata')  # Default to IST
        tz = pytz.timezone(timezone)
        return localtime(obj.start_time, tz).strftime("%I:%M %p")

    def get_formatted_end_time(self, obj):
        timezone = self.context.get('timezone', 'Asia/Kolkata')
        tz = pytz.timezone(timezone)
        return localtime(obj.end_time, tz).strftime("%I:%M %p")

class AppointmentSerializer(serializers.ModelSerializer):
    time_slot_details = TimeSlotSerializer(source="time_slot", read_only=True)

    class Meta:
        model = Appointment
        fields = ['id', 'name', 'email', 'phone', 'query', 'time_slot', 'time_slot_details']

    def validate_time_slot(self, value):
        """Ensure the slot is not already booked"""
        if Appointment.objects.filter(time_slot=value).exists():
            raise serializers.ValidationError("This time slot is already booked.")
        return value