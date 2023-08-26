from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Questions, Comments
# Create your views here.


def index(request):
    if request.method == 'POST':
        id = request.POST['ques']
        print(id)
    allQuestions = Questions.objects.all()
    allComments = Comments.objects.all()
    user = request.user

    context = {
        "questions":allQuestions,
        "comments":allComments,
        "user":user
    }
    return render(request, 'index.html', context)


def addQues(request):
    title = request.GET['title']
    descr = request.GET['desc']

    ques = Questions(title=title, desc=descr)
    ques.save()

    return redirect("/")


def addComment(request):
    comment = request.GET['newComment']
    quesId = request.GET['questionId']
    ques = Questions.objects.get(id=quesId)
    user = request.user
    parentId = request.GET['parentId']

    if parentId == "":
        newComment = Comments(comment=comment, user=user, question=ques)
    else:
        parent = Comments.objects.get(id=parentId)
        newComment = Comments(comment=comment, user=user, question=ques, parent=parent)
    newComment.save()
    return redirect('/')


def handlelogin(request):
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successful.")
            return redirect('/')
        else:
            messages.error(request, "Sorry!! Username of password does not match.")
            return redirect('/')

    return redirect("404 - Page not found.")


def handlelogout(request):
    logout(request)
    messages.success(request, "Logout Successfully.")
    return redirect("/")


# def handlesignup(request):
#     if request.method == "POST":
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         uname = request.POST['uname']
#         email = request.POST['emailA']
#         password = request.POST['pass']
#
#         user = User.objects.create_user(uname, email, password)
#         user.first_name = fname
#         user.last_name = lname
#         user.save()
#         messages.success(request, "Signup Successful.")
#         login(request, user)
#     return redirect('/')


def handlesignup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        email = request.POST['emailA']
        password = request.POST['pass']

        # Check if a user with the same username already exists
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('/signup')  # Redirect back to the signup page with an error message

        user = User.objects.create_user(username=uname, email=email, password=password)
        user.first_name = fname
        user.last_name = lname
        user.save()
        messages.success(request, "Signup Successful.")
        login(request, user)

    return redirect('/')


def search(request):
    query = request.GET['search']

    if len(query) > 30:
        allQuestions = []
    else:
        allQuestions = Questions.objects.filter(title__icontains=query)

    params = {
        "questions":allQuestions
    }
    print(f"Search query : {query}")
    return render(request, "search.html", params)






from django.shortcuts import get_object_or_404


# def delete_question(request, question_id):
#     question = get_object_or_404(Questions, id=question_id)
#
#     # Check if the logged-in user is the creator of the question
#     if request.user == question.user:
#         # Delete associated comments first
#         Comments.objects.filter(question=question).delete()
#
#         # Delete the question
#         question.delete()
#         messages.success(request, "Question deleted successfully.")
#     else:
#         messages.error(request, "You are not authorized to delete this question.")
#
#     return redirect('/')


from django.shortcuts import render, redirect


def delete_question(request, question_id):
    if request.user.is_authenticated:
        try:
            question = Questions.objects.get(id=question_id, user=request.user)
            comments_to_delete = Comments.objects.filter(question=question)

            # Delete the question and associated comments
            question.delete()
            comments_to_delete.delete()

            return redirect('Home')  # Redirect to the home page or a relevant URL
        except Questions.DoesNotExist:
            # Handle case when question doesn't exist or user doesn't own it
            pass
    return redirect('login')  # Redirect to the login page if not authenticated


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)

    # Check if the logged-in user is the creator of the comment
    if request.user == comment.user:
        # Delete the comment
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this comment.")

    return redirect('/')