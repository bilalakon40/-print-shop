# Print Shop - AI Print-on-Demand Store

بوت ذكاء اصطناعي يولد تصاميم SVG للطباعة وينشرها تلقائياً على Gumroad.

## كيف يعمل
1. AI يولد تصميم SVG جديد كل يوم (تيشيرتات، أكواب، بوسترات)
2. يرفع التصميم كمنتج رقمي على Gumroad
3. يعرض التصاميم في معرض GitHub Pages
4. الزبون يشتري → يحمل الملف → يطبعه بنفسه أو عبر Printful/Printify

## الإعداد
1. أنشئ حساب Gumroad واحصل على access token
2. احصل على Groq API key
3. ضف الـ Secrets في GitHub:
   - `GROQ_API_KEY`
   - `GUMROAD_TOKEN`
4. فعل GitHub Pages من Settings → Pages (Source: GitHub Actions)

## الربح
- سعر المنتج: $2.99
- إنتاج يومي: 3 تصاميم
- شهرياً: ~90 منتج في المتجر
- حتى مع 1-2 بيع/يوم = $90-180/شهر
