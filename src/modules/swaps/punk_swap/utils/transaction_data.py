from time import time

from web3.contract import Contract
from web3.types import TxParams
from eth_typing import Address

from config import SLIPPAGE
from web3 import Web3

from src.utils.data.tokens import tokens


def get_amount_out(contract: Contract, amount: int, from_token_address: Address,
                   to_token_address: Address) -> int:
    amount_out = contract.functions.getAmountsOut(
        amount,
        [from_token_address, to_token_address]
    ).call()
    return amount_out[1]


def create_swap_tx(from_token: str, to_token: str, contract: Contract, amount_out: int, from_token_address: str,
                   to_token_address: str, account_address: Address, amount: int, web3: Web3) -> TxParams:
    if from_token.lower() == 'eth':
        tx = contract.functions.swapExactETHForTokens(
            int(amount_out * (1 - SLIPPAGE)),
            [Web3.to_checksum_address(from_token_address), Web3.to_checksum_address(tokens['PUNK']),
             Web3.to_checksum_address(to_token_address)] if not to_token.upper() == 'PUNK' else
            [Web3.to_checksum_address(from_token_address), Web3.to_checksum_address(to_token_address)],
            account_address,
            int(time() + 1200)
        ).build_transaction({
            'value': amount if from_token.lower() == 'eth' else 0,
            'nonce': web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gasPrice': web3.eth.gas_price,
        })
    elif to_token.lower() == 'eth':
        tx = contract.functions.swapExactTokensForETH(
            amount,
            int(amount_out * (1 - SLIPPAGE)),
            [Web3.to_checksum_address(from_token_address), Web3.to_checksum_address(tokens['PUNK']),
             Web3.to_checksum_address(to_token_address)] if not from_token.upper() == 'PUNK' else
            [Web3.to_checksum_address(from_token_address), Web3.to_checksum_address(to_token_address)],
            account_address,
            int(time() + 1200)
        ).build_transaction({
            'value': 0,
            'nonce': web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gasPrice': web3.eth.gas_price,
        })
    else:
        tx = contract.functions.swapExactTokensForTokens(
            amount,
            int(amount_out * (1 - SLIPPAGE)),
            [from_token_address, to_token_address],
            account_address,
            int(time() + 1200)
        ).build_transaction({
            'value': amount if from_token.lower() == 'eth' else 0,
            'nonce': web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gasPrice': web3.eth.gas_price,
        })

    return tx


def create_liquidity_tx(from_token: str, contract: Contract, amount_out: int, to_token_address: str,
                        account_address: Address, amount: int, web3: Web3) -> TxParams:
    if from_token.lower() == 'eth':
        tx = contract.functions.addLiquidityETH(
            to_token_address,
            amount_out,
            int(amount_out * (1 - SLIPPAGE)),
            int(amount * (1 - SLIPPAGE)),
            account_address,
            int(time() + 1200)
        ).build_transaction({
            'value': amount if from_token.lower() == 'eth' else 0,
            'nonce': web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gasPrice': 0,
            'gas': 0
        })
    else:
        from_token_address = tokens[from_token]
        tx = contract.functions.addLiquidity(
            from_token_address,
            to_token_address,
            amount,
            amount_out,
            int(amount * (1 - SLIPPAGE)),
            int(amount_out * (1 - SLIPPAGE)),
            account_address,
            int(time() + 1200)
        ).build_transaction({
            'value': amount if from_token.lower() == 'eth' else 0,
            'nonce': web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gasPrice': web3.eth.gas_price,
        })

    return tx


def create_liquidity_remove_tx(web3: Web3, contract: Contract, from_token_pair_address: str, amount: int,
                               account_address: Address, token: str) -> TxParams:
    if token.lower() == 'eth':
        tx = contract.functions.removeLiquidityETH(
            from_token_pair_address,
            amount,
            0,
            0,
            account_address,
            int(time() + 1200)
        ).build_transaction({
            'value': 0,
            'nonce': web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gasPrice': web3.eth.gas_price,
        })
    else:
        from_token_address = tokens[token]
        tx = contract.functions.removeLiquidity(
            from_token_address,
            from_token_pair_address,
            amount,
            0,
            0,
            account_address,
            int(time() + 1200)
        ).build_transaction({
            'value': 0,
            'nonce': web3.eth.get_transaction_count(account_address),
            'from': account_address,
            'gasPrice': web3.eth.gas_price,
        })

    return tx
