"""
Coordinator Agent
--------------------
"مغز" معماری Deep Agent. مسئولیت‌ها:

1) ساخت Todo Plan اولیه (Planning) و به‌روزرسانی آن بعد از هر مرحله
2) ساخت/بارگذاری Memory پروژه (Persistent Memory)
3) اجرای گراف Multi-Agent با LangGraph (StateGraph) به ترتیب صحیح
4) نگهداری Context Digest فشرده بین Agentها (Context Management)
5) نوشتن مستندات نهایی و صداکردن Skill System
6) بسته‌بندی و گزارش خروجی نهایی از Filesystem

این فایل تنها جایی است که همه‌ی زیرسیستم‌ها را به هم متصل می‌کند؛ خودِ
Agentهای تخصصی هیچ‌کدام از بقیه خبر ندارند (Loose Coupling) — این دقیقاً
همان چیزی است که در معماری Deep Agent به‌عنوان Sub-Agent Support خواسته
شده است.
"""

import json
import os

from langgraph.graph import StateGraph, END

from ai_frontend_builder.agents.state import BuilderState
from ai_frontend_builder.agents.product_analysis import ProductAnalysisAgent
from ai_frontend_builder.agents.design_system import DesignSystemAgent
from ai_frontend_builder.agents.color_branding import ColorBrandingAgent
from ai_frontend_builder.agents.ui_components import UIComponentsAgent
from ai_frontend_builder.agents.animation import AnimationAgent
from ai_frontend_builder.agents.frontend_developer import FrontendDeveloperAgent
from ai_frontend_builder.agents.code_review import CodeReviewAgent

from ai_frontend_builder.llm_provider import LLMProvider
from ai_frontend_builder.memory import ProjectMemory
from ai_frontend_builder.planner import build_default_plan, save_plan
from ai_frontend_builder.context_manager import ContextDigest
from ai_frontend_builder.filesystem_manager import FilesystemManager, slugify
from ai_frontend_builder.skills.base import SkillRegistry


class CoordinatorAgent:
    name = "Coordinator Agent"

    def __init__(self, workspace_root: str = "workspace", multi_page: bool = True,
                 theme_generator: bool = True, enabled_skills=None, on_step=None):
        self.workspace_root = workspace_root
        self.multi_page = multi_page
        self.theme_generator = theme_generator
        self.enabled_skills = enabled_skills  # None = همه Skillها فعال
        self.on_step = on_step or (lambda *a, **k: None)  # callback برای CLI (نمایش زنده)
        self.llm = LLMProvider()

    # ------------------------------------------------------------------
    def run(self, user_idea: str) -> dict:
        # 1) Filesystem + Memory برای این پروژه
        # یک تشخیص سریع (بدون نیاز به LLM) فقط برای ساخت اسلاگ تمیز؛
        # تحلیل کامل و رسمی همچنان توسط Product Analysis Agent در گراف انجام می‌شود.
        from ai_frontend_builder.llm_provider import detect_project_type, detect_project_name
        quick_type = detect_project_type(user_idea)
        quick_name = detect_project_name(user_idea, quick_type)
        temp_slug = slugify(quick_name)
        memory = ProjectMemory(self.workspace_root, temp_slug)
        memory.start_run(user_idea)

        # 2) Planning
        plan = build_default_plan()

        fs = FilesystemManager(self.workspace_root, temp_slug)
        save_plan(plan, os.path.join(fs.root, "plan.json"))

        initial_state: BuilderState = {
            "user_idea": user_idea,
            "project_slug": temp_slug,
            "context_log": [],
            "errors": [],
        }

        def step_callback(step_id, status, agent_name):
            plan.mark(step_id, status)
            save_plan(plan, os.path.join(fs.root, "plan.json"))
            self.on_step(plan, step_id, status, agent_name)

        graph_with_callback = self._rebuild_with_callback(fs, step_callback)

        final_state = graph_with_callback.invoke(initial_state)

        # 3) Skill System (Figma Export, SEO, Accessibility, ...)
        plan.mark("skills", "in_progress")
        step_callback("skills", "in_progress", "Skill System")
        registry = SkillRegistry()
        skills_output = registry.run_all(final_state, enabled=self.enabled_skills)
        final_state["skills_output"] = skills_output
        plan.mark("skills", "done")
        step_callback("skills", "done", "Skill System")

        # 4) نوشتن مستندات + خروجی Skillها روی Filesystem
        plan.mark("finalize", "in_progress")
        step_callback("finalize", "in_progress", self.name)
        self._write_docs_and_skill_outputs(fs, final_state, skills_output)

        # 5) به‌روزرسانی Memory (Persistent) برای اجرای بعدی همین پروژه
        memory.merge_dict("brand", final_state.get("brand", {}))
        memory.update("design_tokens", final_state.get("design_tokens", {}))
        memory.update("pages", final_state.get("pages", []))
        memory.update("components", final_state.get("components", []))
        for entry in final_state.get("context_log", []):
            memory.remember_decision(agent="pipeline", decision=entry)
        memory.save()

        plan.mark("finalize", "done")
        step_callback("finalize", "done", self.name)
        save_plan(plan, os.path.join(fs.root, "plan.json"))

        final_state["_fs_root"] = fs.root
        final_state["_plan"] = plan
        return final_state

    # ------------------------------------------------------------------
    def _rebuild_with_callback(self, fs: FilesystemManager, callback):
        pa = ProductAnalysisAgent(self.llm)
        ds = DesignSystemAgent(self.llm)
        cb = ColorBrandingAgent(self.llm)
        ui = UIComponentsAgent(self.llm)
        an = AnimationAgent(self.llm)
        fd = FrontendDeveloperAgent(self.llm, fs)
        cr = CodeReviewAgent(self.llm)

        graph = StateGraph(BuilderState)

        def node(step_id, agent_name, fn):
            def wrapped(state):
                callback(step_id, "in_progress", agent_name)
                state = fn(dict(state))
                callback(step_id, "done", agent_name)
                return state
            return wrapped

        graph.add_node("analysis", node("analysis", pa.name, lambda s: pa.run(s, multi_page=self.multi_page)))
        graph.add_node("design_system", node("design_system", ds.name, ds.run))
        graph.add_node("branding", node("branding", cb.name, lambda s: cb.run(s, theme_generator=self.theme_generator)))
        graph.add_node("components", node("components", ui.name, ui.run))
        graph.add_node("animation", node("animation", an.name, an.run))
        graph.add_node("codegen", node("codegen", fd.name, fd.run))
        graph.add_node("review", node("review", cr.name, cr.run))

        graph.set_entry_point("analysis")
        graph.add_edge("analysis", "design_system")
        graph.add_edge("design_system", "branding")
        graph.add_edge("branding", "components")
        graph.add_edge("components", "animation")
        graph.add_edge("animation", "codegen")
        graph.add_edge("codegen", "review")
        graph.add_edge("review", END)

        return graph.compile()

    # ------------------------------------------------------------------
    def _write_docs_and_skill_outputs(self, fs: FilesystemManager, state: dict, skills_output: dict):
        # product_spec.md
        pages_md = "\n".join(
            f"- **{p['title']}** (`/{p['slug']}`) — {p['purpose']}\n  - بخش‌ها: {', '.join(p['sections'])}"
            for p in state.get("pages", [])
        )
        fs.write("docs", "product_spec.md", f"""# Product Spec — {state.get('project_name')}

## ایده اولیه
{state.get('user_idea')}

## نوع پروژه
{state.get('project_type')}

## مخاطب هدف
{state.get('target_audience')}

## صفحات
{pages_md}

## ویژگی‌های کلیدی
{', '.join(state.get('key_features', []))}
""")

        # design_system.md
        tokens = state.get("design_tokens", {})
        brand = state.get("brand", {})
        fs.write("docs", "design_system.md", f"""# Design System — {state.get('project_name')}

## Typography
- فونت: {tokens.get('typography', {}).get('font_family')}
- اندازه‌ها: {json.dumps(tokens.get('typography', {}).get('sizes', {}), ensure_ascii=False)}

## Spacing
{json.dumps(tokens.get('spacing', {}), ensure_ascii=False)}

## Radius
{json.dumps(tokens.get('radius', {}), ensure_ascii=False)}

## Brand / Theme(s)
- رنگ اصلی: {brand.get('primary')}
- حال‌وهوا: {brand.get('mood')}
- تم‌های موجود: {', '.join(brand.get('themes', {}).keys())}

## Grid
{json.dumps(tokens.get('grid', {}), ensure_ascii=False)}
""")

        # design/tokens.json (خام، برای استفاده مجدد)
        fs.write("design", "tokens.json", json.dumps(tokens, ensure_ascii=False, indent=2))
        fs.write("design", "brand.json", json.dumps(brand, ensure_ascii=False, indent=2))

        # review_report.md
        review = state.get("review", {})
        issues_md = "\n".join(f"- ⚠️ {i}" for i in review.get("issues", [])) or "- ✅ مشکلی یافت نشد"
        fs.write_root("review_report.md", f"""# Code Review Report

**امتیاز کیفیت:** {review.get('score')}/100
**نتیجه:** {review.get('verdict')}

## بررسی‌های انجام‌شده
{chr(10).join('- ' + c for c in review.get('checks_passed', []))}

## مشکلات یافت‌شده
{issues_md}
""")

        # خروجی Skillها
        if "figma_export" in skills_output:
            fx = skills_output["figma_export"]
            fs.write("design", "figma_tokens.json", json.dumps(fx["figma_tokens_json"], ensure_ascii=False, indent=2))
            fs.write("design", "figma_frames_spec.json", json.dumps(fx["frames_spec"], ensure_ascii=False, indent=2))
            fs.write("docs", "figma_import_guide.md", f"# راهنمای Import به Figma\n\n{fx['import_instructions']}\n")

        if "seo" in skills_output:
            fs.write("docs", "seo_meta.json", json.dumps(skills_output["seo"]["pages_meta"], ensure_ascii=False, indent=2))

        if "accessibility" in skills_output:
            fs.write("docs", "accessibility_report.json", json.dumps(skills_output["accessibility"], ensure_ascii=False, indent=2))

        # components.md (کاتالوگ کتابخانه کامپوننت)
        comp_md = "\n".join(
            f"### {c['name']}\n{c['description']}\n\n**Props:** `{', '.join(c.get('props', [])) or '—'}`\n"
            f"**استفاده‌شده در:** {', '.join(c.get('reused_in_pages', [c.get('used_in','')]))}\n"
            for c in state.get("components", [])
        )
        fs.write("docs", "components.md", f"# Component Library — {state.get('project_name')}\n\n{comp_md}")

        # README نهایی پروژه‌ی خروجی (خودِ Next.js app)
        fs.write_root("README.md", f"""# {state.get('project_name')}

این پروژه به‌صورت خودکار توسط **AI Frontend Builder (Deep Agent)** ساخته شده است.

## اجرا
```bash
npm install
npm run dev
```

## ساختار
- `src/app` — صفحات (Next.js App Router)
- `src/components/ui` — کتابخانه‌ی کامپوننت‌های قابل استفاده مجدد
- `design/tokens.json` — Design Tokens
- `design/figma_tokens.json` — قابل Import در پلاگین Figma Tokens
- `docs/` — مستندات کامل تصمیمات طراحی و محصول
- `review_report.md` — گزارش Code Review خودکار

جزئیات کامل تصمیمات در `docs/product_spec.md` و `docs/design_system.md` موجود است.
""")
