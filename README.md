# AI Frontend Builder — Deep Agent

یک Agent چند-عاملی (Multi-Agent) که نقش یک تیم کامل طراحی و توسعه‌ی Frontend
را بازی می‌کند. کاربر فقط ایده‌ی محصول را به فارسی توضیح می‌دهد؛ سیستم به‌صورت
خودکار تحلیل نیاز، طراحی Design System، برندینگ، تولید کامپوننت، انیمیشن،
تولید کد Next.js/TypeScript/Tailwind و بازبینی کیفیت را انجام می‌دهد.

پیاده‌سازی‌شده به‌عنوان یک **Deep Agent** واقعی — نه صرفاً چند تابع پشت سر هم —
با پنج زیرسیستم مستقل: **Planning، Memory، Context Management، Filesystem،
Skill System** (جزئیات کامل در [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)).

## اجرای سریع (بدون نیاز به هیچ API Key)

```bash
pip install -r requirements.txt
python cli.py "یک فروشگاه آنلاین کفش می‌خوام با صفحه محصول و سبد خرید"
```

سیستم به‌صورت خودکار در **MOCK MODE** اجرا می‌شود (بدون نیاز به کلید) تا
دموی کامل بدون هزینه و بدون وابستگی به سرویس بیرونی قابل اجرا باشد.
اگر خواستی از مدل زبانی واقعی استفاده کنی:

```bash
cp .env.example .env
# OPENAI_API_KEY=sk-... را داخل .env قرار بده
python cli.py "..."
```

## پرچم‌های CLI

```bash
python cli.py "ایده" --no-multi-page   # فقط یک صفحه بساز
python cli.py "ایده" --no-theme        # فقط تم روشن (بدون Dark Mode)
python cli.py "ایده" --workspace out   # مسیر خروجی سفارشی
```

## ساختار مخزن

```
ai_frontend_builder/
├── llm_provider.py        # لایه انتزاعی مدل زبانی (OpenAI یا Mock)
├── memory.py               # Persistent Memory
├── planner.py               # Planning / Todo Plan
├── context_manager.py       # Context Management (خلاصه‌سازی)
├── filesystem_manager.py    # Filesystem Workspace
├── agents/
│   ├── coordinator.py       # هماهنگ‌کننده + گراف LangGraph
│   ├── product_analysis.py
│   ├── design_system.py
│   ├── color_branding.py    # + Theme Generator (dark/light)
│   ├── ui_components.py     # + Component Library
│   ├── animation.py
│   ├── frontend_developer.py
│   └── code_review.py
└── skills/
    ├── base.py               # Skill System (auto-discovery)
    ├── accessibility_skill.py
    ├── seo_skill.py
    └── figma_export_skill.py # + Figma Export

cli.py                        # رابط کاربری CLI
workspace/                     # خروجی هر پروژه (تولید در زمان اجرا)
example-output/                # یک نمونه خروجی از پیش تولیدشده برای مرور سریع
docs/
├── ARCHITECTURE.md            # توضیح کامل معماری Deep Agent
└── DEMO_SCRIPT.md             # راهنمای ضبط ویدیوی دمو
```

## پوشش معیارهای ارزیابی

| بخش | وضعیت |
|---|---|
| معماری Deep Agent | ✅ Planning + Memory + Context + Filesystem + Skill System |
| همکاری Agentها | ✅ ۸ Agent مجزا، هماهنگ‌شده توسط Coordinator روی LangGraph |
| Design System و UI | ✅ Design Tokens + پالت رنگ + RTL/فارسی |
| تولید کد | ✅ Next.js 14 (App Router) + TypeScript + Tailwind واقعی و اجراپذیر |
| Filesystem و Skill System | ✅ Workspace ساختاریافته + Skillهای Plug-in |
| Code Review | ✅ Agent مجزا با بررسی واقعی روی فایل‌های تولیدشده |
| رابط کاربری CLI | ✅ `cli.py` با نمایش زنده‌ی Plan |
| **Multi Page Support (+۱۰)** | ✅ |
| **Theme Generator (+۵)** | ✅ Light/Dark |
| **Component Library (+۱۰)** | ✅ کامپوننت‌های یکتا و بازاستفاده‌شونده |
| **Figma Export (+۱۰)** | ✅ خروجی سازگار با پلاگین Figma Tokens |
