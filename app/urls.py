from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from .forms import LoginForm,ChangePasswordForm,MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    
    path('', views.ProductViews.as_view(),name='home'),
    
    path('product-detail/<int:pk>', views.ProductDetailViews.as_view(), name='product-detail'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('pluscart/', views.plus_cart, name='plus-cart'),

    path('minuscart/', views.minus_cart, name='minus-cart'),

    path('removecart/', views.remove_cart, name='remove-cart'),

    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('cart/', views.show_cart, name='show_cart'),
    
    path('buy/', views.buy_now, name='buy-now'),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('address/', views.address, name='address'),
    
    path('orders/', views.orders, name='orders'),
    
    path('mobile/', views.mobile, name='mobile'),
    
    path('mobile/<slug:data>', views.mobile, name='mobile_data'),
    
    path('laptop/', views.laptop, name='laptop'),
    
    path('laptop/<slug:data>', views.laptop, name='laptop_data'),
    
    path('topwear/', views.topwear, name='topwear'),
    
    path('topwear/<slug:data>', views.topwear, name='topwear_data'),
    
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomwear_data'),
    
    path('account/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=ChangePasswordForm,success_url='/changepassworddone/'), name='changepassword'),
    
    path('changepassworddone/', auth_views.PasswordChangeView.as_view(template_name='app/changepassworddone.html', form_class=ChangePasswordForm, ), name='changepassworddone'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm, ), name='password_reset'),
    
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html' ), name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm,), name='password_reset_confirm'),
    
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    
    path('registration/', views.CustomerRegisterationView.as_view(), name='customerregistration'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
