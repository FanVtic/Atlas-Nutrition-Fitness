from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    height_feet = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Feet'}),
        validators=[MinValueValidator(0)],
        required=False
    )
    height_inches = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Inches'}),
        validators=[MinValueValidator(0), MaxValueValidator(11)],
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['height_feet', 'height_inches', 'weight_lbs', 'fitness_goal', 'target_weight_lbs', 'daily_calorie_goal']
        widgets = {
            'weight_lbs': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Weight in lbs'}),
            'fitness_goal': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', 'Select a goal'),
                ('weight_loss', 'Weight Loss'),
                ('muscle_gain', 'Muscle Gain'),
                ('maintenance', 'Maintenance'),
                ('endurance', 'Endurance'),
            ]),
            'target_weight_lbs': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target weight in lbs'}),
            'daily_calorie_goal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Daily calorie goal'}),
        } 