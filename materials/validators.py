from rest_framework.serializers import ValidationError
from urllib.parse import urlparse


def youtube_url_validator(value):
    """Валидатор для проверки, что ссылка ведет на youtube.com"""
    parsed_url = urlparse(value)
    
    allowed_domains = ['www.youtube.com', 'youtube.com', 'youtu.be']
    
    if parsed_url.netloc not in allowed_domains:
        raise ValidationError(
            f'Разрешены только ссылки на youtube.com. Ваша ссылка: {parsed_url.netloc}'
        )
    
    return value


class YouTubeURLValidator:
    def __init__(self, message=None):
        self.message = message or 'Разрешены только ссылки на youtube.com'
    
    def __call__(self, value):
        parsed_url = urlparse(value)
        allowed_domains = ['www.youtube.com', 'youtube.com', 'youtu.be']
        
        if parsed_url.netloc not in allowed_domains:
            raise ValidationError(f'{self.message}. Ваша ссылка: {parsed_url.netloc}')
        
        return value
