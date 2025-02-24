from django.urls import path
from .views import AvailableSlotsView, BookAppointmentView
from .views import BlogListCreateView, BlogRetrieveUpdateDestroyView
urlpatterns = [
    path('available_slots/', AvailableSlotsView.as_view(), name='available_slots'),
    path('book_appointment/', BookAppointmentView.as_view(), name='book_appointment'),
    path('blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('blogs/<int:pk>/', BlogRetrieveUpdateDestroyView.as_view(), name='blog-detail'),
]
