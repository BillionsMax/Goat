# agents/visualization_agent.py

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime


class VisualizationAgent:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.times = []
        self.prices = []

    def update_data(self, timestamp, price):
        """Добавляет новые данные для отображения."""
        self.times.append(datetime.datetime.fromtimestamp(timestamp / 1000))  # Конвертация из миллисекунд в секунды
        self.prices.append(price)

        # Оставляем последние 100 точек на графике для лучшего отображения
        if len(self.times) > 100:
            self.times.pop(0)
            self.prices.pop(0)

    def animate(self, i):
        """Обновление графика."""
        self.ax.clear()
        self.ax.plot(self.times, self.prices, label="Price")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Price")
        self.ax.set_title("Current Price in Real-Time")
        self.ax.legend()

    def start(self):
        """Запуск анимации графика."""
        ani = FuncAnimation(self.fig, self.animate, interval=1000)
        plt.show()
