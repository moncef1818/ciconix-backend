from .models import SpecialPassRegistration, BasicPassRegistration 
from rest_framework import serializers



class BasicPassRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicPassRegistration
        fields = '__all__'
        read_only_fields = ['date_joined']
        def validate_email(self ,value):
            value =  value.lower()
            if BasicPassRegistration.objects.filter(email__iexact=value).exists():
                raise serializers.ValidationError(
                    "This email is already registered for the Basic Pass!"
                )
            return value
        
        def validate_student_id(self ,value):
            value =  value.upper()
            if BasicPassRegistration.objects.filter(student_id__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Student ID is already registered for the Basic Pass!"
                )
            return value
        
        def validate_discord_id(self ,value):
            value =  value
            if BasicPassRegistration.objects.filter(discord_id__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Discord ID is already registered for the Basic Pass!"
                )
            return value
        
        def validate(self, data):
            return data

class SpecialPassRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialPassRegistration
        fields = '__all__'
        read_only_fields = ['is_approved', 'date_joined','ctfd_team_id']
        def validate_email1(self ,value):
            value =  value.lower()
            if SpecialPassRegistration.objects.filter(email1__iexact=value).exists():
                raise serializers.ValidationError(
                    "This email is already registered for the Special Pass!"
                )
            return value
        def validate_student_id1(self ,value):
            value =  value.upper()
            if SpecialPassRegistration.objects.filter(student_id1__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Student ID is already registered for the Special Pass!"
                )
            return value
        def validate_discord_id1(self ,value):
            value =  value
            if SpecialPassRegistration.objects.filter(discord_id1__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Discord ID is already registered for the Special Pass!"
                )
            return value
        

        def validate_email2(self ,value):
            value =  value.lower()
            if SpecialPassRegistration.objects.filter(email2__iexact=value).exists():
                raise serializers.ValidationError(
                    "This email is already registered for the Special Pass!"
                )
            return value
        def validate_student_id2(self ,value):
            value =  value.upper()
            if SpecialPassRegistration.objects.filter(student_id2__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Student ID is already registered for the Special Pass!"
                )
            return value
        def validate_discord_id2(self ,value):
            value =  value
            if SpecialPassRegistration.objects.filter(discord_id2__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Discord ID is already registered for the Special Pass!"
                )
            return value   
             
        def validate_email3(self ,value):
            value =  value.lower()
            if SpecialPassRegistration.objects.filter(email3__iexact=value).exists():
                raise serializers.ValidationError(
                    "This email is already registered for the Special Pass!"
                )
            return value
        def validate_student_id3(self ,value):
            value =  value.upper()
            if SpecialPassRegistration.objects.filter(student_id3__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Student ID is already registered for the Special Pass!"
                )
            return value
        def validate_discord_id3(self ,value):
            value =  value
            if SpecialPassRegistration.objects.filter(discord_id3__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Discord ID is already registered for the Special Pass!"
                )
            return value

        def validate_email4(self ,value):
            value =  value.lower()
            if SpecialPassRegistration.objects.filter(email4__iexact=value).exists():
                raise serializers.ValidationError(
                    "This email is already registered for the Special Pass!"
                )
            return value
        def validate_student_id4(self ,value):
            value =  value.upper()
            if SpecialPassRegistration.objects.filter(student_id4__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Student ID is already registered for the Special Pass!"
                )
            return value
        def validate_discord_id4(self ,value):
            value =  value
            if SpecialPassRegistration.objects.filter(discord_id4__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Discord ID is already registered for the Special Pass!"
                )
            return value
        
        def validate_email5(self ,value):
            value =  value.lower()
            if SpecialPassRegistration.objects.filter(email5__iexact=value).exists():
                raise serializers.ValidationError(
                    "This email is already registered for the Special Pass!"
                )
            return value
        def validate_student_id5(self ,value):
            value =  value.upper()
            if SpecialPassRegistration.objects.filter(student_id5__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Student ID is already registered for the Special Pass!"
                )
            return value
        def validate_discord_id5(self ,value):
            value =  value
            if SpecialPassRegistration.objects.filter(discord_id5__iexact=value).exists():
                raise serializers.ValidationError(
                    "This Discord ID is already registered for the Special Pass!"
                )
            return value
        

        def validate(self, data):

            all_emails = []
            all_student_ids = []
            all_discord_ids = []

            for i in range(1,6):
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
