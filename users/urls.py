from django.urls import path
from .views import SignUpView, UserListView, UserDetailView, UserCreateView

app_name = 'users'
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user/create/', UserCreateView.as_view(), name='user-create')
]
