from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/change/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('add/', views.add, name='add'),
    path('options/', views.options, name='options'),
    path('question/', views.delete, name='delete'),
    path('question/<int:question_id>/delete/', views.one_delete, name='one_delete'),
    path('email/send/', views.show_email, name='show_email'),
    path('email/send/(?P<email>[0-9]+)$', views.send_email, name='send_email'),
]