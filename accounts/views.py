from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings


from .models import Profile
from .forms import SignupForm,UserActivateForm
from products.models import Product , Review , Brand
from orders.models import Order
# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            user = form.save(commit=False)
            user.is_active = False
            form.save()
            profile = Profile.objects.get(user__username = username)
            code = profile.code
            #send email
            send_mail(
                f"Activate Your account {username}",
                f"Please Use this code {code} to activate.",
                f"{settings.EMAIL_HOST_USER}",
                [email],
                
                    )
            return redirect(f'/accounts/{username}/activate')
    else:
        form = SignupForm()
    return render(request,'accounts/signup.html',{'form':form})
    
def userActivate(request,username):
    profile = Profile.objects.get(user__username = username)
    if request.method == 'POST':
        form = UserActivateForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if code == profile.code:
                profile.code = ""
                
                user  = User.objects.get(username= username)
                user.is_active = True
                user.save()
                profile.save()
                 
                return redirect('accounts/login')
    else:
        form = UserActivateForm()
        
    return render(request,'accounts/activate.html',{'form':form})
    
def dashboard(request):
    products = Product.objects.all().count()
    brands = Brand.objects.all().count()
    reviews = Review.objects.all().count()
    orders = Order.objects.all().count()
    context = {'products':products,'reviews':reviews,'orders':orders,'brands':brands}
     
    return render(request,'accounts/dashboard.html',context=context)