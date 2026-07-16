import { cn } from "@/lib/utils";

export interface FilterSidebarProps {
  filters?: any;
  onChange?: () => void;
}

/**
 * سایدبار فیلتر محصولات
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function FilterSidebar({ filters, onChange }: FilterSidebarProps) {
  return (
    <section
      data-component="FilterSidebar"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">FilterSidebar</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        سایدبار فیلتر محصولات
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: filters, onChange */}
    </section>
  );
}
