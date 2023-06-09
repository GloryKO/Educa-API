from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self,name,email,password,**extra_fields):
        if not email :
            raise ValueError(_("Email is required"))
        if not name:
            raise ValueError(_("Name is required"))
        email = self.normalize_email(email)
        user = self.model(name=name,email=email,**extra_fields)
        user.set_password(password)
        user.save()

        return user 
    
    def create_superuser(self,name,email,password,**extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(name,email, password, **extra_fields)