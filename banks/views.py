from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth,messages
from .models import BankList

def banks(request):
	banks = BankList.objects.all()
	return render(request, 'admin/banklist.html', {'banks': banks})

def addBank(request):
	if request.method=='POST':
		name=request.POST['name']
		btype=request.POST['btype']
		hq=request.POST['hq']
		estd=request.POST['estd']

		if BankList.objects.filter(name=name).exists():
			messages.error(request,'Bank already exists in the list')
			return redirect('addBank')
		else:
			banks=BankList.objects.create(name=name, btype=btype, hq=hq, estd=estd)
			banks.save();
			messages.success(request,"Bank Added Successfully")
			return redirect('banks')
	return render(request, 'admin/addbank.html')

def editBank(request,id):
	banks = BankList.objects.get(id=id)
	if request.method=='POST':
		name=request.POST['name']
		btype=request.POST['btype']
		hq=request.POST['hq']
		estd=request.POST['estd']
		banks.update(name=name, btype=btype, hq=hq, estd=estd)
		banks.save();
		messages.success(request,"Bank Editted Successfully")
		return redirect('banks')
	return render(request, 'admin/editbank.html', {'banks': banks})