"""
Fliqlo Timer - Core Package
A beautiful Pomodoro timer with dual clock system and unlimited sessions.
"""

__version__ = "1.0.0"
__author__ = "Halibut205"
__description__ = "A beautiful Pomodoro timer with dual clock system"

# Core exports
from .core.timer_core import TimerCore
from .core.timer_controller import TimerController

__all__ = ["TimerCore", "TimerController"]
