from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class AdminAccount(models.Model):
    username = models.CharField(max_length=150, unique=True, default='admin')
    password = models.CharField(max_length=255, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hash password automatically on save if not already hashed
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username
