# Manually created

from __future__ import unicode_literals
from django.db import migrations, models
import datetime
from django.contrib.auth.hashers import make_password

def init_admin_account_default(apps, schema_editor):
    Branch = apps.get_model("shops", "Branch")
    default_branch = Branch.objects.filter(root_branch=True).first()

    Role = apps.get_model("users", "Role")
    owner_role = Role.objects.filter(name='Owner').first()

    Shift = apps.get_model("users", "Shift")
    default_shift = Shift.objects.filter(name="Mặc định").first()

    User = apps.get_model("users", "User")
    user = User.objects.create(
        username="admin",
        password=make_password("123456"),
        is_superuser=True,
        is_active=True,
        role=owner_role,
        shift=default_shift,
        branch=default_branch,
    )
    
    BusinessUser = apps.get_model("users", "BusinessUser")
    BusinessUser.objects.create(
        fullname="Nguyễn Bình Minh",
        phone="0315415342",
        address="180 Minh Khai",
        district="Hai Bà Trưng",
        city="Hà nội",
        day_of_birth=23,
        month_of_birth=2,
        year_of_birth=2001,
        user=user
    )

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_init_shift_data')
    ]

    operations = [
        migrations.RunPython(init_admin_account_default),
    ]