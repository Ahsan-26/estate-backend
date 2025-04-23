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
from django.db.models import F, ExpressionWrapper, IntegerField

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
        # slots = TimeSlot.objects.filter(is_booked=False).order_by("date", "start_time")
        slots = TimeSlot.objects.annotate(
            available=ExpressionWrapper(
                F('max_clients') - F('booked_clients'),
                output_field=IntegerField()
            )
        ).filter(available__gt=0).order_by("date", "start_time")
        
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
        #     time_slot = TimeSlot.objects.get(id=time_slot_id, is_booked=False)
        # except TimeSlot.DoesNotExist:
        #     return Response({"error": "Selected time slot is no longer available"}, status=status.HTTP_400_BAD_REQUEST)
            time_slot = TimeSlot.objects.get(id=time_slot_id)
            if time_slot.booked_clients >= time_slot.max_clients:
                return Response({"error": "Slot is full"}, status=400)
        except TimeSlot.DoesNotExist:
            return Response({"error": "Invalid slot"}, status=400)
        

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
        message = f"""Hi {name},

Thank you for scheduling a call with EstateOne. Your appointment is confirmed!

An advisor will call you on {phone} at the designated hour and help you with your queries. Also, while we try to reach you at precisely the specified time, there could be a slight delay if the advisor is still dealing with a prior appointment. Please give us an extra 5–10 mins.

However, if you still don’t hear from us or you want to reschedule this conversation, just drop an e-mail on this thread and we will sort it out for you.

Please note that all conversations with our advisor will be recorded for regulatory purposes. And we may communicate with you over WhatsApp, e-mail, and SMS. If you prefer to have your communication scheduled only on a specific medium, please let us know and we will accommodate this request.

Appointment Details:
Date: {time_slot.date}
Time: {converted_start_time.strftime('%I:%M %p')}

Quick Reminders:
- The 30-minute conversation will be insightful, so keep your questions ready!
- We’ll share useful links, quotes, and other details to make everything simpler for you.
- Don’t worry—we won’t spam you with calls. We’ll only reach out when you ask us to.

We're excited to have you on board and look forward to speaking with you!

Warm regards,
EstateOne"""

        send_mail(
            subject="Appointment Confirmation",
            # message=f"Dear {name}, your appointment is confirmed for {time_slot.date} at {converted_start_time.strftime('%I:%M %p')}.",
            message=message,
            from_email="connect@estateone.in",  
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
            from_email="connect@estateone.in",  
            recipient_list=["connect@estateone.in"],  
            fail_silently=False,
        )

        return Response({"message": "Appointment booked successfully!"}, status=status.HTTP_201_CREATED)

class InquiryCreateView(generics.CreateAPIView):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

    def create(self, request, *args, **kwargs):
        # Create the serializer instance with the request data
        serializer = self.get_serializer(data=request.data)
        
        # Check if the serializer is valid
        if serializer.is_valid():
            # Save the validated data (if needed)
            serializer.save()

            # Return success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If validation fails, return the errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
