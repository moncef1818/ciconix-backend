# tokens/models.py (or flags/models.py)

from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Token(models.Model):
    token_hash = models.CharField(max_length=128)
    base_points = models.IntegerField(
        choices=[
            (5, '5 points'),
            (10, '10 points'),
            (15, '15 points'),
            (20, '20 points'),
            (30, '30 points'),
            (40, '40 points'),
            (50, '50 points'),
            (60, '60 points'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['base_points']

    def __str__(self):
        return f"{self.base_points} pts"

    def set_hash(self, raw_token):
        self.token_hash = make_password(raw_token)

    def check_token(self, raw_token):
        return check_password(raw_token, self.token_hash)


class TokenSubmission(models.Model):
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.CASCADE,
        related_name='token_submissions'
    )
    token = models.ForeignKey(  
        Token,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'token') 
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.team.team_name} - {self.token.base_points} pts"