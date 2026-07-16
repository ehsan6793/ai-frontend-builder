"""
state.py
--------
شِمای State مشترکی که در طول گراف LangGraph بین همه‌ی Agentها رد و بدل
می‌شود. طبق اصل Context Management، این state فقط داده‌های "فشرده" و
تصمیمات کلیدی را نگه می‌دارد؛ محتوای حجیم (کد کامل فایل‌ها) مستقیماً روی
Filesystem نوشته می‌شود و فقط مسیر آن در state باقی می‌ماند.
"""

from typing import Any, Dict, List, Optional, TypedDict


class BuilderState(TypedDict, total=False):
    # ورودی خام کاربر
    user_idea: str
    project_name: str
    project_slug: str
    project_type: str

    # خروجی Product Analysis Agent
    pages: List[Dict[str, Any]]           # [{slug, title, purpose, sections:[...]}]
    target_audience: str
    key_features: List[str]

    # خروجی Design System Agent
    design_tokens: Dict[str, Any]         # typography, spacing, radius, grid

    # خروجی Color & Branding Agent
    brand: Dict[str, Any]                 # {light:{...}, dark:{...}, mood, primary}

    # خروجی UI Components Agent
    components: List[Dict[str, Any]]      # [{name, description, props, code_path, used_in}]

    # خروجی Animation Agent
    animations: List[Dict[str, Any]]

    # خروجی Frontend Developer Agent
    code_files: Dict[str, str]            # relative_path -> filesystem full path

    # خروجی Code Review Agent
    review: Dict[str, Any]

    # خروجی Skill System
    skills_output: Dict[str, Any]

    # زیرساخت Deep Agent (مدیریت‌شده توسط Coordinator)
    context_log: List[str]
    errors: List[str]
