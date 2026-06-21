# 🎮 GG_NEWS - Advanced Gaming News Portal

GG_NEWS is a dynamic, fully responsive web application built with Python and Django. It automatically scrapes, aggregates, and shuffles live gaming news using the NewsAPI stream, featuring a complete ecosystem for gamer community engagement.

## 🚀 Core Features Implemented
* **Automated News Stream:** Integrated with NewsAPI to dynamically pull fresh global gaming news on demand.
* **Smart Content Shuffling:** Custom backend algorithms that shuffle and randomize news grids on every refresh.
* **Full Authentication System:** Live user registration, login, and profile redirection pathways.
* **Interactive Engagement:** Complete commenting system and live "Discussion Rooms" for every news article.
* **Personal Lounge (Bookmarks):** Allows logged-in users to save articles to a personalized reading list on their profile.
* **Upcoming Games Calendar:** A real-time launch tracker that automatically calculates countdown days until a game releases.
* **Expert Game Reviews:** In-depth breakdown dashboards scoring games out of 10 with structural Pros/Cons lists.

## 🛠️ Tech Stack Used
* **Backend:** Python, Django Web Framework
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, Bootstrap 5 (Dark Mode Theme)
* **API Integration:** Requests library interacting with NewsAPI.org

## 💻 How to Run This Project Locally

1. Clone or download this repository.
2. Open your terminal in the project root folder.
3. Apply the database migrations:
   ```bash
 python manage.py migrate
