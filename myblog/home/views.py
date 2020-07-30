from django.shortcuts import render,HttpResponse,redirect
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    return render(request,'home/home.html')
def about(request):
    # messages.success(request,"this is about")

    return render(request,'home/about.html')
def contact(request):
    # messages.success(request,'Enter your details')
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        contact=Contact(name=name,email=email,phone=phone)
        if len(name)<2 or len(email)<3 or len(phone)<10:
            messages.error(request,"Please fill the form correctly")
        else:
            contact.save()
            messages.success(request,"Your form has been submitted")
    return render(request,'home/contact.html')
def search(request):
    query=request.GET['query']
    
    allPostsTitle=Post.objects.filter(title__icontains=query)
    allPostsContent=Post.objects.filter(content__icontains=query)
    allPosts=allPostsTitle.union(allPostsContent)
    if allPosts.count()==0:
        messages.error(request,"No search results found ")
    params={'allPosts':allPosts}
    return render(request,'home/search.html',params)
def handlesignup(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        if len(name)>20:
            messages.error(request,'Your name must be under 20 characters')
            return redirect('home')

        myuser=User.objects.create_user(name,email,password)
        myuser.save()
        messages.success(request,'Your ShivamCoder account has been successfully created')
        return redirect('home')
    else:
        return HttpResponse('Enter credential properly')
def handlelogin(request):
    if request.method=='POST':
       loginname=request.POST['loginname']
       loginpassword=request.POST['loginpassword']
       user=authenticate(username=loginname,password=loginpassword)
       if user is not None:
           login(request,user)
           messages.success(request,"Successfully logged in")
           return redirect('home')
       else:
           messages.error(request,"Access denied try again")
           return redirect('home')
    return HttpResponse('404 not found')
def handlelogout(request):
    
        logout(request)
        messages.success(request,"Successfully Logged out")
        return redirect('home')