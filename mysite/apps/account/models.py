from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.validators import RegexValidator


# directory for avatars
def avatar_directory_path(instance, filename):
    filename = 'photo.' + filename.split('.')[-1]
    return f'avatars/{instance.id}/{filename}'


# username validator
class UsernameValidator(RegexValidator):
    regex = r'^[a-zA-Z][a-zA-Z0-9]{3,60}$'
    message = 'Имя пользователя должно состоять только из букв латинского алфавита и цифр.' \
              ' Длина должна состовлять 4-60 символов.' \
              ' Начинаться должно с буквы.'
    code = 'valid_error'
    flags = 32 # Unicode


class FIOValidator(RegexValidator):
    regex = r'^[a-zA-Zа-яА-ЯёЁ]{2,50}$'
    message = 'Данные должны состоять только из букв латинского и русского алфавитов.' \
              ' Длина должна состовлять 2-50 символов.'
    code = 'valid_error'
    flags = 32


username_validator = UsernameValidator()
fio_validator = FIOValidator()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# ---------------------------
# пользователь              -
# ---------------------------
class User(AbstractBaseUser, PermissionsMixin):
    # main attributes
    username = models.CharField(
            verbose_name='Имя пользователя',
            max_length=60,
            unique=True,
            help_text='Имя, которое будет отображаться для всех пользователей.',
            validators=[username_validator],
            error_messages={
                'unique': 'Пользователь с таким именем уже существует.',
                'invalid': 'Некорректное имя пользователя.',
                'blank': 'Обязательно к заполнению.',
                'null': 'Обязательно к заполнению.',
                'required': 'Обязательно к заполнению.',
            }
    )
    email = models.EmailField(
            verbose_name='Адрес электронной почты',
            max_length=255,
            unique=True,
            help_text='На почту приходит подтверждение и различная важная информация.',
            error_messages={
                'unique': 'Данная почта уже используется.',
            }
    )
    email_confirmed = models.BooleanField(default=False)
    # lite profile
    first_name = models.CharField(
            verbose_name='Имя',
            max_length=50,
            blank=True,
            help_text='Можно как в паспорте.',
            validators=[fio_validator]
    )
    second_name = models.CharField(
            verbose_name='Отчество',
            max_length=50,
            blank=True,
            help_text='Можно как в паспорте.',
            validators=[fio_validator]
    )
    last_name = models.CharField(
            verbose_name='Фамилия',
            max_length=50,
            blank=True,
            help_text='Можно как в паспорте.',
            validators=[fio_validator]
    )
    avatar = models.ImageField(
            upload_to=avatar_directory_path,
            verbose_name='Аватар',
            default='avatars/no-avatar.svg',
            help_text='Графическое представление пользователя.',
    )
    date_of_birth = models.DateField(
            verbose_name='Дата рождения',
            null=True,
            help_text='Дата рождения пользователя.',
    )
    # edu profile
    experience = models.IntegerField(
            verbose_name='Опыт',
            default=0,
            help_text='Опыт пользователя.',
    )
    # admin profile
    is_staff = models.BooleanField(verbose_name='staff status', default=False)
    is_active = models.BooleanField(verbose_name='active', default=True)
    date_joined = models.DateTimeField(verbose_name='date joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        app_label = 'account'

    def clean(self):
        pass

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f'{self.last_name} {self.first_name} {self.second_name}'
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        short_name = f'{self.first_name} {self.second_name}'
        return short_name.strip()

    def show_name(self):
        if self.first_name and self.last_name and self.second_name:
            return self.get_full_name()
        else:
            return self.username

    def __str__(self):
        return self.username

