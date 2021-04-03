from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

ROLE_CHOICES = [
    ('1', 'User'),
    ('2', 'Doctor'),
]


class Doctor(models.Model):
    firstname = models.CharField(max_length=100, null=False, blank=False)
    lastname = models.CharField(max_length=100, null=False, blank=False)
    medicalNumber = models.IntegerField(null=False, blank=False)
    city = models.CharField(max_length=100, null=True, blank=True)
    educationDegree = models.CharField(max_length=100, null=False, blank=False)
    medicalExpertise = models.CharField(max_length=100, null=False, blank=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    # favoriteDoctors = models.ForeignKey(UserPanel, on_delete=models.CASCADE, related_name="Doctor")

    def __str__(self):
        return self.lastname


class UserPanel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=8, choices=ROLE_CHOICES)
    favoriteDoctors = models.ManyToManyField(Doctor)
    age = models.IntegerField()
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


class VisitTime(models.Model):
    user = models.ForeignKey(UserPanel, on_delete=models.CASCADE)
    visitDate = models.DateField()
    visitTime = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__() + " " + self.visitDate.__str__() + " " + self.visitTime.__str__()


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)

    def __str__(self):
        return "From "+self.user.username+" To "+self.doctor.lastname+": "+self.text
