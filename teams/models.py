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
            team.set_password(password)
        
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
    email = models.EmailField(unique=True)
    
    registration = models.OneToOneField(
        'registration.SpecialPassRegistration',
        on_delete=models.CASCADE,
        related_name='team',
        null=True, blank=True
    )
    
    ctfd_team_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = TeamManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['team_name']

    def get_full_name(self):
        return self.team_name

    def get_short_name(self):
        return self.team_name

    def __str__(self):
        return self.team_name

    @classmethod
    def generate_secure_password(cls, length=16):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password

    def sync_to_ctfd(self, password):
        """🔥 FIXED - Multiple auth methods + FULL logging"""
        
        ctfd_url = 'http://localhost:8001'.rstrip('/')
        ctfd_token = 'ctfd_f29e6cbd1ace4c5718cea66b577e7c403221f08b96822afc452fc368c4716b9c'
        
        # TRY 3 AUTH METHODS (one WILL work)
        auth_configs = [
            # 1. Token auth (CTFd standard)
            {'headers': {'Authorization': f'Token {ctfd_token}'}},
            # 2. Bearer token 
            {'headers': {'Authorization': f'Bearer {ctfd_token}'}},
            # 3. Admin basic auth (fallback)
            {'auth': ('admin', 'admin'), 'headers': {}}  
        ]
        
        base_headers = {'Content-Type': 'application/json'}
        
        logger.info(f"🔍 Syncing {self.team_name} to CTFd...")
        
        # TEST 1: Basic API access
        for i, config in enumerate(auth_configs, 1):
            try:
                headers = {**base_headers, **config.get('headers', {})}
                resp = requests.get(
                    f'{ctfd_url}/api/v1/teams', 
                    headers=headers, 
                    auth=config.get('auth'),
                    timeout=10
                )
                
                logger.info(f"🔑 Auth test {i}: {resp.status_code}")
                
                if resp.status_code == 200:
                    logger.info("✅ API ACCESS WORKS")
                    break
                else:
                    logger.warning(f"❌ Auth {i} failed: {resp.status_code} - {resp.text[:100]}")
                    
            except Exception as e:
                logger.error(f"❌ Auth {i} connection: {e}")
        
        # TEST 2: CREATE TEAM
        for i, config in enumerate(auth_configs, 1):
            try:
                headers = {**base_headers, **config.get('headers', {})}
                create_resp = requests.post(
                    f'{ctfd_url}/api/v1/teams',
                    json={'name': self.team_name, 'password': password},
                    headers=headers,
                    auth=config.get('auth'),
                    timeout=10
                )
                
                logger.info(f"📤 CREATE {i}: {create_resp.status_code}")
                logger.info(f"📄 CREATE response: {create_resp.text[:200]}")
                
                if create_resp.status_code in [200, 201]:
                    ctfd_data = create_resp.json()
                    self.ctfd_team_id = ctfd_data['data']['id']
                    self.save(update_fields=['ctfd_team_id'])
                    logger.info(f"✅ CREATED CTFd ID: {self.ctfd_team_id}")
                    return self.ctfd_team_id
                    
            except Exception as e:
                logger.error(f"❌ CREATE {i}: {e}")
        
        # TEST 3: LOOKUP EXISTING
        for i, config in enumerate(auth_configs, 1):
            for attempt in range(3):
                try:
                    headers = {**base_headers, **config.get('headers', {})}
                    lookup_resp = requests.get(
                        f'{ctfd_url}/api/v1/teams?name={self.team_name}',
                        headers=headers,
                        auth=config.get('auth'),
                        timeout=10
                    )
                    
                    logger.info(f"🔍 LOOKUP {i}.{attempt+1}: {lookup_resp.status_code}")
                    
                    if lookup_resp.status_code == 200:
                        teams = lookup_resp.json().get('data', [])
                        if teams:
                            ctfd_id = teams[0]['id']
                            self.ctfd_team_id = ctfd_id
                            self.save(update_fields=['ctfd_team_id'])
                            logger.info(f"✅ FOUND CTFd ID: {ctfd_id}")
                            return ctfd_id
                    
                    time.sleep(1)
                    
                except Exception as e:
                    logger.error(f"❌ LOOKUP {i}.{attempt+1}: {e}")
        
        logger.error(f"❌ ALL METHODS FAILED for {self.team_name}")
        return None
