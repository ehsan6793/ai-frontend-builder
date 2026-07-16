"""
Frontend Developer Agent
--------------------------
مسئولیت: تبدیل تمام تصمیمات Agentهای قبلی (صفحات، توکن‌های طراحی، برند،
کامپوننت‌ها، انیمیشن‌ها) به کد واقعی و قابل اجرای Next.js 14 (App Router)
+ TypeScript + Tailwind CSS + الگوی shadcn/ui.

این Agent مستقیماً روی FilesystemManager می‌نویسد (نه فقط در state)،
چون خروجی نهایی این پروژه باید یک Workspace واقعی از فایل باشد.
"""

import json

from ai_frontend_builder.filesystem_manager import FilesystemManager
from ai_frontend_builder.llm_provider import LLMProvider


def _to_pascal(name: str) -> str:
    # اگر نام از قبل بدون جداکننده است (مثل "FeaturedProducts")، همان‌طور که
    # هست نگه‌داشته می‌شود تا حروف بزرگ داخلی از بین نروند.
    if " " not in name and "-" not in name and "_" not in name:
        return name[0].upper() + name[1:] if name else name
    parts = name.replace("-", " ").replace("_", " ").split()
    return "".join(p[0].upper() + p[1:] for p in parts if p)


def _props_interface(name: str, props: list[str]) -> str:
    if not props:
        return f"export interface {name}Props {{}}\n"
    lines = [f"export interface {name}Props {{"]
    for p in props:
        ptype = "() => void" if p.lower().startswith("on") else "any"
        lines.append(f"  {p}?: {ptype};")
    lines.append("}\n")
    return "\n".join(lines)


def _component_tsx(comp: dict) -> str:
    name = _to_pascal(comp["name"])
    props = comp.get("props", [])
    prop_names = ", ".join(props) if props else ""
    destructure = f"{{ {prop_names} }}: {name}Props" if props else f"_props: {name}Props"

    return f"""import {{ cn }} from "@/lib/utils";

{_props_interface(name, props)}
/**
 * {comp.get("description", "")}
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function {name}({destructure}) {{
  return (
    <section
      data-component="{name}"
      className={{cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">{name}</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        {comp.get("description", "")}
      </p>
      {{/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: {prop_names or "—"} */}}
    </section>
  );
}}
"""


def _page_tsx(page: dict, components_by_name: dict) -> str:
    used = [components_by_name[s] for s in page["sections"] if s in components_by_name]
    imports = "\n".join(
        f'import {{ {_to_pascal(c["name"])} }} from "@/components/ui/{_to_pascal(c["name"])}";'
        for c in used
    )
    body = "\n      ".join(f"<{_to_pascal(c['name'])} />" for c in used)
    return f"""{imports}

export const metadata = {{
  title: "{page['title']}",
  description: "{page['purpose']}",
}};

export default function Page() {{
  return (
    <main dir="rtl" className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-10">
      {body}
    </main>
  );
}}
"""


def _layout_tsx(project_name: str, has_dark: bool) -> str:
    theme_script = (
        """
        <script
          dangerouslySetInnerHTML={{
            __html: `
              try {
                const t = localStorage.getItem('theme');
                if (t === 'dark' || (!t && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                  document.documentElement.classList.add('dark');
                }
              } catch (e) {}
            `,
          }}
        />"""
        if has_dark else ""
    )
    return f"""import type {{ Metadata }} from "next";
import "./globals.css";

export const metadata: Metadata = {{
  title: "{project_name}",
  description: "ساخته‌شده توسط AI Frontend Builder — Deep Agent",
}};

export default function RootLayout({{ children }}: {{ children: React.ReactNode }}) {{
  return (
    <html lang="fa" dir="rtl">
      <head>{theme_script}
      </head>
      <body className="min-h-screen bg-[var(--color-background)] font-sans antialiased">
        {{children}}
      </body>
    </html>
  );
}}
"""


def _globals_css(tokens: dict, brand: dict) -> str:
    light = brand["themes"]["light"]
    dark = brand["themes"].get("dark")
    font = tokens["typography"]["font_family"]

    def vars_block(theme: dict) -> str:
        return "\n".join(f"  --color-{k.replace('_', '-')}: {v};" for k, v in theme.items())

    dark_block = ""
    if dark:
        dark_block = f"""
.dark {{
{vars_block(dark)}
}}
"""

    return f"""@import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/Vazirmatn-font-face.css');
@tailwind base;
@tailwind components;
@tailwind utilities;

:root {{
{vars_block(light)}
  --radius-md: {tokens['radius']['md']};
  --font-sans: {font};
}}
{dark_block}
* {{
  border-color: var(--color-border);
}}

body {{
  font-family: var(--font-sans);
}}

@media (prefers-reduced-motion: reduce) {{
  *, *::before, *::after {{
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }}
}}
"""


def _tailwind_config(tokens: dict, has_dark: bool, animations: list) -> str:
    keyframes = {
        "fade-in": "{ '0%': { opacity: '0' }, '100%': { opacity: '1' } }",
        "fade-in-up": "{ '0%': { opacity: '0', transform: 'translateY(8px)' }, '100%': { opacity: '1', transform: 'translateY(0)' } }",
    }
    dark_mode = '"class"' if has_dark else '"media"'
    return f"""import type {{ Config }} from "tailwindcss";

const config: Config = {{
  darkMode: {dark_mode},
  content: ["./src/**/*.{{ts,tsx}}"],
  theme: {{
    extend: {{
      fontFamily: {{
        sans: ["{tokens['typography']['font_family'].split(',')[0]}", "sans-serif"],
      }},
      borderRadius: {{
        sm: "{tokens['radius']['sm']}",
        md: "{tokens['radius']['md']}",
        lg: "{tokens['radius']['lg']}",
      }},
      keyframes: {{
        "fade-in": {keyframes['fade-in']},
        "fade-in-up": {keyframes['fade-in-up']},
      }},
      animation: {{
        "fade-in": "fade-in 0.3s ease-out",
        "fade-in-up": "fade-in-up 0.6s ease-out",
      }},
    }},
  }},
  plugins: [],
}};

export default config;
"""


def _package_json(project_slug: str) -> str:
    return json.dumps({
        "name": project_slug,
        "version": "0.1.0",
        "private": True,
        "scripts": {"dev": "next dev", "build": "next build", "start": "next start", "lint": "next lint"},
        "dependencies": {
            "next": "^14.2.0",
            "react": "^18.3.0",
            "react-dom": "^18.3.0",
            "clsx": "^2.1.0",
            "tailwind-merge": "^2.3.0",
        },
        "devDependencies": {
            "typescript": "^5.4.0",
            "tailwindcss": "^3.4.0",
            "postcss": "^8.4.0",
            "autoprefixer": "^10.4.0",
            "@types/react": "^18.3.0",
            "@types/node": "^20.11.0",
        },
    }, indent=2, ensure_ascii=False)


def _lib_utils_ts() -> str:
    return """import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
"""


class FrontendDeveloperAgent:
    name = "Frontend Developer Agent"

    def __init__(self, llm: LLMProvider, fs: FilesystemManager):
        self.llm = llm
        self.fs = fs

    def run(self, state: dict) -> dict:
        tokens = state["design_tokens"]
        brand = state["brand"]
        pages = state["pages"]
        components = state["components"]
        animations = state.get("animations", [])
        project_name = state["project_name"]
        project_slug = state["project_slug"]
        has_dark = "dark" in brand.get("themes", {})

        components_by_name = {c["name"]: c for c in components}
        written = {}

        # --- کامپوننت‌های کتابخانه (Component Library) ---
        barrel_lines = []
        for comp in components:
            pascal = _to_pascal(comp["name"])
            code = _component_tsx(comp)
            path = self.fs.write("components", f"{pascal}.tsx", code)
            written[f"components/{pascal}.tsx"] = path
            barrel_lines.append(f'export * from "./{pascal}";')
        index_path = self.fs.write("components", "index.ts", "\n".join(barrel_lines) + "\n")
        written["components/index.ts"] = index_path

        # --- lib/utils.ts (برای cn()) ---
        lib_dir_path = self.fs.write("src", "lib/utils.ts", _lib_utils_ts())
        written["src/lib/utils.ts"] = lib_dir_path

        # --- صفحات (Multi Page Support) ---
        for page in pages:
            page_code = _page_tsx(page, components_by_name)
            rel = "page.tsx" if page["slug"] == "home" else f"{page['slug']}/page.tsx"
            path = self.fs.write("app", rel, page_code)
            written[f"app/{rel}"] = path

        # --- layout, globals.css, tailwind.config.ts, package.json ---
        written["src/app/layout.tsx"] = self.fs.write("app", "layout.tsx", _layout_tsx(project_name, has_dark))
        written["src/app/globals.css"] = self.fs.write("app", "globals.css", _globals_css(tokens, brand))
        written["tailwind.config.ts"] = self.fs.write_root("tailwind.config.ts", _tailwind_config(tokens, has_dark, animations))
        written["package.json"] = self.fs.write_root("package.json", _package_json(project_slug))
        written["tsconfig.json"] = self.fs.write_root("tsconfig.json", json.dumps({
            "compilerOptions": {
                "target": "ES2017", "lib": ["dom", "dom.iterable", "esnext"],
                "jsx": "preserve", "module": "esnext", "moduleResolution": "bundler",
                "strict": True, "skipLibCheck": True, "esModuleInterop": True,
                "paths": {"@/*": ["./src/*"]},
            }
        }, indent=2))

        state["code_files"] = written
        state.setdefault("context_log", []).append(
            f"[Frontend Developer] {len(written)} فایل کد در workspace/{project_slug} نوشته شد "
            f"(Next.js + TypeScript + Tailwind, dark-mode={'بله' if has_dark else 'خیر'})"
        )
        return state
