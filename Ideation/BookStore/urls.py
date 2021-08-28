from django.urls import path
from BookStore import views
urlpatterns= [
    path('addbooks',views.AddBooks.as_view(),name='addbooks'),
    path('getbooks',views.GetBooks.as_view(),name='getbooks'),
    path('cart',views.AddToCart.as_view(),name='cart'),
    path('searchbooks',views.SearchBook.as_view(),name='search_books'),
    path('order',views.OrderPlace.as_view(),name='order')
]