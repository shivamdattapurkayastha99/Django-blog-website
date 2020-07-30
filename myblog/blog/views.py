from django.shortcuts import render,HttpResponse,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras
import math
# Create your views here.
def bloghome(request):
    no_of_posts=3
    page=request.GET.get('page')
    if page is None:
        page=1
    else:
        page=int(page)

    allPosts=Post.objects.all()[(page-1)*no_of_posts:page*no_of_posts]
    blogs1=Post.objects.all()
    length=len(blogs1)
    if page>1:
        prev=page-1
    else:
        prev=None
    if page<math.ceil(length/no_of_posts):
        nxt=page+1
    else:
        nxt=None

    # print(allPosts)
    context={'allposts':allPosts,'prev':prev,'nxt':nxt}
   
    # return HttpResponse('This is bloghome.we will keep only blogposts here')
    return render(request,'blog/bloghome.html',context)
def blogpost(request,slug):
    post=Post.objects.filter(slug=slug).first()
    post.views=post.views+1
    post.save()
    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)


    context={'post':post,'comments':comments,'user':request.user,'replyDict':replyDict}

    return render(request,'blog/blogpost.html',context)
    # return HttpResponse(f'This is blog {slug}')
def postComment(request):
    if request.method=='POST':
        
        comment=request.POST.get("comment")
        user=request.user
        postSno=request.POST.get("postSno")
        post=Post.objects.get(sno=postSno)
        parentSno=request.Post.get("parentSno")
        if parentSno=="":

           comment=BlogComment(comment=comment,user=user,post=post)
           comment.save()
           messages.success(request,"your comment has been posted successfully")
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"your reply has been posted successfully")
            

        
    

    return redirect(request,'/blog/{slug}')
