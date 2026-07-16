"""
llm_provider.py
----------------
لایه انتزاعی بین Agentها و مدل زبانی.

اگر متغیر محیطی OPENAI_API_KEY تنظیم شده باشد، از OpenAI استفاده می‌شود.
در غیر این صورت سیستم به‌صورت خودکار وارد MOCK MODE می‌شود: یک موتور
قانون‌محور (rule-based) که بر اساس ایده‌ی کاربر، خروجی ساختاریافته و
معنادار تولید می‌کند تا کل Deep Agent بدون نیاز به هیچ API Key قابل اجرا
و دمو باشد.

این طراحی عمداً به این شکل است چون هدف پروژه‌ی کلاسی، اثبات درستی
معماری Multi-Agent / Deep Agent است، نه صرفاً صدا زدن یک API.
"""

import json
import os
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMResponse:
    text: str
    raw: dict


class LLMProvider:
    """رابط یکسان برای همه Agentها. provider واقعی (OpenAI) یا mock را
    زیر یک متد generate() پنهان می‌کند تا Agentها اصلاً ندانند کدام
    فعال است."""

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        self.mode = "openai" if self.api_key else "mock"

    def generate(self, system_prompt: str, user_prompt: str, mock_fn=None) -> LLMResponse:
        """
        system_prompt / user_prompt: پرامپت‌هایی که در حالت واقعی به مدل
        زبانی ارسال می‌شوند.
        mock_fn: تابعی بدون آرگومان که در MOCK MODE فراخوانی می‌شود و باید
        یک dict برگرداند. هر Agent منطق مخصوص خودش را برای mock فراهم می‌کند.
        """
        if self.mode == "openai":
            return self._call_openai(system_prompt, user_prompt)
        if mock_fn is None:
            raise ValueError("mock_fn الزامی است وقتی OPENAI_API_KEY تنظیم نشده")
        data = mock_fn()
        return LLMResponse(text=json.dumps(data, ensure_ascii=False), raw=data)

    def _call_openai(self, system_prompt: str, user_prompt: str) -> LLMResponse:
        try:
            from openai import OpenAI
        except ImportError as e:
            raise RuntimeError(
                "پکیج openai نصب نیست. با: pip install openai نصبش کن یا "
                "بدون OPENAI_API_KEY اجرا کن تا وارد MOCK MODE بشه."
            ) from e

        client = OpenAI(api_key=self.api_key)
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.4,
        )
        content = resp.choices[0].message.content
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            data = json.loads(match.group(0)) if match else {"raw": content}
        return LLMResponse(text=content, raw=data)


# ---------------------------------------------------------------------------
# ابزار کمکی مشترک برای mock فایل‌های Agent مختلف: تشخیص نوع پروژه از روی
# متن ایده‌ی کاربر (فارسی/انگلیسی) — این "هوش" ساده‌شده جایگزین LLM واقعی است.
# ---------------------------------------------------------------------------

PROJECT_TYPE_KEYWORDS = {
    "ecommerce": ["فروشگاه", "خرید", "shop", "store", "ecommerce", "e-commerce", "محصول", "سبد خرید", "cart"],
    "saas": ["ساس", "saas", "داشبورد مدیریت", "اشتراک", "subscription", "پنل مدیریت"],
    "portfolio": ["نمونه‌کار", "پورتفولیو", "portfolio", "رزومه", "resume", "personal site"],
    "blog": ["وبلاگ", "blog", "مقاله", "خبر", "news"],
    "restaurant": ["رستوران", "کافه", "restaurant", "cafe", "منو غذا", "food"],
    "landing": ["لندینگ", "landing", "معرفی محصول", "صفحه فرود"],
    "dashboard": ["داشبورد", "dashboard", "آنالیتیکس", "analytics", "گزارش"],
    "education": ["آموزش", "دوره", "course", "آکادمی", "academy", "کلاس"],
}


def detect_project_type(idea: str) -> str:
    idea_lower = idea.lower()
    scores = {}
    for ptype, kws in PROJECT_TYPE_KEYWORDS.items():
        score = sum(1 for kw in kws if kw in idea_lower or kw in idea)
        if score:
            scores[ptype] = score
    if not scores:
        return "generic"
    return max(scores, key=scores.get)


def detect_project_name(idea: str, project_type: str) -> str:
    names = {
        "ecommerce": "فروشگاه آنلاین",
        "saas": "پلتفرم SaaS",
        "portfolio": "پورتفولیوی شخصی",
        "blog": "وبلاگ",
        "restaurant": "سایت رستوران",
        "landing": "صفحه فرود محصول",
        "dashboard": "داشبورد مدیریتی",
        "education": "پلتفرم آموزشی",
        "generic": "وب‌سایت",
    }
    return names[project_type]
