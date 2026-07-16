"""
Design System Agent
--------------------
مسئولیت: تعریف Design Tokens مستقل از رنگ (که وظیفه‌ی Color & Branding
Agent است): Typography scale، Spacing scale، Border Radius، Grid/Breakpoints.
این توکن‌ها بعداً هم در Tailwind config و هم در Figma Export استفاده
می‌شوند تا یکپارچگی طراحی در کل پروژه حفظ شود (Design Consistency).
"""

from ai_frontend_builder.llm_provider import LLMProvider


class DesignSystemAgent:
    name = "Design System Agent"

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def run(self, state: dict) -> dict:
        project_type = state.get("project_type", "generic")

        def mock():
            # چگالی محتوا بر اساس نوع پروژه کمی جمع‌وجورتر/باز تر می‌شود
            dense = project_type in ("dashboard", "ecommerce", "saas")
            return {
                "typography": {
                    "font_family": "Vazirmatn, sans-serif",
                    "sizes": {
                        "xs": "0.75rem", "sm": "0.875rem", "base": "1rem",
                        "lg": "1.125rem", "xl": "1.25rem", "2xl": "1.5rem",
                        "3xl": "1.875rem", "4xl": "2.25rem",
                    },
                    "weights": {"regular": 400, "medium": 500, "bold": 700},
                    "line_height": "1.7",
                },
                "spacing": {
                    "xs": "0.5rem", "sm": "0.75rem", "md": "1rem",
                    "lg": "1.5rem", "xl": "2rem", "2xl": "3rem",
                },
                "radius": {"sm": "0.375rem", "md": "0.5rem", "lg": "0.75rem", "full": "9999px"},
                "grid": {
                    "container_max_width": "1280px" if dense else "1120px",
                    "columns": 12,
                    "gutter": "1.5rem",
                    "breakpoints": {"sm": "640px", "md": "768px", "lg": "1024px", "xl": "1280px"},
                },
                "direction": "rtl",
                "density": "compact" if dense else "comfortable",
            }

        tokens = self.llm.generate(
            system_prompt=(
                "تو Design System Agent هستی. بر اساس نوع پروژه، توکن‌های "
                "Typography، Spacing، Radius و Grid را (سازگار با RTL و فونت "
                "فارسی Vazirmatn) به‌صورت JSON تعریف کن."
            ),
            user_prompt=f"project_type={project_type}",
            mock_fn=mock,
        ).raw

        state["design_tokens"] = tokens
        state.setdefault("context_log", []).append(
            f"[Design System] فونت: {tokens['typography']['font_family']} | "
            f"چگالی: {tokens['density']} | جهت: {tokens['direction']}"
        )
        return state
