from django.db import models
from django.core.exceptions import ValidationError
import uuid

class University(models.Model):
    name = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='university_logo/', blank=True, null=True)
    location = models.CharField(max_length=1000, blank=True, null=True)
    details = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"
    
    def clean(self):
        # Normalize input: remove spaces and lowercase
        normalized_name = ''.join(self.name.lower().split())

        # Check for duplicates
        existing = University.objects.exclude(pk=self.pk)
        for university in existing:
            if ''.join(university.name.lower().split()) == normalized_name:
                raise ValidationError("A University with this name (ignoring case and spaces) already exists.")

    def save(self, *args, **kwargs):
        self.full_clean()  # This calls `clean()` and raises ValidationError if needed
        super().save(*args, **kwargs)


# Create your models here.
class Department(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"
    

class Batch(models.Model):
    department = models.ForeignKey(Department, related_name='batches', on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"Batch: {self.name} ----- {self.department.name}"
    

class Routeen(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    title = models.CharField(max_length=2000)
    pdf_file = models.FileField(upload_to='routeens/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.department.name}:-- {self.title}"
    


class EmailSubscription(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email