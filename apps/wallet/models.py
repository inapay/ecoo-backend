from enum import Enum

from django.db import models

from apps.currency.mixins import CurrencyOwnedMixin
from project import settings
from project.mixins import UUIDModel
from django.db.models import Q


class Company(UUIDModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=32)


class ClaimableAmount(CurrencyOwnedMixin):
    identifier = models.TextField(blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)


class WALLET_STATES(Enum):
    UNVERIFIED = 0
    PENDING = 1
    VERIFIED = 2


WALLET_STATE_CHOICES = (
    (WALLET_STATES.UNVERIFIED.value, 'Unverified'),
    (WALLET_STATES.PENDING.value, 'Pending'),
    (WALLET_STATES.VERIFIED.value, 'Verified'),
)


class Wallet(CurrencyOwnedMixin):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.DO_NOTHING)
    company = models.ForeignKey(
        Company, blank=True, null=True, on_delete=models.SET_NULL)
    walletID = models.CharField(unique=True, max_length=128) # generated in BE -> to be specified...
    address = models.TextField() # TZ adress (maybe not needed)
    pub_key = models.TextField() # tz public_key
    nonce = models.IntegerField(default=0)
    is_owner_wallet = models.BooleanField(default=False) # only true if belongs to "gemeinde"

    state = models.IntegerField(default=0, choices=WALLET_STATE_CHOICES)

    def __str__(self):
        return self.walletID

    @staticmethod
    def getBelongingToUser(user):
        if user.is_superuser:
            return Wallet.objects.all()

        return Wallet.objects.filter(Q(owner=user)|Q(company__owner=user))


class TRANSACTION_STATES(Enum):
    OPEN = 1
    PENDING = 2
    DONE = 3


TRANSACTION_STATE_CHOICES = (
    (TRANSACTION_STATES.OPEN.value, 'Open'),
    (TRANSACTION_STATES.PENDING.value, 'Pending'),
    (TRANSACTION_STATES.DONE.value, 'Done'),
)


class TokenTransaction(UUIDModel):
    # TODO: rename fields to from_wallet etc.
    from_addr = models.ForeignKey(
        Wallet, on_delete=models.DO_NOTHING, related_name='fromtransaction')
    to_addr = models.ForeignKey(
        Wallet, on_delete=models.DO_NOTHING, related_name='totransaction')
    amount = models.FloatField()

    state = models.IntegerField(choices=TRANSACTION_STATE_CHOICES, default=1)
    signature = models.CharField(max_length=64, null=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    submitted_to_chain_at = models.DateTimeField(blank=True, null=True)


    @staticmethod
    def getBelongingToUser(user):
        belonging_wallets = Wallet.getBelongingToUser(user)
        return TokenTransaction.objects.filter(Q(from_addr__in=belonging_wallets)|Q(to_addr__in=belonging_wallets))


# TODO: model to store verified 