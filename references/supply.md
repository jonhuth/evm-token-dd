# D — Supply and concentration

Load for holder concentration, circulating supply, or "who owns this" questions.

## Reconcile

Use methods that match the token's accounting: ERC-20 `totalSupply` + balances; rebasing shares; ERC-4626 / vault shares; internal synthetic units.

Keep distinct:

- raw token balances
- rebasing units
- synthetic claims
- bond / NFT shares
- LP shares
- custody (pool, locker, treasury, bridge)
- total supply
- circulating float (define the denominator)

## Classify material balances

Pool custody, protocol custody, lockers, treasuries, burn addresses, creator allocations, and investor-like balances separately. State exclusions.

A burn address is a burn only if transfers into it are irreversible given the token runtime (not merely a labeled EOA).

## Replay

Use full `Transfer` replay when discrepancies or historical questions justify it. Account for tokens whose balances change without ordinary `Transfer` events (rebase, self-balance rewrite, mint/burn to `address(0)` variants, ERC-777 hooks, custom).

If logs are pruned, that is a coverage limitation. Do not invent a circulating number.

## Concentration

Define the cohort before measuring it: inclusion rule, time bounds, sources, exclusions, coverage. Top-holder percentages without a denominator are not a finding.
