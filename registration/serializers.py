# registration/serializers.py

from .models import SpecialPassRegistration, BasicPassRegistration 
from rest_framework import serializers


class BasicPassRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicPassRegistration
        fields = '__all__'
        read_only_fields = ['date_joined']
        
    def validate_email(self, value):
        value = value.lower()
        if BasicPassRegistration.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "This email is already registered for the Basic Pass!"
            )
        return value
    
    def validate_student_id(self, value):
        value = value.upper()
        if BasicPassRegistration.objects.filter(student_id__iexact=value).exists():
            raise serializers.ValidationError(
                "This Student ID is already registered for the Basic Pass!"
            )
        return value
    
    def validate_discord_id(self, value):
        if BasicPassRegistration.objects.filter(discord_id__iexact=value).exists():
            raise serializers.ValidationError(
                "This Discord ID is already registered for the Basic Pass!"
            )
        return value


class SpecialPassRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialPassRegistration
        fields = '__all__'
        read_only_fields = ['is_approved', 'date_joined']
    
    # Validation for members 1-5 (email, student_id, discord_id)
    def validate_email1(self, value):
        value = value.lower()
        if SpecialPassRegistration.objects.filter(email1__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered!")
        return value
    
    def validate_student_id1(self, value):
        value = value.upper()
        if SpecialPassRegistration.objects.filter(student_id1__iexact=value).exists():
            raise serializers.ValidationError("This Student ID is already registered!")
        return value
    
    def validate_discord_id1(self, value):
        if SpecialPassRegistration.objects.filter(discord_id1__iexact=value).exists():
            raise serializers.ValidationError("This Discord ID is already registered!")
        return value

    def validate_email2(self, value):
        value = value.lower()
        if SpecialPassRegistration.objects.filter(email2__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered!")
        return value
    
    def validate_student_id2(self, value):
        value = value.upper()
        if SpecialPassRegistration.objects.filter(student_id2__iexact=value).exists():
            raise serializers.ValidationError("This Student ID is already registered!")
        return value
    
    def validate_discord_id2(self, value):
        if SpecialPassRegistration.objects.filter(discord_id2__iexact=value).exists():
            raise serializers.ValidationError("This Discord ID is already registered!")
        return value

    def validate_email3(self, value):
        value = value.lower()
        if SpecialPassRegistration.objects.filter(email3__iexact=value).exists():
            raise serializers.ValidationError("This email is already registered!")
        return value
    
    def validate_student_id3(self, value):
        value = value.upper()
        if SpecialPassRegistration.objects.filter(student_id3__iexact=value).exists():
            raise serializers.ValidationError("This Student ID is already registered!")
        return value
    
    def validate_discord_id3(self, value):
        if SpecialPassRegistration.objects.filter(discord_id3__iexact=value).exists():
            raise serializers.ValidationError("This Discord ID is already registered!")
        return value

    def validate_email4(self, value):
        if value:  # ✅ Only validate if provided
            value = value.lower()
            if SpecialPassRegistration.objects.filter(email4__iexact=value).exists():
                raise serializers.ValidationError("This email is already registered!")
        return value
    
    def validate_student_id4(self, value):
        if value:  # ✅ Only validate if provided
            value = value.upper()
            if SpecialPassRegistration.objects.filter(student_id4__iexact=value).exists():
                raise serializers.ValidationError("This Student ID is already registered!")
        return value
    
    def validate_discord_id4(self, value):
        if value:  # ✅ Only validate if provided
            if SpecialPassRegistration.objects.filter(discord_id4__iexact=value).exists():
                raise serializers.ValidationError("This Discord ID is already registered!")
        return value

    def validate_email5(self, value):
        if value:  # ✅ Only validate if provided
            value = value.lower()
            if SpecialPassRegistration.objects.filter(email5__iexact=value).exists():
                raise serializers.ValidationError("This email is already registered!")
        return value
    
    def validate_student_id5(self, value):
        if value:  # ✅ Only validate if provided
            value = value.upper()
            if SpecialPassRegistration.objects.filter(student_id5__iexact=value).exists():
                raise serializers.ValidationError("This Student ID is already registered!")
        return value
    
    def validate_discord_id5(self, value):
        if value:  # ✅ Only validate if provided
            if SpecialPassRegistration.objects.filter(discord_id5__iexact=value).exists():
                raise serializers.ValidationError("This Discord ID is already registered!")
        return value

    def validate(self, data):
        """
        Custom validation:
        1. Members 1-3 are REQUIRED
        2. Members 4-5 are OPTIONAL, but if ANY field is provided, ALL required fields must be provided
        3. Check for duplicate emails, student_ids, and discord_ids within the team
        """
        
        # ✅ Check if member 4 is partially filled
        member4_fields = ['firstname4', 'lastname4', 'school4', 'year4', 
                         'student_id4', 'skills4', 'email4', 'discord_id4']
        member4_provided = [field for field in member4_fields if data.get(field)]
        
        if member4_provided:
            # If any field is provided, ALL required fields must be present
            required_member4 = ['firstname4', 'lastname4', 'school4', 'year4', 
                               'student_id4', 'skills4', 'email4', 'discord_id4']
            missing_fields = [f for f in required_member4 if not data.get(f)]
            
            if missing_fields:
                raise serializers.ValidationError({
                    "member4": f"If providing 4th member info, all required fields must be filled. Missing: {', '.join(missing_fields)}"
                })
        
        # ✅ Check if member 5 is partially filled
        member5_fields = ['firstname5', 'lastname5', 'school5', 'year5', 
                         'student_id5', 'skills5', 'email5', 'discord_id5']
        member5_provided = [field for field in member5_fields if data.get(field)]
        
        if member5_provided:
            # If any field is provided, ALL required fields must be present
            required_member5 = ['firstname5', 'lastname5', 'school5', 'year5', 
                               'student_id5', 'skills5', 'email5', 'discord_id5']
            missing_fields = [f for f in required_member5 if not data.get(f)]
            
            if missing_fields:
                raise serializers.ValidationError({
                    "member5": f"If providing 5th member info, all required fields must be filled. Missing: {', '.join(missing_fields)}"
                })

        # ✅ Check for duplicates within the team
        all_emails = []
        all_student_ids = []
        all_discord_ids = []

        for i in range(1, 6):
            email = data.get(f'email{i}')
            student_id = data.get(f'student_id{i}')
            discord_id = data.get(f'discord_id{i}')

            if email:
                all_emails.append(email.lower())
            if student_id:
                all_student_ids.append(student_id.upper())
            if discord_id:
                all_discord_ids.append(discord_id)

        if len(all_emails) != len(set(all_emails)):
            raise serializers.ValidationError("All team members must have unique email addresses.")
        if len(all_student_ids) != len(set(all_student_ids)):
            raise serializers.ValidationError("All team members must have unique Student IDs.")
        if len(all_discord_ids) != len(set(all_discord_ids)):
            raise serializers.ValidationError("All team members must have unique Discord IDs.")
        
        return data