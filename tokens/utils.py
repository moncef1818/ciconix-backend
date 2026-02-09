# flags/utils.py

import hashlib
import secrets
import csv
import os
from django.conf import settings
from .models import Token
from datetime import datetime


def generate_tokens(num_5=0, num_10=0, num_15=0, num_20=0, num_30=0,num_40=0, num_50=0,num_60=0):
    """
    Simple function to generate tokens and save to CSV.
    
    Usage in Django shell:
        python manage.py shell
        >>> from flags.utils import generate_tokens
        >>> generate_tokens(num_5=5, num_10=3, num_20=2)
    """
    
    token_groups = {
        5: num_5,
        10: num_10,
        15: num_15,
        20: num_20,
        30: num_30,
        40: num_40,
        50: num_50,
        60: num_60,
    }
    
    # Create secure_data directory
    csv_dir = os.path.join(settings.BASE_DIR, 'secure_data')
    os.makedirs(csv_dir, exist_ok=True)
    
    # Prepare CSV file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_file = os.path.join(csv_dir, f'tokens_{timestamp}.csv')
    
    created_count = 0
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Token', 'Points'])
        
        for points, count in token_groups.items():
            for _ in range(count):
                # Generate MD5 hash
                random_bytes = secrets.token_bytes(16)
                md5_hash = hashlib.md5(random_bytes).hexdigest()
                raw_token = f"CIC{{{md5_hash}}}"
                
                # Save to database
                token = Token(base_points=points)
                token.set_hash(raw_token)
                token.save()
                
                writer.writerow([raw_token, points])
                created_count += 1
    
    print(f"✅ Generated {created_count} tokens")
    print(f"📁 Saved to: {csv_file}")
    return csv_file