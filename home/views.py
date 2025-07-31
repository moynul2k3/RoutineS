from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from my_routine.models import *
from django.contrib import messages
from collections import defaultdict
import datetime
import re
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
    if request.user.is_authenticated:
        user = request.user
        university = getattr(user, 'university', None)
        department = getattr(user, 'department', None)
        batch = getattr(user, 'batch', None)
        today_name = datetime.datetime.today().strftime('%A')
        today = today_name.lower()

        shifts = Shift.objects.filter(university=university) if university else Shift.objects.none()

        # Queryset filtered by today's day
        shedules = Shedule.objects.filter(department=department, batch=batch, day__iexact=today) if department and batch else Shedule.objects.none()

        return render(request, 'home.html', {
            'day': today,
            'shedules': shedules,  # queryset with today's schedule(s)
            'shifts': shifts,
        })
    return render(request, 'home.html')




@login_required(login_url='signin') 
def routeenList(request):
    user = request.user
    university = getattr(user, 'university', None)
    department = getattr(user, 'department', None)
    batch = getattr(user, 'batch', None)


    if university and department and batch:
        routeens = Routeen.objects.filter(university=university, department=department, batch=batch)
    else:
        routeens = Routeen.objects.none()
    return render(request, 'routeenList.html', {'routeens': routeens})



@login_required(login_url='signin') 
def routeen(request, pk):
    routeen = Routeen.objects.filter(pk=pk).first()
    return render(request, 'routeen.html', {'routeen': routeen})


@login_required
def university_detail_view(request):
    user = request.user
    selected_university = None
    universities = []

    # Staff or superuser: show dropdown to select any university
    if user.is_staff or user.is_superuser:
        universities = University.objects.all()
        university_id = request.GET.get('university_id')
        if university_id:
            selected_university = get_object_or_404(University, id=university_id)

    # CR user: show their university only
    else :
        selected_university = getattr(user, 'university', None)

    # Get related departments, batches, and shifts if university is selected
    departments = []
    shifts = []
    if selected_university:
        departments = selected_university.department_set.prefetch_related('batches').all()
        shifts = selected_university.shift_set.all()

    context = {
        'universities': universities,
        'selected_university': selected_university,
        'departments': departments,
        'shifts': shifts,
    }

    return render(request, 'university_detail_view.html', context)





from collections import defaultdict

@login_required(login_url='signin') 
def manage_university(request):
    user = request.user
    if not (user.is_staff or user.is_superuser):
        return redirect('/')

    if request.method == 'POST':
        university_name = request.POST.get('university_name')
        university_logo = request.FILES.get('university_logo')  # Use FILES for image
        university_location = request.POST.get('university_location')
        university_details = request.POST.get('university_details')

        university = University.objects.create(
            name=university_name,
            logo=university_logo,
            location=university_location,
            details=university_details
        )

        # Create shifts
        for shift_duration in request.POST.getlist('shifts[]'):
            if shift_duration.strip():
                Shift.objects.create(university=university, duration=shift_duration.strip())

        # Parse departments and batches
        from collections import defaultdict
        dept_data = defaultdict(lambda: {'name': '', 'batches': []})

        for key in request.POST:
            if key.startswith('departments'):
                parts = key.split('[')
                index = parts[1][:-1]
                field = parts[2][:-1]

                if field == 'name':
                    dept_data[index]['name'] = request.POST.get(key)
                elif field == 'batches':
                    dept_data[index]['batches'].extend(request.POST.getlist(key))  # <- Use getlist here

        for data in dept_data.values():
            dept = Department.objects.create(university=university, name=data['name'])
            for batch_name in data['batches']:
                if batch_name.strip():
                    Batch.objects.create(department=dept, name=batch_name.strip())

        messages.success(request, "University and related data saved successfully!")
        return redirect('university_detail_view')

    return render(request, 'manage_university.html')


@login_required(login_url='signin') 
def update_university(request, university_id):
    university = get_object_or_404(University, id=university_id)

    user = request.user
    if not (user.is_staff or user.is_superuser or user.is_CR):
        return redirect('/')

    if request.method == 'POST':
        # Update university basic info
        university.name = request.POST.get('university_name')
        university.location = request.POST.get('university_location')
        university.details = request.POST.get('university_details')

        
        logo = request.FILES.get('university_logo')
        if logo:
            university.logo = logo
        university.save()

        # Clear and recreate shifts
        university.shift_set.all().delete()
        for shift_duration in request.POST.getlist('shifts[]'):
            if shift_duration.strip():
                Shift.objects.create(university=university, duration=shift_duration.strip())

        # Clear departments and batches
        university.department_set.all().delete()

        # Extract and parse departments and batches
        departments_data = defaultdict(lambda: {'name': '', 'batches': []})

        for key in request.POST:
            match = re.match(r'^departments\[(\d+)]\[(\w+)]', key)
            if match:
                index, field = match.groups()
                if field == 'name':
                    departments_data[index]['name'] = request.POST.get(key)
                elif field == 'batches':
                    # getlist for all batches under same key
                    departments_data[index]['batches'].extend(request.POST.getlist(key))

        # Save departments and batches
        for data in departments_data.values():
            if data['name'].strip():
                department = Department.objects.create(university=university, name=data['name'].strip())
                for batch_name in data['batches']:
                    if batch_name.strip():
                        Batch.objects.create(department=department, name=batch_name.strip())

        messages.success(request, "University updated successfully!")
        # return redirect('update_university', university_id=university.id)
        return redirect('university_detail_view')

    context = {
        'university': university,
        'shifts': university.shift_set.all(),
        'departments': university.department_set.prefetch_related('batches').all()
    }
    return render(request, 'update_university.html', context)


@login_required(login_url='signin') 
def create_routeen(request):
    user = request.user
    if not (user.is_CR or user.is_staff or user.is_superuser):
        return redirect('/')
    if request.method == 'POST':
        university_id = request.POST.get('university')
        department_id = request.POST.get('department')
        batch_id = request.POST.get('batch')
        title = request.POST.get('title')
        pdf_file = request.FILES.get('pdf_file')

        if university_id and department_id and batch_id and title and pdf_file:
            Routeen.objects.create(
                university_id=university_id,
                department_id=department_id,
                batch_id=batch_id,
                title=title,
                pdf_file=pdf_file
            )
            return redirect('routeenlist')  # or your desired redirect
    
    if user.is_staff or user.is_superuser:
        universities = University.objects.all()
        departments = Department.objects.all()
        batches = Batch.objects.all()
    elif user.is_CR:
        universities = University.objects.filter(id=user.university.id) if hasattr(user, 'university') and user.university else University.objects.none()
        departments = Department.objects.filter(id=user.department.id) if hasattr(user, 'department') and user.department else Department.objects.none()
        batches = Batch.objects.filter(id=user.batch.id) if hasattr(user, 'batch') and user.batch else Batch.objects.none()
    else:
        universities = University.objects.none()
        departments = Department.objects.none()
        batches = Batch.objects.none()
    return render(request, 'routeen_form.html', {
        'universities': universities,
        'departments': departments,
        'batches': batches,
        'is_edit': False,
    })

@login_required(login_url='signin') 
def edit_routeen(request, pk):
    user = request.user
    if not (user.is_CR or user.is_staff or user.is_superuser):
        return redirect('/')

    routeen = get_object_or_404(Routeen, pk=pk)

    if request.method == 'POST':
        routeen.university_id = request.POST.get('university')
        routeen.department_id = request.POST.get('department')
        routeen.batch_id = request.POST.get('batch')
        routeen.title = request.POST.get('title')
        if request.FILES.get('pdf_file'):
            routeen.pdf_file = request.FILES.get('pdf_file')
        routeen.save()
        return redirect('routeenlist')

    
    if user.is_staff or user.is_superuser:
        universities = University.objects.all()
        departments = Department.objects.all()
        batches = Batch.objects.all()
    elif user.is_CR:
        universities = University.objects.filter(id=user.university.id) if hasattr(user, 'university') and user.university else University.objects.none()
        departments = Department.objects.filter(id=user.department.id) if hasattr(user, 'department') and user.department else Department.objects.none()
        batches = Batch.objects.filter(id=user.batch.id) if hasattr(user, 'batch') and user.batch else Batch.objects.none()
    else:
        universities = University.objects.none()
        departments = Department.objects.none()
        batches = Batch.objects.none()
    return render(request, 'routeen_form.html', {
        'routeen': routeen,
        'universities': universities,
        'departments': departments,
        'batches': batches,
        'is_edit': True,
    })


from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

@csrf_protect
@require_POST
def subscribe_email_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email is required.'}, status=400)

        subscription, created = EmailSubscription.objects.get_or_create(email=email)
        if created:
            return JsonResponse({'status': 'success', 'message': 'Thanks for subscribing!'})
        else:
            return JsonResponse({'status': 'info', 'message': 'You are already subscribed.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)