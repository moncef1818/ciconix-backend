from django.db import models
import requests
from django.conf import settings
from registration.models import SpecialPassRegistration

class Team(models.Model):
    team_name = models.CharField(max_length=150, unique=True)
    registration = models.OneToOneField(
        'registration.SpecialPassRegistration', 
        on_delete=models.CASCADE, 
        related_name='team'  # ← Add this line
    )
    ctfd_team_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def sync_to_ctfd(self, password):
        ctfd_api_url = f"{settings.CTFD_URL}/api/v1/teams"
        ctfd_api_key = settings.CTFD_API_TOKEN

        headers = {
            "Authorization": f"Token {ctfd_api_key}",  # Fixed!
            "Content-Type": "application/json"
        }

        data = {
            "name": self.team_name,
            "email": self.registration.email1,
            "password": password
        }

        print(f"🔄 POST {ctfd_api_url}")
        print(f"📧 Data: {data}")

        response = requests.post(ctfd_api_url, headers=headers, json=data, timeout=10)
        print(f"📊 Status: {response.status_code}")
        print(f"📄 Response: {response.text[:300]}")

        if response.status_code == 200:  # Fixed!
            result = response.json()
            self.ctfd_team_id = result['data']['id']
            self.save()
            print(f"✅ CTFd ID: {self.ctfd_team_id}")
            return self.ctfd_team_id

        print(f"❌ Failed: {response.status_code}")
        return None

    def __str__(self):
        return self.team_name