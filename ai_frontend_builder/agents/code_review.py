"""
Code Review Agent
-------------------
مسئولیت: بازبینی خودکار خروجی Frontend Developer Agent قبل از تحویل
نهایی. بررسی‌ها واقعی و بر پایه‌ی فایل‌های واقعی نوشته‌شده روی دیسک انجام
می‌شود (نه صرفاً یک ادعای متنی)، تا Coordinator بتواند تصمیم بگیرد که آیا
پروژه آماده‌ی Finalize هست یا نیاز به یک Iteration دیگر دارد.
"""

import os

from ai_frontend_builder.llm_provider import LLMProvider


class CodeReviewAgent:
    name = "Code Review Agent"

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def run(self, state: dict) -> dict:
        code_files = state.get("code_files", {})

        issues = []
        checks_passed = []

        # 1) هر صفحه باید حداقل یک کامپوننت داشته باشد
        for page in state.get("pages", []):
            if not page["sections"]:
                issues.append(f"صفحه '{page['title']}' هیچ بخشی (section) ندارد.")
        checks_passed.append("بررسی وجود محتوا در صفحات")

        # 2) وجود واقعی فایل‌ها روی دیسک
        missing = [rel for rel, path in code_files.items() if not os.path.exists(path)]
        if missing:
            issues.append(f"{len(missing)} فایل در state ثبت شده ولی روی دیسک پیدا نشد: {missing}")
        checks_passed.append("بررسی تطابق state با Filesystem واقعی")

        # 3) اگر dark theme تعریف شده، layout باید اسکریپت تم را داشته باشد
        has_dark = "dark" in state.get("brand", {}).get("themes", {})
        layout_path = code_files.get("src/app/layout.tsx")
        if has_dark and layout_path and os.path.exists(layout_path):
            with open(layout_path, "r", encoding="utf-8") as f:
                if "localStorage.getItem('theme')" not in f.read():
                    issues.append("Theme تاریک تعریف شده ولی اسکریپت سوییچ تم در layout یافت نشد.")
        checks_passed.append("بررسی یکپارچگی Theme Generator با layout")

        # 4) دوباره‌کاری کامپوننت: کامپوننتی که در چند صفحه استفاده شده باید فقط یک بار تعریف شده باشد
        names = [c["name"] for c in state.get("components", [])]
        duplicates = {n for n in names if names.count(n) > 1}
        if duplicates:
            issues.append(f"کامپوننت تکراری در فهرست یافت شد (باید یکتا باشد): {duplicates}")
        checks_passed.append("بررسی یکتا بودن کامپوننت‌ها (Component Library)")

        score = max(0, 100 - 15 * len(issues))
        review = {
            "score": score,
            "issues": issues,
            "checks_passed": checks_passed,
            "verdict": "ready" if not issues else "needs-attention",
        }
        state["review"] = review
        state.setdefault("context_log", []).append(
            f"[Code Review] امتیاز کیفیت: {score}/100 | مشکلات: {len(issues)} | نتیجه: {review['verdict']}"
        )
        return state
