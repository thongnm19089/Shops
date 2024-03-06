import datetime
import logging

from django.conf import settings
from django.db import transaction

from .models import Branch, Shop
from apps.users.models import (
    Role, 
    RoleName,
    Shift,
    User,
)
from ..landing_pages.models.time_setting import LandingPageTime
import apps.landing_pages.constant as constant

logger = logging.getLogger(__name__)


def on_created_shop(instance):
        init_default_shop(instance)
        init_default_branch(instance)
        init_default_role(instance)
        init_default_shift(instance)
        init_landing_page_time_setting(instance)
    
    

def init_default_shop(user: User):
    shop = Shop.objects.create(
        name=user.name,
    )
   
    logger.info(f"created default branch {shop.name}")

def init_default_branch(user: User):

    branch = Branch.objects.create(
        name=user.name,
        root_branch=True,
    )
    logger.info(f"created default branch {branch.name}")
    
def init_default_role(user: User):
    default_role_names = [
        RoleName.OWNER.value,
        RoleName.MANAGER.value,
        RoleName.ACCOUNTANT.value,
        RoleName.RECEPTIONIST.value,
        RoleName.SALE_STAFF.value,
    ]
    roles = []
    for name in default_role_names:
        roles.append(Role(
            name=name
        ))
        logger.info(f"created init default role {name}")
        
    Role.objects.bulk_create(roles)

def init_default_shift(user: User):
    shift = Shift.objects.create(
        name="Mặc định",
        start_time=datetime.time(8, 0, 0),
        end_time=datetime.time(18, 0, 0),
        flexible_minutes=15,
    )
    logger.info(f"created init default shift {shift.name}")
    
def init_landing_page_time_setting(instance):
    time_data = []
    for day_of_week in range(2, 9):
        time_setting = LandingPageTime(
            start_time=constant.DEFAULT_START_TIME,
            end_time=constant.DEFAULT_END_TIME,
            is_active=True,
            tenant=instance,
            day_of_week=day_of_week,
        )
        time_data.append(time_setting)
    LandingPageTime.objects.bulk_create(time_data)

