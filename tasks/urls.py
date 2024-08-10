from django.urls import path
from tasks import views

urlpatterns = [
    path('paras/',views.ParagraphsView.as_view(), name='paras'),
    path('tokenized/',views.TokenizedWordsView.as_view(), name='tokenized'),
]
