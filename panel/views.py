from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.utils.timezone import make_aware
from django.utils.timezone import localtime
from pytz import timezone as pytz_timezone
from datetime import datetime
from .models import TimeSlot, Appointment, Inquiry, Blog
from .serializers import TimeSlotSerializer, AppointmentSerializer, BlogSerializer,InquirySerializer
from rest_framework import generics

class BlogDetailAPIView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'pk'

class BlogListAPIView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

# ✅ Get available time slots
class AvailableSlotsView(APIView):
    def get(self, request):
        user_timezone = request.query_params.get("timezone", "Asia/Kolkata")  # Default to IST

        # Get all available (not booked) slots
        slots = TimeSlot.objects.filter(is_booked=False).order_by("date", "start_time")

        available_dates = {}
        for slot in slots:
            slot_date = slot.date.strftime("%Y-%m-%d")

            # Convert slot time to user-specified timezone
            slot_start_time = make_aware(datetime.combine(slot.date, slot.start_time))
            converted_start_time = slot_start_time.astimezone(pytz_timezone(user_timezone))

            slot_end_time = make_aware(datetime.combine(slot.date, slot.end_time))
            converted_end_time = slot_end_time.astimezone(pytz_timezone(user_timezone))

            # Add slot under the corresponding date
            if slot_date not in available_dates:
                available_dates[slot_date] = []
            
            available_dates[slot_date].append({
                "id": slot.id,
                "start_time": converted_start_time.strftime("%I:%M %p"),  # Convert to readable format
                "end_time": converted_end_time.strftime("%I:%M %p"),
            })

        return Response({"dates": available_dates}, status=status.HTTP_200_OK)

# ✅ Book an appointment and send emails
class BookAppointmentView(APIView):
    def post(self, request, *args, **kwargs):
        service_type = request.data.get("service_type")
        time_slot_id = request.data.get("time_slot_id")
        name = request.data.get("name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        query = request.data.get("query")
        location = request.data.get("location")

        if not all([time_slot_id, name, email, phone, query]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            time_slot = TimeSlot.objects.get(id=time_slot_id, is_booked=False)
        except TimeSlot.DoesNotExist:
            return Response({"error": "Selected time slot is no longer available"}, status=status.HTTP_400_BAD_REQUEST)

        # Create and save the appointment
        appointment = Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            query=query,
            location=location,
            time_slot=time_slot,
            service_type=service_type 
        )

        # ✅ Mark the slot as booked
        time_slot.is_booked = True
        time_slot.save()

        # ✅ Convert time slot to readable format
        user_timezone = request.query_params.get("timezone", "Asia/Kolkata")
        slot_start_time = make_aware(datetime.combine(time_slot.date, time_slot.start_time))
        converted_start_time = slot_start_time.astimezone(pytz_timezone(user_timezone))

        # ✅ Send confirmation email to the client
        send_mail(
            subject="Appointment Confirmation",
            message=f"Dear {name}, your appointment is confirmed for {time_slot.date} at {converted_start_time.strftime('%I:%M %p')}.",
            from_email="rehankhan.upr@gmail.com",  
            recipient_list=[email],
            fail_silently=False,
        )

        # ✅ Send notification email to the admin
        send_mail(
            subject="New Appointment Booked",
            message=f"A new appointment has been booked:\n\n"
                    f"Name: {name}\n"
                    f"Date: {time_slot.date}\n"
                    f"Time: {converted_start_time.strftime('%I:%M %p')}\n"
                    f"Phone: {phone}\n"
                    f"Email: {email}\n"
                    f"Query: {query}",
            from_email="rehankhan.upr@gmail.com",  
            recipient_list=["rehankhan.upr@gmail.com"],  
            fail_silently=False,
        )

        return Response({"message": "Appointment booked successfully!"}, status=status.HTTP_201_CREATED)

class InquiryCreateView(generics.CreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

    def create(self, request, *args, **kwargs):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)