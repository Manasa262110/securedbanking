from django.urls import path
from . import views

urlpatterns = [
	path('addcard',views.addCard, name="addCard"),
	path('coinelement',views.coin, name="coin"),
	path('privatekey/<int:id>',views.genPvtKey, name="genPvtKey"),
	path('binarykey/<int:id>',views.genBinKey, name="genBinKey"),
	path('usercards',views.userCards, name="userCards"),
	path('updatecard/<int:id>',views.updateCard, name="updateCard"),
]
