from django.contrib.auth.models import AbstractUser
from django.db import models


# CustomUser replaces Django's default User table.
# We add two extra flags so we know who is a student and whether admin approved them.
class CustomUser(AbstractUser):
    # True when this account signed up as a student (not an admin).
    is_student = models.BooleanField(default=False)

    # False until a superuser clicks "Approve" in the admin dashboard.
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        # Show username in the Django admin list and shell.
        return self.username


# StudentProfile stores the extra details that are NOT part of the login account.
# Each student has exactly one profile, linked with a OneToOne relationship.
class StudentProfile(models.Model):
    # Link this profile row to one CustomUser row.
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=15)

    # Gender choices: M = Male, F = Female, O = Other
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    fathers_name = models.CharField(max_length=200)
    course = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)

    # Which year of the course the student is in (1st through 4th).
    YEAR_CHOICES = [
        ("1st", "First"),
        ("2nd", "Second"),
        ("3rd", "Third"),
        ("4th", "Fourth"),
    ]
    course_year = models.CharField(max_length=10, choices=YEAR_CHOICES)

    def __str__(self):
        return f"Profile for {self.user.username}"
