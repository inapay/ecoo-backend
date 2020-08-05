
from django.urls import include, path
from rest_framework import routers

from apps.wallet.views import TransactionList, MetaTransactionListCreate, WalletPublicKeyTransferRequestListCreate, WalletDetail, WalletListCreate

urlpatterns = [
    path('wallet/', WalletListCreate.as_view(), name='wallet_list_create'),
    path('wallet/<slug:wallet_id>/', WalletDetail.as_view(), name='wallet_detail'),
    path('wallet_public_key_transfer_request/',
         WalletPublicKeyTransferRequestListCreate.as_view(), name='wallet_public_key_transfer_request_list_create'),
    path('transaction/', TransactionList.as_view(),
         name='transaction_list'),
    path('meta_transaction/', MetaTransactionListCreate.as_view(),
         name='meta_transaction_list_create'),
]
