from django.http import HttpResponse
from rest_framework import status
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
import jwt,json
from rest_framework.response import Response
from .models import Dish
from django.core import serializers
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if user:
        payload = {
            'username': username,
        }
        token = jwt.encode(payload, "JWT_SECRET_KEY")
        jwt_token = {'token': token.decode("utf-8")}
        return HttpResponse(
            json.dumps(jwt_token),
            status=200,
            content_type="application/json"
        )
    if not user:
        return Response({'error': 'Invalid Credentials'},
                    status=HTTP_404_NOT_FOUND)

from .serializers import UserSerializer,DishSerializer
from django.contrib.auth.models import User
from django.http import JsonResponse


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_dish(request):
    serialized = DishSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def display_dishes(request):
    dishes = list(Dish.objects.values())
    return JsonResponse(dishes,safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def display_customers(request):
    user = list(User.objects.values())
    return JsonResponse(user,safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def display_particular_customers(request):
    username = request.user.username
    user = User.objects.filter(username=username)
    user_details = serializers.serialize("json",user)
    user = User.objects.get(username=username)
    dish_set = serializers.serialize("json",user.dish_set.all())
    return HttpResponse(user_details+dish_set)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def add_dish(request):
    username = request.user.username
    user = User.objects.get(username=username)
    dish_name = request.data.get("name")
    dish = Dish.objects.get(name=dish_name)
    dish.order = user
    dish.save()
    return Response(status=status.HTTP_202_ACCEPTED,data=serializers.serialize("json",Dish.objects.filter(name=dish_name)))

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_dish(request):
    dish_name = request.data.get("name")
    dish = Dish.objects.get(name=dish_name)
    dish.delete()
    return Response(status=status.HTTP_202_ACCEPTED)
