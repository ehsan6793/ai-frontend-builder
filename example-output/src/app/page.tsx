import { Hero } from "@/components/ui/Hero";
import { FeaturedProducts } from "@/components/ui/FeaturedProducts";
import { Categories } from "@/components/ui/Categories";
import { Newsletter } from "@/components/ui/Newsletter";

export const metadata = {
  title: "صفحه اصلی",
  description: "معرفی برند و محصولات ویژه",
};

export default function Page() {
  return (
    <main dir="rtl" className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-10">
      <Hero />
      <FeaturedProducts />
      <Categories />
      <Newsletter />
    </main>
  );
}
