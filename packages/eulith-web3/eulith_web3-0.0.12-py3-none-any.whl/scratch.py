import boto3

from eulith_web3.erc20 import TokenSymbol
from eulith_web3.eulith_web3 import EulithWeb3
from eulith_web3.kms import KmsSigner
from eulith_web3.signing import construct_signing_middleware
from eulith_web3.uniswap import EulithUniswapPoolLookupRequest, UniswapPoolFee, EulithUniV3StartSwapRequest, \
    EulithUniV3StartLoanRequest

if __name__ == '__main__':
    aws_credentials_profile_name = ''
    key_name = ''
    formatted_key_name = f'alias/{key_name}'

    session = boto3.Session(profile_name=aws_credentials_profile_name)
    client = session.client('kms')
    kms_signer = KmsSigner(client, formatted_key_name)
    print(kms_signer.address)

    ew3 = EulithWeb3(eulith_url="https://eth-main.eulithrpc.com/v0",
                     eulith_refresh_token="",
                     signing_middle_ware=construct_signing_middleware(kms_signer))

    toolkit_address = ew3.v0.ensure_toolkit_contract(kms_signer.address)

    token_a = ew3.v0.get_erc_token(TokenSymbol.LUSD)
    token_b = ew3.v0.get_erc_token(TokenSymbol.USDC)

    pool = ew3.v0.get_univ3_pool(EulithUniswapPoolLookupRequest(
        token_a=token_a,
        token_b=token_b,
        fee=UniswapPoolFee.FiveBips
    ))

    if True:
        ew3.v0.start_atomic_transaction(kms_signer.address)

        ew3.v0.start_flash_loan(EulithUniV3StartLoanRequest())

        swap = ew3.v0.start_uni_swap(EulithUniV3StartSwapRequest())
        ew3.v0.finish_inner()

        their_raw_tx = '0xf8.....'
        ew3.eth.send_raw_transaction(their_raw_tx)

        other_swap = ew3.v0.start_uni_swap(EulithUniV3StartSwapRequest())
        ew3.v0.finish_inner()

        tx = ew3.v0.commit_atomic_transaction()

        tx_hash = ew3.eth.send_transaction(tx)
