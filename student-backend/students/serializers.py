from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser, StudentProfile


# --- SIGNUP ---
# Accepts one flat JSON object with both user fields and profile fields.
class StudentSignupSerializer(serializers.ModelSerializer):
    # Profile fields are write_only because they are not columns on CustomUser.
    name = serializers.CharField(max_length=200, write_only=True)
    age = serializers.IntegerField(write_only=True)
    phone_number = serializers.CharField(max_length=15, write_only=True)
    gender = serializers.CharField(max_length=10, write_only=True)
    fathers_name = serializers.CharField(max_length=200, write_only=True)
    course = serializers.CharField(max_length=100, write_only=True)
    branch = serializers.CharField(max_length=100, write_only=True)
    course_year = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "name",
            "age",
            "phone_number",
            "gender",
            "fathers_name",
            "course",
            "branch",
            "course_year",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        # Pull profile fields out of the dict before creating the user.
        profile_data = {
            "name": validated_data.pop("name"),
            "age": validated_data.pop("age"),
            "phone_number": validated_data.pop("phone_number"),
            "gender": validated_data.pop("gender"),
            "fathers_name": validated_data.pop("fathers_name"),
            "course": validated_data.pop("course"),
            "branch": validated_data.pop("branch"),
            "course_year": validated_data.pop("course_year"),
        }

        # create_user hashes the password automatically (never store plain text).
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            is_student=True,
            is_approved=False,
        )

        # Create the linked profile row.
        StudentProfile.objects.create(user=user, **profile_data)

        return user


# --- LOGIN (JWT) ---
# Extends the default JWT login so we can block unapproved students.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # First let the parent class check username/password and build tokens.
        data = super().validate(attrs)

        # self.user is set by the parent after a successful password check.
        user = self.user

        # Students must be approved by an admin before they can log in.
        if user.is_student and not user.is_approved:
            raise serializers.ValidationError(
                "Your account is waiting for admin approval. Please try again later."
            )

        # Send extra info to React so it knows where to redirect after login.
        data["username"] = user.username
        data["is_student"] = user.is_student

        return data


# --- STUDENT PROFILE (read-only GET) ---
# Returns profile fields plus a few useful user fields for the dashboard.
class StudentProfileReadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    is_approved = serializers.BooleanField(source="user.is_approved", read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "username",
            "email",
            "is_approved",
            "name",
            "age",
            "phone_number",
            "gender",
            "fathers_name",
            "course",
            "branch",
            "course_year",
        ]


# --- ADMIN: list / detail view of every student ---
class AdminStudentListSerializer(serializers.ModelSerializer):
    # Pull data from the linked CustomUser row.
    id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    is_approved = serializers.BooleanField(source="user.is_approved", read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "username",
            "email",
            "is_approved",
            "name",
            "age",
            "phone_number",
            "gender",
            "fathers_name",
            "course",
            "branch",
            "course_year",
        ]
