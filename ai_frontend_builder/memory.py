"""
memory.py
---------
پیاده‌سازی حافظه‌ی پروژه (Memory component در معماری Deep Agent).

دو نوع حافظه پیاده‌سازی شده:
1) Working Memory: در طول یک اجرا (run) در حافظه‌ی برنامه نگه داشته می‌شود
   و بین Agentها به اشتراک گذاشته می‌شود (بخشی از state گراف).
2) Persistent Memory: در انتهای هر اجرا روی دیسک ذخیره می‌شود
   (workspace/<project>/memory/project_memory.json) تا اگر کاربر دوباره
   سراغ همان پروژه برگردد، Agentها تصمیمات قبلی (رنگ برند، توکن‌های طراحی،
   نام کامپوننت‌ها و ...) را به خاطر بیاورند و یکپارچگی طراحی حفظ شود.
"""

import json
import os
from datetime import datetime, timezone


class ProjectMemory:
    def __init__(self, workspace_dir: str, project_slug: str):
        self.dir = os.path.join(workspace_dir, project_slug, "memory")
        os.makedirs(self.dir, exist_ok=True)
        self.path = os.path.join(self.dir, "project_memory.json")
        self.data = self._load()

    def _load(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "runs": [],
            "design_tokens": {},
            "brand": {},
            "pages": [],
            "components": [],
            "decisions_log": [],
        }

    def remember_decision(self, agent: str, decision: str):
        self.data["decisions_log"].append({
            "agent": agent,
            "decision": decision,
            "at": datetime.now(timezone.utc).isoformat(),
        })

    def update(self, key: str, value):
        self.data[key] = value

    def merge_dict(self, key: str, value: dict):
        self.data.setdefault(key, {})
        self.data[key].update(value)

    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def start_run(self, user_idea: str):
        self.data["runs"].append({
            "idea": user_idea,
            "at": datetime.now(timezone.utc).isoformat(),
        })

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def has_history(self) -> bool:
        return len(self.data.get("runs", [])) > 0
