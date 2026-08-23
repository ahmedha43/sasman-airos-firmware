# Original XM airOS webroot

هذا المجلد يحتوي على webroot الأصلي المستخرج من صورة firmware الرسمية التالية:

```text
XM.v6.3.24.33508.251204.1904.bin
```

الرابط الرسمي:

https://dl.ui.com/firmwares/XN-fw/v6.3.24/XM.v6.3.24.33508.251204.1904.bin

SHA256 للصورة الأصلية:

```text
3c4cbf7928954fb27d4d85747a70b5af73232175ffa2225ddba5531a0474f1da
```

تم استخراج هذا المجلد من قسم `rootfs` باستخدام `unsquashfs`. الملفات هنا نسخة مرجعية أصلية للمقارنة والتعليم والتطوير، وليست هي الملفات التي يستخدمها workflow لتطبيق SASMAN.

## الملفات المهمة

| الملف | الوظيفة |
|---|---|
| `index.cgi` | صفحة الحالة الرئيسية وDashboard الرسمي |
| `login.cgi` | المصادقة وشاشة الدخول وتغيير كلمة المرور الأولى |
| `style.css` | التنسيق العام الأصلي |
| `login.css` | تنسيق شاشة الدخول |
| `index.js` | تحديث قيم Dashboard عبر JavaScript وAJAX |
| `common.js` | وظائف JavaScript مشتركة |
| `lib/head.tmpl` | الرأس والقائمة والشعارات وروابط الأدوات |
| `lib/settings.inc` | إعدادات ومتغيرات مشتركة |
| `images/` | صور المنتجات والأيقونات والشعارات |
| `help/` | صفحات المساعدة المحلية |

## تحذيرات التطوير

هذه الملفات تعمل داخل بيئة airOS الخاصة وتستخدم syntax CGI ومكتبات موجودة داخل firmware. لا تشغّل ملفات CGI أو ELF على جهاز التطوير. عند تعديلها، حافظ على form names وCGI IDs وAJAX endpoints ومقاطع `cfg_load` و`cfg_set` و`PasswdAuth` و`ma-auth`.

لإنشاء صورة SASMAN، لا تعدّل هذا المجلد المرجعي مباشرة. مسار البناء يحمّل firmware الرسمي، يفك rootfs، ثم يستخدم `tools/official/rebrand_web.py` و`tools/official/sasman_official.css` لتطبيق التغييرات على نسخة مؤقتة.
