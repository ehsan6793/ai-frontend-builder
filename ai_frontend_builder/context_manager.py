"""
context_manager.py
-------------------
پیاده‌سازی Context Management در معماری Deep Agent.

مشکلی که این ماژول حل می‌کند: اگر خروجی کامل هر Agent (که ممکن است شامل
کد کامل کامپوننت‌ها باشد) عیناً به Agent بعدی پاس داده شود، حجم Prompt به
سرعت منفجر می‌شود. به‌جای آن، بعد از هر Agent یک "خلاصه‌ی فشرده" (Context
Digest) از تصمیمات کلیدی ساخته می‌شود و همین خلاصه در State گراف نگه
داشته می‌شود؛ محتوای کامل (کد، اسپک کامل و ...) در Filesystem ذخیره و فقط
مسیر فایل در Context باقی می‌ماند.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class ContextDigest:
    """خلاصه‌ی سبک‌وزنی که بین Agentها رد و بدل می‌شود."""
    entries: List[str] = field(default_factory=list)
    file_refs: Dict[str, str] = field(default_factory=dict)  # label -> filesystem path

    def add(self, agent: str, summary: str):
        self.entries.append(f"[{agent}] {summary}")

    def add_file_ref(self, label: str, path: str):
        self.file_refs[label] = path

    def as_prompt_context(self, max_entries: int = 12) -> str:
        """فقط N خلاصه‌ی آخر را برمی‌گرداند تا Context رشد نامحدود نداشته
        باشد (شبیه‌سازی‌ی سیاست Sliding Window)."""
        recent = self.entries[-max_entries:]
        lines = ["=== خلاصه تصمیمات پروژه تا این مرحله ==="]
        lines.extend(recent)
        if self.file_refs:
            lines.append("--- فایل‌های مرجع ذخیره‌شده ---")
            for label, path in self.file_refs.items():
                lines.append(f"{label}: {path}")
        return "\n".join(lines)

    def token_estimate(self) -> int:
        # تخمین ساده: هر ۴ کاراکتر ≈ ۱ توکن
        return len(self.as_prompt_context()) // 4
