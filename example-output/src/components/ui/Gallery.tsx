import { cn } from "@/lib/utils";

export interface GalleryProps {
  images?: any;
}

/**
 * گالری تصاویر با Lightbox
 * تولید شده توسط UI Components Agent — Deep Agent Frontend Builder
 */
export function Gallery({ images }: GalleryProps) {
  return (
    <section
      data-component="Gallery"
      className={cn(
        "w-full rounded-lg border border-[var(--color-border)]",
        "bg-[var(--color-surface)] p-6 transition-shadow duration-200",
        "hover:shadow-md"
      )}
    >
      <h3 className="text-lg font-medium text-[var(--color-text)]">Gallery</h3>
      <p className="mt-2 text-sm text-[var(--color-text-muted)]">
        گالری تصاویر با Lightbox
      </p>
      {/* TODO: پیاده‌سازی محتوای واقعی بر اساس props: images */}
    </section>
  );
}
