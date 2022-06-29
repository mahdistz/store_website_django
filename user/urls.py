from django.urls import path
from .views import UserListView , UserDetailView

urlpatterns = [
    path('list-of-users/', UserListView.as_view()),
    path('list-of-users/<int:pk>/', UserDetailView.as_view()),

]
