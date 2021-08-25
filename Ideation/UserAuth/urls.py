from django.urls import path
from UserAuth import views

urlpatterns=[
    path('',views.Index.as_view(),name='homepage')
]