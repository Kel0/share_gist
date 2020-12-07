from django.urls import path

from .views import LexersView, PastesView

urlpatterns = [
    path("lexers/", LexersView.as_view(), name="lexers"),
    path("snippet/", PastesView.as_view(), name="snippet"),
]
