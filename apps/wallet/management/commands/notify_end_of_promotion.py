import datetime

from django.core.management.base import BaseCommand, CommandError
from fcm_django.models import FCMDevice

from apps.wallet.models import WALLET_STATES, Wallet, WALLET_CATEGORIES
from django.conf import settings 
from apps.currency.models import Currency

class Command(BaseCommand):
    help = 'Notifies all wallet users which have not verified yet'

    def add_arguments(self, parser):
        parser.add_argument("--notification_days", nargs="+", default=[15,8,3], help='a amount of days before to notify the deadline')

    def handle(self, *args, **options):
        mapping = {
            WALLET_CATEGORIES.CONSUMER.value:'Das Ende der CURRENCY_NAME Kampagne ist in XXX Tagen. Bitte benutzten Sie ihr restliches Guthaben vorher.',
            WALLET_CATEGORIES.COMPANY.value:'Die Eintschauschfrist für CURRENCY_NAME ist in XXX Tagen. Bitte tauschen Sie Ihr Guthaben vorher bei der Stadt ein.'

        }
        
        today = datetime.datetime.now()


        for days in  options['notification_days']:

            delta = datetime.timedelta(days=days)
            currencies = Currency.objects.filter(campaign_end=(today+delta).date)
            
            for currency in currencies:
                for category, msg in mapping:
                    users_to_notify = Wallet.objects.filter(currency=currency, balance__gt=0,category=category ).values_list('owner').distinct()
                    devices = FCMDevice.objects.filter(user__in=users_to_notify)
                    self.stdout.write(f'Currency: {currency.name} Notifying {len(devices)} potential devices')
                    devices.send_message(title=settings.PUSH_NOTIFICATION_TITLE, body= msg.replace('CURRENCY_NAME',currency.name).replace('XXX', days))
