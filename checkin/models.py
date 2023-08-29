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
    foodChoice = models.CharField(max_length=10, choices=[('veg', 'Veg'), ('nonveg', 'Non-Veg')], default='veg')

    def __str__(self):
        return self.rollNo + " - " + self.name
    
    class Meta:
        permissions = [
            ("can_check_in", "Can allow users to check in"),
            ("can_view_stats", "Can view check-in statistics and data"),
            ("can_manage_all", "Can manage all operations"),
        ]

    
class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rollNo = models.CharField(max_length=9)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True, null=False)
    slot = models.CharField(max_length=20, null=False,choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('snacks', 'Snacks'), ('dinner', 'Dinner')])
    food_type = models.CharField(max_length=10, null=False, choices=[('veg', 'Veg'), ('nonveg', 'Non-Veg')], default='veg')

    def __str__(self):
        return self.rollNo + " - " + self.name + " - " + self.slot + " - " + str(self.date)
    
    def save(self, *args, **kwargs):
        # Set the food_type based on the related User's foodChoice
        super(CheckIn, self).save(*args, **kwargs)
        self.food_type = self.user.foodChoice
        super(CheckIn, self).save(update_fields=['food_type'])

    class Meta:
        unique_together = ('user', 'date', 'slot')
        permissions = [
            ("can_check_in", "Can allow users to check in"),
            ("can_view_stats", "Can view check-in statistics and data"),
            ("can_manage_all", "Can manage all operations"),
        ]
