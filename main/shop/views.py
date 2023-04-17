from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import *


@permission_classes([AllowAny])
@api_view(['POST'])
def sign_up(request):
    if request.method == 'POST':
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'data': {'user_token': token.key}}, status=201)
        else:
            return JsonResponse({'error': {'code': 422, 'message': 'Validation failed', 'errors': serializer.errors}},
                                status=422)


@permission_classes([AllowAny])
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'],
                                password=serializer.validated_data['password'])
            if not user:
                return JsonResponse({'error': {'code': 401, 'message': 'Authentication failed'}}, status=401)

            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'data': {'user_token': token.key}}, status=200)
        else:
            return JsonResponse({'error': {'code': 422, 'message': 'Validation failed', 'errors': serializer.errors}},
                                status=422)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def logout(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'error': {'code': 403, 'message': 'Login failed'}}, status=403)
        request.user.auth_token.delete()
        return JsonResponse({'data': {'message': 'logout'}})


@permission_classes([AllowAny])
@api_view(['GET'])
def products_get(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse({'data': serializer.data}, status=200)


@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['POST'])
def product_add(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'error': {'code': 403, 'message': 'Ошибка логина'}}, status=403)
        if not request.user.is_staff:
            return JsonResponse({'error': {'code': 403, 'message': 'Запрет доступа'}}, status=403)

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': {'id': serializer.data['id'], 'message': 'Product added'}}, status=201)
        else:
            return JsonResponse(
                {'error': {'code': 422, 'message': 'нарушение правил валидации', 'errors': serializer.errors}},
                status=422)


@permission_classes([IsAuthenticated, IsAdminUser])
@api_view(['GET', 'PATCH', 'DELETE'])
def product_detail(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': {'code': 403, 'message': 'Ошибка логина'}}, status=403)
    if not request.user.is_staff:
        return JsonResponse({'error': {'code': 403, 'message': 'Запрет доступа'}}, status=403)
    try:
        product = Product.objects.get(pk=pk)
    except:
        return JsonResponse({'error': {'code': 404, 'message': 'Не найдено'}}, status=404)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return JsonResponse({'data': serializer.data}, status=200)

    if request.method == 'PATCH':
        serializer = ProductSerializer(data=request.data, instance=product, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'data': serializer.data}, status=200)
        else:
            return JsonResponse(
                {'error': {'code': 422, 'message': 'нарушение правил валидации', 'errors': serializer.errors}},
                status=422)

    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({'data': {'message': 'Product removed'}}, status=200)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def cart_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': {'code': 403, 'message': 'Ошибка логина'}}, status=403)
    if request.user.is_staff:
        return JsonResponse({'error': {'code': 403, 'message': 'Запрет доступа'}}, status=403)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return JsonResponse({'body': serializer.data['products']}, status=200)


@permission_classes([IsAuthenticated])
@api_view(['POST', 'DELETE'])
def add_delete_in_cart(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': {'code': 403, 'message': 'Ошибка логина'}}, status=403)
    if request.user.is_staff:
        return JsonResponse({'error': {'code': 403, 'message': 'Запрет доступа'}}, status=403)

    try:
        product = Product.objects.get(pk=pk)
    except:
        return JsonResponse({'error': {'code': 404, 'message': 'Не найдено'}}, status=404)

    if request.method == 'POST':
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart = cart or _
        cart.products.add(product)
        return JsonResponse({'data': {'message': 'Product add to cart'}}, status=201)

    if request.method == 'DELETE':
        cart = Cart.objects.get(user=request.user)
        cart.products.remove(product)
        return JsonResponse({'data': {'message': 'Product removed from cart'}}, status=201)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def add_view_order(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': {'code': 403, 'message': 'Ошибка логина'}}, status=403)
    if request.user.is_staff:
        return JsonResponse({'error': {'code': 403, 'message': 'Запрет доступа'}}, status=403)

    if request.method == 'GET':
        order = Order.objects.get(user=request.user)
        serializer = OrderSerializer(order)
        return  JsonResponse({'data': serializer.data}, status=200)

    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
        except:
            return JsonResponse({'error': {'code': 422, 'message': 'Cart is empty'}}, status=422)

        order = Order.objects.create(user=request.user)
        for product in cart.products.all():
            order.products.add(product)
        order.save()
        cart.delete()
        serializer = OrderSerializer(order)
        return JsonResponse({'data': {'order_id': serializer.data['id'], 'message': 'Order is processed'}}, status=201)


