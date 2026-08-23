# SASMAN airOS firmware

مستودع عام لبناء نسخ firmware مخصصة بواجهة **SASMAN** لأجهزة Ubiquiti airMAX M ذات منصتي **XM** و**XW**. يعتمد المسار الحالي على firmware الرسمي الكامل لكل منصة، ثم يفك root filesystem الرسمي، يضيف طبقة الهوية البصرية SASMAN إلى واجهة airOS الأصلية، يعيد ضغط rootfs، ويعيد تغليف صورة firmware مع الحفاظ على kernel وu-boot وملفات EXEC الرسمية.

## ماذا ينتج المستودع؟

عند نجاح GitHub Actions، ينشئ المشروع Release واحداً يحتوي على ملف BIN منفصل لمنصة XM وملف BIN منفصل لمنصة XW، إضافة إلى ملفات SHA256 وملف تحذير البناء لكل منصة. لا تستخدم صورة XM على XW أو صورة XW على XM.

| المنصة | مصدر firmware الرسمي | SHA256 المثبت في workflow |
| --- | --- | --- |
| XM | `https://dl.ui.com/firmwares/XN-fw/v6.3.24/XM.v6.3.24.33508.251204.1904.bin` | `3c4cbf7928954fb27d4d85747a70b5af73232175ffa2225ddba5531a0474f1da` |
| XW | `https://dl.ui.com/firmwares/XW-fw/v6.3.24/XW.v6.3.24.33508.251204.1816.bin` | `90457c55c3daae3ebf1fb034dcfd56151316d6d6f464fc21c8fef48ed063fa53` |

## تشغيل البناء

يمكن تشغيل البناء من تبويب **Actions** باختيار **Build SASMAN official-based firmware** ثم الضغط على **Run workflow** وإدخال tag مثل `v2.0.0-official`. كما يبدأ البناء تلقائياً عند دفع tag يبدأ بالحرف `v`:

```bash
git tag v2.0.0-official
git push origin v2.0.0-official
```

يبني workflow مهمتي XM وXW بالتوازي على Ubuntu 22.04. قبل التعديل يتحقق من SHA256 وboard marker، ثم يفك SquashFS الرسمي، يطبق الهوية، يعيد الضغط باستخدام LZMA وblock size `131072`، ويتحقق من CRC وحجم القسم قبل رفع الملفات إلى artifact ثم Release.

## الملفات المهمة

| المسار | الوظيفة |
| --- | --- |
| `.github/workflows/build-firmware.yml` | بناء XM وXW الرسميين بالتوازي ونشر BIN وSHA256 في Release |
| `tools/official/ubnt_image.py` | فك rootfs وإعادة تغليف صورة UBNT والتحقق من CRC |
| `tools/official/rebrand_web.py` | إضافة شعار SASMAN وتعديل الرأس وشاشة الدخول دون تغيير منطق CGI |
| `tools/official/sasman_official.css` | طبقة الهوية البصرية الزرقاء الكهربائية/السماوية |
| `tools/official/check_rootfs.py` | التأكد من أن rootfs المعدل يناسب partition allocation |
| `assets/sasman_logo.png` | نسخة مضغوطة من شعار SASMAN مناسبة لحجم فلاش XM/XW |
| `docs/official-sources.md` | روابط firmware الرسمية والبصمات المثبتة |
| `reference/original/xm-v6.3.24/usr/www/` | webroot الأصلي المستخرج من firmware XM، للقراءة والمقارنة فقط |
| `reference/original/xm-v6.3.24/README.md` | توثيق مصدر واجهة XM الأصلية وطريقة استخدامها |
| `reference/original/xw-v6.3.24/usr/www/` | webroot الأصلي المستخرج من firmware XW، للقراءة والمقارنة فقط |
| `reference/original/xw-v6.3.24/README.md` | توثيق مصدر واجهة XW الأصلية وطريقة استخدامها |
| `overlay/xm/` و`overlay/xw/` | المسار القديم المبني على SDK، محفوظ للمقارنة ولا يستخدمه workflow الرسمي الحالي |

## قيد التوقيع والتحذير

الملفات الناتجة من هذا المسار مبنية فوق firmware رسمي، لكنها **ليست موقعة RSA من Ubiquiti** بعد تعديل rootfs. إعادة حساب CRC البنيوي لا تعادل إعادة التوقيع الرسمي، ولذلك يجب اعتبارها صوراً تجريبية إلى أن يتم اختبار قبولها على جهاز XM أو XW مطابق فعلياً.

لا ترفع أي ملف إلى جهاز إنتاجي قبل مطابقة نوع اللوحة والطراز، واحتفظ دائماً بنسخة firmware الأصلية ومسار TFTP Recovery فعال. اختبر أولاً على جهاز غير إنتاجي. نجاح GitHub Actions يعني أن الصورة اجتازت فحوص البناء والبنية، ولا يضمن أن bootloader أو updater سيقبل صورة غير موقعة.

## لماذا المستودع عام؟

المستودع عام عمداً حتى يعمل البناء على GitHub-hosted runners العامة ولا يستهلك دقائق البناء المدفوعة للمستودعات الخاصة. لا يحتاج workflow إلى مفاتيح سرية؛ فهو يستخدم روابط التنزيل الرسمية وصلاحية `contents: write` المخصصة لإنشاء Release.
