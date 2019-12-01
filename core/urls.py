from django.urls import path

from core import views

app_name = "core"
urlpatterns = [
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('ticket/create/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/<int:pk>/update/', views.TicketUpdateView.as_view(), name='ticket-update'),
    path('ticket/<int:pk>/comment/', views.CommentCreateView.as_view(), name='ticket-comment'),
    path('ticket/<int:pk>/attach/', views.AttachmentCreateView.as_view(), name='ticket-attach'),
    path('ticket/<int:pk>/update/state/', views.TicketStateUpdateView.as_view(), name='ticket-state-update'),

    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('product/create/', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),

    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('task/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task-delete'),
]
