import requests
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils.dateparse import parse_datetime
from news.models import Article

class Command(BaseCommand):
    help = 'Fetches latest gaming news from NewsAPI'

    def add_arguments(self, parser):
        # Allow the script to take an optional keyword argument
        parser.add_argument('--keyword', type=str, default='gaming')

    def handle(self, *args, **options):
        search_term = options['keyword']
        
        # ⚠️ PASTE YOUR ACTUAL NEWSAPI KEY HERE
        API_KEY = '1a016a96c3044705ade0647e876d056e' 
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        URL = f'https://newsapi.org/v2/everything?q={search_term}&sortBy=publishedAt&apiKey={API_KEY}'
        
        response = requests.get(URL, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            saved_count = 0
            for item in articles:
                title = item.get('title')
                if not title or "[Removed]" in title:
                    continue
                
                if Article.objects.filter(url=item.get('url')).exists():
                    continue
                
                base_slug = slugify(title)[:200]
                slug = base_slug
                counter = 1
                while Article.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                Article.objects.create(
                    title=title,
                    slug=slug,
                    content=item.get('content', '') or '',
                    summary=item.get('description', '') or '',
                    url=item.get('url'),
                    image_url=item.get('urlToImage'),
                    published_at=parse_datetime(item.get('publishedAt'))
                )
                saved_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'Successfully fetched {saved_count} fresh articles for: {search_term}'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data. HTTP Status: {response.status_code}'))