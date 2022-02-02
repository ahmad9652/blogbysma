
from pickle import NONE
from turtle import title
from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate,login,logout
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from blog.models import blog,contactuser,blogcomment
from django.contrib import messages
from blog.templatetags import extras
import math
from django.db import IntegrityError
# Create your views here.
def index(request):
    try:
        if request.user.is_authenticated:
            return redirect('/dashboard')
        else:
            return render(request,'index.html')
    except:
        # messages.success(request, "Something Went wrong")
        return HttpResponse("404-Page Not Found")
def blog1(request):
    try:
        messages.success(request,"Welcome to worlds best blog Website")
        post_no = 12
        page_no=request.GET.get('page')
        # print(page_no)
        if page_no == None:
            page_no = 1
        else:
            page_no = int(page_no)
            
        # print(page_no)
        # adminblog=blog.objects.all()
        # userblogo=userblog.objects.all()
        # print(userblogo)
        blogs=blog.objects.all().order_by('Time')
        length=len(blogs)
        # print(length)
        blogs=blogs[(page_no-1)*post_no:page_no*post_no]
        if page_no>1:
            prev=page_no-1
        else:
            prev=None
        # print(math.ceil(len(blogs)/post_no))
        if page_no<math.ceil(length/post_no):
            nxt = page_no+1
        else:
            nxt=None
        # print(page_no)
        # print(prev)
        # print(nxt)
        context={'blogs':blogs ,"prev":prev,"next":nxt}
        return render(request, 'bloghome.html' , context)
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")
def blogpost(request,Slug):
    try:
        blogs = blog.objects.filter(Slug=Slug).first()
        # userblogso = userblog.objects.filter(Slug=Slug).first()
        # if adminblogs==None:
        #     blogs=userblogso
        #     instance=userblog
        # else:
        #     blogs=adminblogs
        #     instance=blog
        comments=blogcomment.objects.filter(post=blogs, parent=None)
        replies=blogcomment.objects.filter(post=blogs).exclude(parent=None)
        replydict={}
        for reply in replies:
            if reply.parent.sno not in replydict.keys():
                replydict[reply.parent.sno]=[reply]
            else:
                replydict[reply.parent.sno].append(reply)
        count = len(comments)
        context = {"blogs":blogs ,"Slug":Slug,"comments":comments ,'user':request.user,'count':count,"replies":replydict}
        return render(request, "blogpost.html" ,context)
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")
def contact(request):
    try:
        if request.method=='POST':
            email=request.POST['email']
            name=request.POST['name']
            address=request.POST['address']
            description=request.POST['description']
            contactuserdetail=contactuser(Name=name , Address = address , Description=description , Email=email)
            contactuserdetail.save()
            messages.success(request,"Thank you!  "+ name +" for contacting Us We will let you soon")
        return render(request, 'contact.html' )
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")
def search(request):
    try:
        post_no = 9
        page_no=request.GET.get('page')
        if page_no == None:
            page_no = 1
        else:
            page_no = int(page_no)
        if request.method=='POST':
            srchstring=request.POST["srchstring"]
            if len(srchstring) > 100:
                blogs=blog.objects.none()
                print(blogs.count())
            else:
                allposttitle=blog.objects.filter(Title__contains=srchstring)
                # alluserposttitle=userblog.objects.filter(Title__contains=srchstring)
                allpostcontent=blog.objects.filter(Description__contains=srchstring)
                # alluserpostcontent=userblog.objects.filter(Description__contains=srchstring)
                allpostslug=blog.objects.filter(Slug__contains=srchstring)
                # alluserpostslug=userblog.objects.filter(Slug__contains=srchstring)
                # halfofallpost=allposttitle.union(alluserposttitle,allpostcontent)
                # anotherhalfofallpost=alluserpostcontent.union(allpostslug,alluserpostslug)
                blogs=allposttitle.union(allpostcontent,allpostslug).order_by('Time')
                
            # for i in blogsrch:
            #     if srchstring.lower() in i.Title.lower() or i.Slug.lower() or i.Short_Description.lower():
            #         blogs.append(i)
            blogs=blogs[(page_no-1)*post_no:page_no*post_no]
            if page_no>1:
                prev=page_no-1
            else:
                prev=None
            if page_no<math.ceil(len(blogs)/post_no):
                nxt = page_no+1
            else:
                nxt=None
            context={'blogs':blogs ,"prev":prev,"next":nxt,"searchstring":srchstring}
        if blogs.count==0:
            messages.warning(request, "No search results found. Please refine your query.")
        return render(request, 'search.html' , context)
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")
def handlesignup (request):
    try:
        if request.method=='POST':
            username=request.POST["username"]
            email=request.POST["email"]
            phonenumber = request.POST["phonenumber"]
            pass1=request.POST["pass1"]
            pass2=request.POST["pass2"]
            myuser = User.objects.create_user(username,email,pass1)

            myuser.save()
            messages.success(request,"Your Account has been Created")
            return redirect("/")
        else:
            Http404("Not FOUND")
    except IntegrityError :
        messages.error(request, "Username already exist use a different username")
        return redirect("/")
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/") 
def handlelogin(request):
    try:
        if request.method=="POST":
            loginusername = request.POST["loginusername"]
            loginpassword = request.POST["loginpassword"]
            user = authenticate(username=loginusername,password=loginpassword)
            if user is not None:
                login(request,user)
                messages.success(request, "You are successfully loged in as "+loginusername)
                return redirect("/")
            else:
                messages.error(request, "Invalid credentials")
                return redirect("/")
        else:
            messages.error(request, "Something Went wrong")
            return redirect("/")
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")
def handlelogout(request):
    try:
        username=request.user
        logout(request)
        messages.success(request, username.username+", you are successfully loged out")
        return redirect("/")
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")
def postcomment(request):
    try:
        if request.method=="POST":
            comment= request.POST['commentfield']
            user = request.user
            postsno=request.POST["postsno"]
            post = blog.objects.get(sno=postsno)
            parentsno=request.POST["replysno"]
            if parentsno =="":
                comment = blogcomment(comment=comment,user=user,post=post)
                messages.success(request, user.username+", Your Comment Has been posted Successfully")
            else:
                parent=blogcomment.objects.get(sno=parentsno)
                comment = blogcomment(comment=comment,user=user,post=post,parent=parent)
                messages.success(request, user.username+", Your reply to "+parent.user.username+" Has been posted Successfully")

            comment.save()
            return redirect(f'/blogpost/{post.Slug}')
        else:
            messages.error(request, "Something Went wrong")
            return redirect("/")
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")

def handleuserdashboard(request):
    try:
        post_no = 12
        page_no=request.GET.get('page')
        # print(page_no)
        if page_no == None:
            page_no = 1
        else:
            page_no = int(page_no)
        blogs=blog.objects.filter(user=request.user).order_by('Time')
        length=len(blogs)
        # print(length)
        blogs=blogs[(page_no-1)*post_no:page_no*post_no]
        if page_no>1:
            prev=page_no-1
        else:
            prev=None
        # print(math.ceil(len(blogs)/post_no))
        if page_no<math.ceil(length/post_no):
            nxt = page_no+1
        else:
            nxt=None
        context={"user":request.user,"blogs":blogs,"prev":prev,"next":nxt}
        return render(request,"userdashboard.html",context)
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")
def usercreatedblog(request):
    try:
        if request.method=='POST':
            title=request.POST["userblogtitle"]
            description=request.POST["userblogdescription"]
            shortdescription=request.POST["userblogshortdescription"]
            slug=request.POST["userblogslug"]
            userblogdata=blog(Title=title,Description=description,Short_Description=shortdescription,Slug=slug,user=request.user)
            userblogdata.save()
            messages.success(request, "Your post has been uploaded")
        return redirect("/dashboard")
    except:
        messages.error(request, "Something Went wrong")
        return redirect("/")
    