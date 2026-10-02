# Synthetic reasoning examples

Load only to calibrate verdict language. These are not live findings. Do not treat the addresses as real targets.

## 1. Locked canonical liquidity, removable side liquidity

Canonical v4 position NFT sits in a locker with no withdraw function at the pin. A second v3 pool on the same pair holds 15% of pool-inventory tokens; that NFT is EOA-owned.

**Verdict:** No current executable removal path found at the pinned block for the canonical position. Side-pool principal can be removed by the EOA. NO-GO if the requirement was "all material liquidity locked."

## 2. Fixed supply, severe holder-sized exit degradation

`totalSupply` is constant; no mint selector. Small quote succeeds. A top-holder-sized quote returns <10% of the small-size per-unit output and then reverts above that.

**Verdict:** Sellable at the tested small size under the quoted state. Holder-sized exit is not executable at acceptable degradation. Fixed supply does not pass sellability.

## 3. Upgradeable reward layer around an immutable token

Token runtime has no owner and no mint. Rewards vault is a proxy; admin can change implementation and `rescue` ERC-20s.

**Verdict:** Token controls: no current mint/seize on the token. Admin/treasury/reward custody: admin can take vault assets and rewrite reward logic. Do not average these into "safe token."

## 4. Launch wallets sell and rebuy for new recipients

Launch signer sells into the curve; later buys send tokens to fresh addresses. No authenticated common-control evidence.

**Verdict:** Observed market-mediated redistribution from the launch signer to new recipients. Downstream inventory is not proven cash-out. Coordination/identity remains unknown.

## 5. Vault holding synthetic claims without a proven underlying exit

Vault ERC-20 balance is 1M "sSHARE". Underlying market is a synthetic perps venue. No live `redeem` path delivers WETH/USDG to the holder at the pin.

**Verdict:** Vault balance is a synthetic claim, not proven backing. Redemption rights unenforced at the pinned block.

## 6. RPC failure remains a coverage limitation

`eth_getLogs` times out for the launch block range. Token runtime was read at a pinned header.

**Verdict:** Current runtime permissions are known at the pin. Historical launch integrity is unknown because historical state was unavailable. Timeout is not evidence of a hidden mint.
