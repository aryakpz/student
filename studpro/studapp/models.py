from django.db import models

# Create your models here.
from django.db import models
from django.db import models

# Create your models here.
class StudentMark(models.Model):
    student_name = models.CharField(max_length=100)
    dob = models.DateField()
    subject = models.CharField(max_length=100)
    mark = models.IntegerField()
    out_of = models.IntegerField()

    @property
    def percentage(self):
        return (self.mark / self.out_of) * 100

    @property
    def pass_fail(self):
        return 'Pass' if self.mark >= (self.out_of / 2.5) else 'Fail'
  


class Summery(models.Model):
     student_name = models.CharField(max_length=100)
     dob = models.DateField()
     def total(self):
         return (self)
