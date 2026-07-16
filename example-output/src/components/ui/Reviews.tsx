import { cn } from "@/lib/utils";

export interface ReviewsProps {
  reviews?: any;
}

/**
 * فهرست نظرات کاربران
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function Reviews({ reviews }: ReviewsProps) {
  return (
    <section
      data-component="Reviews"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">Reviews</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        فهرست نظرات کاربران
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: reviews */}
    </section>
  );
}
