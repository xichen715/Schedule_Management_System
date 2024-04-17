from django.urls import path

from . import views
urlpatterns = [path('', views.HomePageView.as_view(), name='home'),
               path('event', views.EventView.as_view(), name='event'),
               path('event/create', views.EventCreateView.as_view(), name='event_create'),
               path('event/detail', views.EventDetailView.as_view(),name='event_detail'),
               path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
               path('event/info', views.EventInfoView.as_view(), name='event_info'),
               path('notebook', views.NotebookListView.as_view(),name='notebook'),
               path('notebook/<int:pk>',views.NotebookDetailView.as_view(),name='notebook_detail'),
               path('notebook/create', views.NotebookCreateView.as_view(), name='notebook_create'),
               path('notebook/<int:pk>/edit/', views.NotebookUpdateView.as_view(), name='notebook_update'),
               path('notebook/<int:pk>/delete/', views.NotebookDeleteView.as_view(), name='notebook_delete'),]

