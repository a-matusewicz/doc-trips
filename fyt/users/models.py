import logging

from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.db import models

from fyt.dartdm.lookup import EmailLookupException, lookup_email

log = logging.getLogger(__name__)

MAX_NETID_LENGTH = 20


class DartmouthUserManager(BaseUserManager):
    """
    Object manager for DartmouthUser
    """

    def get_or_create_by_netid(self, netid, name):
        """
        Return the user with the given netid.

        Create the user if necessary. Does not search via name, since names
        from different sources (CAS, DartDm lookup) can be slightly different.
        """
        (user, created) = self.get_or_create(netid=netid, defaults={"name": name})

        # Try and lookup user's email in the Dartmouth Directory
        # manager, since the CAS response does not contain the email.
        # If not found, email is left empty.
        if created:
            try:
                user.email = lookup_email(netid)
                user.save()
            except EmailLookupException:
                log.error("Email not found for %s %s", name, netid)
                pass

        return (user, created)

    def create_superuser(self, **kwargs):
        raise Exception(
            "create_superuser not implemented. Use 'manage.py setsuperuser' instead."
        )

    def create_user_without_netid(self, name, email):
        """
        Create a user without a netid.

        Used for non-student registrations. The name is used as a stand-in
        netid, truncated if if is too long.
        """
        netid = name

        if len(netid) > MAX_NETID_LENGTH:
            netid = netid[:MAX_NETID_LENGTH]

        return self.create(netid=netid, name=name, email=email)


class NetIdField(models.CharField):
    """
    Saves NetIds as lowercase for easy comparison.
    """

    description = "A field to hold a Dartmouth WebAuth Netid"

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = MAX_NETID_LENGTH
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        """
        Handle uppercase ids
        """
        value = super().to_python(value)
        if value is not None:
            return value.lower()

    def pre_save(self, model_instance, add):
        """
        Update lowercase ids on the instance before saving
        """
        value = getattr(model_instance, self.attname).lower()
        setattr(model_instance, self.attname, value)
        return value


class DartmouthUser(PermissionsMixin):

    objects = DartmouthUserManager()

    netid = NetIdField(unique=True)
    email = models.EmailField('email address')
    name = models.CharField(max_length=255, db_index=True)

    last_login = models.DateTimeField('last login', blank=True, null=True)

    class Meta:
        ordering = ['name']

    USERNAME_FIELD = 'netid'
    REQUIRED_FIELDS = ['email', 'name']

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_username(self):
        return self.netid

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        return True

    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return str(self.name)
