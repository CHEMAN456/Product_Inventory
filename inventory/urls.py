from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import home_view,index_view,create_product,product_list,create_transaction,inventory_status,transaction_list,ProductViewSet,TransactionViewSet


app_name = 'inventory'

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'transactions', TransactionViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('inventory:index')),   
    path('home/', home_view, name='home'),
    path('index/', index_view, name='index'),
    path('home/add_product/',create_product , name='add_product'),
    path('home/product_list/',product_list , name='prod_list'),
    path('home/create_transaction/',create_transaction, name='create_transaction'),
    path('home/inventory/',inventory_status , name='inventory_list'),
    path('home/transaction/',transaction_list , name='trans_list'),
    path('api/', include(router.urls)),
       
]