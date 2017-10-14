from django import forms
from .models import User
from django.core.exceptions import ObjectDoesNotExist


class LoginForm(forms.Form):
    username = forms.CharField(
            label='Имя пользователя или почта',
            validators=[],
            max_length=255,
            widget=forms.TextInput(
                    attrs={
                        'class': 'form-control'
                    }
            )
    )
    password = forms.CharField(
            label='Пароль',
            widget=forms.PasswordInput(
                    attrs={
                        'class': 'form-control'
                    }
            )
    )


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
        error_messages = {
            # 'username': {
            #     'required': 'Обязательно к заполнению.'
            # },
        }
        help_texts = {
            'password': 'Придумайте сложный пароль, чтобы никто не смог завладеть вашим аккаунтом.'
        }

    def clean_username(self):
        name = self.cleaned_data['username']
        try:
            User.objects.get(username__iexact=name)
        except ObjectDoesNotExist:
            return name
        raise forms.ValidationError('Пользователь с таким именем уже существует.')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email__iexact=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Пользователь с таким адресом электронной почты уже существует.')

    # password check
    def clean_password(self):
        data = self.cleaned_data['password']
        return data

    # def is_valid(self):

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    # Avatar fields:
    avatar = forms.ImageField(
            label='',
            widget=forms.FileInput(
                    attrs={'class': 'file-upload', 'onchange': 'return ValidateAndImageUpload()'}
            )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'second_name', 'last_name',
                  'avatar', 'date_of_birth')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.SelectDateWidget(
                    years=range(1930, 2020),
                    empty_label=("Выберите Год", "Выберите Месяц", "Выберите День"),
                    attrs={'class': 'form-control'}
            ),
        }
