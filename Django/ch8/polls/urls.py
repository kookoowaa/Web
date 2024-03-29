# polls/urls.py

from django.urls import path
from . import views

app_name='polls'
urlpatterns = [
    # /polls/
    #path('', views.index, name = 'index'),
    path('', views.IndexView.as_view(), name ='index'),

    #/polls/99/
    #path('<int:question_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),

    #/polls/99/results/
    #path('<int:question_id>/results', views.results, name='results'),
    path('<int:pk>/results', views.ResultsView.as_view(), name='results'),

    #/polls/99/detail/
    path('<int:question_id>/vote/', views.vote, name='vote'),   
]