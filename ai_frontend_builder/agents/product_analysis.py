"""
Product Analysis Agent
-----------------------
مسئولیت: خواندن ایده‌ی خام کاربر و استخراج:
- نوع محصول / نام پروژه
- مخاطب هدف
- فهرست صفحات (Multi Page Support - امتیازی +۱۰)
- ویژگی‌های کلیدی هر صفحه

خروجی این Agent، ورودی مستقیم Design System و Frontend Developer است.
"""

from ai_frontend_builder.llm_provider import (
    LLMProvider, detect_project_type, detect_project_name,
)

PAGE_TEMPLATES = {
    "ecommerce": [
        ("home", "صفحه اصلی", "معرفی برند و محصولات ویژه", ["Hero", "FeaturedProducts", "Categories", "Newsletter"]),
        ("products", "لیست محصولات", "نمایش و فیلتر محصولات", ["FilterSidebar", "ProductGrid", "Pagination"]),
        ("product-detail", "جزئیات محصول", "نمایش کامل یک محصول و افزودن به سبد", ["Gallery", "ProductInfo", "Reviews", "RelatedProducts"]),
        ("cart", "سبد خرید", "مدیریت اقلام سبد خرید و پرداخت", ["CartList", "OrderSummary", "CheckoutButton"]),
    ],
    "saas": [
        ("home", "صفحه اصلی", "معرفی ارزش پیشنهادی محصول", ["Hero", "FeaturesGrid", "PricingTeaser", "Testimonials"]),
        ("pricing", "قیمت‌گذاری", "مقایسه پلن‌های اشتراک", ["PricingTable", "FAQAccordion"]),
        ("dashboard", "داشبورد کاربر", "نمای کلی وضعیت حساب کاربر", ["StatsCards", "ActivityChart", "RecentItems"]),
        ("login", "ورود / ثبت‌نام", "احراز هویت کاربر", ["AuthForm", "SocialLogin"]),
    ],
    "portfolio": [
        ("home", "صفحه اصلی", "معرفی سریع و شاخص‌ترین کارها", ["Hero", "SkillsList", "FeaturedProjects"]),
        ("projects", "نمونه‌کارها", "گالری کامل پروژه‌ها", ["ProjectGrid", "FilterTags"]),
        ("about", "درباره من", "معرفی کامل و مسیر حرفه‌ای", ["Bio", "Timeline", "Skills"]),
        ("contact", "تماس با من", "فرم تماس و شبکه‌های اجتماعی", ["ContactForm", "SocialLinks"]),
    ],
    "blog": [
        ("home", "صفحه اصلی", "آخرین مقالات و دسته‌بندی‌ها", ["Hero", "LatestPosts", "CategoryList"]),
        ("post", "مقاله", "نمایش کامل یک مقاله", ["PostHeader", "PostContent", "CommentSection"]),
        ("category", "دسته‌بندی", "فهرست مقالات یک دسته", ["PostGrid", "Pagination"]),
        ("about", "درباره ما", "معرفی تیم و هدف وبلاگ", ["Bio"]),
    ],
    "restaurant": [
        ("home", "صفحه اصلی", "معرفی فضا و غذاهای ویژه", ["Hero", "SignatureDishes", "Reservation"]),
        ("menu", "منو", "فهرست کامل غذاها و قیمت‌ها", ["MenuCategories", "MenuItemCard"]),
        ("reservation", "رزرو میز", "فرم رزرو آنلاین", ["ReservationForm"]),
        ("about", "درباره ما", "داستان رستوران", ["Bio", "Gallery"]),
    ],
    "landing": [
        ("home", "صفحه فرود", "تمرکز کامل روی تبدیل کاربر به مشتری", ["Hero", "SocialProof", "FeaturesGrid", "CTASection", "FAQAccordion"]),
    ],
    "dashboard": [
        ("home", "نمای کلی", "خلاصه‌ی وضعیت سیستم", ["StatsCards", "ActivityChart", "AlertsList"]),
        ("reports", "گزارش‌ها", "گزارش‌های تفصیلی و فیلترپذیر", ["ReportTable", "FilterBar", "ExportButton"]),
        ("settings", "تنظیمات", "پیکربندی حساب و سیستم", ["SettingsForm", "TeamMembers"]),
    ],
    "education": [
        ("home", "صفحه اصلی", "معرفی دوره‌ها و مزیت‌ها", ["Hero", "CoursesGrid", "Testimonials"]),
        ("course-detail", "جزئیات دوره", "سرفصل و ثبت‌نام دوره", ["CourseHeader", "Curriculum", "EnrollCard"]),
        ("my-courses", "دوره‌های من", "پیگیری پیشرفت یادگیری", ["ProgressList", "CertificateCard"]),
    ],
    "generic": [
        ("home", "صفحه اصلی", "معرفی کلی محصول یا خدمت", ["Hero", "FeaturesGrid", "CTASection"]),
        ("about", "درباره ما", "معرفی کامل", ["Bio"]),
        ("contact", "تماس با ما", "فرم تماس", ["ContactForm"]),
    ],
}


class ProductAnalysisAgent:
    name = "Product Analysis Agent"

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def run(self, state: dict, multi_page: bool = True) -> dict:
        idea = state["user_idea"]

        def mock():
            ptype = detect_project_type(idea)
            pname = detect_project_name(idea, ptype)
            pages_raw = PAGE_TEMPLATES.get(ptype, PAGE_TEMPLATES["generic"])
            if not multi_page:
                pages_raw = pages_raw[:1]
            pages = [
                {"slug": slug, "title": title, "purpose": purpose, "sections": sections}
                for slug, title, purpose, sections in pages_raw
            ]
            return {
                "project_type": ptype,
                "project_name": pname,
                "pages": pages,
                "target_audience": "کاربرانی که به‌دنبال تجربه‌ای سریع، ساده و بومی‌سازی‌شده (فارسی/RTL) هستند",
                "key_features": sorted({sec for _, _, _, secs in pages_raw for sec in secs}),
            }

        result = self.llm.generate(
            system_prompt=(
                "تو Product Analysis Agent هستی. بر اساس ایده‌ی کاربر، نوع محصول، "
                "نام پروژه، مخاطب هدف و فهرست صفحات لازم (هرکدام با بخش‌های داخلی) "
                "را استخراج کن و فقط JSON برگردان."
            ),
            user_prompt=idea,
            mock_fn=mock,
        ).raw

        state.update({
            "project_type": result["project_type"],
            "project_name": result["project_name"],
            "pages": result["pages"],
            "target_audience": result["target_audience"],
            "key_features": result["key_features"],
        })
        state.setdefault("context_log", []).append(
            f"[Product Analysis] نوع پروژه: {result['project_type']} | "
            f"{len(result['pages'])} صفحه شناسایی شد: "
            f"{', '.join(p['title'] for p in result['pages'])}"
        )
        return state
