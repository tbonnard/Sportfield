from django.contrib import admin
from .models import User, Category, Club, Field, Booking, Schedule

# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "field", 'date_book', 'timestamp') 

class FieldAdmin(admin.ModelAdmin):
    list_display = ("field_name", 'club', 'category', 'price') 

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", 'email') 

class ClubAdmin(admin.ModelAdmin):
    list_display = ('club', "owner_club")

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('field', 'schedule_time')


admin.site.register(User, UserAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Category)
admin.site.register(Field, FieldAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Schedule, ScheduleAdmin)