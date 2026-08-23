# دليل تطوير SASMAN airOS من Firmware الرسمي

## وثيقة تسليم لنموذج ذكاء اصطناعي آخر

**المشروع:** SASMAN airOS Firmware  
**المستودع:** [ahmedha43/sasman-airos-firmware](https://github.com/ahmedha43/sasman-airos-firmware)  
**المنصات:** Ubiquiti airMAX M XM وXW  
**الغرض:** تمكين نموذج ذكاء اصطناعي أو مطور آخر من فهم بنية المشروع وتعديل واجهة airOS الرسمية وإعادة بناء صورة firmware كاملة عبر GitHub Actions.

---

## 1. الملخص التنفيذي

هذا المشروع لا يعيد بناء نظام airOS القديم من SDK من الصفر. المسار الحالي يعتمد على **firmware رسمي كامل** لكل منصة، ثم ينفذ العمليات التالية آلياً:

1. تنزيل صورة XM أو XW الرسمية من رابط Ubiquiti.
2. التحقق من SHA256 ومن علامة اللوحة الموجودة في بداية الملف.
3. تحليل حاوية UBNT واستخراج قسم `rootfs`.
4. فك نظام الملفات SquashFS.
5. تعديل واجهة الويب الرسمية فقط، مع الحفاظ على kernel وu-boot وملفات EXEC الرسمية.
6. إعادة بناء SquashFS باستخدام LZMA وblock size مطابقين للصورة الرسمية.
7. فحص أن rootfs الجديد لا يتجاوز مساحة القسم المخصصة في الجهاز.
8. إعادة تغليف الصورة مع إعادة حساب CRC لكل قسم وCRC الخارجي.
9. رفع BIN وSHA256 وملف التحذير إلى GitHub Actions artifacts.
10. نشر ملف XM وملف XW في GitHub Release واحد.

> **قاعدة حاسمة:** الصورة الناتجة مبنية فوق firmware رسمي، لكنها ليست موقعة RSA من Ubiquiti بعد تعديلها. صحة CRC والبنية لا تعني أن bootloader أو أداة التحديث ستقبل الصورة.

المسار الرسمي حل مشكلة SDK القديمة التي كانت تتوقف عند binutils وGCC وBusyBox وautotools. ما زالت ملفات SDK القديمة موجودة في `overlay/xm/` و`overlay/xw/` للمقارنة والتاريخ، لكنها **ليست المسار المستخدم حالياً في workflow**.

---

## 2. عقد العمل المطلوب من أي نموذج ذكاء اصطناعي

عند تحميل هذا المستودع إلى نموذج ذكاء اصطناعي آخر، يجب أن يتعامل معه وفق العقد التالي:

```text
أنت تعمل على مشروع SASMAN airOS firmware.
الهدف هو تعديل واجهة الويب الرسمية داخل firmware XM وXW، وليس إعادة كتابة kernel أو bootloader.
يجب أن يبقى XM وXW منفصلين وغير قابلين للتبادل.
المسار الحالي يبني من firmware الرسمي عبر tools/official و.github/workflows/build-firmware.yml.
لا تستخدم overlay/xm أو overlay/xw للمسار الرسمي إلا إذا طلب المستخدم العودة إلى SDK القديم.
حافظ على CGI IDs وform names وAJAX endpoints وJavaScript الأصلي ما لم يوجد سبب موثق.
أي صورة ناتجة يجب أن تحمل وصف unsigned؛ لا تدّع أنها موقعة رسمياً.
قبل كل commit شغّل py_compile وgit diff --check واختبار البناء المحلي إن أمكن.
بعد كل تغيير شغّل workflow بإصدار جديد ولا تستبدل Release ناجحاً.
```

يجب تصنيف كل طلب تعديل قبل تنفيذه:

| نوع التعديل | مكان التعديل المفضل | مستوى الخطر |
|---|---|---:|
| لون أو خط أو خلفية أو زر | `tools/official/sasman_official.css` | منخفض |
| شعار أو أيقونة | `assets/sasman_logo.png` و`tools/official/rebrand_web.py` | منخفض إلى متوسط |
| رأس الصفحة أو شاشة الدخول | `tools/official/rebrand_web.py` وCSS | متوسط |
| بطاقة جديدة في Dashboard | `rebrand_web.py` مع الحفاظ على IDs الأصلية | متوسط |
| تغيير نموذج إعداد أو endpoint | ملفات CGI الرسمية بعد مراجعة دقيقة | عالٍ |
| kernel أو bootloader أو partition layout | خارج نطاق تعديل الواجهة | عالٍ جداً |

---

## 3. الفرق بين المسار القديم والمسار الرسمي الحالي

### 3.1 مسار SDK القديم

المسار القديم كان يستنسخ SDK مجتمعياً ثم ينسخ overlay فوقه ويشغل `make`. هذا الأسلوب يحاول إعادة بناء toolchain وkernel وBusyBox وrootfs من مصادر قديمة جداً. في Ubuntu حديثة ظهرت أخطاء توافق متتابعة، مثل تعريفات مشتركة في binutils، اختلافات GCC، قواعد Make قديمة، ومشكلات autoconf وKconfig.

الملفات التاريخية لهذا المسار هي:

```text
overlay/xm/
overlay/xw/
ci/config.xm
ci/config.xw
```

### 3.2 مسار firmware الرسمي

المسار الحالي يتعامل مع firmware كامل من Ubiquiti كقاعدة. لذلك لا يحتاج إلى إعادة بناء toolchain القديم أو kernel أو الدرايفرات. التغيير الأساسي يقع داخل rootfs، وبالخصوص داخل `/usr/www`.

| المسار | الدور |
|---|---|
| `tools/official/ubnt_image.py` | فك حاوية UBNT، إعادة التغليف، والتحقق من CRC |
| `tools/official/rebrand_web.py` | تطبيق هوية SASMAN على webroot الرسمي |
| `tools/official/sasman_official.css` | طبقة CSS للواجهة |
| `tools/official/check_rootfs.py` | فحص حجم rootfs مقابل partition allocation |
| `tools/official/optimize_logo.py` | تصغير PNG |
| `assets/sasman_logo.png` | الشعار المستخدم في CI |
| `.github/workflows/build-firmware.yml` | البناء المتوازي والنشر إلى Release |

---

## 4. مصادر firmware الرسمية

يستخدم workflow روابط Ubiquiti التالية، وهي مثبتة مع SHA256 حتى يفشل البناء عند تغير الملف أو تنزيل صفحة HTML بدلاً من firmware:

| المنصة | الرابط | علامة اللوحة | الحجم | SHA256 |
|---|---|---|---:|---|
| XM | `https://dl.ui.com/firmwares/XN-fw/v6.3.24/XM.v6.3.24.33508.251204.1904.bin` | `UBNTXM` و`ar7240` | 7,599,916 bytes | `3c4cbf7928954fb27d4d85747a70b5af73232175ffa2225ddba5531a0474f1da` |
| XW | `https://dl.ui.com/firmwares/XW-fw/v6.3.24/XW.v6.3.24.33508.251204.1816.bin` | `UBNTXW` و`ar934x` | 7,424,986 bytes | `90457c55c3daae3ebf1fb034dcfd56151316d6d6f464fc21c8fef48ed063fa53` |

توجد البيانات أيضاً في [`docs/official-sources.md`](./official-sources.md). لا ينبغي حذف SHA256 أو تحويله إلى قيمة اختيارية، لأن التحقق من مصدر الصورة طبقة أمان أساسية.

أوامر التحقق اليدوي:

```bash
curl -L --fail -o XM.bin \
  https://dl.ui.com/firmwares/XN-fw/v6.3.24/XM.v6.3.24.33508.251204.1904.bin
sha256sum XM.bin
file XM.bin
od -An -tc -N48 XM.bin
```

بداية XM المتوقعة تشبه:

```text
UBNTXM.ar7240.v6.3.24.33508.251204.1904
```

وبداية XW المتوقعة تشبه:

```text
UBNTXW.ar934x.v6.3.24.33508.251204.1816
```

---

## 5. بنية حاوية UBNT الرسمية

صورة firmware حاوية تحتوي header وعدة records. أداة `ubnt_image.py` تقرأ البنية التالية:

```text
+------------------------------+
| UBNT header                  | 268 bytes
+------------------------------+
| PART u-boot header + data   | 56 + data + 8 CRC bytes
+------------------------------+
| PART kernel header + data   | 56 + data + 8 CRC bytes
+------------------------------+
| PART rootfs header + data   | 56 + data + 8 CRC bytes
+------------------------------+
| EXEC script header + data   | 56 + data + 8 CRC bytes
+------------------------------+
| EXEC signtr header + data   | 56 + data + 8 CRC bytes
+------------------------------+
| END. record                 | 12 bytes
+------------------------------+
```

### 5.1 Header

الـ header يتكون من 268 بايت:

| الحقل | الحجم | الوصف |
|---|---:|---|
| magic | 4 | `UBNT` في الصور الرسمية المستخدمة هنا |
| version | 256 | نص الإصدار، مثل `XM.ar7240.v6.3.24...` |
| crc | 4 | CRC32 على أول 260 بايت |
| pad | 4 | صفر عادةً |

### 5.2 Part record

كل record من نوع `PART` أو `EXEC` له header بطول 56 بايت. الحقول الرقمية Big Endian:

| الإزاحة | الحجم | الحقل |
|---:|---:|---|
| 0 | 4 | magic: `PART` أو `EXEC` |
| 4 | 16 | الاسم، مثل `u-boot` أو `kernel` أو `rootfs` |
| 20 | 12 | padding |
| 32 | 4 | memory address |
| 36 | 4 | index |
| 40 | 4 | base address |
| 44 | 4 | entry address |
| 48 | 4 | data size |
| 52 | 4 | allocated partition size |

بعد payload مباشرة يوجد CRC32 بطول 4 بايت وpadding بطول 4 بايت. CRC القسم يحسب على header القسم مع payload.

### 5.3 END record

في نهاية الصورة يوجد record بطول 12 بايت:

```text
END. + outer CRC32 + padding
```

الـ outer CRC يحسب على كل البيانات التي تسبق record النهاية. إعادة حساب CRC ضرورية لصحة البنية، لكنها لا تنشئ توقيع RSA.

---

## 6. مواصفات الصور الحالية

### XM

| القسم | data size | allocated size | ملاحظات |
|---|---:|---:|---|
| `u-boot` | 230,544 | 262,144 | base `0x9f000000` |
| `kernel` | 1,034,829 | 1,048,576 | memory/entry `0x80002000` |
| `rootfs` | 6,291,456 | 6,684,672 | SquashFS 4.0 LZMA |
| `script` | 42,198 | 42,198 | EXEC، يحتوي `bin/preflash` MIPS ELF |
| `signtr` | 289 | 289 | EXEC/signature-related blob |

### XW

| القسم | data size | allocated size | ملاحظات |
|---|---:|---:|---|
| `u-boot` | 241,724 | 262,144 | خاص بصورة XW |
| `kernel` | 979,794 | 1,048,576 | kernel XW لا يجوز استبداله بـ XM |
| `rootfs` | 6,160,384 | 6,684,672 | SquashFS 4.0 LZMA |
| `script` | 42,195 | 42,195 | EXEC، خاص بصورة XW |
| `signtr` | 289 | 289 | EXEC/signature-related blob |

> لا يجوز نسخ kernel أو u-boot أو EXEC من XM إلى XW أو العكس. التعديل الحالي يستبدل rootfs الخاص بالمنصة نفسها فقط.

---

## 7. استخراج firmware يدوياً

يتطلب العمل المحلي أدوات `squashfs-tools` وPython 3:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl python3 squashfs-tools
```

بعد وضع صورة firmware في مجلد `input/`، استخدم:

```bash
python3 tools/official/ubnt_image.py unpack \
  input/XM.v6.3.24.33508.251204.1904.bin \
  work/xm \
  --board UBNTXM
```

ينشئ الأمر:

```text
work/xm/rootfs.squashfs
work/xm/metadata.json
```

ملف `metadata.json` يسجل marker والإصدار والأقسام والأحجام وحالة CRC. بعد ذلك فك rootfs:

```bash
unsquashfs -d work/xm/rootfs work/xm/rootfs.squashfs
```

ستظهر واجهة الويب في:

```text
work/xm/rootfs/usr/www/
```

وهذا هو webroot الرسمي المستخرج، وليس نسخة SDK القديمة.

لمنصة XW استخدم الأمر نفسه مع الصورة والعلامة الخاصتين بها:

```bash
python3 tools/official/ubnt_image.py unpack \
  input/XW.v6.3.24.33508.251204.1816.bin \
  work/xw \
  --board UBNTXW
unsquashfs -d work/xw/rootfs work/xw/rootfs.squashfs
```

### ملاحظة حول فك الملفات

فك SquashFS هنا عملية قراءة واستخراج فقط. لا تشغّل أي ملف ELF أو script مستخرج على جهازك. ملفات CGI تُقرأ كنص، أما binary مثل `bin/preflash` فهو برنامج MIPS مخصص للجهاز ولا ينبغي تشغيله على runner.

---

## 8. بنية واجهة الويب الرسمية

واجهة airOS الرسمية تتكون من CGI وJavaScript وقوالب وCSS وصور. أهم المسارات هي:

| المسار داخل rootfs | الدور |
|---|---|
| `/usr/www/index.cgi` | Dashboard/status page وHTML وتهيئة JavaScript |
| `/usr/www/login.cgi` | المصادقة وشاشة الدخول وتغيير كلمة المرور الأولى |
| `/usr/www/lib/head.tmpl` | الرأس العام وشعار المنتج والقائمة وأدوات النظام |
| `/usr/www/lib/settings.inc` | إعدادات مشتركة ومتغيرات النظام |
| `/usr/www/style.css` | CSS العام |
| `/usr/www/login.css` | CSS الخاص بشاشة الدخول |
| `/usr/www/index.js` | JavaScript الخاص بحالة الصفحة الرئيسية |
| `/usr/www/common.js` | وظائف مشتركة وAJAX |
| `/usr/www/*.cgi` | صفحات الإعدادات والخدمات وحالة الشبكة |
| `/usr/www/images/` | صور المنتجات والأيقونات والشعارات |
| `/usr/www/help/` | صفحات المساعدة المحلية |

### معنى CGI في هذا النظام

ملفات `.cgi` هنا ليست بالضرورة برامج ELF. كثير منها ملفات نصية تستخدم مترجم CGI الخاص بالنظام، وتحتوي مقاطع airOS syntax بين العلامات `<? ... >` مع HTML وJavaScript. لذلك لا ينبغي تحويلها إلى PHP حديث أو HTML ثابت؛ يجب الحفاظ على syntax التي يفهمها `/sbin/cgi` داخل firmware.

### عناصر يجب الحفاظ عليها

عند تعديل صفحة يجب الحفاظ على العناصر التالية ما لم يكن التغيير مقصوداً ومختبراً:

```text
form action وmethod
أسماء الحقول username وpassword وpassword2
معرفات loginform وloginform_submit
معرفات country وui_language وlang_changed
معرفات Dashboard التي يملؤها index.js
روابط CGI مثل index.cgi وlink.cgi وnetwork.cgi وsystem.cgi
استدعاءات jQuery وcommon.js وutil.js وملفات الترجمة
مقاطع cfg_load وcfg_set وPasswdAuth وma-auth
```

تغيير CSS أو HTML حول هذه العناصر آمن نسبياً. حذفها أو إعادة تسميتها قد يجعل الصفحة تبدو جميلة لكنها تفقد الحفظ أو المصادقة أو التحديث الحي.

---

## 9. كيف يطبق المشروع هوية SASMAN

### 9.1 ملف CSS

الملف [`tools/official/sasman_official.css`](../tools/official/sasman_official.css) لا يستبدل CSS الرسمي بالكامل. أداة rebrand تقرأ `style.css` الأصلي ثم تضيف طبقة CSS في نهايته. استخدام `!important` محدود بهدف تجاوز الألوان القديمة مع الحفاظ على selectors الأصلية.

الألوان الأساسية:

```css
:root {
  --sasman-blue: #087bff;
  --sasman-cyan: #12d9ff;
  --sasman-navy: #071a33;
  --sasman-surface: #102b4d;
  --sasman-text: #eaf7ff;
  --sasman-muted: #9fc6df;
}
```

إذا أردت تغيير الهوية، عدّل المتغيرات أولاً قبل إضافة قواعد كثيرة جديدة. بهذه الطريقة يمكن تغيير اللون العام دون البحث في كل selector.

### 9.2 الشعار

الملف `assets/sasman_logo.png` هو نسخة مصغرة ومضغوطة من الشعار الأصلي، أبعاده 246×256 وحجمه نحو 120 KB. الشعار الأصلي الكبير كان حجمه نحو 2.1 MB، وإضافته كما هو جعل rootfs يتجاوز allocation في XM.

يمكن إنشاء نسخة أخرى محلياً:

```bash
python3 tools/official/optimize_logo.py \
  logo-original.png \
  assets/sasman_logo.png \
  256
```

لا تستخدم صورة كبيرة جداً؛ قسم rootfs محدود، وكل byte إضافي يجب أن يبقى ضمن المساحة المخصصة.

### 9.3 أداة rebrand

الملف [`tools/official/rebrand_web.py`](../tools/official/rebrand_web.py) يستقبل ثلاثة مسارات:

```bash
python3 tools/official/rebrand_web.py \
  work/rootfs/usr/www \
  assets/sasman_logo.png \
  tools/official/sasman_official.css
```

ثم ينفذ عمليات محددة:

1. ينسخ الشعار إلى `usr/www/images/sasman_logo.png`.
2. يبحث عن marker رسمي في `lib/head.tmpl` ويضيف رأس SASMAN داخل HTML.
3. يبحث باستخدام regular expression عن شعار airOS في `login.cgi` مهما اختلف رقم مسار الإصدار بين XM وXW.
4. يستبدل العرض فقط، ولا يغيّر منطق المصادقة أو form names.
5. يضيف CSS مرة واحدة بعد marker خاص بـ SASMAN.
6. يفشل إذا لم يجد marker المتوقع، بدلاً من تطبيق تعديل صامت على ملف مختلف.

هذا الفشل المقصود مهم؛ إذا أصدرت Ubiquiti firmware جديداً بتغيير كبير في HTML، يجب مراجعة الأداة يدوياً بدلاً من إنتاج صورة قد تكون واجهتها مكسورة.

### 9.4 الرأس العام

في `head.tmpl` الرسمي توجد روابط القائمة إلى صفحات مثل:

```text
index.cgi
link.cgi
network.cgi
advanced.cgi
services.cgi
system.cgi
```

التعديل الحالي يضيف شعار SASMAN واسم SASMAN ويترك القائمة وروابطها. إذا أردت تحويل القائمة إلى sidebar، يجب تنفيذ ذلك مع إبقاء hrefs وشرط `is_ro` وصلاحيات القراءة فقط. لا تحذف شرط المستخدم read-only لمجرد تغيير شكل القائمة.

### 9.5 شاشة الدخول

`login.cgi` الرسمي يحتوي منطقاً مهماً للتالي:

- تحميل الإعدادات عبر `cfg_load`.
- تحديد أول دخول عبر `is_first_login`.
- فرض تغيير كلمة المرور الافتراضية.
- التحقق عبر `PasswdAuth`.
- إنشاء session عبر `ma-auth`.
- تغيير الدولة واللغة في أول تشغيل.
- تحويل المستخدم إلى URI المطلوب بعد الدخول.

التعديل الحالي يستبدل صورة airOS داخل HTML بصورة SASMAN فقط، ويحافظ على `loginform` و`username` و`password` و`password2` و`country` و`ui_language` و`loginform_submit`.

---
## 10. إعادة بناء rootfs

بعد تعديل الملفات، أعد بناء SquashFS بإعدادات متوافقة مع الصور الرسمية:

```bash
mksquashfs work/xm/rootfs work/xm/rootfs-sasman.squashfs \
  -comp lzma \
  -b 131072 \
  -noappend \
  -all-root \
  -no-xattrs
```

المعاني المهمة:

| الخيار | الغرض |
|---|---|
| `-comp lzma` | مطابقة ضغط rootfs الرسمي |
| `-b 131072` | مطابقة block size الرسمي 128 KiB |
| `-noappend` | إنشاء filesystem جديد من الصفر |
| `-all-root` | توحيد الملكية في بيئة CI غير متطابقة |
| `-no-xattrs` | تجنب إدخال extended attributes غير موجودة في الأصل |

بعد الإنشاء شغّل:

```bash
unsquashfs -s work/xm/rootfs-sasman.squashfs
```

يجب أن يظهر `Squashfs filesystem, little endian, version 4.0` و`Compression lzma` و`Block size 131072`.

### فحص السعة

كل صورة تحتوي allocation ثابتاً لقسم rootfs. يجب ألا يتجاوز rootfs الجديد هذا الرقم:

```bash
python3 tools/official/check_rootfs.py \
  work/xm/metadata.json \
  work/xm/rootfs-sasman.squashfs
```

إذا فشل الفحص، صغّر الصور، احذف ملفات غير ضرورية، أو قلّل تغييرات الواجهة. لا تعالج المشكلة بتغيير partition size في header؛ ذلك سيجعل الصورة غير متوافقة مع تخطيط flash الحقيقي.

---

## 11. إعادة تغليف الصورة

تستخدم أداة `ubnt_image.py` الصورة الرسمية كقالب. فهي تنسخ payload الخاص بـ u-boot وkernel وEXEC كما هو، وتستبدل payload الخاص بـ rootfs فقط:

```bash
python3 tools/official/ubnt_image.py repack \
  input/XM.v6.3.24.33508.251204.1904.bin \
  work/xm/rootfs-sasman.squashfs \
  release-assets/SASMAN-XM-unsigned.bin
```

أثناء ذلك تقوم الأداة بما يلي:

1. الاحتفاظ بـ header version والعناوين الخاصة بالمنصة.
2. تحديث `data_size` لقسم rootfs.
3. رفض rootfs إذا تجاوز `allocated`.
4. إعادة حساب CRC لكل record.
5. إعادة حساب header CRC.
6. إعادة حساب outer CRC في `END.`.
7. إبقاء EXEC الرسمي دون تشغيله أو تعديله.
8. طباعة تحذير واضح بأن الصورة ليست RSA-signed.

التحقق:

```bash
python3 tools/official/ubnt_image.py verify \
  release-assets/SASMAN-XM-unsigned.bin
```

المخرجات المطلوبة تشمل:

```text
header_crc_ok=True
part=u-boot ... fit=True crc_ok=True
part=kernel ... fit=True crc_ok=True
part=rootfs ... fit=True crc_ok=True
part=script ... fit=True crc_ok=True
part=signtr ... fit=True crc_ok=True
outer_crc_ok=True
```

هذه الفحوص تثبت سلامة الحاوية والـ CRC فقط. لا تثبت توقيع RSA ولا قبول الجهاز للصورة.

---

## 12. شرح GitHub Actions

الملف `.github/workflows/build-firmware.yml` هو نقطة الدخول للبناء العام. يستخدم matrix تحتوي هدفين:

```yaml
matrix:
  include:
    - platform: XM
      board: UBNTXM
      source_url: https://dl.ui.com/firmwares/XN-fw/v6.3.24/...
    - platform: XW
      board: UBNTXW
      source_url: https://dl.ui.com/firmwares/XW-fw/v6.3.24/...
```

كل هدف يعمل في runner مستقل على Ubuntu 22.04. مراحل الهدف هي:

| المرحلة | الإجراء |
|---|---|
| Checkout | جلب المستودع العام |
| Install image tools | تثبيت curl وPython و`squashfs-tools` |
| Download and verify | تنزيل المصدر الرسمي والتحقق من SHA256 |
| Unpack official rootfs | تحليل UBNT وفك rootfs |
| Apply SASMAN | تعديل webroot الرسمي |
| Rebuild rootfs | إنشاء SquashFS جديد مع LZMA |
| Repack and verify | إنشاء BIN وفحص CRC والسعة |
| Upload artifact | حفظ ملفات المنصة مؤقتاً |

بعد نجاح XM وXW معاً، تعمل job باسم `Publish XM and XW BIN files`. هذه الوظيفة تجمع artifacts وتستخدم `softprops/action-gh-release@v2` لإنشاء Release.

### تشغيل workflow

من واجهة GitHub:

1. افتح تبويب **Actions**.
2. اختر **Build SASMAN official-based firmware**.
3. اضغط **Run workflow**.
4. أدخل tag يبدأ بـ `v`، مثل `v2.0.2-official`.
5. انتظر نجاح مهمتي XM وXW ومهمة النشر.
6. افتح صفحة Releases ونزّل ملف المنصة المطابقة فقط.

أو من الطرفية:

```bash
gh workflow run build-firmware.yml \
  --repo ahmedha43/sasman-airos-firmware \
  -f version=v2.0.2-official
```

لا تعِد استخدام tag قديم؛ استخدم إصداراً جديداً لكل تغيير حتى تبقى النتائج قابلة للتتبع.

---

## 13. أمثلة تعديل عملية

### 13.1 تغيير اللون فقط

عدّل المتغيرات في `tools/official/sasman_official.css`:

```css
:root {
  --sasman-blue: #087bff;
  --sasman-cyan: #12d9ff;
  --sasman-navy: #071a33;
}
```

لا حاجة لتعديل CGI لهذا النوع من التغيير.

### 13.2 تغيير نص العنوان

إذا كان النص ثابتاً في HTML، عدّله داخل marker المناسب في `rebrand_web.py` أو أضف replacement واضحاً ومحدداً. لا تستخدم replacement عاماً لكلمة `Status` لأنها قد تظهر في صفحات كثيرة.

مثال آمن من حيث المبدأ:

```python
index = webroot / "index.cgi"
text = index.read_text(encoding="utf-8")
text = text.replace(
    '<th colspan="2"><? echo dict_translate("Status"); ></th>',
    '<th colspan="2">SASMAN Network Status</th>',
    1,
)
index.write_text(text, encoding="utf-8")
```

قبل اعتماد المثال، يجب التأكد أن النص مطابق فعلاً لإصدار XM وXW. إذا اختلف الإصداران، يجب استعمال replacement منفصل مع فشل واضح عند عدم العثور على marker.

### 13.3 إضافة بطاقة Dashboard

الأفضل إضافة HTML قرب أقسام `general_info` أو `radioinfo` مع class جديد، لكن عدم إعادة تسمية IDs التي يملؤها `index.js`. إذا كانت البطاقة تعرض قيمة جديدة، يجب تحديد مصدرها: متغير CGI موثوق، أو endpoint قائم، أو قراءة آمنة من النظام. لا تضف shell command من مدخل المستخدم ولا تعرض بيانات غير مهروبة داخل HTML.

### 13.4 إضافة صفحة SASMAN جديدة

لإضافة صفحة مثل `sasman.cgi`:

1. أنشئ ملف CGI باستخدام syntax airOS الصحيح.
2. استخدم القوالب المشتركة عند الحاجة.
3. أضف رابطاً في `head.tmpl` مع احترام شرط read-only.
4. أضف CSS في `sasman_official.css`.
5. لا تستخدم endpoint جديداً قبل التأكد من أن الخدمة موجودة في firmware.
6. اختبر الصفحة بعد استخراج webroot، ثم شغّل CI.

### 13.5 تعديل الصور

استخدم صوراً صغيرة ومضغوطة. أي صورة كبيرة قد تجعل rootfs يتجاوز allocation. شغّل `optimize_logo.py` أو نفّذ عملية تحسين مناسبة قبل إضافتها إلى `assets/`.

---

## 14. فحص التغييرات قبل commit

نفّذ الفحوص التالية:

```bash
cd sasman-airos-firmware
git diff --check
python3 -m py_compile tools/official/*.py
```

اختبار محلي كامل:

```bash
mkdir -p /tmp/sasman-test/xm
python3 tools/official/ubnt_image.py unpack \
  /path/to/XM.v6.3.24.33508.251204.1904.bin \
  /tmp/sasman-test/xm --board UBNTXM
unsquashfs -d /tmp/sasman-test/xm/rootfs \
  /tmp/sasman-test/xm/rootfs.squashfs
python3 tools/official/rebrand_web.py \
  /tmp/sasman-test/xm/rootfs/usr/www \
  assets/sasman_logo.png \
  tools/official/sasman_official.css
mksquashfs /tmp/sasman-test/xm/rootfs \
  /tmp/sasman-test/xm/rootfs-sasman.squashfs \
  -comp lzma -b 131072 -noappend -all-root -no-xattrs
python3 tools/official/check_rootfs.py \
  /tmp/sasman-test/xm/metadata.json \
  /tmp/sasman-test/xm/rootfs-sasman.squashfs
python3 tools/official/ubnt_image.py repack \
  /path/to/XM.v6.3.24.33508.251204.1904.bin \
  /tmp/sasman-test/xm/rootfs-sasman.squashfs \
  /tmp/sasman-test/SASMAN-XM-unsigned.bin
python3 tools/official/ubnt_image.py verify \
  /tmp/sasman-test/SASMAN-XM-unsigned.bin
```

كرّر الاختبار لـ XW مع تغيير المصدر والعلامة إلى `UBNTXW`.

---
## 15. التوقيع والقبول على الجهاز

أداة إعادة التغليف تعيد حساب CRC البنيوي، لكنها لا تمتلك مفاتيح Ubiquiti الخاصة اللازمة لإنتاج توقيع RSA رسمي. لذلك يجب التفريق بين ثلاثة مستويات:

| المستوى | ما يثبته | ما لا يثبته |
|---|---|---|
| SHA256 للمصدر | أن الملف الذي نُزّل هو الملف المتوقع | أن الصورة المعدلة صالحة للفلاش |
| CRC للأقسام والحاوية | أن البنية لم تتلف أثناء إعادة التغليف | قبول bootloader أو updater |
| RSA signature | صحة التوقيع وفق مفتاح Ubiquiti العام الموجود في الجهاز | لا يضمن توافق board مختلف |

الإصدارات المنشورة حالياً تحمل لاحقة `unsigned` وملف `BUILD-NOTICE`. لا تحذف هذه اللاحقة ولا تغيّر نص التحذير إلى «official signed».

لا تحاول استخراج أو تخمين مفاتيح توقيع Ubiquiti، ولا تحاول تعطيل secure boot أو patch bootloader ضمن مشروع تعديل واجهة. هذا خارج نطاق المشروع ويحوّل تعديل واجهة إلى مخاطرة دائمة على الجهاز.

### الاختبار الآمن

قبل أي اختبار فعلي يجب توفر:

1. جهاز مطابق تماماً للمنصة، مع التحقق من XM أو XW من الجهاز نفسه.
2. نسخة firmware الأصلية التي يمكن الرجوع إليها.
3. وصول serial أو TFTP recovery مناسب للجهاز.
4. جهاز غير إنتاجي للتجربة الأولى.
5. خطة استرجاع مكتوبة، وعدم الاعتماد على صفحة الويب وحدها.

صورة XM لا تُستخدم على جهاز XW، وصورة XW لا تُستخدم على جهاز XM، حتى لو تشابه اسم المنتج أو التردد.

---

## 16. استكشاف الأخطاء

### الخطأ: `board marker mismatch`

يعني ذلك أن الصورة لا تطابق المنصة المطلوبة. لا تتجاوز الفحص بتعديل النص يدوياً؛ صحح رابط الإدخال أو قيمة `board` في matrix.

### الخطأ: فشل SHA256

قد يكون رابط التنزيل أعاد صفحة HTML، أو تغير firmware في الرابط، أو حدث تلف أثناء التنزيل. لا تكمل البناء ولا تستبدل SHA256 بشكل عشوائي. افحص `file` وHTTP response والرابط الرسمي.

### الخطأ: `official head.tmpl marker not found`

يعني أن إصدار firmware الجديد غيّر بنية القالب. افتح `head.tmpl` المستخرج، حدد marker جديداً، ثم حدّث `rebrand_web.py` باختبار صريح. لا تجعل الأداة تستخدم replacement عاماً قد يعدّل ملفاً خاطئاً.

### الخطأ: `official login.cgi marker not found`

يعني أن موضع شعار airOS أو صيغة login تغيرت. راجع `login.cgi` الرسمي لكل منصة، مع الحفاظ على منطق المصادقة والـ IDs. لا تستبدل login.cgi بملف قديم من SDK إلا بعد مقارنة كاملة.

### الخطأ: `modified rootfs exceeds official partition allocation`

الحل هو تقليل حجم asset أو إزالة ملفات غير ضرورية. تصغير شعار SASMAN هو سبب وجود `optimize_logo.py`. لا تعدّل `allocated` في header لفرض صورة أكبر.

### الخطأ: `crc_ok=False`

يجب إيقاف النشر. راجع أداة `ubnt_image.py` وحقول big-endian وoffsets. لا تنشر BIN تم تجاوز فحص CRC الخاص به.

### فشل GitHub Release

تحقق من أن مهمتي matrix نجحتا وأن job النشر لديها `contents: write`. لا ترفع BIN يدوياً إلى Release إذا كان artifact ناقصاً أو فحوصه غير مكتملة.

### تغير firmware الرسمي لاحقاً

إذا تم تحديث المصدر الرسمي، يجب تحديث الرابط وSHA256 وجدول المواصفات، ثم اختبار XM وXW محلياً. يجب ألا يعتمد rebrand على رقم إصدار ثابت في مسارات الصور؛ لذلك يستخدم المسار النسبي `images/sasman_logo.png` في الإضافات الجديدة.

---

## 17. طريقة تطوير النظام باستخدام نموذج ذكاء اصطناعي آخر

عند فتح المستودع في نموذج أقوى، حمّل له هذا الملف مع الملفات التالية:

```text
README.md
docs/AI-DEVELOPMENT-GUIDE-AR.md
docs/official-sources.md
.github/workflows/build-firmware.yml
tools/official/ubnt_image.py
tools/official/rebrand_web.py
tools/official/sasman_official.css
tools/official/check_rootfs.py
tools/official/optimize_logo.py
assets/sasman_logo.png
```

ثم استخدم prompt شبيهاً بالتالي:

```text
أنت المطور الرئيسي لمشروع SASMAN airOS Firmware.
اقرأ README.md وdocs/AI-DEVELOPMENT-GUIDE-AR.md وجميع ملفات tools/official قبل التعديل.

أريد تطوير واجهة الويب الرسمية داخل firmware XM وXW، مع إبقاء kernel وu-boot وEXEC الخاصة بكل منصة كما هي.
يجب أن تعدل webroot الرسمي بعد فك SquashFS، لا أن تعود إلى SDK القديم.

المتطلبات الإلزامية:
- XM وXW مساران منفصلان ولا يجوز تبادل binary بينهما.
- حافظ على CGI IDs وform names وAJAX endpoints وJavaScript الأصلي.
- لا تستبدل login.cgi أو ملفات CGI الكاملة بملفات قديمة دون مقارنة.
- استخدم rebrand_web.py أو أداة patch واضحة ذات markers وفشل صريح.
- حافظ على فحص SHA256 وboard marker وحجم rootfs وCRC.
- أي BIN ناتج يجب أن يحمل وصف unsigned، لأن إعادة حساب CRC لا تنشئ RSA signature.
- شغّل الاختبارات المحلية وgit diff --check وpy_compile قبل commit.
- بعد التعديل شغّل GitHub Actions بإصدار جديد، ثم تحقق من XM وXW وRelease.

مهمتك الحالية:
[اكتب هنا التعديل المطلوب بالتفصيل]

قبل التنفيذ، اشرح الملفات التي ستتغير، واحتمالات كسر الوظائف، وكيف ستختبر المحافظة على endpoints. لا تنفذ تغييراً في kernel أو bootloader أو partition layout ضمن تعديل الواجهة.
```

هذا الأسلوب يجعل النموذج الآخر يعرف الفرق بين «تعديل واجهة» و«تعديل نظام منخفض المستوى»، ويمنعه من حذف عناصر حيوية لمجرد إنشاء تصميم جميل.

---

## 18. منهج اقتراح واجهة جديدة

للحصول على نتيجة جيدة من النموذج، اكتب طلبك على شكل طبقات:

| الطبقة | أمثلة لما يجب وصفه |
|---|---|
| الهوية | اسم SASMAN، اللون الأساسي، اللون الثانوي، شكل الشعار |
| التخطيط | sidebar أو top navigation، عدد البطاقات، ترتيب المعلومات |
| البيانات | Device Model، Device Name، Network Mode، Wireless Mode، SSID، Version، Uptime |
| السلوك | تحديث حي، حالة نجاح/تحذير، responsive على الهاتف |
| القيود | عدم تغيير endpoint، عدم حذف IDs، دعم XM وXW |
| الاختبار | screenshot أو تحقق من DOM أو تشغيل workflow |

مثال طلب واضح:

```text
حوّل Dashboard الرسمي إلى تصميم SASMAN حديث باستخدام CSS فقط قدر الإمكان.
ضع شريطاً علوياً باسم SASMAN، واجعل المعلومات العامة في أربع بطاقات.
احتفظ بمعرفات devmodel وhostname وnetmode وwmode وfwversion لأن index.js يملؤها.
لا تغيّر روابط index.cgi وlink.cgi وnetwork.cgi وadvanced.cgi وservices.cgi وsystem.cgi.
طبّق التصميم على XM وXW، وافشل إذا اختلف HTML الرسمي بينهما.
```

---

## 19. ما هو موجود في GitHub الآن

تم تنفيذ المسار الرسمي بنجاح ونشر الإصدار التالي:

| العنصر | الرابط |
|---|---|
| المستودع العام | [github.com/ahmedha43/sasman-airos-firmware](https://github.com/ahmedha43/sasman-airos-firmware) |
| workflow | [Build SASMAN official-based firmware](https://github.com/ahmedha43/sasman-airos-firmware/actions/workflows/build-firmware.yml) |
| آخر بناء ناجح | [run 32643303496](https://github.com/ahmedha43/sasman-airos-firmware/actions/runs/32643303496) |
| Release | [v2.0.1-official](https://github.com/ahmedha43/sasman-airos-firmware/releases/tag/v2.0.1-official) |
| XM BIN | [SASMAN-XM-XM.v6.3.24.33508.251204.1904-unsigned.bin](https://github.com/ahmedha43/sasman-airos-firmware/releases/download/v2.0.1-official/SASMAN-XM-XM.v6.3.24.33508.251204.1904-unsigned.bin) |
| XW BIN | [SASMAN-XW-XW.v6.3.24.33508.251204.1816-unsigned.bin](https://github.com/ahmedha43/sasman-airos-firmware/releases/download/v2.0.1-official/SASMAN-XW-XW.v6.3.24.33508.251204.1816-unsigned.bin) |

الإصدار الحالي يثبت أن البناء الآلي لـ XM وXW يعمل، لكنه لا يلغي شرط اختبار قبول الصورة غير الموقعة على جهاز مطابق.

---

## 20. مراجع المشروع

[1]: https://github.com/ahmedha43/sasman-airos-firmware "مستودع SASMAN العام"
[2]: https://www.ui.com/download/airmax-m "صفحة تنزيلات Ubiquiti airMAX M"
[3]: https://dl.ui.com/firmwares/XN-fw/v6.3.24/XM.v6.3.24.33508.251204.1904.bin "Firmware XM الرسمي v6.3.24"
[4]: https://dl.ui.com/firmwares/XW-fw/v6.3.24/XW.v6.3.24.33508.251204.1816.bin "Firmware XW الرسمي v6.3.24"
[5]: https://github.com/blinkstar88/SDK_XW.v5.6.3 "مرآة SDK XW القديمة للمقارنة"
[6]: https://github.com/zioproto/SDK.UBNT.v5.3.3 "مرآة SDK XM القديمة للمقارنة"
[7]: https://openwrt.org/toh/ubiquiti/common "مرجع OpenWrt العام لأجهزة Ubiquiti"

---

## 21. قائمة تحقق قبل التسليم

```text
[ ] المصدر الرسمي XM أو XW صحيح.
[ ] SHA256 مطابق للقيمة المثبتة.
[ ] board marker مطابق للمنصة.
[ ] تم فك rootfs من الصورة نفسها.
[ ] تم تعديل webroot الرسمي وليس SDK القديم.
[ ] بقيت login IDs وDashboard IDs وendpoints الأصلية.
[ ] rootfs الجديد ضمن allocated partition size.
[ ] mksquashfs يستخدم LZMA وblock size 131072.
[ ] CRC لكل قسم وCRC الخارجي ناجحة.
[ ] الملف معلّم unsigned ولا توجد ادعاءات RSA.
[ ] XM وXW منفصلان في الأسماء والـ artifacts.
[ ] GitHub Actions نجح في المهمتين.
[ ] Release يحتوي BIN وSHA256 وBUILD-NOTICE.
[ ] توجد نسخة firmware أصلية ومسار TFTP Recovery قبل اختبار الجهاز.
```
