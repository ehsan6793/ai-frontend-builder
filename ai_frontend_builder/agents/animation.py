"""
Animation Agent
-----------------
مسئولیت: تعریف Animation و Micro-interaction برای کامپوننت‌های تولیدشده.
خروجی این Agent به‌صورت کلاس‌های Tailwind (transition/animate) و چند
Keyframe سفارشی در tailwind.config.ts استفاده می‌شود؛ به این ترتیب بدون
نیاز به کتابخانه‌ی سنگین انیمیشن، حس تعامل و روانی به رابط کاربری اضافه
می‌شود.
"""

from ai_frontend_builder.llm_provider import LLMProvider


class AnimationAgent:
    name = "Animation Agent"

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def run(self, state: dict) -> dict:
        components = state.get("components", [])

        def mock():
            rules = []
            for comp in components:
                name = comp["name"]
                if name in ("Hero", "CTASection"):
                    rules.append({"component": name, "on": "mount", "effect": "fade-in-up", "duration_ms": 600})
                elif "Grid" in name or "List" in name:
                    rules.append({"component": name, "on": "mount", "effect": "stagger-fade-in", "duration_ms": 400})
                elif "Button" in name or name in ("CheckoutButton",):
                    rules.append({"component": name, "on": "hover", "effect": "scale-105", "duration_ms": 150})
                elif "Card" in name:
                    rules.append({"component": name, "on": "hover", "effect": "shadow-lift", "duration_ms": 200})
                elif "Accordion" in name:
                    rules.append({"component": name, "on": "toggle", "effect": "height-expand", "duration_ms": 250})
                else:
                    rules.append({"component": name, "on": "mount", "effect": "fade-in", "duration_ms": 300})
            return {
                "rules": rules,
                "global_transition": "all 150ms ease-in-out",
                "reduced_motion_respected": True,
            }

        result = self.llm.generate(
            system_prompt=(
                "تو Animation Agent هستی. برای هر کامپوننت یک افکت مناسب و ملایم "
                "(بدون شلوغی بصری) تعریف کن و به prefers-reduced-motion هم احترام "
                "بگذار. فقط JSON برگردان."
            ),
            user_prompt=str([c["name"] for c in components]),
            mock_fn=mock,
        ).raw

        state["animations"] = result["rules"]
        state.setdefault("context_log", []).append(
            f"[Animation] {len(result['rules'])} قانون انیمیشن تعریف شد | "
            f"reduced-motion رعایت شد: {result['reduced_motion_respected']}"
        )
        return state
