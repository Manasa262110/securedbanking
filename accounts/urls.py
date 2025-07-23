from django.urls import path
from . import views
from details.views import contact

urlpatterns = [
	path('',views.home, name="home"),
	path('signup/',views.userReg, name="userReg"),
	path('vendorRegistration/',views.vendorReg, name="vendorReg"),
	path('admin/', views.admin, name="admin"),
	path('puf/', views.puf, name="puf"),
	path('otp/',views.otpVerify, name="otpVerify"),
	path('profile/',views.editprofile, name="editprofile"),
	path('resetpassword/',views.resetPassword, name="resetPassword"),
	path('changepassword/',views.changePassword, name="changePassword"),
	path('about/',views.about, name="about"),
	path('contact/',contact, name="contact"),
	path('identity/',views.identity, name="identity"),
	path('vendors/',views.vendors, name="vendors"),
	path('delete/<int:id>',views.deleteUser, name="deleteUser"),
]