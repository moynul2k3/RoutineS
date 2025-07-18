from django.db import models
from home.models import *
# Create your models here.
DAY_CHOICE = {
    'sunday': 'Sunday',
    'monday': 'Monday',
    'tuesday': 'Tuesday',
    'wednesday': 'Wednesday',
    'thursday': 'Thursday',
    'friday': 'Friday',
    'saturday': 'saturday',
}

class Shift(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    duration = models.CharField(max_length=500)
    shift_no = models.PositiveIntegerField(blank=True, null=True, editable=False)

    class Meta:
        ordering = ['university', 'shift_no']
        unique_together = ('university', 'shift_no')

    def __str__(self):
        return f"{self.duration} - {self.university.name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            last_shift = Shift.objects.filter(university=self.university).order_by('-shift_no').first()
            self.shift_no = (last_shift.shift_no + 1) if last_shift else 1
        super().save(*args, **kwargs)



class Shedule(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    day = models.CharField(choices=DAY_CHOICE, default='sunday', max_length=500)

    def __str__(self):
        return f"{self.day}: {self.department.name}"
    
class Details(models.Model):
    shedule = models.ForeignKey(Shedule, on_delete=models.CASCADE, related_name='details')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    course = models.CharField(max_length=500, verbose_name='Course Name')
    room = models.CharField(max_length=500, verbose_name='Romm no.')
    faculty = models.CharField(max_length=500, verbose_name='Faculty details')

    def __str__(self):
        return f"{self.shift.duration}----{self.course}"