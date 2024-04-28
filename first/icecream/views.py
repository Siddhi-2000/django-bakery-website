from first import settings
from django.shortcuts import render,redirect
from icecream.models import Contact
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

@login_required(login_url='/signin')
def index(request):
    if request.user.is_authenticated:
        print(request.user.username)
        print("hi kr")
        return render(request,'index.html')
    else:
        return redirect("/signin")
    # return render(request,'index.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        desc=request.POST.get("desc")
        contact=Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request,'SUBMIT SUCCESSFUL!')

        myuser = contact
        print(myuser.name,myuser.email)
        subject="welcome to HOP SCOTCH!!"
        message="greetings"+ myuser.name +"\n\nWe have recived your sugestion and will work on it to improve ourselves \n\n Hope to see you at HOP SCOTCH! \n Visit again"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

    return render(request,'contact.html')



def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        print(username,fname)
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if password1 != password2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'You have successfully registered')

        
        subject="welcome to HOP SCOTCH!!"
        message="greetings "+ myuser.first_name +"\n\nEnjoy our newly produced flavors and give yourself a break \n\n Hope to see you at HOP SCOTCH!"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return redirect("/signin")
    
    
    return render(request,'signup.html')



def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        print(username,pass1)
        user = authenticate(username=username, password=pass1)
        print(user)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success("logged out successfully")
    return redirect('signin')


def order(request):
    if request.method=="POST":
        address=request.POST.get("adress")
        quantity=request.POST.get("quantity")
        phone=request.POST.get("phone")
        addinfo=request.POST.get("addinfo")
        flavor=request.POST.get("flavor")
        print(request.user.email)
        subject="YOUR ORDER"
        print(subject)
        message="\nYour order is: "+flavor+" ice-cream and the qauntity is"+quantity+"\nWe will diliver your icecream soon!!"+"\n\nTHANYOU FOR YOUR ORDER"+"\n p.s. we will contact you on "+phone
        from_email=settings.EMAIL_HOST_USER
        to_list=[request.user.email]
        print(subject,message,to_list)
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        return redirect("/")
    return render(request,"order.html")