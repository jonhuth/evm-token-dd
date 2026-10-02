# F — Fees, treasury, and proceeds

Load for fee recipient, treasury, buyback, "where did the ETH go", or creator-fee questions.

## Map the fee

- Basis: percent of gross trade value vs percent of a fee bucket
- Denomination: input token, output token, native, or a separate currency
- Splits, escrow, claim authority, recipients, configurable routes
- Current configuration vs historically realized rates

A 1% swap fee with a 30% protocol share of that fee is not a 30% tax.

## Reconcile each relevant asset

```
opening balance + inflows + explained adjustments
  = outflows + closing balance + explicitly bounded unexplained delta
```

Account for wraps, burns, bridge legs, gas, and reverted transactions. Do not double-count transformations (WETH wrap, then bridge, then unwrap).

## Bridges

Match source execution, identifiers, destination chain, recipient, delivered amount, and destination evidence. Pin both chains. Stop exact attribution at commingling.

## Proceeds

Do not call a flow profit without cost basis, material flows, fees, and retained inventory.

Stop at commingling. An exchange deposit does not prove a sale, fiat withdrawal, or final beneficiary.

If the question is "did this vault balance come from LP fees?", load [`rewards.md`](rewards.md) and reconcile to receipt-level fee collections and forwarding. Distinguish vault holdings, pool inventory, and unclaimed fees.
