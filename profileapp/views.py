from django.shortcuts import render
from .models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import UserSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "User registered successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED
        )

    return Response(
        {"message": "Registration failed", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST
    )
@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # check email exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {"message": "Email does not exist"},
            status=status.HTTP_400_BAD_REQUEST
        )

    #  password validation
    if not check_password(password, user.password):
        return Response(
            {"message": "Invalid email or password"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # return user data
    user_data = UserSerializer(user).data

    return Response(
        {
            "message": "Login successful",
            "user": user_data
        },
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    serializer = UserSerializer(user)
    return Response({"profile": serializer.data}, status=200)

@api_view(['PUT'])
def update_profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    data = request.data.copy()

    #  not allow email updates
    if 'email' in data:
        data.pop('email')

    # If password updated (hash it)
    if 'password' in data and data['password'] != "":
        data['password'] = make_password(data['password'])
    else:
        data.pop('password', None)  # old password

    serializer = UserSerializer(user, data=data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Profile updated", "profile": serializer.data}, status=200)

    return Response({"errors": serializer.errors}, status=400)
@api_view(['PATCH'])
def update_profile_image(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=404)

    if 'profile_image' not in request.FILES:
        return Response({"message": "No image uploaded"}, status=400)

    user.profile_image = request.FILES['profile_image']
    user.save()

    return Response({"message": "Profile image updated"}, status=200)
@api_view(['POST'])
def logout_user(request):
    request.session.flush()
    return Response({"message": "Logged out successfully"}, status=200)
