from django.urls import path
from django.views.generic import TemplateView

from core import views

app_name = "core"
urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('ticket/create/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
]
