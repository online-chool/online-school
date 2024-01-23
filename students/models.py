from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Student(models.Model):
    phone_number = PhoneNumberField(unique=True)
    telegram_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)

    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    @property
    def full_name(self):
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    def __str__(self):
        return self.full_name
    