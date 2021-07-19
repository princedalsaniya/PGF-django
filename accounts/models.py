from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenantID = models.CharField(max_length=200, unique=True, primary_key=True)
    phone = models.CharField(max_length=10, unique=True)
    workplace = models.CharField(max_length=500)
    bdate = models.DateField(null=False)
    # isVarified = models.BooleanField(default=False)
    profilePicID = models.CharField(unique=True, max_length=200, null=True)
    adharNo = models.CharField(unique=True, max_length=20, null=False)

    def __str__(self):
        return self.tenantID

class Owner(models.Model):
    ownerID = models.CharField(max_length=200, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, unique=True)
    # isVarified = models.BooleanField(default=False)
    profilePicID = models.CharField(unique=True, max_length=200, null=False)
    adharNo = models.CharField(unique=True, max_length=20, null=False)

    def __str__(self):
        return self.ownerID