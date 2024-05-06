from django.urls import path



from .views import homePageView, addView, deleteView, signUpView, logOutView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('delete/', deleteView, name='delete'),
    path('signup/', signUpView, name='signup'),
    path('logout/', logOutView, name='logout'),


]
