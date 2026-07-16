# Component Library — فروشگاه آنلاین

### Hero
بخش ابتدایی صفحه با تیتر، توضیح کوتاه و CTA

**Props:** `title, subtitle, ctaText, ctaHref`
**استفاده‌شده در:** home

### FeaturedProducts
اسلایدر/گرید محصولات ویژه

**Props:** `products`
**استفاده‌شده در:** home

### Categories
دسته‌بندی‌های محصول در صفحه اصلی

**Props:** `categories`
**استفاده‌شده در:** home

### Newsletter
فرم عضویت در خبرنامه

**Props:** `onSubmit`
**استفاده‌شده در:** home

### FilterSidebar
سایدبار فیلتر محصولات

**Props:** `filters, onChange`
**استفاده‌شده در:** products

### ProductGrid
گرید محصولات با صفحه‌بندی

**Props:** `products, columns`
**استفاده‌شده در:** products

### Pagination
صفحه‌بندی عمومی

**Props:** `page, totalPages, onChange`
**استفاده‌شده در:** products

### Gallery
گالری تصاویر با Lightbox

**Props:** `images`
**استفاده‌شده در:** product-detail

### ProductInfo
اطلاعات قیمت و انتخاب گزینه‌های محصول

**Props:** `product`
**استفاده‌شده در:** product-detail

### Reviews
فهرست نظرات کاربران

**Props:** `reviews`
**استفاده‌شده در:** product-detail

### RelatedProducts
پیشنهاد محصولات مرتبط

**Props:** `products`
**استفاده‌شده در:** product-detail

### CartList
فهرست اقلام سبد خرید با امکان تغییر تعداد

**Props:** `items, onChange`
**استفاده‌شده در:** cart

### OrderSummary
خلاصه‌ی مبلغ سفارش

**Props:** `subtotal, shipping, total`
**استفاده‌شده در:** cart

### CheckoutButton
دکمه‌ی نهایی‌سازی خرید

**Props:** `disabled, onClick`
**استفاده‌شده در:** cart
