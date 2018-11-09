from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^home/', views.home, name="home"),
    url(r'^market/', views.market, name="market"),
    url(r'^marketWithParam/(\d+)/(\d+)/(\d+)', views.marketWithParam, name="marketWithParam"),
    url(r'^cart/', views.cart, name="cart"),
    url(r'^mine/', views.mine, name="mine"),
    url(r'^login/', views.login, name="login"),
    url(r'^logout/', views.logout, name="logout"),
    url(r'^register/', views.register, name="register"),
    url(r'^checkUserUnique/', views.checkUserUnique),  # 检查用户名唯一性的
    url(r'^addToCart/', views.addToCart, name="addToCart"),
    url(r'^subToCart/', views.subToCart, name="subToCart"),
    url(r'^addCart/', views.addCart,name='addCart'),
    url(r'^subCart/', views.subCart, name="subCart"),
    url(r'^chanageSelect/', views.chanageSelect, name="chanageSelect"),
    url(r'^changeManySelect/', views.changeManySelect, name="changeManySelect"),
    url(r'^createOrder/', views.createOrder, name="createOrder"),
    url(r'^orderInfo/(.+)', views.orderInfo, name="orderInfo"),
    url(r'^changeOrderStatu/', views.changeOrderStatu, name="changeOrderStatu"),
    url(r'^totalNumberAndPrice/', views.totalNumberAndPrice, name="totalNumberAndPrice"),
    # 待收货界面
    url(r'^pending_receipt', views.pending_receipt, name="pending_receipt"),

]
