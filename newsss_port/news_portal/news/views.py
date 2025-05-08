from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from .models import Category, Article, Subscription
from .forms import CustomUserCreationForm

class CategoryListView(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'news/category_detail.html'
    context_object_name = 'category'

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'

class SubscribeCategoryView(LoginRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        Subscription.objects.get_or_create(user=request.user, category=category)
        return redirect('category_detail', pk=category.pk)

class UnsubscribeCategoryView(LoginRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        Subscription.objects.filter(user=request.user, category=category).delete()
        return redirect('category_detail', pk=category.pk)

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('category_list')
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        print("Dispatch called for SignUpView")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print("POST request received. CSRF token:", request.POST.get('csrfmiddlewaretoken'))
        print("Request headers:", request.headers)
        print("Request body:", request.body)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print("Form is valid! Saving user...")
        response = super().form_valid(form)
        print("User saved:", self.object.username)
        login(self.request, self.object)
        print("User logged in:", self.request.user)
        try:
            category_list_url = f"{settings.SITE_URL}/"
            html_content = (
                f'Привет, {self.object.username}! <br><br>'
                f'Спасибо за регистрацию на нашем новостном портале!<br><br>'
                f'Перейдите к категориям: <a href="{category_list_url}">Категории</a><br><br>'
                f'С уважением,<br>Команда новостей'
            )
            msg = EmailMultiAlternatives(
                subject='Добро пожаловать в News Portal!',
                body=f'Привет, {self.object.username}!\n\nСпасибо за регистрацию на нашем новостном портале!\n\nПерейдите к категориям: {category_list_url}\n\nС уважением,\nКоманда новостей',
                from_email=None,
                to=[self.object.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print("Welcome email sent to:", self.object.email)
        except Exception as e:
            print("Failed to send email:", str(e))
        return response

    def form_invalid(self, form):
        print("Form is invalid. Errors:", form.errors)
        return super().form_invalid(form)