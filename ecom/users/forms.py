from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import  MaxValueValidator, MinValueValidator, RegexValidator

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]+$',
                message='First Name must contain only alphabets.',
            ),
        ],
    )
    last_name = forms.CharField(
        validators=[
            RegexValidator(
                regex='^[a-zA-Z]+$',
                message='Last Name must contain only alphabets.',
            ),
        ],
    )
    mob_num = forms.IntegerField(
        label='Mobile Number',
        validators=[
            RegexValidator(
                regex='^[0-9]{10}$',
                message='Mobile Number must be a 10-digit numeric value.',
            ),
            MaxValueValidator(9999999999, message='Mobile number must be at most 10 digits.'),
            MinValueValidator(1000000000, message='Enter a valid mobile number with only numeric characters.'),
        ],
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'mob_num', 'password1', 'password2']
