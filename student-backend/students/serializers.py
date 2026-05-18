from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser, StudentProfile


# --- SIGNUP (public) ---
# Accepts one flat JSON object with both user fields and profile fields.
class StudentSignupSerializer(serializers.ModelSerializer):
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

        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            is_student=True,
            is_approved=False,
        )

        StudentProfile.objects.create(user=user, **profile_data)
        return user


# --- LOGIN (JWT) ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if user.is_student and not user.is_approved:
            raise serializers.ValidationError(
                "Your account is waiting for admin approval. Please try again later."
            )

        data["username"] = user.username
        data["is_student"] = user.is_student
        return data


# --- STUDENT PROFILE (read-only GET) ---
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


# --- ADMIN: read one student or list all students ---
class AdminStudentListSerializer(serializers.ModelSerializer):
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


# --- ADMIN: create a new student (POST) ---
class AdminStudentCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    is_approved = serializers.BooleanField(default=True)

    name = serializers.CharField(max_length=200)
    age = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=15)
    gender = serializers.CharField(max_length=10)
    fathers_name = serializers.CharField(max_length=200)
    course = serializers.CharField(max_length=100)
    branch = serializers.CharField(max_length=100)
    course_year = serializers.CharField(max_length=10)

    def create(self, validated_data):
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

        is_approved = validated_data.pop("is_approved")

        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            is_student=True,
            is_approved=is_approved,
        )

        profile = StudentProfile.objects.create(user=user, **profile_data)
        return profile


# --- ADMIN: update an existing student (PUT / PATCH) ---
class AdminStudentUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    is_approved = serializers.BooleanField()

    name = serializers.CharField(max_length=200)
    age = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=15)
    gender = serializers.CharField(max_length=10)
    fathers_name = serializers.CharField(max_length=200)
    course = serializers.CharField(max_length=100)
    branch = serializers.CharField(max_length=100)
    course_year = serializers.CharField(max_length=10)

    def update(self, instance, validated_data):
        # instance is a StudentProfile object
        user = instance.user

        user.username = validated_data.get("username", user.username)
        user.email = validated_data.get("email", user.email)
        user.is_approved = validated_data.get("is_approved", user.is_approved)

        # Only change password if admin typed a new one
        new_password = validated_data.get("password")
        if new_password:
            user.set_password(new_password)

        user.save()

        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.gender = validated_data.get("gender", instance.gender)
        instance.fathers_name = validated_data.get(
            "fathers_name", instance.fathers_name
        )
        instance.course = validated_data.get("course", instance.course)
        instance.branch = validated_data.get("branch", instance.branch)
        instance.course_year = validated_data.get(
            "course_year", instance.course_year
        )
        instance.save()

        return instance
