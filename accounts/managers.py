from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, Login_id, password=None, **extra_fields):
        if not Login_id:
            raise ValueError('The Login_id field must be set')
        user = self.model(Login_id=Login_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Login_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(Login_id, password, **extra_fields)
    
        