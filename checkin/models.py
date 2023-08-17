from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    rollNo = models.CharField(max_length=9,unique=True)
    type = models.CharField(max_length=4, choices=[('UG', 'UG'), ('PG', 'PG'), ('RS', 'RS')])
    batch = models.IntegerField()
    name = models.CharField(max_length=50)
    hall = models.CharField(max_length=4)
    profilePic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.rollNo + " - " + self.name
    
class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rollNo = models.CharField(max_length=9)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, null=False)
    slot = models.CharField(max_length=20, null=False,choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('snacks', 'Snacks'), ('dinner', 'Dinner')])

    def __str__(self):
        return self.rollNo + " - " + self.name + " - " + self.slot + " - " + str(self.date)

    class Meta:
        unique_together = ('user', 'date', 'slot')
