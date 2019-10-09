from django.urls import path
from django.views.generic import TemplateView

from core.views import TicketListView

app_name = "core"
urlpatterns = [
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
]
