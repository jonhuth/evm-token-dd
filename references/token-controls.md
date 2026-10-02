# A — Token code and control

Load for mint, pause, blacklist, tax, upgrade, owner, or "renounced" questions.

## Inspect

Mint, burn, rebase, balance rewrite, seizure, pause, blacklist, whitelist, taxes, exemptions, cooldowns, transaction limits, trading gates, external calls, `delegatecall`, and upgrade paths.

Read current owners, roles, multisig thresholds, timelocks, and who can change them. A role that can grant mint is still mint authority.

"No owner" and "renounced" are claims. Check:

- `owner()` / `getOwner` / AccessControl / Ownable2Step pending owner
- whether `renounceOwnership` actually executed, and whether another module still has admin
- whether the implementation can still be swapped
- whether a separate router, hook, or wrapper can still seize or tax

## Distinguish

| Current code permits | Admin can introduce by replacement |
|---|---|
| Functions and modifiers on the pinned runtime | New implementation, new hook, new trusted caller |

If the token is immutable but a wrapper, vault, or hook is upgradeable, rate those layers separately. See [`examples.md`](examples.md).

## Output for this surface

- Who can change balances or restrict transfers now
- Who can change that set of people
- Whether ordinary holders can be prevented from selling by token logic alone (trading gates, blacklist, pause, tax-to-100)
- Confidence and what would stale the claim (new implementation, role grant, unpause)

Do not treat missing verification or unread bytecode as "no mint".
