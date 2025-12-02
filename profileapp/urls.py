from django.urls import path
from .views import register_user,login_user, get_profile,update_profile,update_profile_image,logout_user

urlpatterns = [
    path('register/', register_user),
     path('login/', login_user),
     path('profile/<int:user_id>/', get_profile),
    path('profile/update/<int:user_id>/', update_profile),
    path('profile/update-image/<int:user_id>/', update_profile_image),
    path('logout/', logout_user)
]
