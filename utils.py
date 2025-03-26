import re
import difflib
from PIL import Image

def validate_image_content(content: str, expected_content: list[str] | None = None) -> dict:
    pattern = re.compile(
        r'@(?P<platform>[A-Za-z0-9_]+(?:[A-Za-z0-9_ ]+[A-Za-z0-9_]+)?)'
        r'\s+Bs\.\s*'
        r'(?P<rate>(?:\.)*\d{1,3}(?:\.\d{3})*(?:,\d{2}))' 
        r'(?P<format_issue>\.\s|\s[^0-9])?' 
    )
    
    for match in pattern.finditer(content):
        platform = match.group('platform').replace(' ', '_')  # Replace spaces with underscores
        rate_str = match.group('rate')

        # Possible format issues
        rate_str = rate_str.startswith('.') and rate_str[1:] or rate_str
        rate_str = rate_str.replace('.', '', rate_str.count('.') - 1 if ',' in rate_str else -1)
        rate_str = rate_str.replace(',', '.')
        
        try:
            rate = float(rate_str)
        except ValueError:
            break

        if expected_content: 
            # Search for the closest match
            closest = difflib.get_close_matches(platform, expected_content, n=1, cutoff=0.6)
            if closest:
                return {
                    'platform': closest[0],
                    'rate': rate
                }
        else:
            return {
                'platform': platform,
                'rate': rate
            }
    
    return None