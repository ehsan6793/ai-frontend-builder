"""
filesystem_manager.py
----------------------
پیاده‌سازی Filesystem در معماری Deep Agent.

هر پروژه‌ای که کاربر می‌سازد یک Workspace مستقل می‌گیرد:

workspace/<project-slug>/
├── memory/project_memory.json
├── plan.json
├── docs/
│   ├── product_spec.md
│   └── design_system.md
├── design/
│   ├── tokens.json
│   └── figma_tokens.json         (اگر Skill Figma فعال باشد)
├── src/
│   ├── app/                      (صفحات Next.js)
│   ├── components/ui/            (Component Library)
│   └── styles/globals.css
├── tailwind.config.ts
├── package.json
└── review_report.md

این ماژول فقط مسئول ایجاد/نوشتن ایمن فایل‌ها در این ساختار است؛ منطق
تصمیم‌گیری درباره‌ی محتوا به Agentها تعلق دارد.
"""

import os
import re


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\u0600-\u06FF\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text[:40] or "project"


class FilesystemManager:
    def __init__(self, workspace_root: str, project_slug: str):
        self.root = os.path.join(workspace_root, project_slug)
        self.paths = {
            "root": self.root,
            "memory": os.path.join(self.root, "memory"),
            "docs": os.path.join(self.root, "docs"),
            "design": os.path.join(self.root, "design"),
            "src": os.path.join(self.root, "src"),
            "app": os.path.join(self.root, "src", "app"),
            "components": os.path.join(self.root, "src", "components", "ui"),
            "styles": os.path.join(self.root, "src", "styles"),
        }
        for p in self.paths.values():
            os.makedirs(p, exist_ok=True)

    def write(self, relative_key: str, filename: str, content: str) -> str:
        """relative_key یکی از کلیدهای self.paths است."""
        target_dir = self.paths[relative_key]
        os.makedirs(target_dir, exist_ok=True)
        full_path = os.path.join(target_dir, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path

    def write_root(self, filename: str, content: str) -> str:
        full_path = os.path.join(self.root, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path

    def list_tree(self) -> str:
        lines = []
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
            depth = dirpath.replace(self.root, "").count(os.sep)
            indent = "  " * depth
            lines.append(f"{indent}{os.path.basename(dirpath)}/")
            for fn in sorted(filenames):
                lines.append(f"{indent}  {fn}")
        return "\n".join(lines)
