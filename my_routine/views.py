from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *

# Create your views here.
@login_required(login_url='signin') 
def shedule_view(request):
    user = request.user
    university = getattr(user, 'university', None)
    department = getattr(user, 'department', None)
    batch = getattr(user, 'batch', None)

    DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    shifts = Shift.objects.filter(university=university) if university else Shift.objects.none()
    shedules = Shedule.objects.filter(department=department, batch=batch) if department and batch else Shedule.objects.none()

    return render(request, 'shedule.html', {
        'days': DAYS,
        'shedule': shedules,
        'shifts': shifts,
    })

@login_required(login_url='signin') 
def shedule_update(request):
    user = request.user

    if not (user.is_CR or user.is_staff or user.is_superuser):
        return redirect('/')

    university = getattr(user, 'university', None)
    department = getattr(user, 'department', None)
    batch = getattr(user, 'batch', None)
    DAYS = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    shifts = Shift.objects.filter(university=university) if university else Shift.objects.none()
    shedules = {s.day: s for s in Shedule.objects.filter(department=department, batch=batch)} if department and batch else {}

    if request.method == 'POST':
        for day in DAYS:
            shedule = shedules.get(day)
            if not shedule:
                shedule = Shedule.objects.create(department=department, batch=batch, day=day)
                shedules[day] = shedule

            for shift in shifts:
                subject = request.POST.get(f"routine_{day}_{shift.id}_subject", "").strip()
                room = request.POST.get(f"routine_{day}_{shift.id}_room", "").strip()
                faculty = request.POST.get(f"routine_{day}_{shift.id}_faculty", "").strip()

                if subject or room or faculty:
                    detail, created = Details.objects.get_or_create(
                        shedule=shedule,
                        shift=shift,
                        defaults={'course': subject, 'room': room, 'faculty': faculty}
                    )
                    if not created:
                        detail.course = subject
                        detail.room = room
                        detail.faculty = faculty
                        detail.save()

        messages.success(request, "Schedule updated successfully.")
        return redirect('my_shedule')  # Or use request.path if no named URL

    return render(request, 'shedule_update.html', {
        'days': DAYS,
        'shifts': shifts,
        'shedule': shedules,
    })