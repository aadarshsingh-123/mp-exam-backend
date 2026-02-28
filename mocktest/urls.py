from django.urls import path
from .views import SubmitTestView, HistoryView, LeaderboardView, QuestionListView

urlpatterns = [
    path('submit/', SubmitTestView.as_view(), name='submit-test'),
    path('history/', HistoryView.as_view(), name='test-history'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('questions/', QuestionListView.as_view(), name='questions_api'),
]
