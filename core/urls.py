from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Index page
    path('login/', views.signin, name='login'),  # Login page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('logout/', views.user_logout, name='logout'),  # Logout page
    path('converter/', views.converter, name='converter'),  # Converter page with trailing slash
    path('history/', views.DownloadHistoryAPI.as_view(), name='download_history'),  # Download history API
]
