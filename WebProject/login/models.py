from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#A model for hobbies that stores the name of the hobby
class Hobby(models.Model):
    name = models.CharField(max_length=4096)

    def __str__(self):
        return self.name

    #Converting model object to JSON for ajax response
    def as_json(self):
        return {
            'name': self.name
        }

#Model for our User Profile that extends the normal Django user and adds the fields seen below
class User(User):
    GENDER_CHOICES = (
        (None, 'Gender...'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    #The commented line below was used to store profile images on amazon bucket server
    #image = models.ImageField(default='profile_images/default.png', upload_to='webprogprofimages')
    image = models.ImageField(default='profile_images/default.png', upload_to='profile_images')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    dob = models.DateField(blank=True, null=True)
    hobby = models.ManyToManyField(Hobby) #Each user can have multuple hobbies

    def __str__(self):
        return self.username

    def addHobbies(self, hobbies):
        for h in hobbies:
            self.hobby.add(Hobby.objects.get(id=h))

    #Converting model object to JSON for ajax response
    def as_json(self):
        return dict(
            username=self.username,
            email=self.email,
            gender=self.gender,
            dob=self.dob,
            image=self.image.url,
            hobby=[h.as_json() for h in self.hobby.all()],
            liked=self.userLikedBy.all().count()
        )

#Model for likes, holds the user that is liking and the user that is liked
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLiked")##The user that is liking
    userLiked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userLikedBy")##User that is being liked
