from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.management import call_command
import random
from .models import Article, Comment, UpcomingGame, GameReview, BugReport

# ... leave existing views untouched ...

def about_and_support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if name and email and title and description:
            BugReport.objects.create(
                reporter_name=name,
                email=email,
                bug_title=title,
                description=description
            )
            return render(request, 'news/about.html', {'success': True})
            
    return render(request, 'news/about.html')

def home(request):
    articles_queryset = Article.objects.all()
    
    # Check if user searched for something
    query = request.GET.get('q')
    if query:
        articles_queryset = articles_queryset.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )
        latest_news = articles_queryset[:10]
    else:
        # Get all articles and convert to a list
        all_articles = list(articles_queryset)
        # Randomly shuffle the list completely on every refresh (Ctrl + R)
        random.shuffle(all_articles)
        # Take the first 10 random articles
        latest_news = all_articles[:10]
        
    trending_news = Article.objects.order_by('-view_count')[:5]
    
    context = {
        'latest_news': latest_news,
        'trending_news': trending_news
    }
    return render(request, 'news/home.html', context)

def force_api_refresh(request):
    """
    Randomizes the search keyword sent to the API so that clicking 
    Option B ALWAYS brings in completely different, fresh news articles.
    """
    gaming_keywords = ['playstation', 'xbox', 'nintendo', 'cyberpunk', 'gta6', 'esports', 'steam', 'pc-gaming']
    chosen_keyword = random.choice(gaming_keywords)
    
    try:
        # Pass a random keyword to our command dynamically
        call_command('fetch_news', keyword=chosen_keyword)
    except Exception as e:
        print(f"API Error during live refresh: {e}")
        
    return redirect('home')

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.view_count += 1
    article.save()
    
    if request.method == 'POST' and request.user.is_authenticated:
        comment_text = request.POST.get('comment_text')
        if comment_text:
            Comment.objects.create(article=article, user=request.user, text=comment_text)
            return redirect('article_detail', slug=slug)

    comments = article.comments.order_by('-created_at')
    is_bookmarked = article.bookmarks.filter(id=request.user.id).exists() if request.user.is_authenticated else False

    context = {
        'article': article,
        'comments': comments,
        'is_bookmarked': is_bookmarked
    }
    return render(request, 'news/article_detail.html', context)

@login_required
def toggle_bookmark(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.bookmarks.filter(id=request.user.id).exists():
        article.bookmarks.remove(request.user)
    else:
        article.bookmarks.add(request.user)
    return redirect('article_detail', slug=slug)

def calendar_view(request):
    from datetime import date
    upcoming_games = UpcomingGame.objects.filter(release_date__gte=date.today()).order_by('release_date')
    for game in upcoming_games:
        game.days_remaining = (game.release_date - date.today()).days
    return render(request, 'news/calendar.html', {'games': upcoming_games})

def review_list(request):
    reviews = GameReview.objects.order_by('-created_at')
    return render(request, 'news/review_list.html', {'reviews': reviews})

def review_detail(request, slug):
    review = get_object_or_404(GameReview, slug=slug)
    return render(request, 'news/review_detail.html', {'review': review})