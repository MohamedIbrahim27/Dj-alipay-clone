from django.shortcuts import render,redirect
from django.contrib.auth.models import User
# Create your views here.
from accounts.models import Profile
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
import qrcode
import base64
from io import BytesIO
from django.contrib import messages
from.models import Pay,Wallet,Order
from django.contrib.auth.hashers import make_password,check_password


def home_page(request):
    if request.user.is_authenticated:
        chats=Pay.objects.all()
        return render(request, "payment/index.html",{'chats':chats})
    else:
        return render(request, "payment/use_not_login.html")


def dayly_expenses(request):
    user_profile = Profile.objects.get(user=request.user)
    chats=Pay.objects.filter(sender=user_profile)
    return render(request, "payment/dayly.html",{'chats':chats})


def trasform_qr(request):
    user_profile = Profile.objects.get(user=request.user)
    uid = urlsafe_base64_encode(force_bytes(user_profile.pk))
    token = default_token_generator.make_token(request.user)
    unique_identifier = f"{uid}/{token}"
    url = f"/tarnsfrom/{unique_identifier}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return render(request, "payment/qrcode_recive.html", {'img_str': img_str})

def tarnsfrom(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid) 
        user_profile = Profile.objects.get(user=user)
        login_profile = Profile.objects.get(user=request.user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, Profile.DoesNotExist):
        messages.error(request, 'Error')
        return redirect('/')

    # Check if the user and token are valid
    if user_profile and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Handle POST request logic here if needed
            wallet =Wallet.objects.get(owner=login_profile)
            money_transorm = request.POST['money_transorm']
            password = request.POST['password']
            if check_password(password, wallet.password):
                print('yes')
                print(money_transorm)
                SendMoney=Pay.objects.create(
                    amount_paid=int(money_transorm),
                    sender=login_profile,
                    receiver=user_profile,
                    status='TRANSFORM'
                )
            else:
                print('no')
                print(money_transorm)
    else:
        messages.error(request, 'Error')
        return redirect('/')
    
    return render(request, "payment/qr_code_pay_scan.html")

def  wallet(request):
    user_profile = Profile.objects.get(user=request.user)
    wallet =Wallet.objects.get(owner=user_profile)
    return render(request, "payment/wallet.html",
                            {'wallet':wallet,})


def  password_make(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        user_profile = Profile.objects.get(user=request.user)
        if 'password' in request.POST: password=request.POST['password']
        else : messages.error(request,'Error in password !')
        
        if 'confirmPassword' in request.POST: confirmPassword=request.POST['confirmPassword']
        else : messages.error(request,'Error in Password Configration !')
        if password and confirmPassword:
            if password != confirmPassword:
                
                messages.error(request,'The two password fields didn’t match.')
                return render(request,'registration/change_password.html')
            else:
                wallet =Wallet.objects.get(owner=user_profile)
                wallet.password =make_password(password)
                wallet.save()
                messages.success(request,'password reset successfully !')
                return redirect('/password_make')
        else:
            messages.error(request,'Please fill in all fields !')
            return render(request,'registration/change_password.html')
    return render(request, "payment/password_ma.html")

def pay_qr(request):
    user_profile = Profile.objects.get(user=request.user)
    uid = urlsafe_base64_encode(force_bytes(user_profile.pk))
    token = default_token_generator.make_token(request.user)
    unique_identifier = f"{uid}/{token}"
    url = f"/pay/{unique_identifier}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return render(request, "payment/qrcode_recive.html", {'img_str': img_str})


def pay(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid) 
        user_profile = Profile.objects.get(user=user)
        login_profile = Profile.objects.get(user=request.user)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, Profile.DoesNotExist):
        messages.error(request, 'Error')
        return redirect('/')

    # Check if the user and token are valid
    if user_profile and default_token_generator.check_token(user, token):
        order=Order.objects.filter(user=user_profile, is_finished=False).first()
        if order is not None:
            pay=Pay.objects.create(
                    amount_paid=int(order.total),
                    sender=user_profile,
                    receiver=login_profile,
                    status='PAY'
                )
            order.is_finished =True
            order.save()
            print(order.id)
            print(order.total)
        else:
            messages.error(request, 'No order found for the user.')
            return redirect('/')
        messages.error(request, 'oky')
        return redirect('/')
    else:
        messages.error(request, 'Error')
        return redirect('/')
    
    # return render(request, "payment/qr_code_pay_scan.html")

# from django.shortcuts import render
# import qrcode
# from PIL import Image
# from io import BytesIO
# import base64

# def index(request):
#     context = {}
#     if request.method == "POST":
#         qr_text = request.POST.get("qr_text", "")
#         qr_image = qrcode.make(qr_text, box_size=15)
#         qr_image_pil = qr_image.get_image()
#         stream = BytesIO()
#         qr_image_pil.save(stream, format='PNG')
#         qr_image_data = stream.getvalue()
#         qr_image_base64 = base64.b64encode(qr_image_data).decode('utf-8')
#         context['qr_image_base64'] = qr_image_base64
#         context['variable'] = qr_text
#     return render(request, 'index.html', context=context)
