from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import requests
import secrets
import string

class TeamManager(BaseUserManager):
    def create_user(self, email, team_name, password=None, **extra_fields):
        if not email:
            raise ValueError("Teams must have an email address")
        
        email = self.normalize_email(email)
        team = self.model(email=email, team_name=team_name, **extra_fields)
        
        if password:
            team.set_password(password)  # ✅ Securely hashes password
        
        team.save(using=self._db)
        return team

    def create_superuser(self, email, team_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, team_name, password, **extra_fields)

class Team(AbstractBaseUser, PermissionsMixin):
    team_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)  # ✅ Login field
    
    registration = models.OneToOneField(
        'registration.SpecialPassRegistration',
        on_delete=models.CASCADE,
        related_name='team',
        null=True, blank=True
    )
    
    ctfd_team_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # ✅ REQUIRED Django auth fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = TeamManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['team_name']

    # ✅ REQUIRED: Django needs these methods
    def get_full_name(self):
        return self.team_name

    def get_short_name(self):
        return self.team_name

    def __str__(self):
        return self.team_name

    # ✅ Secure random password generator
    @classmethod
    def generate_secure_password(cls, length=16):
        """Generate secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    def sync_to_ctfd(self, password):
        """Sync team to CTFd"""
        ctfd_api_url = f"{settings.CTFD_URL}/api/v1/teams"
        headers = {
            "Authorization": f"Token {settings.CTFD_API_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "name": self.team_name,
            "email": self.email,
            "password": password
        }
        try:
            response = requests.post(ctfd_api_url, headers=headers, json=data, timeout=10)
            print(f"CTFd {self.team_name}: {response.status_code}")
            if response.status_code == 201:
                self.ctfd_team_id = response.json()['data']['id']
                self.save()
                return self.ctfd_team_id
        except Exception as e:
            print(f"CTFd Error {self.team_name}: {e}")
        return None
