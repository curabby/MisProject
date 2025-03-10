from django.urls import path
from .views import (
    RegisterDoctorView,
    RegisterPatientView,
    CustomTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path(
        'register/patient/',
        RegisterPatientView.as_view(),
        name='register_patient'
    ),
    path(
        'register/doctor/',
        RegisterDoctorView.as_view(),
        name='register_doctor'
    ),
    path(
        'login/',
        CustomTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'logout/',
        TokenBlacklistView.as_view(),
        name='token_blacklist'
    ),
]
