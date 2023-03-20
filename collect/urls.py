from django.urls import path

from . import views


urlpatterns = [
    path('<str:dataset_filename>/', views.view_dataset, name='view_dataset'),
    path('<str:dataset_filename>/valuecount/', views.view_dataset_value_count, name='view_dataset_value_count'),
    path("", views.view_datasets, name="view_datasets"),
]