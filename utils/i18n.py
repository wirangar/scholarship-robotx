# -*- coding: utf-8 -*-
"""
Internationalization (i18n) module.
Contains all user-facing strings in a multi-language dictionary.
"""

MESSAGES = {
    'fa': {
        'welcome': "🇮🇹 به ربات راهنمای دانشجویان و مهاجران پروجا خوش آمدید!\n\nلطفا برای دسترسی به امکانات ثبت‌نام کنید.",
        'main_menu_title': "منوی اصلی:",
        'register_prompt': "برای استفاده از ربات، لطفاً با دستور /register ثبت‌نام کنید.",
        'error_general': "خطایی رخ داد. لطفاً دوباره تلاش کنید یا با ادمین تماس بگیرید.",
        'invalid_input': "ورودی نامعتبر است. لطفاً دوباره تلاش کنید.",
        'registration_success': "✅ ثبت‌نام شما با موفقیت انجام شد!",
        'button_register': "📝 ثبت‌نام",
        'button_main_menu': "🏠 منوی اصلی",
        'button_back': "➡️ بازگشت",
        'button_res_hub': "📚 مرکز منابع",
        'button_scholarships': "🎓 بورسیه‌ها",
        'button_isee': "📊 محاسبه ISEE",
        'button_weather': "🌦 آب و هوا",
        'button_news': "📰 اخبار",
        'button_fx': "💱 تبدیل ارز",
        'button_profile': "👤 پروفایل",
        'button_roommate': "👥 هم‌اتاقی",
        'button_live_chat': "💬 چت با ادمین",
        # --- Registration Form ---
        'register_ask_name': "لطفاً نام کامل خود را وارد کنید:",
        'register_ask_age': "لطفاً سن خود را وارد کنید (بین 16 تا 100):",
        'register_ask_country': "لطفاً کشور خود را وارد کنید:",
        'register_ask_major': "لطفاً رشته تحصیلی خود را وارد کنید:",
        'register_ask_email': "لطفاً ایمیل خود را وارد کنید:",
        # --- ISEE Form ---
        'isee_intro': "این یک شبیه‌ساز آموزشی برای محاسبه ISEE است. نتایج ممکن است دقیق نباشد.",
        'isee_ask_income': "لطفاً درآمد سالانه خانواده خود را به یورو وارد کنید:",
        'isee_ask_property': "لطفاً متراژ کل املاک خانواده خود را به متر مربع وارد کنید (اگر ندارید 0):",
        'isee_ask_family': "تعداد اعضای خانواده شما چند نفر است؟",
        'isee_result': "📊 نتیجه محاسبه ISEE:\n\n- مقدار ISEE شما: `{isee_value:.2f}`\n- وضعیت بورسیه: `{status}`",
        'isee_status_full': "کامل",
        'isee_status_partial': "جزئی",
        'isee_status_none': "نامناسب",
        # --- Cost of Living ---
        'cost_select_city': "لطفاً برای مشاهده هزینه تخمینی زندگی، یک شهر را انتخاب کنید:",
        'error_cost_data_unavailable': "متاسفانه اطلاعات هزینه زندگی در حال حاضر در دسترس نیست.",
        'error_city_not_found': "متاسفانه اطلاعات این شهر یافت نشد.",
        'button_back_to_cities': "⬅️ بازگشت به لیست شهرها",
        'cost_details_template': """💰 *هزینه‌های تخمینی ماهانه در {city_name}*

🏠 *مسکن*:
  - اتاق یک نفره: *~€{rent_single}*
  - اتاق اشتراکی: *~€{rent_shared}*
  - خدمات (آب، برق، گاز): *~€{utilities}*

🚌 *سبک زندگی*:
  - بلیط حمل و نقل عمومی: *€{transport}*
  - خواربار: *~€{groceries}*
  - پیتزا بیرون‌بر: *€{pizza}*

_{notes}_""",
        # --- Discounts ---
        'discounts_title': "💸 *تخفیف‌های دانشجویی*\n\n",
        'error_discounts_unavailable': "متاسفانه اطلاعات تخفیف‌ها در حال حاضر در دسترس نیست.",
        'error_no_more_discounts': "تخفیف دیگری یافت نشد.",
        'button_previous': "⬅️ قبلی",
        'button_next': "بعدی ➡️",
        # --- Language ---
        'language_select_category': "لطفاً برای یادگیری چند عبارت ایتالیایی، یک دسته را انتخاب کنید:",
        'error_language_unavailable': "متاسفانه درس‌های زبان در حال حاضر در دسترس نیستند.",
        'error_category_not_found': "دسته مورد نظر یافت نشد.",
        'button_back_to_categories': "⬅️ بازگشت به دسته‌بندی‌ها",
        # --- Upload ---
        'upload_prompt': "لطفاً فایلی را که می‌خواهید آپلود کنید ارسال کنید (مانند PDF، JPG، PNG).\nحداکثر حجم فایل: ۱۰ مگابایت.\n\nبرای لغو /cancel را تایپ کنید.",
        'upload_processing': "در حال پردازش فایل شما، لطفاً صبر کنید...",
        'upload_success': "✅ فایل شما با موفقیت و به صورت امن آپلود شد!",
        'upload_canceled': "آپلود لغو شد.",
        'error_upload_no_file': "این یک فایل به نظر نمی‌رسد. لطفاً یک سند یا عکس ارسال کنید.",
        'error_upload_too_large': "فایل بیش از حد بزرگ است. لطفاً یک فایل کوچکتر از ۱۰ مگابایت ارسال کنید.",
        'error_upload_mime_type': "نوع فایل '{mime_type}' پشتیبانی نمی‌شود.",
        'error_upload_telegram_download': "متاسفانه در هنگام دانلود فایل شما از سرورهای تلگرام خطایی رخ داد.",
        'error_upload_drive': "متاسفانه در هنگام آپلود فایل شما در حافظه ما خطایی رخ داد.",
        'error_upload_log_failed': "فایل شما آپلود شد، اما در سیستم ما خطایی رخ داد. لطفاً با ادمین تماس بگیرید.",
        # --- Weather ---
        'weather_prompt': "لطفاً نام شهر را وارد کنید، یا از گزینه پیش‌فرض زیر استفاده کنید.",
        'weather_button_perugia': "🌦 آب و هوای پروجا",
        'error_invalid_city': "نام شهر نامعتبر است. لطفاً دوباره تلاش کنید.",
        'error_weather_unavailable': "متاسفانه سرویس آب و هوا در حال حاضر در دسترس نیست.",
        'error_weather_city_not_found': "متاسفانه شهر '{city}' یافت نشد. لطفاً املا را بررسی کرده و دوباره تلاش کنید.",
        'weather_details_template': """{emoji} *آب و هوا در {city}*

*{description}*
🌡️ دما: *{temp:.1f}°C*
🤔 دمای محسوس: *{feels_like:.1f}°C*
💧 رطوبت: *{humidity}%*
💨 سرعت باد: *{wind_speed:.1f} m/s*""",
    },
    'en': {
        'welcome': "🇮🇹 Welcome to the Perugia Student and Immigrant Helper Bot!\n\nPlease register to access the features.",
        'main_menu_title': "Main Menu:",
        'register_prompt': "To use the bot, please register with the /register command.",
        'error_general': "An error occurred. Please try again or contact the admin.",
        'invalid_input': "Invalid input. Please try again.",
        'registration_success': "✅ Your registration was successful!",
        'button_register': "📝 Register",
        'button_main_menu': "🏠 Main Menu",
        'button_back': "➡️ Back",
        'button_res_hub': "📚 Resources Hub",
        'button_scholarships': "🎓 Scholarships",
        'button_isee': "📊 ISEE Calculator",
        'button_weather': "🌦 Weather",
        'button_news': "📰 News",
        'button_fx': "💱 Currency Exchange",
        'button_profile': "👤 Profile",
        'button_roommate': "👥 Roommate",
        'button_live_chat': "💬 Live Chat with Admin",
         # --- Registration Form ---
        'register_ask_name': "Please enter your full name:",
        'register_ask_age': "Please enter your age (between 16 and 100):",
        'register_ask_country': "Please enter your country:",
        'register_ask_major': "Please enter your field of study:",
        'register_ask_email': "Please enter your email:",
        # --- ISEE Form ---
        'isee_intro': "This is an educational simulator for ISEE calculation. Results may not be exact.",
        'isee_ask_income': "Please enter your annual family income in EUR:",
        'isee_ask_property': "Please enter the total size of your family's properties in square meters (0 if none):",
        'isee_ask_family': "How many members are in your family?",
        'isee_result': "📊 ISEE Calculation Result:\n\n- Your ISEE value: `{isee_value:.2f}`\n- Scholarship Status: `{status}`",
        'isee_status_full': "Full",
        'isee_status_partial': "Partial",
        'isee_status_none': "Not eligible",
        # --- Cost of Living ---
        'cost_select_city': "Please select a city to see the estimated cost of living:",
        'error_cost_data_unavailable': "Sorry, cost of living data is currently unavailable.",
        'error_city_not_found': "Sorry, information for this city could not be found.",
        'button_back_to_cities': "⬅️ Back to City List",
        'cost_details_template': """💰 *Estimated Monthly Costs in {city_name}*

🏠 *Housing*:
  - Single Room: *~€{rent_single}*
  - Shared Room: *~€{rent_shared}*
  - Utilities: *~€{utilities}*

🚌 *Lifestyle*:
  - Transport Pass: *€{transport}*
  - Groceries: *~€{groceries}*
  - Pizza Out: *€{pizza}*

_{notes}_""",
        # --- Discounts ---
        'discounts_title': "💸 *Student Discounts*\n\n",
        'error_discounts_unavailable': "Sorry, discount information is currently unavailable.",
        'error_no_more_discounts': "No more discounts found.",
        'button_previous': "⬅️ Previous",
        'button_next': "Next ➡️",
        # --- Language ---
        'language_select_category': "Please select a category to learn some Italian phrases:",
        'error_language_unavailable': "Sorry, language lessons are currently unavailable.",
        'error_category_not_found': "Category not found.",
        'button_back_to_categories': "⬅️ Back to Categories",
        # --- Upload ---
        'upload_prompt': "Please send the file you wish to upload (e.g., PDF, JPG, PNG).\nMax file size: 10 MB.\n\nType /cancel to abort.",
        'upload_processing': "Processing your file, please wait...",
        'upload_success': "✅ Your file has been successfully and securely uploaded!",
        'upload_canceled': "Upload canceled.",
        'error_upload_no_file': "That doesn't seem to be a file. Please send a document or photo.",
        'error_upload_too_large': "The file is too large. Please send a file smaller than 10 MB.",
        'error_upload_mime_type': "File type '{mime_type}' is not supported.",
        'error_upload_telegram_download': "Sorry, there was an error downloading your file from Telegram's servers.",
        'error_upload_drive': "Sorry, there was an error uploading your file to our storage.",
        'error_upload_log_failed': "Your file was uploaded, but there was an error in our system. Please contact an admin.",
        # --- Weather ---
        'weather_prompt': "Please enter a city name, or use the default option below.",
        'weather_button_perugia': "🌦 Weather in Perugia",
        'error_invalid_city': "Invalid city name. Please try again.",
        'error_weather_unavailable': "Sorry, the weather service is currently unavailable.",
        'error_weather_city_not_found': "Sorry, I couldn't find the city '{city}'. Please check the spelling and try again.",
        'weather_details_template': """{emoji} *Weather in {city}*

*{description}*
🌡️ Temperature: *{temp:.1f}°C*
🤔 Feels like: *{feels_like:.1f}°C*
💧 Humidity: *{humidity}%*
💨 Wind: *{wind_speed:.1f} m/s*""",
    },
    'it': {
        # Italian translations would go here
    },
    'ar': {
        # Arabic translations would go here
    }
}

# Default language is Persian
DEFAULT_LANG = 'fa'

def get_text(key: str, lang: str = DEFAULT_LANG) -> str:
    """
    Retrieves a text string from the MESSAGES dictionary for a given language.
    Falls back to the default language if the key is not found in the target language.
    Returns the key itself if not found in default language either.
    """
    return MESSAGES.get(lang, {}).get(key, MESSAGES.get(DEFAULT_LANG, {}).get(key, key))
