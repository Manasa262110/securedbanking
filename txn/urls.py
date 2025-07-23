from django.urls import path
from . import views
from .views import balance_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('deposit', views.deposit, name='deposit'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('transfer', views.transfer, name='transfer'),
    path('transactions', views.txnHistory, name='transactions'),
    path('verification/<int:id>', views.txnVerify, name='txnVerify'),
    path('data', views.form, name='form'),
    path('predict', views.predict, name='predict'),
    path('download_receipt/<int:txn_id>/', views.download_receipt, name='download_receipt'),
    path('balance/', balance_view, name='balance'),
]
