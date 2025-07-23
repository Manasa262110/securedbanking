from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth,messages
from .models import CardList
from banks.models import BankList

def userCards(request):
	cards = CardList.objects.all()
	return render(request,'admin/user_cards.html', {'cards': cards})

def addCard(request):
	username = request.user.username
	if request.method == 'POST':
		name = request.POST['name']
		bank = request.POST['bank']
		card = request.POST['card']
		if CardList.objects.filter(card=card).exists() and CardList.objects.filter(bank=bank).exists():
			messages.error(request,'Card Already Exists')
			return redirect('addCard')
		else:
			cards = CardList.objects.create(username=username, name=name, bank=bank, card=card, pvtkey=None, binary=None)
			cards.save()
			messages.success(request,'Card Added Successfully')
			return redirect('../profile')
	banks = BankList.objects.all()
	return render(request, 'user/addcard.html',{'banks':banks})

def updateCard(request,id):
	cards=CardList.objects.get(id=id)
	username = request.user.username
	if request.method == 'POST':
		cards.name = request.POST['name']
		cards.bank = request.POST['bank']
		cards.card = request.POST['card']
		cards.save()
		messages.success(request,'Card Update Successful')
		return redirect('../profile')
	banks = BankList.objects.all()
	return render(request, 'user/updatecard.html',{'banks':banks, 'cards':cards})

def coin(request):
	cards = CardList.objects.all()
	return render(request, 'admin/coin_element.html',{'cards':cards})

def genBinKey(request, id):
	cards = CardList.objects.get(id=id)
	cardNo = int(cards.card)
	cards.binary = bin(cardNo).replace("0b","")
	cards.save()
	messages.info(request,'Binary Key Generated')
	return redirect('coin')

def genPvtKey(request,id):
	"""cards = CardList.objects.get(id=id)
	key = cards.id
	cardNo = str(cards.card)
	cards.pvtkey = str(encrypt(cardNo,key))
	cards.save()"""
	cards = CardList.objects.get(id=id)
	cardNo = int(cards.card)
	cards.pvtkey= bin(cardNo).replace("0b", "")
	cards.save()
	messages.info(request,'Private Key Generated')
	return redirect('../identity')



#AES encryption for private key generation

import base64
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
 
BLOCK_SIZE = 16 
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)

"""def get_private_key(password):
    #salt = b"this is a salt"
    #kdf = PBKDF2(password, salt, 64, 1000)
    #key = kdf[:32]
	key = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
    #return key"""



def encrypt(raw, password):
	cards = CardList.objects.get(id=id)
	cardNo = int(cards.card)
	cards.binary = bin(cardNo).replace("0b", "")
	cards.save()

def get_private_key(raw, password):
	cards = CardList.objects.get(id=id)
	cardNo = int(cards.card)
	cards.binary = bin(cardNo).replace("0b", "")
	cards.save()