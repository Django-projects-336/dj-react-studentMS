from django.urls import path

from .views import (
    AdminApproveStudentView,
    AdminDeleteStudentView,
    AdminStudentDetailView,
    AdminStudentListView,
    StudentLoginView,
    StudentProfileView,
    StudentSignupView,
)

# All API routes for the students app live here.
urlpatterns = [
    # Public routes (no JWT required)
    path("signup/", StudentSignupView.as_view(), name="student-signup"),
    path("login/", StudentLoginView.as_view(), name="student-login"),
    # Student route (JWT required)
    path("profile/", StudentProfileView.as_view(), name="student-profile"),
    # Admin routes (JWT required + must be superuser/staff)
    path("admin/students/", AdminStudentListView.as_view(), name="admin-student-list"),
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
    path(
        "admin/students/<int:user_id>/delete/",
        AdminDeleteStudentView.as_view(),
        name="admin-student-delete",
    ),
]
