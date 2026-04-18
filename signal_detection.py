# signal_detection.py
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np


class SignalDetection:
    def __init__(self, hits, misses, false_alarms, correct_rejections):
        "Initialize with four counts."
        self.hits = hits
        self.misses = misses
        self.false_alarms = false_alarms
        self.correct_rejections = correct_rejections
    
    def hit_rate(self):
        "Return hit rate H = hits / (hits + misses)."
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    def false_alarm_rate(self):
        "Return false alarm rate FA = false_alarms / (false_alarms + correct_rejections)."
        total = self.false_alarms + self.correct_rejections
        return self.false_alarms / total if total > 0 else 0.0
    
    def d_prime(self):
        "Return sensitivity d' = Z(H) - Z(FA)."
        h = self.hit_rate()
        fa = self.false_alarm_rate()
        # Clip to avoid extreme values
        h = max(0.0001, min(0.9999, h))
        fa = max(0.0001, min(0.9999, fa))
        return norm.ppf(h) - norm.ppf(fa)
    
    def criterion(self):
        "Return criterion C = -0.5 * (Z(H) + Z(FA))."
        h = self.hit_rate()
        fa = self.false_alarm_rate()
        h = max(0.0001, min(0.9999, h))
        fa = max(0.0001, min(0.9999, fa))
        return -0.5 * (norm.ppf(h) + norm.ppf(fa))
    
    def __add__(self, other):
        "Add two SignalDetection objects elementwise."
        if not isinstance(other, SignalDetection):
            return NotImplemented
        return SignalDetection(
            self.hits + other.hits,
            self.misses + other.misses,
            self.false_alarms + other.false_alarms,
            self.correct_rejections + other.correct_rejections
        )
    
    def __sub__(self, other):
        "Subtract two SignalDetection objects elementwise."
        if not isinstance(other, SignalDetection):
            return NotImplemented
        return SignalDetection(
            self.hits - other.hits,
            self.misses - other.misses,
            self.false_alarms - other.false_alarms,
            self.correct_rejections - other.correct_rejections
        )
    
    def __mul__(self, factor):
        if not isinstance(factor, (int, float)):
            return NotImplemented
        return SignalDetection(
            self.hits * factor,
            self.misses * factor,
            self.false_alarms * factor,
            self.correct_rejections * factor
        )
    
    def __rmul__(self, factor):
        return self.__mul__(factor)
    
    def plot_sdt(self):
        "Plot overlapping normal distributions with criterion and d'."
        dprime = self.d_prime()
        criterion = self.criterion()
        
        x = np.linspace(-4, dprime + 4, 500)
        noise = norm.pdf(x, 0, 1)
        signal = norm.pdf(x, dprime, 1)
        
        fig, ax = plt.subplots()
        ax.plot(x, noise, label='Noise')
        ax.plot(x, signal, label='Signal')
        ax.axvline(criterion, color='r', linestyle='--', label=f'Criterion (C={criterion:.2f})')
        
        # Add d' arrow
        y_pos = max(noise.max(), signal.max()) * 0.7
        ax.annotate('', xy=(dprime, y_pos), xytext=(0, y_pos),
                    arrowprops=dict(arrowstyle='<->', lw=1))
        ax.text(dprime/2, y_pos * 1.05, f"d' = {dprime:.2f}", ha='center')
        
        ax.set_xlabel('Decision Axis')
        ax.set_ylabel('Probability Density')
        ax.set_title('Signal Detection Theory')
        ax.legend()
        return fig, ax
    
    @staticmethod
    def plot_roc(sdt_list):
        "Plot ROC curve"
        points = [(0, 0)]  # Start at (0,0)
        for sdt in sdt_list:
            points.append((sdt.false_alarm_rate(), sdt.hit_rate()))
        points.append((1, 1))  # End at (1,1)
        points.sort()
        
        fig, ax = plt.subplots()
        x_vals, y_vals = zip(*points)
        ax.plot(x_vals, y_vals, 'o-')
        ax.set_xlabel('False Alarm Rate')
        ax.set_ylabel('Hit Rate')
        ax.set_title('ROC Curve')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)
        return fig, ax