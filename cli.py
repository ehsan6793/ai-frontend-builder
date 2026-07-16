#!/usr/bin/env python3
"""
cli.py
------
رابط کاربری خط فرمان (CLI) پروژه‌ی AI Frontend Builder.

نحوه اجرا:
    python cli.py                     # حالت تعاملی
    python cli.py "یک فروشگاه کفش آنلاین می‌خوام"
    python cli.py "..." --no-multi-page --no-theme
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text

from ai_frontend_builder.agents.coordinator import CoordinatorAgent

console = Console()

BANNER = r"""
   _    ___    _____                _                 _   ____        _ _     _
  / \  |_ _|  |  ___| __ ___  _ __ | |_ ___ _ __   __| | | __ ) _   _(_) | __| | ___ _ __
 / _ \  | |   | |_ | '__/ _ \| '_ \| __/ _ \ '_ \ / _` | |  _ \| | | | | |/ _` |/ _ \ '__|
/ ___ \ | |   |  _|| | | (_) | | | | ||  __/ | | | (_| | | |_) | |_| | | | (_| |  __/ |
/_/   \_\___|  |_|  |_|  \___/|_| |_|\__\___|_| |_|\__,_| |____/ \__,_|_|_|\__,_|\___|_|
"""


def render_plan(plan) -> Panel:
    return Panel(Text(plan.pretty(), justify="right"), title="📋 Todo Plan (Planning)", border_style="cyan")


def main():
    parser = argparse.ArgumentParser(description="AI Frontend Builder - Deep Agent CLI")
    parser.add_argument("idea", nargs="?", help="توضیح ایده‌ی محصول/وب‌سایت")
    parser.add_argument("--no-multi-page", action="store_true", help="غیرفعال کردن Multi Page Support")
    parser.add_argument("--no-theme", action="store_true", help="غیرفعال کردن Theme Generator (dark/light)")
    parser.add_argument("--workspace", default="workspace", help="مسیر Workspace خروجی")
    args = parser.parse_args()

    console.print(BANNER, style="bold magenta")
    console.print(
        "یک [bold]Deep Agent[/bold] چند-عاملی برای طراحی و تولید Frontend — "
        "پشتیبانی کامل از فارسی و RTL\n", style="dim"
    )

    idea = args.idea
    if not idea:
        console.print("[bold cyan]ایده‌ی خودت رو توصیف کن[/bold cyan] (مثال: یک فروشگاه آنلاین کفش می‌خوام با صفحه محصول و سبد خرید):")
        idea = console.input("> ")

    if not idea or not idea.strip():
        console.print("[red]ایده‌ای وارد نشد. خروج.[/red]")
        return

    coordinator = CoordinatorAgent(
        workspace_root=args.workspace,
        multi_page=not args.no_multi_page,
        theme_generator=not args.no_theme,
        on_step=lambda plan, *a, **k: live.update(render_plan(plan)) if 'live' in globals() else None,
    )

    console.print(f"\n[bold green]مد اجرا:[/bold green] {coordinator.llm.mode.upper()} "
                  f"({'با OpenAI API' if coordinator.llm.mode == 'openai' else 'بدون نیاز به API Key'})\n")

    global live
    from ai_frontend_builder.planner import build_default_plan
    with Live(render_plan(build_default_plan()), console=console, refresh_per_second=6) as live:
        final_state = coordinator.run(idea)

    console.print()
    console.print(Panel.fit(
        f"[bold]{final_state.get('project_name')}[/bold]\n"
        f"نوع پروژه: {final_state.get('project_type')}\n"
        f"تعداد صفحات: {len(final_state.get('pages', []))}\n"
        f"تعداد کامپوننت (Component Library): {len(final_state.get('components', []))}\n"
        f"امتیاز Code Review: {final_state.get('review', {}).get('score')}/100\n"
        f"مسیر خروجی: {final_state.get('_fs_root')}",
        title="✅ ساخت پروژه تمام شد", border_style="green",
    ))

    console.print("\n[bold]فایل‌های کلیدی تولید شده:[/bold]")
    console.print(f"  📄 {final_state['_fs_root']}/docs/product_spec.md")
    console.print(f"  🎨 {final_state['_fs_root']}/docs/design_system.md")
    console.print(f"  🧩 {final_state['_fs_root']}/docs/components.md")
    console.print(f"  📝 {final_state['_fs_root']}/review_report.md")
    if "figma_export" in final_state.get("skills_output", {}):
        console.print(f"  🎯 {final_state['_fs_root']}/design/figma_tokens.json  (Figma Export)")
    console.print(f"  💻 {final_state['_fs_root']}/src/  (کد کامل Next.js)")

    console.print("\n[dim]برای اجرای پروژه‌ی تولیدشده:[/dim]")
    console.print(f"  cd {final_state['_fs_root']} && npm install && npm run dev\n")


if __name__ == "__main__":
    main()
