from django.contrib import admin
from .models import *

# Register your models here.


# class SheduleAdmin(admin.ModelAdmin):
#     ordering = ['day']
#     list_display=['department', 'batch', 'day']
#     fieldsets=(
#         ("Basic Info", {'fields': ('department', 'batch', 'day')}),
#         ("9:00 AM - 10:25 AM", {'fields': ('shift1_course', 'shift1_room', 'shift1_faculty')}),
#         ("10:30 AM - 11:55 AM", {'fields': ('shift2_course', 'shift2_room', 'shift2_faculty')}),
#         ("12:00 PM to 01:25 PM", {'fields': ('shift3_course', 'shift3_room', 'shift3_faculty')}),
#         ("01:30 PM to 02:55 PM", {'fields': ('shift4_course', 'shift4_room', 'shift4_faculty')}),
#         ("03:00 PM to 04:25 PM", {'fields': ('shift5_course', 'shift5_room', 'shift5_faculty')}),
#         ("04:30 PM to 05:55 PM", {'fields': ('shift6_course', 'shift6_room', 'shift6_faculty')}),
#     )
#     search_fields=('department', 'day', 'batch')

admin.site.register([Shedule, Details, Shift])