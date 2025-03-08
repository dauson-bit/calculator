# models.py
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings



class Program(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Course(models.Model):
    
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='courses')
    year = models.CharField(max_length=50) 
    semester = models.CharField(max_length=50)  
    name = models.CharField(max_length=100)
    credit_hours = models.DecimalField(max_digits=4, decimal_places=1)

    def __str__(self):
        return f"{self.name} (Year {self.year}, Semester {self.semester}, {self.credit_hours} Credit Hours)"





