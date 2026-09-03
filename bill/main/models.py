from django.db import models
from datetime import datetime

# Create your models here.
rooms= (('1', '1:Balcony room'),
        ('2', '2:Back right room'),
        ('3', '3:Back left room'),
        ('4', '4:Top room'))
#should i make rooms class?

class Tenant(models.Model):
  
    name            = models.CharField(max_length=100,null=False)
    DOB             = models.DateField(null=True,blank=True)
    occup           = models.CharField(max_length=100,null=True,blank=True)
    mother_name     = models.CharField(max_length=100,null=True,blank=True)
    father_name     = models.CharField(max_length=100,null=True,blank=True)
    parents_contact = models.CharField(max_length=100,null=True,blank=True)
    hometown        = models.CharField(max_length=100,null=True,blank=True)
    address         = models.TextField(null=True,blank=True)
    contact         = models.CharField(max_length=100,null=True)
    ID_proof        = models.FileField(null=True,blank=True)
    room            = models.CharField(null=True,choices=rooms)
    status          = models.BooleanField(null=True)
    joined_date     = models.DateTimeField(null=True,blank=True)
    leaving_date    = models.DateTimeField(null=True,blank=True)
    #paid_date      = models.DateTimeField(null=True,blank=True)
    
    def __str__(self):
        return self.name

    

###

bill_status= (('paid' , 'Paid'),
                ('due' , 'Due'))

class Bill(models.Model):

    tenant    = models.ManyToManyField(Tenant,null=True,blank=True)#automatically creates a table
    month     = models.CharField(max_length=100,null=False)
    room      = models.IntegerField(null=True)
    previous  = models.IntegerField(null=True,db_default=0,default=0)
    previous2 = models.IntegerField(null=True,db_default=0,default=0)
    previous3 = models.IntegerField(null=True,db_default=0,default=0)
    current   = models.IntegerField(null=False)
    current2  = models.IntegerField(null=False)
    current3  = models.IntegerField(null=False,default=0)
    diff      = models.IntegerField(null=False)
    diff2     = models.IntegerField(null=False)
    diff3     = models.IntegerField(null=False,default=0)
    amount    = models.IntegerField(null=False)
    amount2   = models.IntegerField(null=False)
    amount3   = models.IntegerField(null=False)
    amount4   = models.IntegerField(null=False,default=0)
    total     = models.IntegerField(null=False)
    remark1   = models.TextField(null=True,blank=True)
    remark2   = models.TextField(null=True,blank=True)
    remark3   = models.TextField(null=True,blank=True)
    bill_status  = models.CharField(null=True,choices=bill_status,blank=True)
    date_created = models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        names = ", ".join(t.name for t in self.tenant.all())
        return f"{names} ID{self.id} {self.month}"
    