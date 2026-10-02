# E — Launch integrity

Load for launch, fair launch, insider allocation, Pons, bonding curve, or "did they dump" questions. Load [`platforms.md`](platforms.md) for Pons v2 / Robinhood Chain mechanics.

## Decode

Launch parameters, allocations, fee exemptions, direct buy recipients, funding, deterministic addresses, deployment sequence, and early transfers or sales.

Distinguish automatic launch-platform behavior from manually supplied exceptions. Verify the exact factory version and deployed behavior against runtime, not against a blog.

## Cohort

Define any investigated wallet cohort before measuring it: inclusion rule, time bounds, sources, exclusions, coverage.

Track initial allocation, transfers, sales, rebuys, downstream inventory, proceeds, fees, and retained assets.

A wallet reaching zero does not prove a cash-out. An exchange deposit does not prove a sale, fiat withdrawal, or final beneficiary.

Prove sales from successful execution and pool/curve mechanics. Router transfers alone are insufficient.

## Pons-style launches

Inspect the **direct curve buy recipient** and applicable tax treatment. Do not assume the transaction sender received the tokens.

Read `CurveBuy(buyer, recipient, quoteIn, tokensOut, fee, tax)` (or the deployed equivalent). Follow `recipient`, not `tx.from`.

Creator tax, protocol fee share, snipe tax, and later `transferCreatorFeeRecipient` are separate knobs. Verify each on the launch instance.

Graduation into a locked Uniswap v4 position is not proof that all liquidity is locked or that side pools do not exist.

## Language

Launch-wallet sells followed by rebuys to new recipients are **market-mediated redistribution** unless stronger coordination evidence exists. See [`examples.md`](examples.md).
