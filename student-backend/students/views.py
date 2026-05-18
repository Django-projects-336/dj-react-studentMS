from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser, StudentProfile
from .serializers import (
    AdminStudentCreateSerializer,
    AdminStudentListSerializer,
    AdminStudentUpdateSerializer,
    CustomTokenObtainPairSerializer,
    StudentProfileReadSerializer,
    StudentSignupSerializer,
)


# --- PUBLIC: Student signup ---
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

        if not user.is_student:
            return Response(
                {"detail": "Only students can view this profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            profile = user.student_profile
        except StudentProfile.DoesNotExist:
            return Response(
                {"detail": "Student profile not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = StudentProfileReadSerializer(profile)
        return Response(serializer.data)


# --- ADMIN CRUD: List (GET) and Create (POST) ---
class AdminStudentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return StudentProfile.objects.filter(user__is_student=True)

    def get_serializer_class(self):
        # POST uses create serializer; GET uses read serializer
        if self.request.method == "POST":
            return AdminStudentCreateSerializer
        return AdminStudentListSerializer


# --- ADMIN CRUD: Read (GET), Update (PUT/PATCH), Delete (DELETE) ---
class AdminStudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    lookup_field = "user_id"
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        return StudentProfile.objects.filter(user__is_student=True)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return AdminStudentUpdateSerializer
        return AdminStudentListSerializer

    # After update, return the full student data using the read serializer
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        read_serializer = AdminStudentListSerializer(instance)
        return Response(read_serializer.data)


# --- ADMIN: Quick approve button (still handy for the dashboard) ---
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
