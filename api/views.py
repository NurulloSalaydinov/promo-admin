from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from clients.models import Client, Order
from common.models import Promo, Product

from .serializers import ClientSerializer, ProductSerializer

TOKEN = ""

def client_detail(request, client_id):
    token = request.GET.get('token', None)
    if token == TOKEN:
        try:
            client = Client.objects.get(telegram_id=client_id)
            obj = ClientSerializer(client)
            return JsonResponse({"status": 100, "client": obj.data}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status": 104})
    return JsonResponse({"status": 107})

def register_client(request):
    token = request.GET.get('token', None)
    first_name = request.GET.get('first_name', None)
    last_name = request.GET.get('last_name', None)
    phone = request.GET.get('phone', None)
    telegram_id = request.GET.get('user_id', None)
    username = request.GET.get('username', None)
    if first_name and phone and telegram_id:
        if token == TOKEN:
            try:
                client = Client.objects.get(telegram_id=telegram_id)
                return JsonResponse({"status": 100})
            except Client.DoesNotExist as e:
                client = Client.objects.create(
                    telegram_id=telegram_id,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    username=username
                )
                return JsonResponse({"status": 101})
        return JsonResponse({"status": 107})
    else:
        return JsonResponse({"error": "Invalid data"})


# check user if exists and return user if not exists return False
def get_user(telegram_id):
    try:
        user = Client.objects.get(telegram_id=telegram_id)
        return user
    except Client.DoesNotExist as e:
        return False


def receive_code(request, client_id):
    code = request.GET.get('code', None)
    token = request.GET.get('token', None)
    if code and token == TOKEN:
        try:
            code = Promo.objects.select_related('category').get(promocode=code)
            user = get_user(client_id)
            if user:
                print(user.points)
                user.points += code.category.points
                user.save()
                code.delete()
                print(user.points)
                return JsonResponse({"status": 102, 'points': user.points})
            else:
                return JsonResponse({"status": 108})
        except Promo.DoesNotExist as e:
            print(e)
            return JsonResponse({"status": 104})
    else:
        return JsonResponse({"status": 107})

def products_list(request):
    token = request.GET.get('token', None)
    if token == TOKEN:
        try:
            products = Product.objects.all()
            obj = ProductSerializer(products, many=True)
            return JsonResponse({"status": 102, "products": obj.data}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"status": 104})
    return JsonResponse({"status": 107})


def order_product(request, product_id):
    token = request.GET.get('token', None)
    user_id = request.GET.get('user_id', None)
    if token == TOKEN:
        try:
            product = Product.objects.get(id=product_id)
            user = get_user(user_id)
            if user:
                if user.points >= product.req_points:
                    user.points -= product.req_points
                    user.save()
                    Order.objects.create(client=user, product=product)
                    return JsonResponse({"status": 102, "points": user.points, "product": ProductSerializer(product).data})
                else:
                    return JsonResponse({"status": 103, "points": user.points})
            else:
                return JsonResponse({"status": 108})
        except Product.DoesNotExist as e:
            print(e)
            return JsonResponse({"status": 104})
    return JsonResponse({"status": 107, "msg": "Unauthorized"})

# 100 -> already exist
# 101 -> created
# 107 > unauthorized
# 104 -> does not exist
# 102 -> success
# 103 -> point is not enough
# 108 -> client unauthorized
