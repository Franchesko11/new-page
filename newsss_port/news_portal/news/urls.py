from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('article/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('category/<int:pk>/subscribe/', views.SubscribeCategoryView.as_view(), name='subscribe_category'),
    path('category/<int:pk>/unsubscribe/', views.UnsubscribeCategoryView.as_view(), name='unsubscribe_category'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='category_list'), name='logout'),
]