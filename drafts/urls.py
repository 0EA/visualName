from django.contrib import admin
from django.urls import path
from . import views

app_name = "drafts"

urlpatterns = [
    path('datasetDraft/', views.datasetDraft, name="datasetDraft"),
    path('addDataset/', views.addDataset, name="addDataset"),
    path('update/<int:id>', views.updateDataset, name='updateDatasetDraft'),
    path('delete/<int:id>', views.deleteDataset, name='deleteDatasetDraft'),
    path('download/<int:id>', views.downloadDataset, name='downloadDatasetDraft'),

    path('funcDraft/', views.funcDraft, name="funcDraft"),
    path('addFunc/', views.addFunc, name="addFunc"),
    path('updateFunc/<int:id>', views.updateFunc, name='updateFuncDraft'),
    path('deleteFunc/<int:id>', views.deleteFunc, name='deleteFuncDraft'),
    path('downloadFunc/<int:id>', views.downloadFunc, name='downloadFuncDraft'),

]


