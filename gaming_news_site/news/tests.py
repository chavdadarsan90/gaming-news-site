from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta
from django.utils import timezone
from .models import GameReview, UpcomingGame, Article

class HomeViewTest(TestCase):
    def setUp(self):
        self.article1 = Article.objects.create(
            title="Elden Ring DLC Released",
            slug="elden-ring-dlc-released",
            content="Full coverage of Shadow of the Erdtree.",
            summary="Shadow of the Erdtree expands the Lands Between.",
            published_at=timezone.now(),
            view_count=150
        )
        self.article2 = Article.objects.create(
            title="PlayStation State of Play Summary",
            slug="playstation-state-of-play-summary",
            content="All game announcements from the showcase.",
            summary="New announcements for PS5.",
            published_at=timezone.now(),
            view_count=300
        )

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Elden Ring DLC Released")
        self.assertContains(response, "Trending Now")

    def test_home_search_view(self):
        response = self.client.get(reverse('home') + '?q=Elden')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Elden Ring DLC Released")

    def test_article_detail_view(self):
        response = self.client.get(reverse('article_detail', kwargs={'slug': self.article1.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shadow of the Erdtree")


class GameReviewsViewTest(TestCase):
    def setUp(self):
        self.review = GameReview.objects.create(
            game_name="Cyberpunk 2077: Phantom Liberty",
            slug="cyberpunk-2077-phantom-liberty",
            summary="An incredible expansion that redefines Night City.",
            gameplay_review="Tight combat and deep skill tree overhauls.",
            graphics_performance_review="Stunning ray tracing and high frame rates.",
            pros="Great story, Excellent graphics, Deep skill system",
            cons="Minor visual glitches",
            rating=9,
            cover_image_url="https://images.example.com/cyberpunk.jpg"
        )

    def test_review_list_view(self):
        response = self.client.get(reverse('review_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cyberpunk 2077")
        self.assertContains(response, "9/10")

    def test_review_detail_view(self):
        response = self.client.get(reverse('review_detail', kwargs={'slug': self.review.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Gameplay & Mechanics")
        self.assertContains(response, "Great story")


class UpcomingGameViewTest(TestCase):
    def setUp(self):
        self.game = UpcomingGame.objects.create(
            title="GTA VI",
            platform="PS5, Xbox Series X",
            release_date=date.today() + timedelta(days=100),
            cover_image_url="https://images.example.com/gta6.jpg"
        )

    def test_calendar_view(self):
        response = self.client.get(reverse('calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "GTA VI")
        self.assertContains(response, "100 Days Left")
        self.assertEqual(self.game.get_platform_list(), ["PS5", "Xbox Series X"])
