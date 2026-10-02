# Chains, Uniswap, Pons, Robinhood Chain

Load when the target is not a plain v2 pair on a well-known chain, or when the user names Uniswap v3/v4, Pons, or Robinhood Chain.

Catalog rows in `scripts/chain_catalog.py` are **discovery hints**. Verify `eth_chainId` on the RPC used. Verify factory/hook/manager addresses onchain before treating them as in-scope.

## Uniswap v3

- Pool identity is the pool contract (`token0`, `token1`, `fee`).
- Principal lives in the pool; control of principal is the NonfungiblePositionManager NFT (or a fork's manager).
- Record `tokenId`, `tickLower`, `tickUpper`, `liquidity`, owner, `operator` / approvals, and any locker.
- `collect` is fees. `decreaseLiquidity` + `collect` + `burn` removes principal.
- A locker that can `arbitraryCall` or is upgradeable can still remove principal.

## Uniswap v4

- One PoolManager singleton holds accounting for many pools. **Do not treat its ERC-20 balance as one pool's reserves.**
- Pool identity is `PoolKey`: `currency0`, `currency1`, `fee`, `tickSpacing`, `hooks`. Native ETH is `address(0)` and sorts first.
- `PoolId = keccak256(abi.encode(PoolKey))`. Compute with `scripts/evm.py` (`uniswap_v4_pool_id`). Currencies must already be ordered.
- Same pair + different hook or fee = different pool.
- Hook permissions are encoded in the hook address flags. Read the hook runtime.
- Positions are NFTs (or equivalent keys) in a PositionManager. Follow owner, operator, locker.
- Use `extsload` / pool state reads keyed by PoolId, not PoolManager `balanceOf`.

## Pons-style launches (Robinhood Chain and copies)

Treat published factory addresses as candidates. Confirm the token's deployer/factory by create trace or factory event.

On a Pons v2-style stack, typical pieces (verify, do not assume):

- Launch factory, per-launch bonding curve, launch-and-buy router
- Fee escrow, creator-fee recipient (possibly transferable)
- Meme/snipe hook on the graduated v4 pool
- Launch locker for the graduated position

Procedure:

1. Confirm factory version from the deployed factory runtime, not the website.
2. Entire supply often mints to the curve — check the mint recipient.
3. Buys: decode `buyer` vs `recipient`. The sender may not receive tokens.
4. Read fee bps, protocol share, creator tax, snipe tax from the launch instance.
5. Graduation: confirm the v4 PoolKey, locker, and that the NFT/position cannot be withdrawn *by the locker's runtime*.
6. After graduation, still search for side pools and later-created positions.

`transferCreatorFeeRecipient` (or equivalent) can retarget fees after launch. Current recipient ≠ launch-time recipient.

## Robinhood Chain

- Mainnet chain ID **4663**. Testnet **46630**. Never substitute testnet state for mainnet.
- EVM, Arbitrum Orbit, ETH gas, public explorer `robinhoodchain.blockscout.com`.
- Tokenized stocks and ETFs: a matching ticker is not the canonical Robinhood stock token. Bind the exact address.
- WETH / USDG catalog hints must be confirmed onchain.
- Sequencer is centralized. Note as an external dependency for liveness and ordering, not as a hidden mint.
- Bridged assets: match L1/L2 gateway legs. See [`fees.md`](fees.md).

If an RPC for 4663 is unavailable, that is a coverage limitation. Do not silently switch to another chain's same-ticker token.
