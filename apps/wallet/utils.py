from rest_framework.pagination import CursorPagination
from pytezos import pytezos, michelson
from django.utils.timezone import now
from apps.wallet.models import MetaTransaction, Transaction, TRANSACTION_STATES
from django.conf import settings


class CustomCursorPagination(CursorPagination):
    ordering = 'created'


MESSAGE_STRUCTURE = {
    "prim": "pair",
            "args": [
                {
                    "prim": "key"
                },
                {
                    "prim": "pair",
                    "args": [
                        {
                            "prim": "nat"
                        },
                        {
                            "prim": "list",
                            "args": [
                                {
                                    "prim": "pair",
                                    "args": [
                                        {"prim": "address"},
                                        {
                                            "prim": "pair",
                                            "args": [
                                                {"prim": "nat"},
                                                {"prim": "nat"}
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
}


def create_message(from_wallet, to_wallet, nonce, token_id, amount):
    message_to_encode = {
        "prim": "Pair",
        "args": [
                {
                    "string": from_wallet.public_key
                },
            {
                    "prim": "Pair",
                    "args": [
                        {
                            'int': nonce
                        },
                        [
                            {
                                "prim": "Pair",
                                "args": [
                                    {
                                        "string": to_wallet.address
                                    },
                                    {
                                        "prim": "Pair",
                                        "args": [
                                            {
                                                "int": token_id
                                            },
                                            {
                                                'int': amount
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    ]
            }
        ]
    }
    return michelson.pack.pack(message_to_encode, MESSAGE_STRUCTURE)


def pack_meta_transaction(meta_transaction):
    message_to_encode = {
        "prim": "Pair",
        "args": [
            {
                "string": meta_transaction['from_public_key']
            },
            {
                "prim": "Pair",
                "args": [
                    {
                        'int': meta_transaction['nonce']
                    },
                    []
                ]
            }
        ]
    }

    for transaction in meta_transaction['txs']:
        message_to_encode['args'][1]['args'][1].append({
            "prim": "Pair",
            "args": [
                {
                    "string": transaction['to_']
                },
                {
                    "prim": "Pair",
                    "args": [
                        {
                            "int": transaction['token_id']
                        },
                        {
                            'int': transaction['amount']
                        }
                    ]
                }
            ]
        })

    return michelson.pack.pack(message_to_encode, MESSAGE_STRUCTURE)


def read_nonce_from_chain(address):
    pytezos_client = pytezos.using(
        key=settings.TEZOS_ADMIN_ACCOUNT_PRIVATE_KEY, shell=settings.TEZOS_NODE)
    token_contract = pytezos_client.contract(
        settings.TEZOS_TOKEN_CONTRACT_ADDRESS)
    try:
        return int(token_contract.nonce_of(callback='{}%receive_nonce'.format(settings.TEZOS_CALLBACK_CONTRACT_ADDRESS), requests=[address]).operation_group.sign().preapply()['contents'][0]['metadata']['internal_operation_results'][0]['parameters']['value'][0]['args'][0]['int'])
    except:
        return 0


def publish_open_meta_transactions_to_chain():
    open_transactions = MetaTransaction.objects.filter(
        state=TRANSACTION_STATES.OPEN.value)
    selected_transaction_ids = set(
        open_transactions.values_list('uuid', flat=True))
    selected_transactions = MetaTransaction.objects.filter(
        uuid__in=selected_transaction_ids)
    open_meta_transactions = list(map(
        lambda selected_transaction: selected_transaction.to_meta_transaction_dictionary(), selected_transactions))
    selected_transactions.update(state=TRANSACTION_STATES.PENDING.value)
    try:
        pytezos_client = pytezos.using(
            key=settings.TEZOS_ADMIN_ACCOUNT_PRIVATE_KEY, shell=settings.TEZOS_NODE)
        token_contract = pytezos_client.contract(
            settings.TEZOS_TOKEN_CONTRACT_ADDRESS)
        operation_result = token_contract.meta_transfer(open_meta_transactions).operation_group.sign().inject(
            _async=False, preapply=True, check_result=True, num_blocks_wait=settings.TEZOS_BLOCK_WAIT_TIME)

        if operation_result['contents'][0]['metadata']['operation_result']['status'] == 'applied':
            selected_transactions.update(
                state=TRANSACTION_STATES.DONE.value, submitted_to_chain_at=now(), operation_hash=operation_result['hash'])
        else:
            selected_transactions.update(
                state=TRANSACTION_STATES.FAILED.value, submitted_to_chain_at=now())
    except Exception as error:
        print(error)
        selected_transactions.update(
            state=TRANSACTION_STATES.FAILED.value, submitted_to_chain_at=now())


def publish_open_mint_transactions_to_chain():
    open_transactions = Transaction.objects.filter(
        state=TRANSACTION_STATES.OPEN.value, from_wallet=None)
    selected_transaction_ids = set(
        open_transactions.values_list('uuid', flat=True))
    selected_transactions = Transaction.objects.filter(
        uuid__in=selected_transaction_ids)

    selected_transactions.update(state=TRANSACTION_STATES.PENDING.value)
    try:
        pytezos_client = pytezos.using(
            key=settings.TEZOS_ADMIN_ACCOUNT_PRIVATE_KEY, shell=settings.TEZOS_NODE)
        token_contract = pytezos_client.contract(
            settings.TEZOS_TOKEN_CONTRACT_ADDRESS)
        for transaction in selected_transactions:
            operation_result = token_contract.mint(address=transaction.to_wallet.address, decimals=transaction.to_wallet.currency.decimals, name=transaction.to_wallet.currency.name, token_id=transaction.to_wallet.currency.token_id, symbol=transaction.to_wallet.currency.symbol, amount=transaction.amount).operation_group.sign().inject(
                _async=False, preapply=True, check_result=True, num_blocks_wait=settings.TEZOS_BLOCK_WAIT_TIME)

            if operation_result['contents'][0]['metadata']['operation_result']['status'] == 'applied':
                selected_transactions.update(
                    state=TRANSACTION_STATES.DONE.value, submitted_to_chain_at=now(), operation_hash=operation_result['hash'])
            else:
                selected_transactions.update(
                    state=TRANSACTION_STATES.FAILED.value, submitted_to_chain_at=now())
    except Exception as error:
        selected_transactions.update(
            state=TRANSACTION_STATES.FAILED.value, submitted_to_chain_at=now())


def publish_open_transfer_transactions_to_chain():
    open_transfer_transactions = Transaction.objects.filter(
        state=TRANSACTION_STATES.OPEN.value).exclude(from_wallet=None).exclude(uuid__in=MetaTransaction.objects.all())
    selected_transaction_ids = set(
        open_transfer_transactions.values_list('uuid', flat=True))
    selected_transactions = Transaction.objects.filter(
        uuid__in=selected_transaction_ids)

    selected_transactions.update(state=TRANSACTION_STATES.PENDING.value)
    try:
        pytezos_client = pytezos.using(
            key=settings.TEZOS_ADMIN_ACCOUNT_PRIVATE_KEY, shell=settings.TEZOS_NODE)
        token_contract = pytezos_client.contract(
            settings.TEZOS_TOKEN_CONTRACT_ADDRESS)
        last_from_wallet = None
        transfer_transaction_payloads = []
        for transaction in selected_transactions:
            if last_from_wallet != transaction.from_wallet:
                transfer_transaction_payloads.append({
                    "from_": transaction.from_wallet.address,
                    "txs": []
                })
            transfer_transaction_payloads[-1]['txs'].append({
                "to_": transaction.to_wallet.address,
                "token_id": transaction.to_wallet.currency.token_id,
                "amount": transaction.amount
            })
            last_from_wallet = transaction.from_wallet

        operation_result = token_contract.transfer(transfer_transaction_payloads).operation_group.sign().inject(
            _async=False, preapply=True, check_result=True, num_blocks_wait=settings.TEZOS_BLOCK_WAIT_TIME)

        if operation_result['contents'][0]['metadata']['operation_result']['status'] == 'applied':
            selected_transactions.update(
                state=TRANSACTION_STATES.DONE.value, submitted_to_chain_at=now(), operation_hash=operation_result['hash'])
        else:
            selected_transactions.update(
                state=TRANSACTION_STATES.FAILED.value, submitted_to_chain_at=now())
    except Exception as error:
        selected_transactions.update(
            state=TRANSACTION_STATES.FAILED.value, submitted_to_chain_at=now())


def wallet_recovery_transfer_balance(source_wallet, destination_public_key):
    publish_open_mint_transactions_to_chain()
    publish_open_transfer_transactions_to_chain()
    publish_open_meta_transactions_to_chain()
    pytezos_client = pytezos.using(
        key=settings.TEZOS_ADMIN_ACCOUNT_PRIVATE_KEY, shell=settings.TEZOS_NODE)
    token_contract = pytezos_client.contract(
        settings.TEZOS_TOKEN_CONTRACT_ADDRESS)
    try:
        return int(token_contract.nonce_of(callback='{}%receive_nonce'.format(settings.TEZOS_CALLBACK_CONTRACT_ADDRESS), requests=[address]).operation_group.sign().preapply()['contents'][0]['metadata']['internal_operation_results'][0]['parameters']['value'][0]['args'][0]['int'])
    except:
        return 0
