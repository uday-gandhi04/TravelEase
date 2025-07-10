from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile, Booking, TravelOption


class CustomUserCreationForm(UserCreationForm):
    email         = forms.EmailField(required=True)
    first_name    = forms.CharField(required=True)
    last_name     = forms.CharField(required=True)
    phone_number  = forms.CharField(required=False)
    address       = forms.CharField(widget=forms.Textarea, required=False)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model  = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email      = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name  = self.cleaned_data["last_name"]
        if commit:
            user.save()
            # Create associated UserProfile
            UserProfile.objects.create(
                user           = user,
                phone_number   = self.cleaned_data.get("phone_number", ""),
                address        = self.cleaned_data.get("address", ""),
                date_of_birth  = self.cleaned_data.get("date_of_birth", None),
            )
        return user


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial  = user.last_name
            self.fields["email"].initial      = user.email

    # Expose the User fields alongside the profile fields
    first_name = forms.CharField(required=True)
    last_name  = forms.CharField(required=True)
    email      = forms.EmailField(required=True)

    class Meta:
        model  = UserProfile
        fields = ["phone_number", "address", "date_of_birth"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            # pre-fill the user fields
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial  = user.last_name
            self.fields["email"].initial      = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user    = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name  = self.cleaned_data["last_name"]
        user.email      = self.cleaned_data["email"]
        if commit:
            user.save()
            profile.save()
        return profile


class UserForm(forms.ModelForm):
    """If you still use a separate UserForm in your function‑based view."""
    class Meta:
        model  = User
        fields = ["first_name", "last_name", "email"]


class UserProfileForm(forms.ModelForm):
    """If you still use a separate UserProfileForm in your function‑based view."""
    class Meta:
        model  = UserProfile
        fields = ["phone_number", "address", "date_of_birth"]


class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ["seats"]
        widgets = {
            "seats": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter number of seats",
                    "min": 1,
                }
            )
        }

    def clean_seats(self):
        seats = self.cleaned_data.get("seats", 0)
        if seats <= 0:
            raise ValidationError("Number of seats must be a positive integer.")
        return seats


class TravelOptionForm(forms.ModelForm):
    class Meta:
        model  = TravelOption
        # adjust 'departure_datetime' to match your model field
        fields = [
            "travel_id",
            "type",
            "source",
            "destination",
            "departure_datetime",
            "price",
            "available_seats",
        ]
        widgets = {
            "type": forms.Select(attrs={"class": "form-select"}),
            "source": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Source"}
            ),
            "destination": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Destination"}
            ),
            "departure_datetime": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "YYYY-MM-DD HH:MM",
                    "type": "datetime-local",
                }
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Price"}
            ),
            "available_seats": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Available Seats", "min": 0}
            ),
        }

    def clean_departure_datetime(self):
        dt = self.cleaned_data.get("departure_datetime")
        if dt and dt < timezone.now():
            raise ValidationError("Departure date cannot be in the past.")
        return dt
