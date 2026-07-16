import { Gallery } from "@/components/ui/Gallery";
import { ProductInfo } from "@/components/ui/ProductInfo";
import { Reviews } from "@/components/ui/Reviews";
import { RelatedProducts } from "@/components/ui/RelatedProducts";

export const metadata = {
  title: "جزئیات محصول",
  description: "نمایش کامل یک محصول و افزودن به سبد",
};

export default function Page() {
  return (
    <main dir="rtl" className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-10">
      <Gallery />
      <ProductInfo />
      <Reviews />
      <RelatedProducts />
    </main>
  );
}
