from django.contrib import admin
from .models import TimeSlot, Appointment
from .models import Blog
from .models import Blog, Author, BlogSection, Inquiry
from django.contrib.auth.models import User, Group

admin.site.register(TimeSlot)
admin.site.unregister(User)
admin.site.unregister(Group)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "location", "time_slot")  # Fields displayed in the list view
    search_fields = ("name", "email", "phone", "location")  # Enable searching by these fields
    list_filter = ("location", "time_slot")  # Add filtering options

    # Set fields as read-only
    readonly_fields = ("name", "email", "phone", "query", "location", "time_slot", "service_type")

    def has_add_permission(self, request):
        """Prevent admin from adding new records manually."""
        return False
    def has_change_permission(self, request, obj=None):
        return False  # ❌ Disable "Save" button

    

admin.site.register(Appointment, AppointmentAdmin)

class BlogSectionInline(admin.StackedInline):
    model = BlogSection
    extra = 1

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'reading_time', 'created_at')
    search_fields = ('title', 'author__name')
    list_filter = ('author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogSectionInline]

class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "message")  # Show these fields in the list view
    search_fields = ("name", "phone", "email", "message")  # Enable search bar
    list_filter = ("email",)  # Enable filtering by email

    # Make all fields read-only
    readonly_fields = ("name", "phone", "email", "message")

    # **Disable all editing, adding, and deleting options**
    def has_add_permission(self, request):
        return False  # ❌ Disable "Add" button

    def has_change_permission(self, request, obj=None):
        return False  # ❌ Disable "Save" button

# Register the Inquiry model with these settings
admin.site.register(Inquiry, InquiryAdmin)

admin.site.site_header = "Estate Management Admin Panel"  # Top Left Title
admin.site.site_title = "Estate Admin"  # Browser Tab Title
admin.site.index_title = "Welcome to Estate Management Dashboard" 
