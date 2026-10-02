# Evidence, attribution, bytecode

Load with any material onchain claim.

## Evidence types

| Type | Use for | Not sufficient for |
|---|---|---|
| Runtime / `eth_getCode` / code hash | What the deployed bytes permit now | Intent, offchain promises |
| Storage / slots / mappings | Current roles, balances, config | Historical values unless pinned historically |
| Calldata + successful receipt | What a transaction actually did | Failed or simulated calls |
| Correctly decoded logs | Transfers, role changes, pool events | Events without a successful receipt |
| Read-only call at pin | Current view | Future state |
| Disposable-fork simulation | Counterfactual path existence | Realized user outcome |
| Explorer / dashboard / scanner | Discovery, labels | Identity of the token |
| Website / repo / metadata | Claimed design | Deployed behavior |
| X/Twitter | Claimed locks, utility, launch story | Control, custody, or cash-out |

Record: chain, address, pin or tx, method, params (credentials redacted), raw result, decoder, and why it is stale later.

## Classification

- **Proven:** runtime, storage, receipt, or log at a stated pin/tx, correctly decoded.
- **Strongly supported:** multiple independent proven facts that close reasonable alternatives.
- **Inferred:** a coherent reading that still has a live alternative.
- **Unknown:** not checked, not available, or contradictory.

Never promote unknown or skipped to pass.

## Attribution

Use launch signer, fee recipient, funder, observed controller, position owner until stronger authenticated control evidence exists.

Shared funding, routers, CEX deposit addresses, timing, CREATE2, or settlement destinations do not prove common ownership, human identity, coordination, fraud, or intent.

Describe sale-then-rebuy routing as **market-mediated redistribution** unless independently established otherwise.

Do not call proceeds profit without a defensible cost basis, material flows, fees, and retained inventory.

Do not run broad personal-identity searches by default. Keep public attribution narrow and tied to authenticated project-control evidence (signed posts that match onchain controllers, verified repo deploy keys, documented multisig signers).

## Bytecode ladder

Escalate only as needed:

1. Runtime bytes and 4-byte selectors at the pin. Note `delegatecall`, `sstore` of balances, external calls, `selfdestruct` (if present), upgrade patterns.
2. Verified predecessor source and compiler metadata. Treat explorer "verified" as a claim. Compare bytecode.
3. Storage layout and historical calls that changed owners, implementations, or config.
4. Decompilation or reconstruction only if 1–3 cannot answer a material question. Decompiler output is not verified source.
5. Claim executable equivalence only when compilation and byte comparison close meaningful differences (metadata/CBOR excluded, constructor args accounted for).

Proxy resolution: EIP-1967 implementation/admin, beacon, EIP-1822, custom slots, cloning (`clone` / minimal proxy), and who can change them. Distinguish what current code permits from what an administrator could introduce by replacing it.

## Coverage vs findings

Timeouts, pruning, rate limits, DNS failures, and missing APIs are coverage limitations. Write them as limitations, not as token defects.
