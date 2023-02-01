from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import MyTask


def home(request):
    return render(request, 'home/index.html')


class UserLogin(LoginView):
    template_name = 'home/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home-page')


class UserRegister(FormView):
    template_name = 'home/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegister, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home-page')
        return super(UserRegister, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = MyTask
    template_name = 'home/home_page.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = context['items'].filter(user=self.request.user)
        context['count'] = context['items'].filter(status__in=['N', 'P']).count()

        search_text = self.request.GET.get('search-task') or ''
        if search_text:
            context['items'] = context['items'].filter(title__icontains=search_text)
        context['search_text'] = search_text
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = MyTask
    template_name = 'home/item_detail.html'
    context_object_name = 'item'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = MyTask
    fields = ['title', 'description', 'priority', 'status']
    template_name = 'home/item_create.html'
    success_url = reverse_lazy('home-page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = MyTask
    fields = ['title', 'description', 'priority', 'status']
    template_name = 'home/item_update.html'
    success_url = reverse_lazy('home-page')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = MyTask
    template_name = 'home/delete_confirmation.html'
    success_url = reverse_lazy('home-page')
