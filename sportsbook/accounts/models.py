from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password

class WebsiteUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class Account(models.Model):
    user = models.OneToOneField(WebsiteUser, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    balance = models.IntegerField(default=0)
    exp = models.IntegerField(default=0)

    def __str__(self):
        return self.username
    
class Matchess(models.Model):
    match_id = models.IntegerField(unique=True)
    match_name = models.CharField(max_length=100)
    Team1 = models.CharField(max_length=50)
    Team2 = models.CharField(max_length=50)
    TEAM_CHOICES = [('Team1', 'Team1'),('Team2', 'Team2'),]
    winner_team = models.CharField(max_length=10, choices=TEAM_CHOICES, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    STATUS_CHOICES = [('UpComing', 'UpComing'),('Active', 'Active'),('Completed', 'Completed'),]
    match_status = models.CharField(default='UpComing', choices=STATUS_CHOICES)
    img = models.ImageField(upload_to='images/')
    url = models.URLField()

    def __str__(self):
        return self.match_name
    
    def save(self, *args, **kwargs):  
        super().save(*args, **kwargs) 
        if self.match_status == "Completed" and self.winner_team:   
            betss = bets.objects.filter(match_id=self.match_id, bet_status="Active")
            for bet in betss:
                account = Account.objects.get(username=bet.username)
                if bet.bet_team == self.winner_team:
                    account.balance += bet.win_amount  
                account.save()
                bet.bet_status = "Settled"
                bet.save()
    
class bets(models.Model):
    bet_id = models.IntegerField(primary_key=True)
    username = models.CharField()
    match_id = models.IntegerField()
    bet_amount = models.IntegerField()
    win_amount = models.IntegerField()
    TEAM_CHOICES = [('Team1', 'Team1'),('Team2', 'Team2'),]
    bet_team = models.CharField(max_length=10, choices=TEAM_CHOICES)
    STATUS_CHOICES = [('Active', 'Active'),('Settled', 'Settled'),]
    bet_status = models.CharField(default='Active', choices=STATUS_CHOICES)
    bet_time = models.DateField(auto_now_add=True)
    def save(self, *args, **kwargs):  
        is_new = self._state.adding
        if is_new:
            account = Account.objects.get(username=self.username)
            if account.balance < self.bet_amount:
                raise ValidationError("Insufficient balance for bet.")
            account.balance -= self.bet_amount
            account.save()
        super().save(*args, **kwargs)

class Deposite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    deposite_id = models.IntegerField(primary_key=True)
    username = models.CharField()
    amount = models.IntegerField()
    payment_SS = models.ImageField(upload_to="deposits/")
    UTR = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    approved_at = models.DateTimeField(null=True, blank=True)

class Withdraw(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    withdraw_id = models.IntegerField(primary_key=True)
    username = models.CharField()
    amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validate before saving."""
        from .models import Account
        try:
            account = Account.objects.get(username=self.username)
        except Account.DoesNotExist:
            raise ValidationError(f"Account for {self.username} not found.")

        if self._state.adding and account.balance < self.amount:
            raise ValidationError("Insufficient balance in account.")

    def save(self, *args, **kwargs):
        """Deduct balance when creating new withdrawal."""
        from .models import Account
        is_new = self._state.adding
        if is_new:
            account = Account.objects.get(username=self.username)
            account.balance -= self.amount
            account.save()
        super().save(*args, **kwargs)
