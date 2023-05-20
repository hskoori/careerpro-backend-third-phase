from django.db import models
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import Account
from django.db import (
    DEFAULT_DB_ALIAS, DJANGO_VERSION_PICKLE_KEY, DatabaseError, connection,
    connections, router, transaction,
)
from django.db.models.deletion import CASCADE, Collector




class BaseModel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    auto_id = models.PositiveIntegerField(db_index = True,unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(Account, on_delete=models.PROTECT, null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    

    class Meta:
        abstract = True
