import logging

class MonitoringAgent:
    def __init__(self):
        self.positions = {}

    def update_position(self, symbol, side, quantity):
        if side == "BUY":
            self.positions[symbol] = self.positions.get(symbol, 0) + quantity
        elif side == "SELL":
            self.positions[symbol] = self.positions.get(symbol, 0) - quantity
        if self.positions.get(symbol) == 0:
            del self.positions[symbol]

    def log_positions(self):
        logging.info(f"Текущие позиции: {self.positions}")