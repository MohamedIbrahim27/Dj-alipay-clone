from unicodedata import name
from django.urls import path ,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name='payment'


urlpatterns = [

    path('',views.home_page,name='home_page'),
    path('wallet',views.wallet,name='wallet'),
    path('password_make',views.password_make,name='password_make'),
    ## to transform or send money 
    path('trasform',views.trasform_qr,name='trasform_qr'),
    path('tarnsfrom/<uidb64>/<token>/',views.tarnsfrom,name='tarnsfrom'),
    ## to pay money  
    path('pay',views.pay_qr,name='pay_qr'),
    path('pay/<uidb64>/<token>/',views.pay,name='pay'),
    
    
    
    path('day-expenses',views.dayly_expenses,name='dayly_expenses'),
]
