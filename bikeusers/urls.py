from django.urls import path
from bikeusers import views

urlpatterns=[
    path('account/home', views.UserHome.as_view(), name= 'user_home'),
    path('account/signup', views.SignUp.as_view(), name= 'signup'),
    path('activate/<uidb64>/<token>/', views.ActivateView.as_view(), name="activate"),
    path('check-email/', views.CheckEmailView.as_view(), name="check_email"),
    path('success/', views.SuccessView.as_view(), name="success"),
    path('account/signin',views.SigninView.as_view(),name='signin'),
    path('bikes/add_new-bike',views.Post_BikeView.as_view(),name='post_bikes'),
    path('bikes/details/<int:bike_id>',views.BikeDetailView.as_view(),name='bike_details'),
    path('bikes/make_deal/<int:bike_id>',views.makeoffer,name='make_offer')


]