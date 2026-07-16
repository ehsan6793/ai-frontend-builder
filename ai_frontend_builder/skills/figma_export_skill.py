"""
figma_export_skill.py
----------------------
Skill امتیازی: Figma Export (+۱۰)

نکته‌ی صادقانه‌ی فنی: ساخت فایل باینری .fig نیازمند Figma REST API و
OAuth Token شخصی کاربر است و از بیرون Figma قابل تولید نیست. راه استاندارد
صنعتی برای "خروجی گرفتن به Figma" بدون دسترسی API، تولید یک فایل
Design Tokens با فرمت مورد قبول پلاگین معروف "Figma Tokens / Tokens
Studio" است — کاربر با نصب همین پلاگین (رایگان) در Figma، این فایل را
Import می‌کند و تمام رنگ‌ها/تایپوگرافی/spacing به‌صورت Local Styles و
Variables در Figma ساخته می‌شود. این Skill دقیقاً همین فایل را می‌سازد،
به‌علاوه یک Layout Spec (frames.json) که ساختار صفحات و کامپوننت‌ها را
برای بازسازی سریع در Figma توصیف می‌کند.
"""

import json

from ai_frontend_builder.skills.base import Skill


class FigmaExportSkill(Skill):
    name = "figma_export"
    description = "تولید فایل Design Tokens سازگار با پلاگین Figma Tokens + Layout Spec"

    def run(self, state: dict) -> dict:
        tokens = state.get("design_tokens", {})
        colors = tokens.get("colors", {})
        typography = tokens.get("typography", {})
        spacing = tokens.get("spacing", {})

        figma_tokens = {
            "global": {
                "color": {
                    name: {"value": value, "type": "color"}
                    for name, value in colors.items()
                },
                "fontSize": {
                    name: {"value": str(value).replace("rem", ""), "type": "fontSizes"}
                    for name, value in typography.get("sizes", {}).items()
                },
                "spacing": {
                    name: {"value": str(value).replace("rem", ""), "type": "spacing"}
                    for name, value in spacing.items()
                },
            },
            "$themes": [],
            "$metadata": {"tokenSetOrder": ["global"]},
        }

        frames = []
        for page in state.get("pages", []):
            frames.append({
                "frame": page["title"],
                "width": 1440,
                "sections": [c["name"] for c in state.get("components", [])
                             if c.get("used_in") in (None, page["slug"])],
            })

        return {
            "figma_tokens_json": figma_tokens,
            "frames_spec": frames,
            "import_instructions": (
                "۱) پلاگین رایگان 'Figma Tokens' (Tokens Studio) را در Figma نصب کن.\n"
                "۲) از داخل پلاگین گزینه Import را بزن و فایل design/figma_tokens.json را انتخاب کن.\n"
                "۳) با دکمه Apply to document، تمام رنگ‌ها/تایپوگرافی/spacing به صورت "
                "Styles و Variables در فایل Figma ساخته می‌شوند.\n"
                "۴) از design/figma_frames_spec.json برای بازسازی سریع چیدمان صفحات "
                "به‌عنوان راهنما استفاده کن."
            ),
        }
