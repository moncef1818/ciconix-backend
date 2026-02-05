from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import requests
import secrets
import string
import logging
import time

logger = logging.getLogger(__name__)

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
        """Sync to CTFd with RETRY + LOOKUP logic"""
        ctfd_url = getattr(settings, 'CTFD_URL', 'http://localhost:8001')
        ctfd_token = getattr(settings, 'CTFD_API_TOKEN', '')
        
        if not ctfd_token:
            logger.warning("No CTFD_API_TOKEN in settings")
            return None
        
        headers = {
            'Authorization': f'Token {ctfd_token}',
            'Content-Type': 'application/json'
        }
        
        # STEP 1: Try to CREATE team in CTFd
        create_payload = {
            'name': self.team_name,
            'password': password,
            'captain_id': None  # Will be set later
        }
        
        try:
            create_resp = requests.post(
                f'{ctfd_url}/api/v1/teams',
                json=create_payload,
                headers=headers,
                timeout=10
            )
            
            if create_resp.status_code in [200, 201]:
                ctfd_data = create_resp.json()
                self.ctfd_team_id = ctfd_data['data']['id']
                self.save(update_fields=['ctfd_team_id'])
                logger.info(f"✅ Created CTFd team {self.ctfd_team_id}")
                return self.ctfd_team_id
                
        except Exception as e:
            logger.error(f"❌ CTFd CREATE failed: {e}")
        
        # STEP 2: If create failed, LOOKUP existing team (3 retries)
        for attempt in range(3):
            try:
                lookup_resp = requests.get(
                    f'{ctfd_url}/api/v1/teams?name={self.team_name}',
                    headers=headers,
                    timeout=10
                )
                
                if lookup_resp.status_code == 200:
                    teams = lookup_resp.json().get('data', [])
                    if teams:
                        ctfd_id = teams[0]['id']
                        self.ctfd_team_id = ctfd_id
                        self.save(update_fields=['ctfd_team_id'])
                        logger.info(f"✅ Found existing CTFd team {ctfd_id}")
                        return ctfd_id
                        
                # Wait before retry
                time.sleep(2 ** attempt)  # 1s, 2s, 4s
                
            except Exception as e:
                logger.error(f"❌ Lookup attempt {attempt+1} failed: {e}")
        
        logger.error(f"❌ Could not sync {self.team_name} to CTFd")
        return None
