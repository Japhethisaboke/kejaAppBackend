from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import ImageField, Q


# Create your models here.


class CustomUserManager(UserManager):

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )


class User(AbstractUser):
    email = models.EmailField(max_length=40, unique=True)
    phone = models.IntegerField(null=True)
    isOwner = models.BooleanField(default=False)
    picture = ImageField(upload_to='media/profile_picture/%y/%m/%d', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['id', 'email', 'first_name', 'last_name', 'phone', 'picture']
    objects = CustomUserManager()

    def get_username(self):
        return self.username


class Category(models.Model):
    house_category = models.CharField(max_length=15)

    def __str__(self):
        return str(self.id) + '. ' + self.house_category


def my_default():
    return {
        'wifi': False,
        'dstv': False
    }


class House(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rooms = models.IntegerField(default=0)
    price = models.IntegerField()
    location = models.PointField()
    amenities = JSONField(default=my_default)
    master_image = ImageField(upload_to='media/master_image/%y/%m/%d')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    average_rating = models.IntegerField(default=5)

    def __str__(self):
        return str(self.id) + '. ' + self.name


class HouseImages(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    image = ImageField(upload_to='media/house_images/%y/%m/%d', blank=True)

    def __str__(self):
        return str(self.id)


class Review(models.Model):
    review = models.CharField(max_length=500)
    rating = models.IntegerField(default=1)
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE)
    reviewer = models.EmailField(max_length=40)
    reviewer_fname = models.CharField(max_length=10, blank=True)
    reviewer_lname = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.reviewee.email + " ." + str(self.rating) + " "
        self.review


class Report(models.Model):
    complainant_email = models.EmailField(max_length=40)
    complainant_fname = models.CharField(max_length=10)
    complainant_lname = models.CharField(max_length=10)
    complain_against = models.ForeignKey(User, on_delete=models.CASCADE)
    complaint = models.CharField(max_length=500)

    def __str__(self):
        return 'Complain against: ' + self.complain_against.email + ' Complainant Email: ' + self.complainant_email
