from django.urls import path
from . import views

urlpatterns = [
	path('banklist',views.banks, name="banks"),
	path('addbank',views.addBank, name="addBank"),
	path('editbank/<int:id>',views.editBank, name="editBank"),
]