from django.urls import path
from django.views.generic import TemplateView

from core import views

app_name = "core"
urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('ticket/create/', views.TicketCreateView.as_view(), name='ticket-create'),
]
