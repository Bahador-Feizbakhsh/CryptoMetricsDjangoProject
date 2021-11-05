from django.urls import path
from twitter_metric.views import get_twitter_handle_page

urlpatterns = [
    path('', get_twitter_handle_page, name='get_twitter_handle_page'),
    # path('twitter-metric/<str:twitter_handle>-<str:user_id>/', show_twitter_metrics, name='show_twitter_metrics'),
]
