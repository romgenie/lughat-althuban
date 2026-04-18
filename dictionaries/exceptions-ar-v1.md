# Arabic Exception Dictionary — exceptions-ar-v1

This document lists the translated exception type names and message templates used by the `arabicpython.tracebacks` module.

## Exception Type Names

| Python | Arabic |
|---|---|
| `BaseException` | `استثناء_أساسي` |
| `Exception` | `استثناء` |
| `ArithmeticError` | `خطأ_حسابي` |
| `AssertionError` | `خطأ_تأكيد` |
| `AttributeError` | `خطأ_خاصية` |
| `BlockingIOError` | `خطأ_إدخال_إخراج_حاجب` |
| `EOFError` | `خطأ_نهاية_الملف` |
| `FileExistsError` | `خطأ_الملف_موجود` |
| `FileNotFoundError` | `خطأ_الملف_غير_موجود` |
| `FloatingPointError` | `خطأ_فاصلة_عائمة` |
| `ImportError` | `خطأ_استيراد` |
| `IndentationError` | `خطأ_إزاحة` |
| `IndexError` | `خطأ_فهرس` |
| `IsADirectoryError` | `خطأ_هذا_مجلد` |
| `KeyError` | `خطأ_مفتاح` |
| `KeyboardInterrupt` | `مقاطعة_لوحة_المفاتيح` |
| `LookupError` | `خطأ_بحث` |
| `MemoryError` | `خطأ_ذاكرة` |
| `ModuleNotFoundError` | `خطأ_الوحدة_غير_موجودة` |
| `NameError` | `خطأ_اسم` |
| `NotADirectoryError` | `خطأ_ليس_مجلدا` |
| `NotImplementedError` | `خطأ_غير_منفذ` |
| `OSError` | `خطأ_نظام` |
| `OverflowError` | `خطأ_فيضان` |
| `PermissionError` | `خطأ_صلاحيات` |
| `RecursionError` | `خطأ_عودية` |
| `RuntimeError` | `خطأ_تشغيل` |
| `StopIteration` | `إيقاف_التكرار` |
| `SyntaxError` | `خطأ_صياغة` |
| `SystemExit` | `خروج_نظام` |
| `TabError` | `خطأ_تبويب` |
| `TimeoutError` | `خطأ_انتهاء_مهلة` |
| `TypeError` | `خطأ_نوع` |
| `UnicodeDecodeError` | `خطأ_فك_يونيكود` |
| `UnicodeEncodeError` | `خطأ_ترميز_يونيكود` |
| `UnicodeError` | `خطأ_يونيكود` |
| `ValueError` | `خطأ_قيمة` |
| `ZeroDivisionError` | `خطأ_القسمة_على_صفر` |

## Message Templates

| Pattern (Python regex) | Arabic template |
|---|---|
| `^division by zero$` | `القسمة على صفر` |
| `^integer division or modulo by zero$` | `قسمة صحيحة أو باقي على صفر` |
| `^float division by zero$` | `قسمة عشرية على صفر` |
| `^name '(?P<name>[^']+)' is not defined$` | `الاسم '{name}' غير معرّف` |
| `^name '(?P<name>[^']+)' is not defined\. Did you mean: '(?P<sugg>[^']+)'\?$` | `الاسم '{name}' غير معرّف. هل تقصد: '{sugg}'؟` |
| `^free variable '(?P<name>[^']+)' referenced before assignment in enclosing scope$` | `المتغير الحر '{name}' مستخدم قبل تعريفه في النطاق المحيط` |
| `^local variable '(?P<name>[^']+)' referenced before assignment$` | `المتغير المحلي '{name}' مستخدم قبل تعريفه` |
| `^'(?P<type>[^']+)' object has no attribute '(?P<attr>[^']+)'$` | `الكائن من نوع '{type}' لا يملك الخاصية '{attr}'` |
| `^'(?P<type>[^']+)' object is not subscriptable$` | `الكائن من نوع '{type}' لا يقبل الفهرسة` |
| `^'(?P<type>[^']+)' object is not callable$` | `الكائن من نوع '{type}' غير قابل للاستدعاء` |
| `^'(?P<type>[^']+)' object is not iterable$` | `الكائن من نوع '{type}' غير قابل للتكرار` |
| `^'(?P<type>[^']+)' object cannot be interpreted as an integer$` | `الكائن من نوع '{type}' لا يمكن تفسيره كعدد صحيح` |
| `^argument of type '(?P<type>[^']+)' is not iterable$` | `الوسيط من نوع '{type}' غير قابل للتكرار` |
| `^list index out of range$` | `فهرس القائمة خارج النطاق` |
| `^tuple index out of range$` | `فهرس الصف خارج النطاق` |
| `^string index out of range$` | `فهرس النص خارج النطاق` |
| `^pop from empty list$` | `إخراج من قائمة فارغة` |
| `^pop from an empty (set\|deque\|dict)$` | `إخراج من {1} فارغ` |
| `^dictionary changed size during iteration$` | `تغير حجم القاموس أثناء التكرار` |
| `^maximum recursion depth exceeded(?P<rest>.*)$` | `تم تجاوز عمق العودية الأقصى{rest}` |
| `^No module named '(?P<name>[^']+)'$` | `لا توجد وحدة باسم '{name}'` |
| `^cannot import name '(?P<name>[^']+)' from '(?P<module>[^']+)'(?P<rest>.*)$` | `لا يمكن استيراد الاسم '{name}' من '{module}'{rest}` |
| `^unsupported operand type\(s\) for (?P<op>\S+): '(?P<a>[^']+)' and '(?P<b>[^']+)'$` | `أنواع المعاملات غير مدعومة لـ {op}: '{a}' و '{b}'` |
| `^can only concatenate (?P<a>\w+) \(not "(?P<b>\w+)"\) to \w+$` | `يمكن فقط ضم {a} (لا {b}) إلى {a}` |
| `^invalid literal for int\(\) with base (?P<base>\d+): '(?P<val>[^']*)'$` | `قيمة غير صالحة للدالة int() بالأساس {base}: '{val}'` |
| `^could not convert string to float: '(?P<val>[^']*)'$` | `تعذر تحويل النص إلى عدد عشري: '{val}'` |
| `^expected (?P<n>\d+) (?P<arg_kind>positional argument\|positional arguments), got (?P<got>\d+)$` | `كان متوقعا {n} {arg_kind} لكن تم تمرير {got}` |
| `^(?P<func>\w+)\(\) missing (?P<n>\d+) required positional argument(?P<plural>s?): (?P<rest>.+)$` | `{func}() ينقصها {n} وسيط إجباري{plural}: {rest}` |
| `^(?P<func>\w+)\(\) got an unexpected keyword argument '(?P<name>[^']+)'$` | `{func}() استلمت وسيطا مفتاحيا غير متوقع '{name}'` |
| `^\[Errno (?P<errno>\d+)\] (?P<msg>[^:]+): '(?P<path>.+)'$` | `[رقم الخطأ {errno}] {msg}: '{path}'` |

## Frame Line Strings

| English | Arabic |
|---|---|
| `Traceback (most recent call last):` | `تتبع_الأخطاء (المكدس الأحدث آخرا):` |
| `  File "{path}", line {N}, in {scope}` | `  ملف "{path}", سطر {N}, في {scope}` |
| `  File "{path}", line {N}` | `  ملف "{path}", سطر {N}` |
| `<module>` | `<الوحدة>` |
