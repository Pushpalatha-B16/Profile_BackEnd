from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to="uploads/", null=True, blank=True)

    def __str__(self):
        return self.email