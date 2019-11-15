from django.urls import path

from core import views

app_name = "core"
urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('ticket/create/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/<int:pk>/update/', views.TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/comment/', views.CommentCreateView.as_view(), name='ticket-comment'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('attachment/create/', views.AttachmentCreateView.as_view(), name='attachment-create'),
]
