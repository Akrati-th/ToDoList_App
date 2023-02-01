from django.urls import path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, UserLogin, UserRegister

from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='index'),
    path('home/', TaskList.as_view(), name='home-page'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='item-detail'),
    path('item-create/', TaskCreate.as_view(), name='item-create'),
    path('item-update/<int:pk>', TaskUpdate.as_view(), name='item-update'),
    path('item-delete/<int:pk>', TaskDelete.as_view(), name='item-delete'),
]