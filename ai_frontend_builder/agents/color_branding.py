"""
Color & Branding Agent
------------------------
مسئولیت: انتخاب پالت رنگ و هویت بصری بر اساس نوع پروژه.
شامل قابلیت امتیازی Theme Generator (Dark / Light) +۵: برای هر پروژه دو
ست کامل توکن رنگی (روشن و تاریک) تولید می‌شود که مستقیماً به CSS
Variables و استراتژی dark-mode کلاسیک Tailwind (class="dark") تبدیل
می‌گردد.
"""

from ai_frontend_builder.llm_provider import LLMProvider

# پالت پایه به ازای mood هر نوع پروژه — این خودِ "برندینگ" است که Agent
# بر اساس نوع محصول انتخاب می‌کند.
MOOD_PALETTES = {
    "ecommerce": {"primary": "#E11D48", "accent": "#F59E0B", "mood": "پرانرژی و متقاعدکننده"},
    "saas": {"primary": "#4F46E5", "accent": "#06B6D4", "mood": "حرفه‌ای و قابل‌اعتماد"},
    "portfolio": {"primary": "#111827", "accent": "#8B5CF6", "mood": "مینیمال و خلاقانه"},
    "blog": {"primary": "#0F766E", "accent": "#F59E0B", "mood": "گرم و خوانا"},
    "restaurant": {"primary": "#B91C1C", "accent": "#D97706", "mood": "اشتها آور و صمیمی"},
    "landing": {"primary": "#7C3AED", "accent": "#EC4899", "mood": "جسور و متمرکز روی تبدیل"},
    "dashboard": {"primary": "#2563EB", "accent": "#10B981", "mood": "دقیق و کم‌حجم بصری"},
    "education": {"primary": "#0284C7", "accent": "#F59E0B", "mood": "دوستانه و انگیزشی"},
    "generic": {"primary": "#4F46E5", "accent": "#F59E0B", "mood": "متعادل و مدرن"},
}


class ColorBrandingAgent:
    name = "Color & Branding Agent"

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def run(self, state: dict, theme_generator: bool = True) -> dict:
        project_type = state.get("project_type", "generic")

        def mock():
            base = MOOD_PALETTES.get(project_type, MOOD_PALETTES["generic"])
            light = {
                "primary": base["primary"],
                "accent": base["accent"],
                "background": "#FFFFFF",
                "surface": "#F9FAFB",
                "text": "#111827",
                "text_muted": "#6B7280",
                "border": "#E5E7EB",
                "success": "#16A34A",
                "warning": "#D97706",
                "danger": "#DC2626",
            }
            dark = {
                "primary": base["primary"],
                "accent": base["accent"],
                "background": "#0B0F19",
                "surface": "#111827",
                "text": "#F9FAFB",
                "text_muted": "#9CA3AF",
                "border": "#1F2937",
                "success": "#22C55E",
                "warning": "#F59E0B",
                "danger": "#EF4444",
            }
            themes = {"light": light}
            if theme_generator:
                themes["dark"] = dark
            return {"mood": base["mood"], "primary": base["primary"], "themes": themes}

        result = self.llm.generate(
            system_prompt=(
                "تو Color & Branding Agent هستی. بر اساس نوع پروژه یک پالت رنگ "
                "کامل (Light و در صورت نیاز Dark) با تضمین کنتراست مناسب برای "
                "متن روی پس‌زمینه تعریف کن و فقط JSON برگردان."
            ),
            user_prompt=f"project_type={project_type}",
            mock_fn=mock,
        ).raw

        state["brand"] = result
        # این توکن‌ها به design_tokens هم اضافه می‌شوند تا Figma Export و
        # Tailwind config به یک منبع واحد دسترسی داشته باشند.
        state.setdefault("design_tokens", {})["colors"] = result["themes"]["light"]
        state.setdefault("context_log", []).append(
            f"[Color & Branding] رنگ اصلی: {result['primary']} | حال‌وهوا: {result['mood']} | "
            f"تم‌ها: {', '.join(result['themes'].keys())}"
        )
        return state
