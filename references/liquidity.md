# B — Liquidity custody

Load for LP lock, rug, pool, Uniswap, or "who can pull liquidity" questions. Load [`platforms.md`](platforms.md) when v3/v4 or a launch locker is in play.

## Identify pools

Each material pool needs an exact address (v2/v3) or a complete pool key (v4): currencies, fee, tick spacing, hook, derived PoolId.

Declare discovery sources, searched ranges, and coverage limits. Separate **canonical** liquidity from **side** pools. A locked canonical position does not establish that all liquidity is locked, that price is supported, or that liquidity will remain in range.

## v3 positions

Resolve position manager, NFT/position ID, tick range, liquidity, owner, approvals, operators, and locker or hook authority.

Inspect `decreaseLiquidity`, `collect`, `burn`, `permit`, `setApprovalForAll`, `transferFrom` of the NFT, and any locker `withdraw` / `rescue` / `arbitraryCall` / upgrade.

## v4 positions

Record currency ordering, fee, tick spacing, hook, and PoolId. Never treat the singleton PoolManager's token balance as one pool's reserves.

Resolve the position manager NFT, salt/position key, owner, operators, hook permissions encoded in the hook address, and locker.

A hook can take fees, gate swaps, or move liquidity depending on its flags and code. Inspect the hook as its own privileged actor.

## Removal paths

For each material position, answer: who can remove **principal** (not merely unclaimed fees), through which function, with which approval, at the pinned block.

If a locker holds the NFT, read the locker runtime. "Locked on a dashboard" is corroboration only.

## Coverage statement

State which factories, managers, and block ranges were searched, and which pool types were not. Unknown side liquidity is a coverage limit plus a residual removal risk, not a pass.
