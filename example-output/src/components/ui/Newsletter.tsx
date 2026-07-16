import { cn } from "@/lib/utils";

export interface NewsletterProps {
  onSubmit?: () => void;
}

/**
 * فرم عضویت در خبرنامه
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function Newsletter({ onSubmit }: NewsletterProps) {
  return (
    <section
      data-component="Newsletter"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">Newsletter</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        فرم عضویت در خبرنامه
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: onSubmit */}
    </section>
  );
}
