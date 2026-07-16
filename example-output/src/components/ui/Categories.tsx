import { cn } from "@/lib/utils";

export interface CategoriesProps {
  categories?: any;
}

/**
 * دسته‌بندی‌های محصول در صفحه اصلی
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function Categories({ categories }: CategoriesProps) {
  return (
    <section
      data-component="Categories"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">Categories</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        دسته‌بندی‌های محصول در صفحه اصلی
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: categories */}
    </section>
  );
}
