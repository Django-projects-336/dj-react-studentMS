from django.urls import path

from .views import (
    AdminApproveStudentView,
    AdminStudentDetailView,
    AdminStudentListCreateView,
    StudentLoginView,
    StudentProfileView,
    StudentSignupView,
)

urlpatterns = [
    path("signup/", StudentSignupView.as_view(), name="student-signup"),
    path("login/", StudentLoginView.as_view(), name="student-login"),
    path("profile/", StudentProfileView.as_view(), name="student-profile"),
    # Admin CRUD: GET+POST on collection, GET+PUT+PATCH+DELETE on one student
    path(
        "admin/students/",
        AdminStudentListCreateView.as_view(),
        name="admin-student-list-create",
    ),
    path(
        "admin/students/<int:user_id>/",
        AdminStudentDetailView.as_view(),
        name="admin-student-detail",
    ),
    path(
        "admin/students/<int:user_id>/approve/",
        AdminApproveStudentView.as_view(),
        name="admin-student-approve",
    ),
]
