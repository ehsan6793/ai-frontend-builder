"""
skills/base.py
--------------
پیاده‌سازی Skill System در معماری Deep Agent.

هدف: امکان افزودن قابلیت جدید (مثلاً Figma Export، SEO، Accessibility)
بدون تغییر در معماری اصلی (Coordinator/Agentها). هر Skill کافیست:

1) در پوشه‌ی ai_frontend_builder/skills/ یک فایل جدید بسازد
2) یک کلاس که از Skill ارث‌بری می‌کند تعریف کند
3) متد run(state) را پیاده‌سازی کند

SkillRegistry به‌صورت خودکار همه‌ی Skillهای موجود در این پوشه را کشف
می‌کند (بدون نیاز به ثبت دستی در جای دیگر کد).
"""

import importlib
import inspect
import pkgutil
from abc import ABC, abstractmethod


class Skill(ABC):
    name: str = "unnamed-skill"
    description: str = ""

    @abstractmethod
    def run(self, state: dict) -> dict:
        """state را می‌خواند، کار خودش را انجام می‌دهد، و یک dict از
        خروجی‌های تولیدشده برمی‌گرداند (که در state["skills_output"]
        ذخیره می‌شود)."""
        raise NotImplementedError


class SkillRegistry:
    def __init__(self):
        self._skills = []
        self._discover()

    def _discover(self):
        import ai_frontend_builder.skills as skills_pkg

        for _, module_name, _ in pkgutil.iter_modules(skills_pkg.__path__):
            if module_name in ("base",):
                continue
            module = importlib.import_module(f"ai_frontend_builder.skills.{module_name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if issubclass(obj, Skill) and obj is not Skill:
                    self._skills.append(obj())

    def all(self):
        return self._skills

    def run_all(self, state: dict, enabled: list[str] | None = None) -> dict:
        outputs = {}
        for skill in self._skills:
            if enabled is not None and skill.name not in enabled:
                continue
            outputs[skill.name] = skill.run(state)
        return outputs
