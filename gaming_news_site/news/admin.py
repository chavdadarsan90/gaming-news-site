from django.contrib import admin
from .models import Category, Article, Comment, UpcomingGame, GameReview, BugReport

# Pre-populate slugs using the game name automatically in the admin dashboard
class GameReviewAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('game_name',)}
admin.site.register(BugReport)
admin.site.register(GameReview, GameReviewAdmin)
admin.site.register(UpcomingGame)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Category)   