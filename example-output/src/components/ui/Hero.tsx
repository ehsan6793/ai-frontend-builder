import { cn } from "@/lib/utils";

export interface HeroProps {
  title?: any;
  subtitle?: any;
  ctaText?: any;
  ctaHref?: any;
}

/**
 * بخش ابتدایی صفحه با تیتر، توضیح کوتاه و CTA
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function Hero({ title, subtitle, ctaText, ctaHref }: HeroProps) {
  return (
    <section
      data-component="Hero"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">Hero</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        بخش ابتدایی صفحه با تیتر، توضیح کوتاه و CTA
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: title, subtitle, ctaText, ctaHref */}
    </section>
  );
}
