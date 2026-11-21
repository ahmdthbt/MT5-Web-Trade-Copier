"""Replay synthetic position updates between two simulated accounts."""
from dataclasses import replace

from trade_model import Trade


class DemoCopier:
    def __init__(self):
        self.accounts = {"web": {}, "mt5": {}}
        self.peers = {}
        self.next_id = 1

    def observe(self, platform, position_id, position):
        """Apply one observation. A missing position represents a full close."""
        account = self.accounts[platform]
        if account.get(position_id) == position:
            return
        peer_platform = "mt5" if platform == "web" else "web"
        peer_account = self.accounts[peer_platform]
        key = (platform, position_id)
        if position is None:
            peer_id = self.peers.pop(key)
            del self.peers[(peer_platform, peer_id)]
            del account[position_id]
            del peer_account[peer_id]
            return
        if position.source_id != position_id:
            raise ValueError("Observation and position identifiers must match")
        if key not in self.peers:
            while True:
                peer_id = f"copy-{self.next_id}"
                self.next_id += 1
                if peer_id not in peer_account:
                    break
            self.peers[key] = peer_id
            self.peers[(peer_platform, peer_id)] = position_id
        peer_id = self.peers[key]
        account[position_id] = position
        peer_account[peer_id] = replace(position, source_id=peer_id)


if __name__ == "__main__":
    copier = DemoCopier()
    trade = Trade("demo-web-1", "XAUUSD", "BUY", 0.02, 0.0, 0.0)
    copier.observe("web", trade.source_id, trade)
    print("Open:", copier.accounts)
    peer_id, peer = next(iter(copier.accounts["mt5"].items()))
    copier.observe("mt5", peer_id, replace(peer, volume=0.01))
    print("Partial close:", copier.accounts)
    copier.observe("web", trade.source_id, None)
    print("Full close:", copier.accounts)
