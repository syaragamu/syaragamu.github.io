from django.urls import path
from baseball_game.views import BaseballGameView

app_name = 'baseball_game'

urlpatterns = [
    path('', BaseballGameView.as_view(), name='game'),
    path('reset/', BaseballGameView.as_view(), name='game_reset')
]