import { cn } from "@/lib/utils";

export interface ProductInfoProps {
  product?: any;
}

/**
 * اطلاعات قیمت و انتخاب گزینه‌های محصول
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function ProductInfo({ product }: ProductInfoProps) {
  return (
    <section
      data-component="ProductInfo"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">ProductInfo</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        اطلاعات قیمت و انتخاب گزینه‌های محصول
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: product */}
    </section>
  );
}
