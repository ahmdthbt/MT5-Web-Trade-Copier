from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Trade:
    source_id: str
    symbol: str
    side: str
    volume: float
    sl: float
    tp: float

    def payload(self):
        return asdict(self)
