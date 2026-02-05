from django.db import models
from django.conf import settings

class SpecialPassRegistration(models.Model):  

    Year_Choices = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
        (5, '5th Year '),
    ]

    School_Choices = [
        ('NSCS', 'National School of Cybersecurity'),
        ('ENSIA', 'National School of Artificial Intelligence'),
        ('NHSM', 'National Higher School of Mathematics'),
        ('NHSAST', 'National Higher School of Autonomous Systems Technology'),
        ('NHSNNT', 'National Higher School of Nano And Nanotechnology'),
        ('ESI', 'National School of Computer Science'),
        ('ESI-SBA', 'National School of Computer Science Sidi Bel Abbes'),
        ('ESTIN','Higher School in Computer Science and Digital Technologies'),
        ('NIT', 'Numidia Institute of Technology'),
        ('Other', 'Other'),
    ]

    Skills_Choices = [
        ('Cryptography', 'Cryptography'),
        ('Web Security', 'Web Security'),
        ('PWN & Binary Exploitation', 'PWN & Binary Exploitation'),
        ('Reverse Engineering', 'Reverse Engineering'),
        ('Forensics', 'Forensics'),
        ('OSINT', 'OSINT'),
        ('Web Development', 'Web Development'),
        ('Programming', 'Programming'),
        ('problem Solving', 'Problem Solving'),
        ('Other', 'Other'),
    ]

    # Team Leader Information
    firstname1 = models.CharField(max_length=150, unique=True) 
    lastname1 = models.CharField(max_length=150)
    school1 = models.CharField(max_length=255 , choices=School_Choices)
    year1 = models.IntegerField(choices=Year_Choices)
    student_id1 = models.CharField(max_length=50, unique=True)
    skills1 = models.TextField(max_length=50,choices=Skills_Choices)
    profile_link1 = models.URLField(blank=True, null=True, help_text="Link to your profile (GitHub, TryHackMe, CTFTime, etc.)")
    email1 = models.EmailField(unique=True)
    discord_id1 = models.CharField(max_length=100, unique=True)

    # Second Team member Information
    firstname2 = models.CharField(max_length=150, unique=True) 
    lastname2 = models.CharField(max_length=150)
    school2 = models.CharField(max_length=255 , choices=School_Choices)
    year2 = models.IntegerField(choices=Year_Choices)
    student_id2 = models.CharField(max_length=50, unique=True)
    skills2 = models.TextField(max_length=50,choices=Skills_Choices)
    profile_link2 = models.URLField(blank=True, null=True, help_text="Link to your profile (GitHub, TryHackMe, CTFTime, etc.)")
    email2 = models.EmailField(unique=True)
    discord_id2 = models.CharField(max_length=100, unique=True)

    # Third Team member Information
    firstname3 = models.CharField(max_length=150, unique=True) 
    lastname3 = models.CharField(max_length=150)
    school3 = models.CharField(max_length=255 , choices=School_Choices)
    year3 = models.IntegerField(choices=Year_Choices)
    student_id3 = models.CharField(max_length=50, unique=True)
    skills3 = models.TextField(max_length=50,choices=Skills_Choices)
    profile_link3 = models.URLField(blank=True, null=True, help_text="Link to your profile (GitHub, TryHackMe, CTFTime, etc.)")
    email3 = models.EmailField(unique=True)
    discord_id3 = models.CharField(max_length=100, unique=True)

    # forth Team member Information
    firstname4 = models.CharField(max_length=150, unique=True) 
    lastname4 = models.CharField(max_length=150)
    school4 = models.CharField(max_length=255 , choices=School_Choices)
    year4 = models.IntegerField(choices=Year_Choices)
    student_id4 = models.CharField(max_length=50, unique=True)
    skills4 = models.TextField(max_length=50,choices=Skills_Choices)
    profile_link4 = models.URLField(blank=True, null=True, help_text="Link to your profile (GitHub, TryHackMe, CTFTime, etc.)")
    email4 = models.EmailField(unique=True)
    discord_id4 = models.CharField(max_length=100, unique=True)

    # fifth Team member Information
    firstname5 = models.CharField(max_length=150, unique=True) 
    lastname5 = models.CharField(max_length=150)
    school5 = models.CharField(max_length=255 , choices=School_Choices)
    year5 = models.IntegerField(choices=Year_Choices)
    student_id5 = models.CharField(max_length=50, unique=True)
    skills5 = models.TextField(max_length=50,choices=Skills_Choices)
    profile_link5 = models.URLField(blank=True, null=True, help_text="Link to your profile (GitHub, TryHackMe, CTFTime, etc.)")
    email5 = models.EmailField(unique=True)
    discord_id5 = models.CharField(max_length=100, unique=True)

    # team Information
    team_name = models.CharField(max_length=150, unique=True)
    is_approved = models.BooleanField(default=False, help_text="Admin approves for competition")

    # Date Joined
    date_joined = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.team_name + " - " + self.firstname1 + " " + self.lastname1
    
class BasicPassRegistration(models.Model):
    
    Year_Choices = [
        (1, '1st Year'),
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
        (5, '5th Year '),
    ]

    School_Choices = [
        ('NSCS', 'National School of Cybersecurity'),
        ('ENSIA', 'National School of Artificial Intelligence'),
        ('NHSM', 'National Higher School of Mathematics'),
        ('NHSAST', 'National Higher School of Autonomous Systems Technology'),
        ('NHSNNT', 'National Higher School of Nano And Nanotechnology'),
        ('ESI', 'National School of Computer Science'),
        ('ESI-SBA', 'National School of Computer Science Sidi Bel Abbes'),
        ('ESTIN','Higher School in Computer Science and Digital Technologies'),
        ('NIT', 'Numidia Institute of Technology'),
        ('Other', 'Other'),
    ]

    # Team Leader Information
    firstname = models.CharField(max_length=150, unique=True) 
    lastname = models.CharField(max_length=150)
    school = models.CharField(max_length=255 , choices=School_Choices)
    year = models.IntegerField(choices=Year_Choices)
    student_id = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    discord_id = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstname + " " + self.lastname
    
