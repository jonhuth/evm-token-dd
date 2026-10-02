# Triggered deep investigations

Load only when a screening finding fires the trigger. Each track states trigger, minimum evidence, stop, and residual unknown.

## 1. Full holder or Transfer replay

**Trigger:** `totalSupply` disagrees with observed balances; rebase/self-balance rewrite; historical "who got supply" question.
**Minimum:** consecutive logs or archive traces over the stated range; accounting method matching the token.
**Stop:** conservation holds within a bounded delta, or logs are unavailable.
**If incomplete:** circulating supply and concentration remain unknown for the missing range.

## 2. Complete pool and position history

**Trigger:** canonical lock claimed; side-pool residual could change the rug verdict; v3/v4 NFT owner changed.
**Minimum:** every initialize/mint/decrease/burn/transfer of material positions in range; locker runtime.
**Stop:** current principal owners mapped, or factory/manager logs pruned.
**If incomplete:** side-pool removal risk stays unknown, not passed.

## 3. Launch-cohort accounting

**Trigger:** insider allocation, exemption, or early sell is material to the user's question.
**Minimum:** defined cohort; launch tx decoded; sales proven via pool/curve execution.
**Stop:** cohort inventory + proceeds reconciled, or coverage ends at commingling.
**If incomplete:** do not call it a cash-out.

## 4. Fee-wallet and cross-chain proceeds

**Trigger:** treasury/fee-origin question; material value left the chain.
**Minimum:** per-asset conservation; bridge legs matched both sides.
**Stop:** commingling or missing destination pin.
**If incomplete:** beneficiary unknown.

## 5. Proxy authority and critical bytecode reconstruction

**Trigger:** upgradeable token, hook, locker, or vault can change the verdict; source missing or mismatched.
**Minimum:** follow the bytecode ladder in [`evidence.md`](evidence.md).
**Stop:** current permissions answered, or reconstruction cannot close byte differences.
**If incomplete:** treat upgrade/mint/seize as unknown, never as absent.

## 6. Reward-epoch accounting and backlog

**Trigger:** advertised yield, dividends, or epochs; unpaid backlog could invert backing.
**Minimum:** entitlement rule, cumulative paid vs owed, remaining inventory, liveness of the payer.
**Stop:** conservation holds or admin can mint/redirect the stream.
**If incomplete:** liveness and solvency unknown.

## 7. External dependency and redemption analysis

**Trigger:** utility or backing depends on oracle, bridge, keeper, stock token, or sequencer.
**Minimum:** live call path from holder action to delivered asset; failure modes.
**Stop:** path proven or proven broken.
**If incomplete:** redemption rights unenforced.

## 8. Narrow operational attribution

**Trigger:** user asked who controls a specific function, and onchain roles are not enough.
**Minimum:** authenticated control evidence tied to the same key that can call the function.
**Stop:** at the first unauthenticated hop. No broad identity search.

## Exploit / invariant work

Route protocol-wide invariant work or substantial exploit campaigns to a separate audit workflow when available. This skill stops at economic-system diligence.
