# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class BugReport(models.Model):
    reporter_name = models.CharField(max_length=100)
    email = models.EmailField()
    bug_title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bug: {self.bug_title} by {self.reporter_name}"
class GameReview(models.Model):
    game_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField(help_text="Short introductory summary of the review.")
    
    # Structural breakdown criteria
    gameplay_review = models.TextField()
    graphics_performance_review = models.TextField()
    
    # Lists for quick scanning
    pros = models.TextField(help_text="Enter pros separated by commas.")
    cons = models.TextField(help_text="Enter cons separated by commas.")
    
    # Rating validation (Scale of 1 to 10)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Enter a score from 1 to 10."
    )
    
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game_name} - {self.rating}/10"

    # Helper methods to split commas into lists in templates easily
    def get_pros_list(self):
        return [item.strip() for item in self.pros.split(',') if item.strip()]

    def get_cons_list(self):
        return [item.strip() for item in self.cons.split(',') if item.strip()]

class UpcomingGame(models.Model):
    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=100) # e.g., "PS5, Xbox Series X, PC"
    release_date = models.DateField()
    cover_image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    source_api_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, null=True)
    
    # FIX: Changed 'on_file' to 'on_delete' below
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_articles', blank=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"