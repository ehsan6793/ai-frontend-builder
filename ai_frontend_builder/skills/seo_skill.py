from ai_frontend_builder.skills.base import Skill


class SEOSkill(Skill):
    name = "seo"
    description = "تولید متادیتای SEO (title، description، Open Graph) برای هر صفحه"

    def run(self, state: dict) -> dict:
        pages = state.get("pages", [])
        project_name = state.get("project_name", "پروژه")
        meta = {}
        for page in pages:
            title = f"{page['title']} | {project_name}"
            meta[page["slug"]] = {
                "title": title[:60],
                "description": f"{page['title']} در {project_name} — {page.get('purpose','')}"[:155],
                "og_title": title,
                "og_type": "website",
            }
        return {"pages_meta": meta}
