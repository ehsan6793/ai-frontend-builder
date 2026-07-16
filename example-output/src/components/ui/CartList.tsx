import { cn } from "@/lib/utils";

export interface CartListProps {
  items?: any;
  onChange?: () => void;
}

/**
 * فهرست اقلام سبد خرید با امکان تغییر تعداد
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function CartList({ items, onChange }: CartListProps) {
  return (
    <section
      data-component="CartList"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">CartList</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        فهرست اقلام سبد خرید با امکان تغییر تعداد
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: items, onChange */}
    </section>
  );
}
