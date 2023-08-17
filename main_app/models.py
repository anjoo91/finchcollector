from django.db import models
from django.urls import reverse
# importing User model for authentication
# since we're importing it already
# we don't need to define a user model
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
# Define Toy before you 
class Toy(models.Model):
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('toys_detail', kwargs={'pk': self.id})

class Finch(models.Model):
    # name of Finch can be nullable
    name = models.CharField(max_length=100, null=True)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # create M:M relationship with Toy model
    # toys is the related manager
    toys = models.ManyToManyField(Toy)
    # create O:M relationship with User model
    # adding FK link to user instance
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.name} ({self.id})'
    # overrwrite url method 
    def get_absolute_url(self):
        return reverse("detail", kwargs={"finch_id": self.id})
    # check if finch has been fed to completion today
    # if feeding_set.count() = 3 then it's complete for the day
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

class Photo(models.Model):
    # URL to photo on s3
    url = models.CharField(max_length=250)
    # O:M relationship
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Photo for finch_id: {self.finch_id} @{self.url}"

class Feeding(models.Model):
    date = models.DateField()
    # this will create a select menu on the form
    # where the choices are the elements of the MEALS
    # tuple, & default value is 'B','Breakfast'
    meal = models.CharField(max_length=1, 
                            choices = MEALS, 
                            default = MEALS[0][0])
    # create a cat_id FK; it will automatically add _id to key name
    # on_delete = models.CASCADE is required 
    # in a one:many relationship bc it ensures that 
    # children are also removed when a parent (cat) record is deleted
    finch = models.ForeignKey(Finch, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"
    
    # set default sort method to ascending date
    class Meta:
        ordering = ['-date']