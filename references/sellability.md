# C — Sellability and executable depth

Load for "can I sell", exit, slippage, or holder-sized dump questions.

## Historical execution

Find a successful historical sell of the target token when available. Record tx, route, amount in, amount out, block, and that the receipt succeeded. Historical execution proves execution at that historical state only.

Router `Transfer` events alone are not a sale. Need the pool or curve mechanism plus the successful swap.

## Current quotes

At the pin, obtain read-only quotes at:

- a small size
- relevant holder-sized amounts (the user's size if given; otherwise a stated top-holder remainder after excluding pools/lockers)

Report route, input, quote asset, expected output, fees, per-unit degradation, and failure reasons.

Distinguish price impact, slippage tolerance, gas, spot price, and executable depth. Quotes and previews do not prove a realized exit.

## Decisive simulated sale

Only on a verified disposable local fork, synthetic accounts, labeled counterfactual.

Require a successful receipt **and** the intended underlying-asset balance delta, with route and costs explained. A returned success flag or emitted event alone is insufficient.

## Failure modes to name

- Token pause / blacklist / trading gate
- Tax or hook taking the output
- Tick range with no liquidity
- Pool empty or one-sided
- Allowance or recipient restrictions

Fixed supply does not imply sellability. See [`examples.md`](examples.md).
