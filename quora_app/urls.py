from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="Home"),
    path('addques', views.addQues, name="Add New Question"),
    path('addcomment', views.addComment, name="New Comment"),
    path('login', views.handlelogin, name="Login"),
    path('logout', views.handlelogout, name="Logout"),
    path('signup', views.handlesignup, name="Signup"),
    path('search', views.search, name="Search"),
    path('delete/question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('delete/comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]