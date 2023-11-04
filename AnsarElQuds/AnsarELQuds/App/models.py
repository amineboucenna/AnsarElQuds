from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from datetime import date,timezone,datetime
from django.utils import timezone
from django.core.files.storage import FileSystemStorage
# Create your models here.
class Leaderboard(models.Model):
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_answers = models.IntegerField(default=0)
    valid_answers = models.IntegerField(default=0)

    def time_remaining(self):
        now = timezone.now()
        remaining = self.end_date - now
        weeks = remaining.days // 7
        days = remaining.days % 7
        hours, remainder = divmod(remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{weeks}w {days}d {hours}h {minutes}m"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Leaderboards"


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            self.delete(name)
        return name


class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError("You have not provided a valid e-mail address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    username = models.CharField(max_length=50, blank=False, unique=True)
    first_name = models.CharField(max_length=50, blank=True, default='')
    last_name = models.CharField(max_length=50, blank=True, default='')
    profile_picture = models.FileField(upload_to='ProfilePictures/',storage=OverwriteStorage(),default=None)
    

    country = models.CharField(max_length=50,default='')
    total_validated_answers = models.IntegerField(default=0)
    total_answers = models.IntegerField(default=0)
    total_ratio = models.FloatField(default=0)

    monthly_validated_answers = models.IntegerField(default=0)
    monthly_total_answers = models.IntegerField(default=0)
    monthly_ratio = models.FloatField(default=0)


    leaderboards = models.ManyToManyField(to=Leaderboard, name="leaderboards")
    color_theme = models.CharField(max_length=7, default="#0e4bf1")

    is_darkmode = models.BooleanField(default=False)
    date_joined = models.DateField(default=date.today)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def getprofilepicture(self):
        return str(self.profile_picture)

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]

    def calculate_monthly_ratio(self):
        if self.monthly_total_answers == 0:
            self.monthly_ratio = 0
        else:
            self.monthly_ratio = self.monthly_validated_answers / self.monthly_total_answers

    def calculate_total_ratio(self):
        if self.total_answers == 0:
            self.total_ratio = 0
        else:
            self.total_ratio = self.total_validated_answers / self.total_answers



class News(models.Model):
    media = models.FileField(upload_to='News/', storage=OverwriteStorage())
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE) 
    title = models.CharField(max_length=500)
    position = models.CharField(max_length=250,null=True)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)
    date_posted = models.DateTimeField(default=datetime.now)
    media_type = models.CharField(max_length=10)


    def __str__(self):
        return str(self.media)


class NewsVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=10)

    class Meta:
        unique_together = ('user', 'news') 