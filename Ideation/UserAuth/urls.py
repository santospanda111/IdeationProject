from django.urls import path
from UserAuth import views

urlpatterns=[
    path('',views.Index.as_view(),name='homepage'),
    path('/register', views.Register.as_view(), name='user_registration'),
    path('register/<int:pk>/', views.Register.as_view(), name='user_registration'),
]