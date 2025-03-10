from django.urls import path
from .views import (
    ConsultationCreateView,
    DoctorsInClinicsAPIView,
    ConsultationListForDoctorsView,
    ConsultationUpdateView,
    ConsultationChangeStatusView,
    ConsultationDetailView,
    ConsultationDeleteView

)

urlpatterns = [
    path('consultations/create/',
         ConsultationCreateView.as_view(),
         name='consultation_create'
         ),
    path('consultations/',
         ConsultationListForDoctorsView.as_view(),
         name='consultation_list'
         ),
    path('consultations/<int:id>',
         ConsultationDetailView.as_view(),
         name='consultation_detail'
         ),

    path('consultations/update/<int:id>',
         ConsultationUpdateView.as_view(),
         name='consultation_update_data'
         ),
    path('consultations/<int:id>/change-status',
         ConsultationChangeStatusView.as_view(),
         name='consultation_change_status'
         ),

    path('consultations/<int:id>/delete',
         ConsultationDeleteView.as_view(),
         name='consultation_delete'
         ),
    path('doctors/',
         DoctorsInClinicsAPIView.as_view(),
         name='list_doctors_in_clinics'
         ),
]
