from django.db import models
from django.contrib.auth.models import User
from accounts.models import Owner, Tenant

# Create your models here.
class pgDetails(models.Model):
    pgID = models.CharField(max_length=10, primary_key=True, unique=True, null=False)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)
    floors = models.IntegerField(null=False)
    rooms = models.IntegerField(null=False)
    name = models.CharField(max_length=100, null=False)
    address = models.TextField(max_length=2000, null=False)
    area = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    total_intakes = models.IntegerField(null=False)
    available_intakes = models.IntegerField(null=False)
    description = models.TextField(max_length=1000, null=False)
    start_rent = models.IntegerField(null=False)
    end_rent = models.IntegerField(null=False)
    type = models.CharField(max_length=100, null=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.pgID

class pgFacilities(models.Model):
    pg = models.OneToOneField(pgDetails, on_delete=models.CASCADE)
    ac = models.BooleanField(default=False)
    balcony = models.BooleanField(default=False)
    laundry = models.BooleanField(default=False)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)
    cleaning = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    fridge = models.BooleanField(default=False)
    ro = models.BooleanField(default=False)
    gym = models.BooleanField(default=False)
    lift = models.BooleanField(default=False)
    generator = models.BooleanField(default=False)

    def __str__(self):
        return self.pg

class roomDetails(models.Model):
    roomID = models.CharField(max_length=10, primary_key=True, unique=True, null=False)
    pg = models.OneToOneField(pgDetails, on_delete=models.CASCADE)
    roomNo = models.IntegerField()
    floorNo = models.IntegerField()
    totalBed = models.IntegerField()
    availableBed = models.IntegerField()
    rent = models.IntegerField()

    def __str__(self):
        return self.roomID

class pgPhotos(models.Model):
    pg = models.ForeignKey(pgDetails, on_delete=models.CASCADE)
    photoPID = models.CharField(max_length=200, null=False)
    message = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.photoPID

class pgRules(models.Model):
    pg = models.OneToOneField(pgDetails, to_field='pgID', on_delete=models.CASCADE)
    deposit = models.IntegerField(null=False)
    haveClosingTime = models.BooleanField(default=True)
    visitors = models.BooleanField(default=False)
    nonVeg = models.BooleanField(default=False)
    oppositeGender = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    drinking = models.BooleanField(default=False)
    loudMusic = models.BooleanField(default=False)
    party = models.BooleanField(default=False)

    def __str__(self):
        return self.pg

class applicationDetails(models.Model):
    applicationID = models.CharField(max_length=20, unique=True, primary_key=True, null=False)
    pg = models.OneToOneField(pgDetails, on_delete=models.CASCADE)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    owner = models.OneToOneField(Owner, on_delete=models.CASCADE)
    sentDate = models.DateField(auto_now=True)
    message = models.TextField(max_length=1000)
    joiningDate = models.DateField(null=False)
    approvedDate = models.DateField()
    isApproved = models.BooleanField(default=False)

    def __str__(self):
        return self.applicationID

class messages(models.Model):
    message = models.TextField(max_length=2000, null=False)
    mFrom = models.CharField(max_length=10, null=False)
    mTo = models.CharField(max_length=10, null=False)
    mDate = models.DateField(auto_now=True)
    mTime = models.TimeField(auto_now=True)

    def __str__(self):
        return self.message

class ratings(models.Model):
    pg = models.OneToOneField(pgDetails, on_delete=models.CASCADE)
    overall = models.FloatField(default=0.0)
    ac = models.FloatField(default=0.0)
    co = models.FloatField(default=0.0)
    balcony = models.FloatField(default=0.0)
    laundry = models.FloatField(default=0.0)
    breakfast = models.FloatField(default=0.0)
    lunch = models.FloatField(default=0.0)
    dinner = models.FloatField(default=0.0)
    parking = models.FloatField(default=0.0)
    cleaning = models.FloatField(default=0.0)
    wifi = models.FloatField(default=0.0)
    tv = models.FloatField(default=0.0)
    fridge = models.FloatField(default=0.0)
    ro = models.FloatField(default=0.0)
    gym = models.FloatField(default=0.0)
    lift = models.FloatField(default=0.0)
    generator = models.FloatField(default=0.0)

    def __str__(self):
        return self.pg

class pgApplication(models.Model):
    pg = models.OneToOneField(pgDetails, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    appicationDate = models.DateField(auto_now=True)
    appicationTime = models.TimeField(auto_now=True)