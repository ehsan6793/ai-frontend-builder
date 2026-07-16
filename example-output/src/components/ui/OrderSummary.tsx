import { cn } from "@/lib/utils";

export interface OrderSummaryProps {
  subtotal?: any;
  shipping?: any;
  total?: any;
}

/**
 * خلاصه‌ی مبلغ سفارش
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function OrderSummary({ subtotal, shipping, total }: OrderSummaryProps) {
  return (
    <section
      data-component="OrderSummary"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">OrderSummary</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        خلاصه‌ی مبلغ سفارش
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: subtotal, shipping, total */}
    </section>
  );
}
