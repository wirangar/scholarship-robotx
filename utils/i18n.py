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
