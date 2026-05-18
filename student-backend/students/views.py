from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser, StudentProfile
from .serializers import (
    AdminStudentListSerializer,
    CustomTokenObtainPairSerializer,
    StudentProfileReadSerializer,
    StudentSignupSerializer,
)


# --- PUBLIC: Student signup ---
# Anyone can POST here to register. Account starts unapproved.
class StudentSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = StudentSignupSerializer
    permission_classes = [AllowAny]


# --- PUBLIC: Login (returns access + refresh JWT tokens) ---
class StudentLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


# --- PROTECTED: Logged-in student reads their own profile (GET only) ---
class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Only student accounts have a profile endpoint.
        if not user.is_student:
            return Response(
                {"detail": "Only students can view this profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Every approved student should have a profile row from signup.
        try:
            profile = user.student_profile
        except StudentProfile.DoesNotExist:
            return Response(
                {"detail": "Student profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StudentProfileReadSerializer(profile)
        return Response(serializer.data)


# --- PROTECTED: Admin lists all students ---
class AdminStudentListView(generics.ListAPIView):
    serializer_class = AdminStudentListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Return profiles only for accounts marked as students.
        return StudentProfile.objects.filter(user__is_student=True)


# --- PROTECTED: Admin sees one student by user id ---
class AdminStudentDetailView(generics.RetrieveAPIView):
    serializer_class = AdminStudentListSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "user_id"

    def get_queryset(self):
        return StudentProfile.objects.filter(user__is_student=True)


# --- PROTECTED: Admin approves a pending student ---
class AdminApproveStudentView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id, is_student=True)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Student not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        user.is_approved = True
        user.save()

        return Response({"detail": "Student approved successfully."})


# --- PROTECTED: Admin deletes a student account ---
class AdminDeleteStudentView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id, is_student=True)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "Student not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Deleting the user also deletes the profile (CASCADE on OneToOne).
        user.delete()

        return Response(
            {"detail": "Student deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
