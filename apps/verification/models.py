from enum import Enum

from django.db import models

from apps.currency.mixins import CurrencyOwnedMixin
from apps.wallet.models import Wallet
from apps.profiles.models import CompanyProfile, UserProfile
from project.mixins import UUIDModel
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import requests
from django.urls import reverse
from django.utils.html import format_html
import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError


class VERIFICATION_STATES(Enum):
    OPEN = 1
    PENDING = 2
    CLAIMED = 3
    FAILED = 5
    MAX_CLAIMS = 6


VERIFICATION_STATES_CHOICES = (
    (VERIFICATION_STATES.OPEN.value, _('Open')),
    (VERIFICATION_STATES.PENDING.value, _('Pending')),
    (VERIFICATION_STATES.CLAIMED.value, _('Claimed')),
    (VERIFICATION_STATES.FAILED.value, _('Failed')),
    (VERIFICATION_STATES.MAX_CLAIMS.value, _('Max Claims'))
)


class AbstractVerification(UUIDModel):
    state = models.IntegerField(verbose_name=_(
        'State'), choices=VERIFICATION_STATES_CHOICES, default=VERIFICATION_STATES.OPEN.value)
    notes = models.TextField(editable=False, blank=True)

    class Meta:
        abstract = True


class CompanyVerification(AbstractVerification):
    company_profile = models.OneToOneField(
        CompanyProfile, on_delete=models.SET_NULL, related_name='company_verification', blank=True, null=True)
    name = models.CharField(verbose_name=_('Name'), max_length=128)
    uid = models.CharField(verbose_name=_(
        'Uid'), max_length=15, blank=True, null=True)

    address_street = models.CharField(verbose_name=_(
        'Street'), max_length=128)
    address_town = models.CharField(verbose_name=_(
        'Town'), max_length=128)
    address_postal_code = models.CharField(verbose_name=_(
        'Postal code'), max_length=128)

    class Meta:
        verbose_name = _('Company verification')
        verbose_name_plural = _('Company verifications')
        ordering = ['name']


class UserVerification(AbstractVerification):
    user_profile = models.OneToOneField(
        UserProfile, on_delete=models.SET_NULL, related_name='user_verification', blank=True, null=True)
    # TODO: move this as FK to UserProfile??
    first_name = models.CharField(verbose_name=_('Firstname'), max_length=128)
    last_name = models.CharField(verbose_name=_('Lastname'), max_length=128)

    address_street = models.CharField(verbose_name=_('Street'), max_length=128)
    address_town = models.CharField(verbose_name=_('Town'), max_length=128)
    address_postal_code = models.CharField(
        verbose_name=_('Postal code'), max_length=128)

    date_of_birth = models.DateField(verbose_name=_('Date of birth'))

    class Meta:
        verbose_name = _('User verification')
        verbose_name_plural = _('User verifications')
        ordering = ['last_name']


class AddressPinVerification(AbstractVerification):
    company_profile = models.OneToOneField(
        CompanyProfile, on_delete=models.CASCADE, related_name='address_pin_verification')
    pin = models.CharField(verbose_name=_('Pin'), max_length=8, blank=True)
    external_id = models.CharField(max_length=36, editable=False, blank=True)

    def preview_image(self, side="front"):
        if self.external_id:
            POST_API_CONFIG = settings.POST_API_CONFIG
            client = BackendApplicationClient(
                client_id=POST_API_CONFIG['client_id'], scope=POST_API_CONFIG['scope'])
            oauth = OAuth2Session(client=client)
            token = oauth.fetch_token(
                token_url=POST_API_CONFIG['token_url'], client_id=POST_API_CONFIG['client_id'], client_secret=POST_API_CONFIG['client_secret'])
            preview_url = POST_API_CONFIG['base_url'] + \
                'v1/postcards/{}/previews/{}'.format(self.external_id, side)
            response = requests.get(preview_url, headers={
                'Authorization': token['token_type'] + ' ' + token['access_token']})
            return "data:{};base64,{}".format(response.json()['fileType'], response.json()['imagedata'])

    @property
    def preview_back_image(self):
        return self.preview_image(side="back")

    @property
    def preview_front_image(self):
        return self.preview_image(side="front")

    def preview_link(self):
        if self.external_id:
            return format_html('<a href="{}">Preview</a>'.format(reverse('verification:addresspinverification_detail', args=(self.pk,))))
        else:
            return '-'

    preview_link.allow_tags = True
    preview_link.short_description = _('Preview')

    class Meta:
        verbose_name = _('Address pin verification')
        verbose_name_plural = _('Address pin verifications')


class SMSPinVerification(AbstractVerification):
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='sms_pin_verifications')
    pin = models.CharField(verbose_name=_('Pin'), max_length=8, blank=True)

    def clean(self, *args, **kwargs):
        errors = {}
        if hasattr(self, 'user_profile') and self.user_profile.sms_pin_verifications.filter(state=VERIFICATION_STATES.FAILED.value).exists():
            last_timestamp = self.user_profile.sms_pin_verifications.filter(
                state=VERIFICATION_STATES.FAILED.value).last().updated_at
            exponential_threshold_delta = datetime.timedelta(seconds=settings.SMS_PIN_WAIT_TIME_THRESHOLD_SECONDS**self.user_profile.sms_pin_verifications.filter(
                state=VERIFICATION_STATES.FAILED.value).count())
            if timezone.now() < last_timestamp + exponential_threshold_delta:
                seconds_left = last_timestamp + exponential_threshold_delta - timezone.now()
                errors['pin'] = ValidationError(
                    _('You are retrying too fast, please wait for {} seconds'.format(seconds_left.seconds)))

        if len(errors) > 0:
            raise ValidationError(errors)
        super(SMSPinVerification, self).clean(*args, **kwargs)

    class Meta:
        verbose_name = _('SMS pin verification')
        verbose_name_plural = _('SMS pin verifications')


class PlaceOfOrigin(UUIDModel):
    place_of_origin = models.CharField(max_length=128)
    user_verification = models.ForeignKey(
        UserVerification, on_delete=models.CASCADE, related_name='places_of_origin')
