import { CartList } from "@/components/ui/CartList";
import { OrderSummary } from "@/components/ui/OrderSummary";
import { CheckoutButton } from "@/components/ui/CheckoutButton";

export const metadata = {
  title: "سبد خرید",
  description: "مدیریت اقلام سبد خرید و پرداخت",
};

export default function Page() {
  return (
    <main dir="rtl" className="mx-auto flex max-w-6xl flex-col gap-8 px-4 py-10">
      <CartList />
      <OrderSummary />
      <CheckoutButton />
    </main>
  );
}
