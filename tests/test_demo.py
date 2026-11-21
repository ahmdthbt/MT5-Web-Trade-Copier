import unittest
from dataclasses import replace

from demo import DemoCopier
from trade_model import Trade


class DemoTests(unittest.TestCase):
    def test_lifecycle_from_either_platform(self):
        for origin, target in (("web", "mt5"), ("mt5", "web")):
            with self.subTest(origin=origin):
                engine = DemoCopier()
                trade = Trade("manual", "XAUUSD", "BUY", 0.02, 0, 0)
                engine.observe(origin, "manual", trade)
                peer_id, peer = next(iter(engine.accounts[target].items()))
                engine.observe(target, peer_id, peer)
                engine.observe(origin, "manual", trade)
                self.assertEqual(len(engine.accounts[target]), 1)
                self.assertEqual(len(engine.accounts[origin]), 1)
                engine.observe(target, peer_id, replace(peer, sl=3000, tp=5000, volume=0.01))
                self.assertEqual(engine.accounts[origin]["manual"], replace(trade, sl=3000, tp=5000, volume=0.01))
                engine.observe(origin, "manual", None)
                self.assertEqual(engine.accounts, {"web": {}, "mt5": {}})
                self.assertEqual(engine.peers, {})
