"""Discovery catalog of EVM chain metadata. Not proof of the connected RPC.

Always verify eth_chainId against the live endpoint before using a row.
Addresses and RPCs here are hints. Confirm on the target chain.
"""

from __future__ import annotations

from typing import Any

# Public discovery only. Do not store credentials or private RPC URLs.
CHAINS: dict[int, dict[str, Any]] = {
    1: {
        "name": "Ethereum",
        "native": "ETH",
        "explorers": ["https://etherscan.io"],
        "uniswap_v4_pool_manager": "0x000000000004444c5dc75cB358380D2e3dE08A90",
    },
    10: {"name": "Optimism", "native": "ETH", "explorers": ["https://optimistic.etherscan.io"]},
    56: {"name": "BNB Smart Chain", "native": "BNB", "explorers": ["https://bscscan.com"]},
    137: {"name": "Polygon", "native": "POL", "explorers": ["https://polygonscan.com"]},
    8453: {"name": "Base", "native": "ETH", "explorers": ["https://basescan.org"]},
    42161: {"name": "Arbitrum One", "native": "ETH", "explorers": ["https://arbiscan.io"]},
    43114: {"name": "Avalanche C-Chain", "native": "AVAX", "explorers": ["https://snowtrace.io"]},
    534352: {"name": "Scroll", "native": "ETH", "explorers": ["https://scrollscan.com"]},
    59144: {"name": "Linea", "native": "ETH", "explorers": ["https://lineascan.build"]},
    81457: {"name": "Blast", "native": "ETH", "explorers": ["https://blastscan.io"]},
    7777777: {"name": "Zora", "native": "ETH", "explorers": ["https://explorer.zora.energy"]},
    480: {"name": "World Chain", "native": "ETH", "explorers": ["https://worldscan.org"]},
    4663: {
        "name": "Robinhood Chain",
        "native": "ETH",
        "explorers": ["https://robinhoodchain.blockscout.com"],
        "public_rpc_hint": "https://rpc.mainnet.chain.robinhood.com",
        "stack_note": "Arbitrum Orbit L2; sequencer is an external dependency",
        "weth": "0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73",
        "usdg": "0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168",
        "uniswap_v4_pool_manager_hint": "0x8366a39cc670b4001a1121b8f6a443a643e40951",
        "pons_v2_hint": {
            "factory": "0x7eD598BcEf8bd9Edd8C97A195C6d13f40801EC7e",
            "meme_hook": "0xE5e702641Ea86F4ae6cC3cDaeD2B886f976Be044",
            "fee_escrow": "0xd3AFEB2a57f70eF218Aa82451c51B2fb0416Ac9e",
            "buyback_vault": "0x42df2a798f82289E177311362e8f5ccC45c1219c",
            "launch_locker": "0x267444D099b10fB5Ed7c3Cc7B7c767AdcA574952",
            "launch_and_buy": "0xe33E9E479dF8802cb0866d5d05258bEc4cF62948",
        },
    },
    46630: {
        "name": "Robinhood Chain Testnet",
        "native": "ETH",
        "explorers": ["https://explorer.testnet.chain.robinhood.com"],
        "public_rpc_hint": "https://rpc.testnet.chain.robinhood.com",
        "note": "Testnet assets are not mainnet assets. Never substitute 46630 for 4663.",
    },
    11155111: {"name": "Sepolia", "native": "ETH", "explorers": ["https://sepolia.etherscan.io"]},
}


def lookup(chain_id: int) -> dict[str, Any] | None:
    row = CHAINS.get(chain_id)
    return dict(row) if row else None
