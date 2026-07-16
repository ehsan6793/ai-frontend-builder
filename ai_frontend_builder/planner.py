"""
planner.py
----------
پیاده‌سازی Planning در معماری Deep Agent.

قبل از شروع اجرای Agentها، Coordinator یک Todo Plan می‌سازد (لیستی از
مراحل با وضعیت pending). در طول اجرا، هر Agent با اتمام کارش وضعیت مرحله‌ی
مربوطه را به‌روزرسانی می‌کند. این پلن هم در کنسول (CLI) نمایش داده می‌شود
و هم به‌صورت plan.json در Filesystem پروژه ذخیره می‌شود تا قابل ردیابی و
Resume باشد.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class TodoStep:
    id: str
    title: str
    agent: str
    status: str = "pending"  # pending | in_progress | done | skipped


@dataclass
class Plan:
    steps: List[TodoStep] = field(default_factory=list)

    def to_dict(self):
        return {"steps": [asdict(s) for s in self.steps]}

    def mark(self, step_id: str, status: str):
        for s in self.steps:
            if s.id == step_id:
                s.status = status
                return
        raise KeyError(f"step {step_id} not found in plan")

    def pretty(self) -> str:
        icon = {"pending": "⏳", "in_progress": "🔄", "done": "✅", "skipped": "⏭️"}
        lines = []
        for s in self.steps:
            lines.append(f"{icon.get(s.status,'?')} [{s.agent}] {s.title}")
        return "\n".join(lines)


DEFAULT_PLAN_TEMPLATE = [
    ("analysis", "تحلیل نیازمندی و استخراج ساختار صفحات", "Product Analysis Agent"),
    ("design_system", "تعریف Design Tokens، Typography و Grid", "Design System Agent"),
    ("branding", "انتخاب رنگ و هویت بصری (Theme روشن/تاریک)", "Color & Branding Agent"),
    ("components", "طراحی و تولید کامپوننت‌های UI", "UI Components Agent"),
    ("animation", "تعریف Animation و Micro-interaction ها", "Animation Agent"),
    ("codegen", "تولید کد Next.js + TypeScript + Tailwind", "Frontend Developer Agent"),
    ("review", "بازبینی کیفیت کد (Code Review)", "Code Review Agent"),
    ("skills", "اجرای Skillهای اضافه (Figma Export، ...)", "Skill System"),
    ("finalize", "بسته‌بندی خروجی نهایی در Workspace", "Coordinator Agent"),
]


def build_default_plan() -> Plan:
    return Plan(steps=[TodoStep(id=i, title=t, agent=a) for i, t, a in DEFAULT_PLAN_TEMPLATE])


def save_plan(plan: Plan, path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(plan.to_dict(), f, ensure_ascii=False, indent=2)
