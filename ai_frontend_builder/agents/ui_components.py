"""
UI Components Agent
---------------------
مسئولیت: تبدیل بخش‌های هر صفحه (sections) که Product Analysis Agent
استخراج کرده، به یک فهرست کامپوننت یکتا با Props مشخص. کامپوننت‌های
تکراری بین صفحات (مثلاً Hero در چند صفحه) فقط یک بار تعریف می‌شوند —
همین رفتار پایه‌ی قابلیت امتیازی Component Library (+۱۰) است: خروجی یک
کتابخانه‌ی کامپوننت قابل استفاده‌ی مجدد در src/components/ui است، نه
کدهای تکراری per-page.
"""

from ai_frontend_builder.llm_provider import LLMProvider

# توضیح و props پیش‌فرض برای پرتکرارترین کامپوننت‌ها — بقیه fallback عمومی می‌گیرند
COMPONENT_SPECS = {
    "Hero": {"description": "بخش ابتدایی صفحه با تیتر، توضیح کوتاه و CTA", "props": ["title", "subtitle", "ctaText", "ctaHref"]},
    "FeaturesGrid": {"description": "گرید نمایش ویژگی‌های محصول", "props": ["items"]},
    "FeaturedProducts": {"description": "اسلایدر/گرید محصولات ویژه", "props": ["products"]},
    "ProductGrid": {"description": "گرید محصولات با صفحه‌بندی", "props": ["products", "columns"]},
    "ProductInfo": {"description": "اطلاعات قیمت و انتخاب گزینه‌های محصول", "props": ["product"]},
    "Gallery": {"description": "گالری تصاویر با Lightbox", "props": ["images"]},
    "Reviews": {"description": "فهرست نظرات کاربران", "props": ["reviews"]},
    "RelatedProducts": {"description": "پیشنهاد محصولات مرتبط", "props": ["products"]},
    "CartList": {"description": "فهرست اقلام سبد خرید با امکان تغییر تعداد", "props": ["items", "onChange"]},
    "OrderSummary": {"description": "خلاصه‌ی مبلغ سفارش", "props": ["subtotal", "shipping", "total"]},
    "CheckoutButton": {"description": "دکمه‌ی نهایی‌سازی خرید", "props": ["disabled", "onClick"]},
    "PricingTable": {"description": "جدول مقایسه‌ی پلن‌های قیمت‌گذاری", "props": ["plans"]},
    "FAQAccordion": {"description": "آکاردئون سوالات متداول", "props": ["items"]},
    "StatsCards": {"description": "کارت‌های آماری خلاصه", "props": ["stats"]},
    "ActivityChart": {"description": "نمودار فعالیت زمانی", "props": ["data"]},
    "RecentItems": {"description": "فهرست آخرین موارد", "props": ["items"]},
    "AuthForm": {"description": "فرم ورود/ثبت‌نام", "props": ["mode", "onSubmit"]},
    "SocialLogin": {"description": "دکمه‌های ورود با شبکه‌های اجتماعی", "props": ["providers"]},
    "SkillsList": {"description": "فهرست مهارت‌ها با سطح تسلط", "props": ["skills"]},
    "FeaturedProjects": {"description": "نمایش پروژه‌های شاخص", "props": ["projects"]},
    "ProjectGrid": {"description": "گرید کامل پروژه‌ها با فیلتر", "props": ["projects", "tags"]},
    "FilterTags": {"description": "تگ‌های فیلتر کردن محتوا", "props": ["tags", "onSelect"]},
    "Bio": {"description": "بخش معرفی/بیوگرافی", "props": ["name", "role", "text", "avatarUrl"]},
    "Timeline": {"description": "تایم‌لاین مسیر حرفه‌ای", "props": ["events"]},
    "Skills": {"description": "نمایش بصری مهارت‌ها", "props": ["skills"]},
    "ContactForm": {"description": "فرم تماس", "props": ["onSubmit"]},
    "SocialLinks": {"description": "لینک شبکه‌های اجتماعی", "props": ["links"]},
    "LatestPosts": {"description": "فهرست آخرین مقالات", "props": ["posts"]},
    "CategoryList": {"description": "فهرست دسته‌بندی مقالات", "props": ["categories"]},
    "PostHeader": {"description": "هدر مقاله شامل تیتر و نویسنده", "props": ["title", "author", "date"]},
    "PostContent": {"description": "بدنه‌ی محتوای مقاله", "props": ["html"]},
    "CommentSection": {"description": "بخش نظرات مقاله", "props": ["comments", "onSubmit"]},
    "PostGrid": {"description": "گرید مقالات یک دسته", "props": ["posts"]},
    "Pagination": {"description": "صفحه‌بندی عمومی", "props": ["page", "totalPages", "onChange"]},
    "SignatureDishes": {"description": "معرفی غذاهای ویژه رستوران", "props": ["dishes"]},
    "Reservation": {"description": "دعوت به رزرو میز", "props": ["onReserve"]},
    "MenuCategories": {"description": "دسته‌بندی‌های منو", "props": ["categories"]},
    "MenuItemCard": {"description": "کارت یک آیتم منو", "props": ["item"]},
    "ReservationForm": {"description": "فرم کامل رزرو میز", "props": ["onSubmit"]},
    "SocialProof": {"description": "لوگو/آمار اعتمادسازی", "props": ["logos", "stats"]},
    "CTASection": {"description": "بخش دعوت به اقدام نهایی", "props": ["title", "ctaText", "ctaHref"]},
    "ReportTable": {"description": "جدول گزارش با مرتب‌سازی", "props": ["rows", "columns"]},
    "FilterBar": {"description": "نوار فیلتر داده‌ها", "props": ["filters", "onChange"]},
    "ExportButton": {"description": "دکمه خروجی گرفتن از داده", "props": ["onExport"]},
    "SettingsForm": {"description": "فرم تنظیمات حساب", "props": ["values", "onSubmit"]},
    "TeamMembers": {"description": "مدیریت اعضای تیم", "props": ["members"]},
    "CoursesGrid": {"description": "گرید دوره‌های آموزشی", "props": ["courses"]},
    "Testimonials": {"description": "نظرات کاربران/دانشجویان", "props": ["items"]},
    "CourseHeader": {"description": "هدر صفحه‌ی جزئیات دوره", "props": ["title", "instructor", "price"]},
    "Curriculum": {"description": "سرفصل‌های دوره", "props": ["sections"]},
    "EnrollCard": {"description": "کارت ثبت‌نام و قیمت", "props": ["price", "onEnroll"]},
    "ProgressList": {"description": "پیشرفت دوره‌های در حال گذراندن", "props": ["items"]},
    "CertificateCard": {"description": "نمایش گواهی‌نامه‌ها", "props": ["certificates"]},
    "AlertsList": {"description": "فهرست هشدارهای سیستم", "props": ["alerts"]},
    "PricingTeaser": {"description": "معرفی کوتاه پلن‌ها در صفحه اصلی", "props": ["plans"]},
    "Categories": {"description": "دسته‌بندی‌های محصول در صفحه اصلی", "props": ["categories"]},
    "Newsletter": {"description": "فرم عضویت در خبرنامه", "props": ["onSubmit"]},
    "FilterSidebar": {"description": "سایدبار فیلتر محصولات", "props": ["filters", "onChange"]},
}


class UIComponentsAgent:
    name = "UI Components Agent"

    def __init__(self, llm: LLMProvider):
        self.llm = llm

    def run(self, state: dict) -> dict:
        pages = state.get("pages", [])

        def mock():
            seen = {}
            for page in pages:
                for section in page["sections"]:
                    spec = COMPONENT_SPECS.get(section, {
                        "description": f"کامپوننت {section}", "props": ["data"],
                    })
                    if section not in seen:
                        seen[section] = {
                            "name": section,
                            "description": spec["description"],
                            "props": spec["props"],
                            "used_in": page["slug"],   # اولین صفحه‌ای که استفاده‌اش کرد
                            "reused_in_pages": [page["slug"]],
                        }
                    else:
                        seen[section]["reused_in_pages"].append(page["slug"])
            return {"components": list(seen.values())}

        result = self.llm.generate(
            system_prompt=(
                "تو UI Components Agent هستی. بخش‌های تکراری بین صفحات را "
                "شناسایی کن و به‌عنوان یک کامپوننت واحد و قابل استفاده مجدد "
                "با props مشخص تعریف کن. فقط JSON برگردان."
            ),
            user_prompt=str(pages),
            mock_fn=mock,
        ).raw

        state["components"] = result["components"]
        reused = sum(1 for c in result["components"] if len(c.get("reused_in_pages", [])) > 1)
        state.setdefault("context_log", []).append(
            f"[UI Components] {len(result['components'])} کامپوننت یکتا ساخته شد "
            f"({reused} مورد بین چند صفحه بازاستفاده شد → Component Library)"
        )
        return state
