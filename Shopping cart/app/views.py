import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

# home 主页
from django.urls import reverse

from app.models import Wheel, Nav, Mustbuy, Shop, Mainshow, Foodtype, goods, User, CartModel, OrderModel, OrderAndGoods


def home(request):
    # 查询主页顶部轮播图的全部数据
    wheels = Wheel.objects.all()

    # 查询主页nav的全部数据
    navs = Nav.objects.all()

    # 查询主页mustbuy的全部数据
    mustbuys = Mustbuy.objects.all()

    # 查询主页shop的全部数据
    shops = Shop.objects.all()
    # 拆分shops数据
    shops1 = shops[0]
    shops2_3 = shops[1:3]
    shops4_7 = shops[3:7]
    shops8 = shops[7:]

    mainShows = Mainshow.objects.all()

    data = {
        'title': '主页',
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shops1': shops1,
        'shops2_3': shops2_3,
        'shops4_7': shops4_7,
        'shops8': shops8,
        'mainShows': mainShows,
    }
    return render(request, 'home/home.html', context=data)


def market(request):
    # 查询所有的商品类型信息
    # foodtypes = FoodType.objects.all().order_by("typesort")
    # # 查询所有的商品数据
    # goodses =  goods.objects.all()
    #
    # data = {
    #     "title": "闪购",
    #     'foodtypes':foodtypes,
    #     'goodses':goodses,
    # }
    #
    # return  render(request,'market/market.html',context=data)
    # 默认104749表示显示热销榜   0 默认是全部分类    0默认是综合排序
    return redirect(reverse('axf:marketWithParam', args=(104749, 0, 0)))


# market 闪购 带参数的
# typeid 商品分类id
def marketWithParam(request, typeid, childid, sortType):
    # 查询所有的商品类型信息
    foodtypes = Foodtype.objects.all().order_by('typesort')

    # 查询所有的商品类型
    # 根据商品类型来查询数据
    goodses = goods.objects.filter(categoryid=typeid)
    if not str(childid) == '0':
        goodses = goodses.filter(childcid=childid)

    # 在原有的查询结果上排序
    sortType = str(sortType)
    if sortType == "0":  # 综合排序
        pass
    elif sortType == "1":  # 销量排序
        goodses = goodses.order_by("productnum")
    elif sortType == "2":  # 价格降序
        goodses = goodses.order_by("-price")
    elif sortType == "3":  # 价格升序
        goodses = goodses.order_by("price")
    # 根据类型查询除所有的子分类信息
    foodType = Foodtype.objects.filter(typeid=typeid).first()
    # foodType = Foodtype()
    childtypenames = foodType.childtypenames.split('#')
    allChild = []
    for child in childtypenames:
        allChild.append(child.split(':'))
    print(allChild)

    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goodses': goodses,
        "currentType": typeid,
        'allChild': allChild,
        'childid': int(childid),
    }

    # 加载用户商品数量
    userid = request.session.get('user_id')
    user = User.objects.filter(pk=userid)
    if userid:
        cartes = CartModel.objects.filter(c_user=user).all()
        data['cartes']=cartes

    return render(request, 'market/market.html', context=data)


# mine 我的
def mine(request):
    # 判断是否登录
    userid = request.session.get('user_id')
    print(userid)
    if userid:  # 登录
        user = User.objects.filter(pk=userid).first()
        imgUrl = '/static/upload/' + user.u_img.url
        print(imgUrl)
        # user = User()
        # 获取各种状态的订单数量
        # 查出该用户下的所有订单
        objects = user.ordermodel_set
        nopay = objects.filter(o_status=1).count()  # 待付款
        noCollect = objects.filter(o_status=2).count()  # 待收货
        noEvaluate = objects.filter(o_status=3).count()  # 待评价
        returnGoods = objects.filter(o_status=4).count()  # 退款/退货
        # 注意如果没有获取到值,count为 0

        data = {
            'title': '我的',
            "user": user,
            "imgUrl": imgUrl,
            "nopay": nopay,
            "noCollect": noCollect,
            "noEvaluate": noEvaluate,
            "returnGoods": returnGoods,
        }
        return render(request, 'mine/mine.html', context=data)
    else:  # 没有登录
        return render(request, 'mine/mine.html', context={'user': None})


# 注册
def register(request):
    if request.method == 'GET':  # 展示注册页面
        return render(request, 'user/user_register.html')
    elif request.method == 'POST':
        # 获取信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        img = request.FILES.get('img')

        # 保存数据
        user = User()
        user.u_name = username
        user.u_password = password
        user.u_mail = email
        user.u_img = img

        user.save()

        return redirect(reverse('axf:login'))


# 检查用户名的唯一性
def checkUserUnique(request):
    username = request.GET.get('username')
    resQuery = User.objects.filter(u_name=username)
    data = {}
    if resQuery.exists():  # 是否存在
        data['usernamecode'] = 800  # 表示用户已经存在
        data['usernamemsg'] = '该用户已经存在'
    else:
        data['usernamecode'] = 888  # 表示用户名可用
        data['usernamemsg'] = '用户名可用'

    email = request.GET.get('email')
    resQuery1 = User.objects.filter(u_mail=email)
    if resQuery1.exists():  # 是否存在
        data['emailcode'] = 800  # 表示用户已经存在
        data['emailmsg'] = '该邮箱已经存在'
    else:
        data['emailcode'] = 888  # 表示用户名可用
        data['emailmsg'] = '邮箱可用'

    return JsonResponse(data)


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        resQu = User.objects.filter(u_name=username)
        if resQu.exists():  # 用户存在
            user = resQu.first()

            # 验证密码
            if password == user.u_password:  # 验证密码
                request.session['user_id'] = user.id

                return redirect(reverse('axf:mine'))
    # 登录失败
    return redirect(reverse('axf:login'))


# 注销
def logout(request):
    # 清除session
    request.session.flush()

    return redirect(reverse("axf:login"))


# cart 购物车
def cart(request):
    # 先判断是否登录了
    userid = request.session.get('user_id')
    if userid:
        user = User.objects.filter(pk=userid).first()
        carts = CartModel.objects.filter(c_user=user)

        totalNumberPrice = totalNumberAndPrice(user)

        # 订单是否全部选中
        isAllSelect = True
        for cart in carts:
            if not cart.c_isselect:
                isAllSelect = False

        data = {
            'title': '购物车',
            'u_name':user.u_name,
            'carts': carts,
            'is_allselect': isAllSelect,
            'selectCount': totalNumberPrice.get('selectCount'),
            'totalPrice': totalNumberPrice.get('totalPrice'),
        }
        return render(request, 'cart/cart.html', context=data)
    return redirect(reverse('axf:login'))


# 将数据添加到购物车
def addToCart(request):
    user_id = request.session.get('user_id')
    data = {}
    if user_id:
        user = User.objects.filter(pk=user_id).first()
    else:  # 未登录
        # 在ajax请求中,不能进行重定向
        # return redirect('axf:login')
        data['code'] = 302
        data['msg'] = '未登录,需要重新登录'
        return JsonResponse(data)

    # 获得商品id
    goodsid = request.GET.get('goodsid')
    goodses = goods.objects.filter(pk=goodsid).first()

    # 根据用户来查数据,然后再过滤该商品的购物车数据
    cartRes = CartModel.objects.filter(c_user=user).filter(c_goods=goodses)

    if cartRes.exists():  # 找到购物车记录
        cart = cartRes.first()

        cart.c_num += 1
        cart.save()
        data['code'] = 200
        data['msg'] = '加入购物车成功'
        data['num'] = cart.c_num
    else:  # 没有购物车
        # 创建一个新的购物车
        cart = CartModel()
        cart.c_user = user
        cart.c_goods = goodses
        cart.c_num = 1
        cart.c_isselect = True
        cart.save()
        data['code'] = 200
        data['msg'] = '加入购物车成功'
        data['num'] = 1
    return JsonResponse(data)


# 将购物车中商品数量 减一个
def subToCart(request):
    user_id = request.session.get('user_id')
    data = {}
    if user_id:
        user = User.objects.filter(pk=user_id).first()
    else:  # 未登录
        data['code'] = 302
        data['msg'] = '未登录,需要重新登录'
        return JsonResponse(data)

    # 获得商品id
    goodsid = request.GET.get('goodsid')
    goodses = goods.objects.filter(pk=goodsid).first()

    # 根据用户来查数据,然后再过滤该商品的购物车数据
    cartRes = CartModel.objects.filter(c_user=user).filter(c_goods=goodses)

    if cartRes.exists():  # 找到购物车记录
        cart = cartRes.first()

        if cart.c_num == 1:
            cart.delete()
            data['code'] = 200
            data['msg'] = '操作成功'
            data['num'] = cart.c_num
        else:  # 大于1
            cart.c_num -= 1
            cart.save()
            data['code'] = 200
            data['msg'] = '操作成功'
            data['num'] = cart.c_num
    else:
        data['code'] = 200
        data['msg'] = '操作成功'
        data['num'] = 0

    return JsonResponse(data)


# 修改购物车中商品的数量 +
def addCart(request):
    # 获取cartid
    cartid = request.GET.get('cartid')
    cart = CartModel.objects.filter(pk=cartid).first()
    # cart = CartModel()
    cart.c_num += 1
    cart.save()
    data = {}
    data['code'] = 200  # 添加成功
    data['msg'] = '数量增加成功'
    data['num'] = cart.c_num

    # 计算总数量和价格
    user_id = request.session.get('user_id')
    user = User.objects.filter(pk=user_id).first()
    totalNumberPrice = totalNumberAndPrice(user)
    data['selectCount'] = totalNumberPrice.get('selectCount')
    data['totalPrice'] = totalNumberPrice.get('totalPrice')

    return JsonResponse(data)


# 修改购物车中商品的数量 -
def subCart(request):
    cartid = request.GET.get('cartid')
    cart = CartModel.objects.filter(pk=cartid).first()
    # cart = CartModel()
    data = {}
    if cart.c_num == 1:
        cart.delete()
        data['code'] = 300  # 商品数量为0,应该移除该cart记录
        data['msg'] = '移除该购物车记录'
    elif cart.c_num > 1:
        cart.c_num -= 1
        cart.save()
        data['code'] = 200
        data['msg'] = '数量减少成功'
        data['num'] = cart.c_num

    # 计算总数量和价格
    user_id = request.session.get('user_id')
    user = User.objects.filter(pk=user_id).first()
    totalNumberPrice = totalNumberAndPrice(user)
    data['selectCount'] = totalNumberPrice.get('selectCount')
    data['totalPrice'] = totalNumberPrice.get('totalPrice')

    return JsonResponse(data)


# 改变购物车中商品的选中状态
def chanageSelect(request):
    # 获取购物车id
    cartid = request.GET.get('cartid')
    # 根据购物车id查询出cart 购物车记录
    cart = CartModel.objects.filter(pk=cartid).first()
    # 修改购物车的状态
    cart.c_isselect = not cart.c_isselect
    cart.save()

    # 是否全选
    user_id = request.session.get('user_id')
    user = User.objects.filter(pk=user_id).first()
    # 获得该用户下的所有的购物车数据
    carts = CartModel.objects.filter(c_user=user)

    isAllSelect = True
    for cart1 in carts:
        if not cart1.c_isselect:
            isAllSelect = False
            break
    data = {
        'code': 200,  # 状态码,修改成功
        'msg': '修改成功',
        'isselect': cart.c_isselect,
        'isAllSelect': isAllSelect,
    }
    # 计算总数量和价格
    totalNumberPrice = totalNumberAndPrice(user)
    data['selectCount'] = totalNumberPrice.get('selectCount')
    data['totalPrice'] = totalNumberPrice.get('totalPrice')
    return JsonResponse(data)


# 改变多条数据的选中状态
def changeManySelect(request):
    # 查询出多条cart记录
    cartidList = request.GET.get('cartidList').split('#')
    flag = request.GET.get('flag')

    data = {}
    for cartid in cartidList:
        cart = CartModel.objects.filter(pk=cartid).first()
        if flag == '1':
            cart.c_isselect = True
            data['msg'] = '全部变为选中'
        elif flag == '2':
            cart.c_isselect = False
            data['msg'] = '全部变为未选中'

        cart.save()

    data['code'] = 200
    # 计算总数量和价格
    user_id = request.session.get('user_id')
    user = User.objects.filter(pk=user_id).first()
    totalNumberPrice = totalNumberAndPrice(user)
    data['selectCount'] = totalNumberPrice.get('selectCount')
    data['totalPrice'] = totalNumberPrice.get('totalPrice')
    return JsonResponse(data)


# 计算选中的数量及总价
def totalNumberAndPrice(user):
    # 获取该用户所有的订单
    cartsSelect = CartModel.objects.filter(c_user=user).filter(c_isselect=True)
    # 计算选中的数量
    selectCount = 0
    totalPrice = 0
    for cart in cartsSelect:
        goods = cart.c_goods
        totalPrice += goods.price * cart.c_num
        selectCount += cart.c_num
    # 保留两位小数
    totalPrice = round(totalPrice,2)

    data = {
        'selectCount': selectCount,
        'totalPrice': totalPrice,
    }

    return data


# 生成一个订单
def createOrder(request):
    user_id = request.session.get('user_id')
    user = User.objects.filter(pk=user_id).first()

    # 创建一个订单
    order = OrderModel()
    # 订单号
    order.o_number = str(uuid.uuid4())
    order.o_user = user  # 绑定
    order.o_status = 1  # 未付款状态
    order.save()

    # 创建多个订单商品关系
    # 获得购物车中选中的商品
    cartids = request.GET.get('selectList').split('#')
    for cartid in cartids:
        cart = CartModel.objects.filter(pk=cartid).first()
        orderAndGoods = OrderAndGoods()
        orderAndGoods.o_number = order  # 绑定订单对象
        orderAndGoods.o_goods = cart.c_goods  # 绑定商品对象
        orderAndGoods.o_count = cart.c_num  # 绑定商品数量
        orderAndGoods.save()

        # 同时删除购物车中的对应的记录
        cart.delete()
    data = {
        'code': 200,
        'orderNumber': order.o_number,
    }
    return JsonResponse(data)


# 展示当前订单信息
def orderInfo(request, orderNumber):
    # 获取到订单号
    print(orderNumber)
    # 根据订单号查询出对应的商品
    order = OrderModel.objects.filter(o_number=orderNumber).first()
    # order = OrderModel()
    # 获取该订单下的所有的商品
    orderAndGoodses = order.orderandgoods_set.all()
    data = {
        'orderNumber': orderNumber,
        'orderAndGoodses': orderAndGoodses,
    }

    return render(request, 'cart/orderInfo.html', context=data)


# 改变订单状态
def changeOrderStatu(request):
    # 获取订单号
    ordernumber = request.GET.get('ordernumber')
    status = request.GET.get('status')

    order = OrderModel.objects.filter(o_number=ordernumber).first()

    order.o_status = status
    order.save()
    data = {
        'code': 200,
    }
    return JsonResponse(data)


# 待收货
def pending_receipt(request):
    user_id = request.session.get('user_id')
    user = User.objects.filter(pk=user_id).first()
    print(user.u_name)
    orders = OrderModel.objects.filter(o_user=user)
    print(orders)
    # orderNumberlist = []
    orderAndGoodses = []
    for order in orders:
        print(order)
        if str(order.o_status) == '2':
            orderAndGoods = OrderAndGoods.objects.filter(o_number=order).all()
            orderAndGoodses.append(orderAndGoods)
            # orderNumberlist.append(order.o_number)
        else:
            orderAndGoodses=None
    # print(orderNumberlist)
    print(orderAndGoodses)
    data={
        'orderAndGoodses':orderAndGoodses,
        # 'orderNumberlist':orderNumberlist,
    }
    return render(request,'mine/pending_receipt.html',context=data)




































