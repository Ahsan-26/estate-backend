from django.urls import path
from .views import AvailableSlotsView, BookAppointmentView
from .views import BlogDetailAPIView, BlogListAPIView, InquiryCreateView

urlpatterns = [
    path('available_slots/', AvailableSlotsView.as_view(), name='available_slots'),
    path('book_appointment/', BookAppointmentView.as_view(), name='book_appointment'),
    path('blogs/', BlogListAPIView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogDetailAPIView.as_view(), name='blog-detail'),
    path("inquiries/submit/", InquiryCreateView.as_view(), name="inquiry-submit"),
]
