# MT5 Web Trade Copier

An offline Python demo of the two-way synchronization engine from an IntelliPrime Web and MetaTrader 5 demo-account copier. The engine pairs positions opened on either platform, propagates stop-loss and take-profit edits, and reconciles partial and full closes. This edition runs locally with simulated accounts and Python's standard library.

## Run the demo tests

From the repository root with Python 3.10 or newer:

```sh
python -m unittest discover -s tests -v
```

The eight tests exercise both copy directions, partial and full closes, stop changes, stale quotes, definite rejections, and uncertain submissions. For example, one test opens a synthetic 0.02-lot position, reduces it to 0.01 on the web side, then checks that the paired MT5 position shrinks without a second opening order.

## How the copier handles retries

Each position pair stores the identifiers assigned by both platforms. The engine uses those identifiers on its next observation so that a copied position does not trigger a copy back to the original account.

Before requesting an operation, the engine writes an intent to a SQLite journal. A stale quote detected before submission allows a later attempt. A timeout after submission leaves the outcome uncertain: repeating the order could duplicate a position. The journal records the uncertainty and pauses reconciliation until it is resolved.

## Source layout

| File | Purpose |
| --- | --- |
| `sync_core.py` | Pair tracking, persistent operation journal, and reconciliation |
| `trade_model.py` | Position representation shared by the simulated platforms |
| `tests/test_sync.py` | In-memory accounts, controlled clock, and executable scenarios |

This portfolio edition uses the project's archived synchronization core. The broker website, MT5 terminal, and private deployment configuration are outside the scope of the offline tests.
