from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import auth,messages
from accounts.models import User
from django.core.mail import send_mail
from django.contrib.auth import password_validation
from cards.models import CardList
from banks.models import BankList
import math
import random

otp = None
# Create your views here.

def about(request):
	return render(request, 'about.html')

def home(request):
	if not request.user.is_authenticated:
		if request.method=="POST" and "user-login" in request.POST:
			username=request.POST['username']
			password=request.POST['password']

			user=auth.authenticate(username=username,password=password)

			if user is not None:
				if not user.is_superuser:
					if not user.is_staff:
						auth.login(request,user)
						return redirect('otpVerify')
					else:
						messages.error(request,'Incorrect Username or Password')
						return redirect('home')
				else:
					messages.error(request,'Incorrect Username or Password')
					return redirect('home')
			
		if request.method=="POST" and "vendor-login" in request.POST:
			username=request.POST['username']
			password=request.POST['password']

			user=auth.authenticate(username=username,password=password)

			if user is not None:
				if not user.is_superuser:
					if user.is_staff:
						auth.login(request,user)
						return redirect('otpVerify')
					else:
						messages.error(request,'Invalid Credentials')
						return redirect('home')
				else:
					messages.error(request,'Incorrect Username or Password')
					return redirect('home')
			else:
				messages.error(request,'Incorrect Username or Password')
				return redirect('home')
		else:
			return render(request,'index.html')
	elif request.user.is_superuser:
		return render(request, 'admin/adminhome.html')
	elif request.user.is_staff:
		return render(request, 'vendor/vendorhome.html')
	else:
		return render(request, 'user/userhome.html')

def puf(request):
	return render(request, 'admin/puf.html')

def admin(request):
	if request.user.is_authenticated:
		return redirect('home')

	if request.method=="POST":
		username=request.POST['username']
		password=request.POST['password']

		user=auth.authenticate(username=username,password=password)

		if user is not None:
			if user.is_superuser:
				auth.login(request,user)
				return redirect('otpVerify')
			else:
				messages.error(request,'Incorrect Username or Password')
				return redirect('admin')
		else:
			messages.error(request,'Incorrect Username or Password')
			return redirect('admin')
	else:
		return render(request,'admin/adminlogin.html')


def otpGen(request):
	string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	OTP = ''
	for i in range(6):
		OTP += string[math.floor(random.random() * len(string))]
	return OTP

def otpSend(request,user,otp):
    emailto = user.email
    if emailto:
    	send_mail(
			"OTP",
			"Your OTP is "+otp+". Do not share it with anyone by any means. This is confidential and to be used by you only.",
			'admin@no-reply.com',
			[emailto],
			fail_silently=False,
			)

def otpVerify(request):
	global otp
	user = request.user
	if otp == None:
		otp = otpGen(request)
		otpSend(request,user,otp)
		return render(request,'otp.html')
	else:
		if request.method == "POST":
			otpfield = request.POST['otp']
			if otpfield == otp:
				return redirect('home')
			else:
				auth.logout(request)
				return HttpResponse('home')
		else:
			otp = otpGen(request)
			otpSend(request,user,otp)
			auth.logout(request)
			return render(request,'otp.html')

def userReg(request):
	if request.method=='POST':
		username=request.POST['username']
		email=request.POST['email']
		mobile=request.POST['mobile']
		gender=request.POST['gender']
		dob=request.POST['dob']
		password1=request.POST['password1']
		password2=request.POST['password2']

		if password1==password2:
			if User.objects.filter(username=username).exists():
				messages.warning(request,'Username Taken')
				return redirect('userReg')
			elif User.objects.filter(email=email).exists():
				messages.warning(request,'Email already exists')
				return redirect('userReg')
			else:
				user=User.objects.create_user(username, password=password1, email=email, mobile=mobile, gender=gender, dob=dob)
				user.save()
				messages.success(request,"Account Created Successfully")
				return redirect('home')
		else:
			messages.error(request,"Password doesn't match")
		return redirect('/')
	else:
		return render(request,'user/user_reg.html')


def vendorReg(request):
	if request.method=='POST':
		username=request.POST['username']
		email=request.POST['email']
		mobile=request.POST['mobile']
		gender=request.POST['gender']
		dob=request.POST['dob']
		bank=request.POST['bank']
		branch=request.POST['branch']
		password1=request.POST['password1']
		password2=request.POST['password2']

		if password1==password2:
			if User.objects.filter(username=username).exists():
				messages.warning(request,'Username Taken')
				return redirect('vendorReg')
			elif User.objects.filter(email=email).exists():
				messages.warning(request,'Email already exists')
				return redirect('vendorReg')
			else:
				user=User.objects.create_user(username, password=password1, email=email, mobile=mobile, gender=gender, dob=dob, bank=bank, branch=branch,  is_staff = True)
				user.save();
				messages.success(request,"Account Created Successfully")
				return redirect('home')
		else:
			messages.error(request,"Password doesn't match")
		return redirect('/')
	else:
		return render(request,'vendor/vendor_reg.html')


def logout(request):
	auth.logout(request)
	return redirect('home')


def editprofile(request):
	banks = BankList.objects.all()
	cards = CardList.objects.all()
	user = request.user
	if request.method=="POST":
		email=request.POST['email']
		pic=request.POST['pic']
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		gender=request.POST['gender']
		mobile=request.POST['mobile']
		if pic is not None:
			user.pic=pic
		user.first_name=first_name
		user.last_name=last_name
		user.gender=gender
		user.mobile=mobile
		user.email=email
		user.save()
		messages.success(request,"Profile Updated Successfully")
		return redirect('editprofile')
	return render(request,'profile.html',{'userdata':user,'cards':cards,'banks':banks})

def resetPassword(request):
	if request.method=="POST":
		email=request.POST['email']
		password1=request.POST['password1']
		password2=request.POST['password2']
		if User.objects.filter(email=email).exists():
			user = User.objects.get(email=email)
			user.set_password(password1)
			user.save()
			messages.success(request,'Password Reset Successful')
			return redirect('home')
		else:
			messages.error(request,'Email does not exist')
			return redirect(request, 'resetPassword')
	else:
		return render(request, 'passwordreset.html')

def changePassword(request):
	user = request.user
	if request.method=="POST":
		password1=request.POST['password1']
		password2=request.POST['password2']
		passwordnow=request.POST['passwordnow']
		if password1==password2:
			if user.check_password(passwordnow):
				user.set_password(password1)
				user.save()
				messages.success(request,'Password Updated')
				return redirect('devProfile')
			else:
				messages.error(request,'Incorrect Password')
				return redirect('changePassword')
		else:
			messages.error(request,'Password does not match')
			return redirect('changePassword')
	else:
		return render(request, 'changepassword.html')

def identity(request):
	userdata=User.objects.all()
	cards = CardList.objects.all()
	return render(request, 'admin/identity_element.html',{'userdata':userdata, 'cards':cards})

def vendors(request):
	vendors = User.objects.all()
	return render(request, 'admin/vendors.html',{'vendors':vendors})

def deleteUser(request, id):
	user = User.objects.get(id=id)
	user.delete()
	messages.error(request,'User deleted')
	return redirect('identity')