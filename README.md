# MT5 Web Trade Copier

A runnable Python demonstration of bidirectional position synchronization, inspired by an IntelliPrime Web and MetaTrader 5 demo-account project. Either simulated platform can originate a change.

## Run locally

Use Python 3.10 or newer. The example uses only the standard library.

```sh
python demo.py
python -m unittest discover -s tests -v
```

The example opens a synthetic 0.02-lot gold position on the web side, reduces its MT5 counterpart to 0.01, and closes the pair from the web side. It prints both simulated accounts after each step. The last line shows two empty accounts.

## Why keep a pair of identifiers?

Each platform assigns a local identifier. The copier records the link in both directions, so a later stop change or partial close can find its counterpart. When an observation matches the position already recorded, the copier skips it. This keeps an echoed opening update from spawning a second pair.

## What the tests cover

The lifecycle test runs once with each platform as origin. It checks replayed observations, stop-loss and take-profit edits, partial closes, and removal of both positions after a full close.

## Scope

This public edition is an independently written, in-memory simulation. All positions are synthetic. The original project also explored SQLite operation journaling and ambiguous order responses. This repository demonstrates pairing and reconciliation only. It requires no broker login or MT5 installation.
