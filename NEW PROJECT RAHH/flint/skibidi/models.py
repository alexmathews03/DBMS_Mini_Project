from django.db import models

class Donor(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    has_disqualifying_disease = models.BooleanField(
        default=False,
        verbose_name="Do you have HIV, Hepatitis B/C, or other blood-borne diseases?"
    )

    def save(self, *args, **kwargs):
        if self.has_disqualifying_disease:
            raise ValueError("Cannot save donor with disqualifying diseases")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Receiver(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Plaintext (for demo)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    medical_condition = models.CharField(max_length=255, blank=True, null=True)  # Optional

    def __str__(self):
        return self.name