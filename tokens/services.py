import hashlib
import secrets
import csv
from io import StringIO
from django.conf import settings
from django.http import HttpResponse
from .models import Token

class TokenGenerator:
    @staticmethod
    def generate_md5_token():
        random_bytes = secrets.token_bytes(8)  # 64 bits randomness
        md5_hash = hashlib.md5(random_bytes).hexdigest()[:32]  
        return md5_hash
    
    @staticmethod
    def generate_and_store_token(num_5pts,num_10pts,num_15pts,num_20pts,num_30pts,num_50pts):

        token_group = {
            5:num_5pts,
            10:num_10pts,
            15:num_15pts,
            20:num_20pts,
            30:num_30pts,
            50:num_50pts,
        }
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Token', 'Base Points'])
        created_count = 0
        for points, count in token_group.items():
            if count > 0:
                tokens = []
                for _ in range(count):
                    raw_token = TokenGenerator.generate_md5_token()
                    token = Token(base_points=points)
                    token.set_hash(raw_token)
                    token.save()
                    tokens.append(raw_token)
                    created_count += 1
                    writer.writerow([points,raw_token])


        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="ciconix_tokens_{created_count}_tokens.csv"'
        
        return response
    
