# Original XW airOS webroot

هذا المجلد يحتوي على webroot الأصلي المستخرج من صورة firmware الرسمية التالية:

```text
XW.v6.3.24.33508.251204.1816.bin
```

الرابط الرسمي:

https://dl.ui.com/firmwares/XW-fw/v6.3.24/XW.v6.3.24.33508.251204.1816.bin

SHA256 للصورة الأصلية:

```text
90457c55c3daae3ebf1fb034dcfd56151316d6d6f464fc21c8fef48ed063fa53
```

تم استخراج هذا المجلد من قسم `rootfs` باستخدام `unsquashfs`. الملفات هنا نسخة مرجعية أصلية للمقارنة والتعليم والتطوير، وليست هي الملفات التي يستخدمها workflow لتطبيق SASMAN.

## البنية

```text
reference/original/xw-v6.3.24/
├── README.md
└── usr/
    └── www/
        ├── index.cgi
        ├── login.cgi
        ├── style.css
        ├── login.css
        ├── index.js
        ├── common.js
        ├── lib/
        ├── images/
        └── help/
```

## الملفات الرئيسية

| الملف | الوظيفة |
|---|---|
| `usr/www/index.cgi` | صفحة الحالة الرئيسية وDashboard الرسمي |
| `usr/www/login.cgi` | المصادقة وشاشة الدخول وتغيير كلمة المرور الأولى |
| `usr/www/style.css` | التنسيق العام الأصلي |
| `usr/www/login.css` | تنسيق شاشة الدخول |
| `usr/www/index.js` | تحديث قيم Dashboard عبر JavaScript وAJAX |
| `usr/www/common.js` | وظائف JavaScript مشتركة |
| `usr/www/lib/head.tmpl` | الرأس والقائمة والشعارات وروابط الأدوات |
| `usr/www/lib/settings.inc` | إعدادات ومتغيرات مشتركة |
| `usr/www/images/` | صور المنتجات والأيقونات والشعارات |
| `usr/www/help/` | صفحات المساعدة المحلية |

## تحذيرات التطوير

هذه الملفات تعمل داخل بيئة airOS الخاصة وتستخدم syntax CGI ومكتبات موجودة داخل firmware. لا تشغّل ملفات CGI أو ELF على جهاز التطوير. عند تعديلها، حافظ على form names وCGI IDs وAJAX endpoints ومقاطع `cfg_load` و`cfg_set` و`PasswdAuth` و`ma-auth`.

لإنشاء صورة SASMAN، لا تعدّل هذا المجلد المرجعي مباشرة. مسار البناء يحمّل firmware الرسمي XW، يفك rootfs، ثم يستخدم `tools/official/rebrand_web.py` و`tools/official/sasman_official.css` لتطبيق التغييرات على نسخة مؤقتة.

يجب عدم استخدام ملفات هذا المجلد لبناء XM، كما يجب عدم استخدام مرجع XM لبناء XW. اختلاف board marker وkernel وu-boot يجعل المنصتين غير قابلتين للتبادل.
