from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    code = models.CharField(max_length=6, blank=True, unique=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="ref_by")

    balance = models.FloatField(default=0.00, max_length=7)
    purchase_balance = models.FloatField(default=0.00, max_length=7)
    click = models.IntegerField(default=0)
    per_hour = models.FloatField(default=0.00, max_length=7)
    profit = models.FloatField(default=0.00, max_length=7)
    alltime_earning = models.FloatField(default=0.00)
    all_deposits = models.FloatField(default=0.00, max_length=7)
    earned_click = models.FloatField(default=0.00, max_length=7)
    deposit = models.FloatField(default=0.00, max_length=7)
    paid_out = models.FloatField(default=0.00, max_length=7)
    payeer = models.CharField(max_length=9, blank=True, null=True, unique=True)
    perfectmoney = models.CharField(max_length=9, blank=True, null=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    plan_created = models.DateTimeField(auto_now_add=True)
    no_plan = models.IntegerField(default=0)
    no_ad = models.IntegerField(default=0)
    title = models.CharField(max_length=70, blank=True, null=True)
    url = models.URLField(blank=True, max_length=200)
    ads = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def recs_number(self):
        return Profile.objects.all().count()

    def save(self, *args, **kwargs):
        if self.code == '':
            code = self.recs_number()+1
            self.code = code
        super().save(*args, **kwargs)


class Ad(models.Model):
    left_views = models.IntegerField(default=0)
    viewed = models.IntegerField(default=0)
    site_balance = models.FloatField(default=0.00, max_length=7)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class AdsPlan(models.Model):
    name = models.CharField(max_length=25, null=True, unique=True)
    time = models.IntegerField(default=1)
    price_per_1 = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class PlansPlan(models.Model):
    per_hour = models.FloatField(default=0.00)
    fee = models.FloatField(default=0.00, max_length=2)
    newfield = models.FloatField(default=0.00, max_length=2)

    def __str__(self):
        return f"Investment plan"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
