import { FilterSidebar } from "@/components/ui/FilterSidebar";
import { ProductGrid } from "@/components/ui/ProductGrid";
import { Pagination } from "@/components/ui/Pagination";

export const metadata = {
  title: "لیست محصولات",
  description: "نمایش و فیلتر محصولات",
};

export default function Page() {
  return (
    <main dir="rtl" className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-10">
      <FilterSidebar />
      <ProductGrid />
      <Pagination />
    </main>
  );
}
