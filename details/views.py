from django.shortcuts import render, redirect
from django.contrib import auth,messages
from .models import ContactDetails

# Create your views here.

def contact(request):
	contacts = ContactDetails.objects.get(id=1)
	if request.method == 'POST':
		phone = request.POST['phone']
		email = request.POST['email']
		address = request.POST['address']
		contacts.update(phone=phone, email=email, address=address)
		messages.success(request,'Changes Saved')
		return redirect('contact')
	return render(request,'contact.html',{'contacts':contacts})