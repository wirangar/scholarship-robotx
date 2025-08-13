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
        # --- Simulation ---
        'sim_select_city': "شبیه‌ساز بودجه: لطفاً یک شهر را انتخاب کنید.",
        'sim_ask_housing': "چه نوع مسکنی را ترجیح می‌دهید؟",
        'sim_housing_single': "اتاق یک نفره",
        'sim_housing_shared': "اتاق اشتراکی",
        'sim_ask_lifestyle': "سبک زندگی و تفریحات خود را چگونه توصیف می‌کنید؟",
        'sim_results_template': """✅ *نتیجه شبیه‌سازی بودجه ماهانه*

- اجاره: *€{rent}*
- خدمات (آب، برق، ...): *€{utilities}*
- حمل و نقل: *€{transport}*
- خواربار: *€{groceries}*
- تفریحات و سایر: *€{leisure}*

- *مجموع تخمینی: €{total}*""",
        # --- Consultation ---
        'consult_start': "به سرویس مشاوره تحصیلی خوش آمدید.\nبرای شناخت بهتر پروفایل شما، چند سوال خواهیم پرسید.\n\nابتدا، رشته تحصیلی مورد نظر شما چیست؟",
        'consult_ask_gpa': "معدل فعلی شما چند است؟ (در مقیاس ۴ یا ۲۰ - لطفاً مقیاس را مشخص کنید)",
        'consult_ask_budget': "بودجه سالانه تخمینی شما برای تحصیل به یورو چقدر است؟",
        'consult_ask_language': "سطح فعلی زبان ایتالیایی یا انگلیسی شما چیست؟ (مانند B1، آیلتس ۶.۵)",
        'consult_ask_cv': "در آخر، لطفاً فایل رزومه (CV) خود را با فرمت PDF یا DOCX آپلود کنید.",
        'consult_uploading_cv': "در حال آپلود رزومه شما، لطفاً صبر کنید...",
        'consult_error_cv_upload': "در هنگام آپلود رزومه شما خطایی رخ داد. لطفاً دوباره تلاش کنید یا با ادمین تماس بگیرید.",
        'consult_error_cv_format': "این یک فایل رزومه معتبر به نظر نمی‌رسد. لطفاً یک سند PDF یا DOCX ارسال کنید.",
        'consult_success': "✅ متشکریم! درخواست مشاوره شما ثبت شد. به زودی با شما تماس خواهیم گرفت.",
        'consult_error_saving': "در هنگام ذخیره درخواست شما خطایی رخ داد. لطفاً با ادمین تماس بگیرید.",
        # --- Roommate ---
        'roommate_welcome': "به بخش هم‌اتاقی‌یابی خوش آمدید! چه کاری می‌خواهید انجام دهید؟",
        'roommate_button_create': "📝 ساخت / به‌روزرسانی پروفایل",
        'roommate_button_search': "🔍 جستجوی هم‌اتاقی",
        'roommate_create_start': "بیایید پروفایل هم‌اتاقی شما را بسازیم.\n\nبودجه ماهانه شما برای اجاره به یورو چقدر است؟",
        'roommate_ask_location': "در کدام منطقه به دنبال خانه هستید؟ (مانند Centro، Elce)",
        'roommate_ask_habits': "شما در خانه فردی آرام هستید یا اجتماعی؟ (آرام/اجتماعی)",
        'roommate_ask_bio': "عالی! در آخر، یک بیوگرافی کوتاه درباره خودتان بنویسید (مثلاً سرگرمی‌ها، رشته تحصیلی).",
        'roommate_profile_saved': "✅ پروفایل هم‌اتاقی شما با موفقیت ذخیره شد!",
        'roommate_error_saving': "هنگام ذخیره پروفایل شما خطایی رخ داد.",
        'roommate_search_wip': "🔍 بخش جستجوی هم‌اتاقی هنوز پیاده‌سازی نشده است. لطفاً بعداً دوباره سر بزنید!",
        'error_invalid_budget': "لطفاً برای بودجه یک عدد معتبر وارد کنید.",
        'roommate_error_no_profile': "برای جستجو، ابتدا باید پروفایل هم‌اتاقی خود را با استفاده از دکمه 'ساخت پروفایل' ایجاد کنید.",
        'roommate_no_matches': "متاسفانه هیچ مورد منطبقی با پروفایل شما یافت نشد.",
        'roommate_no_more_matches': "مورد دیگری یافت نشد.",
        'roommate_match_template': """*یک هم‌اتاقی بالقوه پیدا شد!*

*درباره*: {bio}
*بودجه*: €{budget}
*مکان*: {location}
*عادات*: {habits}

*برای تماس*: `{contact}`""",
        'roommate_match_template_scored': """*یک هم‌اتاقی بالقوه پیدا شد!*
*امتیاز تطابق*: {score}/100

*درباره*: {bio}
*بودجه*: €{budget}
*مکان*: {location}
*عادات*: {habits}

*برای تماس*: `{contact}`""",
        # --- Appointment Booking ---
        'appt_select_service': "به بخش رزرو وقت خوش آمدید. لطفاً نوع خدمات مورد نظر خود را انتخاب کنید:",
        'appt_select_slot': "عالی. لطفاً یک زمان آزاد را انتخاب کنید:",
        'appt_confirm_booking': "شما زمان '{slot}' را انتخاب کردید. آیا این انتخاب را تایید می‌کنید؟",
        'appt_success': "✅ وقت شما با موفقیت رزرو شد! در صورت نیاز با شما تماس خواهیم گرفت.",
        'appt_canceled': "رزرو وقت لغو شد.",
        'error_appointments_unavailable': "متاسفانه در حال حاضر امکان رزرو وقت وجود ندارد.",
        'button_confirm': "✅ تایید",
        'button_cancel': "❌ لغو",
        'appt_reminder_24h': "🔔 یادآوری: شما فردا یک وقت مشاوره در ساعت {slot} دارید.",
        # --- Success Story ---
        'story_start': "ما دوست داریم داستان موفقیت شما را بشنویم! لطفاً داستان خود را در یک پیام بنویسید.",
        'story_ask_photo': "عالی! آیا می‌خواهید یک عکس به داستان خود اضافه کنید؟",
        'story_success': "✅ داستان شما با موفقیت ثبت شد و پس از بازبینی منتشر خواهد شد. متشکریم!",
        'button_yes': "✅ بله",
        'button_no': "❌ نه",
        # --- Q&A ---
        'qna_ask_question': "سوال خود را تایپ کنید. ما ابتدا در سوالات متداول جستجو می‌کنیم.",
        'qna_suggestions_found': "چند سوال مشابه پیدا کردیم. آیا جواب شما اینجاست؟\nاگر نه، دکمه زیر را بزنید تا سوالتان ثبت شود.",
        'qna_submit_anyway': "سوال من این نیست، ثبتش کن",
        'qna_success': "✅ سوال شما با موفقیت ثبت شد. ادمین‌ها به زودی پاسخ خواهند داد.",
        'qna_answer_notification': """پاسخ سوال شما داده شد:

*سوال شما*: {question}
*پاسخ*: {answer}""",
        # --- Migration Status ---
        'migration_checklist_title': "📋 *چک‌لیست مراحل مهاجرت و اقامت*\n\nاین یک راهنمای کلی است. مراحل ممکن است متفاوت باشند.",
        # --- Points ---
        'points_display': "🏆 شما در حال حاضر *{points}* امتیاز دارید. برای مشارکت بیشتر، امتیاز بیشتری کسب کنید!",
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
        # --- Simulation ---
        'sim_select_city': "Budget Simulator: Please select a city.",
        'sim_ask_housing': "What type of housing do you prefer?",
        'sim_housing_single': "Single Room",
        'sim_housing_shared': "Shared Room",
        'sim_ask_lifestyle': "How would you describe your lifestyle and leisure habits?",
        'sim_results_template': """✅ *Monthly Budget Simulation Results*

- Rent: *€{rent}*
- Utilities (water, electricity, ...): *€{utilities}*
- Transport: *€{transport}*
- Groceries: *€{groceries}*
- Leisure & Other: *€{leisure}*

- *Estimated Total: €{total}*""",
        # --- Consultation ---
        'consult_start': "Welcome to the Academic Consultation service.\nWe will ask a few questions to understand your profile.\n\nFirst, what is your intended field of study?",
        'consult_ask_gpa': "What is your current GPA (on a scale of 4.0 or 20)? Please specify the scale.",
        'consult_ask_budget': "What is your estimated annual budget for studying in EUR?",
        'consult_ask_language': "What is your current Italian or English language proficiency level (e.g., B1, IELTS 6.5)?",
        'consult_ask_cv': "Finally, please upload your CV or resume as a PDF or DOCX file.",
        'consult_uploading_cv': "Uploading your CV, please wait...",
        'consult_error_cv_upload': "There was an error uploading your CV. Please try again or contact an admin.",
        'consult_error_cv_format': "That doesn't seem to be a valid CV file. Please send a PDF or DOCX document.",
        'consult_success': "✅ Thank you! Your consultation request has been submitted. We will get back to you soon.",
        'consult_error_saving': "There was an error saving your request. Please contact an admin.",
        # --- Roommate ---
        'roommate_welcome': "Welcome to the Roommate Finder! What would you like to do?",
        'roommate_button_create': "📝 Create / Update Profile",
        'roommate_button_search': "🔍 Search for Roommates",
        'roommate_create_start': "Let's create your roommate profile.\n\nWhat is your monthly budget for rent in EUR?",
        'roommate_ask_location': "Which area are you looking to live in? (e.g., Centro, Elce)",
        'roommate_ask_habits': "Are you more of a quiet or social person at home? (Quiet/Social)",
        'roommate_ask_bio': "Great! Lastly, write a short bio about yourself (e.g., your hobbies, what you're studying).",
        'roommate_profile_saved': "✅ Your roommate profile has been saved successfully!",
        'roommate_error_saving': "An error occurred while saving your profile.",
        'roommate_search_wip': "🔍 Roommate search is not yet implemented. Please check back later!",
        'error_invalid_budget': "Please enter a valid number for your budget.",
        'roommate_error_no_profile': "To search, you first need to create your own roommate profile using the 'Create Profile' button.",
        'roommate_no_matches': "Sorry, no suitable matches were found for your profile.",
        'roommate_no_more_matches': "No more matches found.",
        'roommate_match_template': """*Found a potential roommate!*

*About*: {bio}
*Budget*: €{budget}
*Location*: {location}
*Habits*: {habits}

*To get in touch*: `{contact}`""",
        'roommate_match_template_scored': """*Found a potential roommate!*
*Match Score*: {score}/100

*About*: {bio}
*Budget*: €{budget}
*Location*: {location}
*Habits*: {habits}

*To get in touch*: `{contact}`""",
        # --- Appointment Booking ---
        'appt_select_service': "Welcome to the appointment booking section. Please select the service you need:",
        'appt_select_slot': "Great. Please select an available time slot:",
        'appt_confirm_booking': "You selected the time slot '{slot}'. Do you confirm this choice?",
        'appt_success': "✅ Your appointment has been successfully booked! We will contact you if needed.",
        'appt_canceled': "Appointment booking canceled.",
        'error_appointments_unavailable': "Sorry, appointment booking is currently unavailable.",
        'button_confirm': "✅ Confirm",
        'button_cancel': "❌ Cancel",
        'appt_reminder_24h': "🔔 Reminder: You have an advising appointment tomorrow at {slot}.",
        # --- Success Story ---
        'story_start': "We'd love to hear your success story! Please write your story in a single message.",
        'story_ask_photo': "Great! Would you like to add a photo to your story?",
        'story_success': "✅ Your story has been successfully submitted and will be published after review. Thank you!",
        'button_yes': "✅ Yes",
        'button_no': "❌ No",
        # --- Q&A ---
        'qna_ask_question': "Type your question. We'll search our FAQ first.",
        'qna_suggestions_found': "We found a few similar questions. Is your answer here?\nIf not, press the button below to submit your question.",
        'qna_submit_anyway': "This is not my question, submit it",
        'qna_success': "✅ Your question has been successfully submitted. The admins will answer it soon.",
        'qna_answer_notification': """Your question has been answered:

*Your Question*: {question}
*Answer*: {answer}""",
        # --- Migration Status ---
        'migration_checklist_title': "📋 *Migration & Residency Checklist*\n\nThis is a general guide. Your steps may vary.",
        # --- Points ---
        'points_display': "🏆 You currently have *{points}* points. Keep participating to earn more!",
    },
    'it': {
        'welcome': "🇮🇹 Benvenuto nel Bot di Aiuto per Studenti e Immigrati a Perugia!\n\nPer favore, registrati per accedere alle funzionalità.",
        'main_menu_title': "Menu Principale:",
        'register_prompt': "Per usare il bot, per favore registrati con il comando /register.",
        'error_general': "Si è verificato un errore. Per favore, riprova o contatta l'amministratore.",
        'invalid_input': "Input non valido. Per favore, riprova.",
        'registration_success': "✅ La tua registrazione è stata completata con successo!",
        'button_register': "📝 Registrati",
        'button_main_menu': "🏠 Menu Principale",
        'button_back': "➡️ Indietro",
        'button_res_hub': "📚 Centro Risorse",
        'button_scholarships': "🎓 Borse di Studio",
        'button_isee': "📊 Calcolatore ISEE",
        'button_weather': "🌦 Meteo",
        'button_news': "📰 Notizie",
        'button_fx': "💱 Cambio Valuta",
        'button_profile': "👤 Profilo",
        'button_roommate': "👥 Coinquilino",
        'button_live_chat': "💬 Chat con Admin",
        'register_ask_name': "Per favore, inserisci il tuo nome completo:",
        'register_ask_age': "Per favore, inserisci la tua età (tra 16 e 100):",
        'register_ask_country': "Per favore, inserisci il tuo paese:",
        'register_ask_major': "Per favore, inserisci il tuo corso di studi:",
        'register_ask_email': "Per favore, inserisci la tua email:",
        'isee_intro': "Questo è un simulatore educativo per il calcolo dell'ISEE. I risultati potrebbero non essere esatti.",
        'isee_ask_income': "Per favore, inserisci il reddito annuo della tua famiglia in EUR:",
        'isee_ask_property': "Per favore, inserisci la dimensione totale delle proprietà della tua famiglia in metri quadrati (0 se nessuna):",
        'isee_ask_family': "Quanti membri ci sono nella tua famiglia?",
        'isee_result': "📊 Risultato Calcolo ISEE:\n\n- Il tuo valore ISEE: `{isee_value:.2f}`\n- Stato Borsa di Studio: `{status}`",
        'isee_status_full': "Completa",
        'isee_status_partial': "Parziale",
        'isee_status_none': "Non idoneo",
        'cost_select_city': "Per favore, seleziona una città per vedere il costo della vita stimato:",
        'error_cost_data_unavailable': "Spiacenti, i dati sul costo della vita non sono attualmente disponibili.",
        'error_city_not_found': "Spiacenti, le informazioni per questa città non sono state trovate.",
        'button_back_to_cities': "⬅️ Torna alla Lista Città",
        'cost_details_template': """💰 *Costi Mensili Stimati a {city_name}*

🏠 *Alloggio*:
  - Stanza Singola: *~€{rent_single}*
  - Stanza Condivisa: *~€{rent_shared}*
  - Utenze: *~€{utilities}*

🚌 *Stile di Vita*:
  - Abbonamento Trasporti: *€{transport}*
  - Spesa: *~€{groceries}*
  - Pizza Fuori: *€{pizza}*

_{notes}_""",
        'discounts_title': "💸 *Sconti per Studenti*\n\n",
        'error_discounts_unavailable': "Spiacenti, le informazioni sugli sconti non sono attualmente disponibili.",
        'error_no_more_discounts': "Nessun altro sconto trovato.",
        'button_previous': "⬅️ Precedente",
        'button_next': "➡️ Successivo",
        'language_select_category': "Per favore, seleziona una categoria per imparare alcune frasi in italiano:",
        'error_language_unavailable': "Spiacenti, le lezioni di lingua non sono attualmente disponibili.",
        'error_category_not_found': "Categoria non trovata.",
        'button_back_to_categories': "⬅️ Torna alle Categorie",
        'upload_prompt': "Per favore, invia il file che desideri caricare (es. PDF, JPG, PNG).\nDimensione massima: 10 MB.\n\nDigita /cancel per annullare.",
        'upload_processing': "Elaborazione del tuo file, attendere prego...",
        'upload_success': "✅ Il tuo file è stato caricato con successo e in modo sicuro!",
        'upload_canceled': "Caricamento annullato.",
        'error_upload_no_file': "Questo non sembra essere un file. Per favore, invia un documento o una foto.",
        'error_upload_too_large': "Il file è troppo grande. Per favore, invia un file più piccolo di 10 MB.",
        'error_upload_mime_type': "Il tipo di file '{mime_type}' non è supportato.",
        'error_upload_telegram_download': "Spiacenti, si è verificato un errore durante il download del file dai server di Telegram.",
        'error_upload_drive': "Spiacenti, si è verificato un errore durante il caricamento del file sul nostro storage.",
        'error_upload_log_failed': "Il tuo file è stato caricato, ma si è verificato un errore nel nostro sistema. Per favore, contatta un admin.",
        'weather_prompt': "Per favore, inserisci il nome di una città o usa l'opzione predefinita qui sotto.",
        'weather_button_perugia': "🌦 Meteo a Perugia",
        'error_invalid_city': "Nome della città non valido. Per favore, riprova.",
        'error_weather_unavailable': "Spiacenti, il servizio meteo non è attualmente disponibile.",
        'error_weather_city_not_found': "Spiacenti, non sono riuscito a trovare la città '{city}'. Per favore, controlla l'ortografia e riprova.",
        'weather_details_template': """{emoji} *Meteo a {city}*

*{description}*
🌡️ Temperatura: *{temp:.1f}°C*
🤔 Percepita: *{feels_like:.1f}°C*
💧 Umidità: *{humidity}%*
💨 Vento: *{wind_speed:.1f} m/s*""",
        'sim_select_city': "Simulatore di Budget: Per favore, seleziona una città.",
        'sim_ask_housing': "Che tipo di alloggio preferisci?",
        'sim_housing_single': "Stanza Singola",
        'sim_housing_shared': "Stanza Condivisa",
        'sim_ask_lifestyle': "Come descriveresti il tuo stile di vita e le tue abitudini di svago?",
        'sim_results_template': """✅ *Risultati Simulazione Budget Mensile*

- Affitto: *€{rent}*
- Utenze (acqua, luce, ...): *€{utilities}*
- Trasporti: *€{transport}*
- Spesa: *€{groceries}*
- Svago e Altro: *€{leisure}*

- *Totale Stimato: €{total}*""",
        'consult_start': "Benvenuto al servizio di Consulenza Accademica.\nTi faremo alcune domande per capire il tuo profilo.\n\nInnanzitutto, qual è il tuo campo di studi previsto?",
        'consult_ask_gpa': "Qual è la tua media attuale (GPA)? Per favore, specifica la scala.",
        'consult_ask_budget': "Qual è il tuo budget annuale stimato per studiare in EUR?",
        'consult_ask_language': "Qual è il tuo attuale livello di competenza linguistica in italiano o inglese (es. B1, IELTS 6.5)?",
        'consult_ask_cv': "Infine, per favore carica il tuo CV o resume come file PDF o DOCX.",
        'consult_uploading_cv': "Caricamento del tuo CV in corso, attendere prego...",
        'consult_error_cv_upload': "Si è verificato un errore durante il caricamento del tuo CV. Per favore, riprova o contatta un admin.",
        'consult_error_cv_format': "Questo non sembra un file CV valido. Per favore, invia un documento PDF o DOCX.",
        'consult_success': "✅ Grazie! La tua richiesta di consulenza è stata inviata. Ti risponderemo presto.",
        'consult_error_saving': "Si è verificato un errore durante il salvataggio della tua richiesta. Per favore, contatta un admin.",
        'roommate_welcome': "Benvenuto nel Trovatore di Coinquilini! Cosa vorresti fare?",
        'roommate_button_create': "📝 Crea / Aggiorna Profilo",
        'roommate_button_search': "🔍 Cerca Coinquilini",
        'roommate_create_start': "Creiamo il tuo profilo da coinquilino.\n\nQual è il tuo budget mensile per l'affitto in EUR?",
        'roommate_ask_location': "In quale zona stai cercando casa? (es. Centro, Elce)",
        'roommate_ask_habits': "Sei una persona più tranquilla o socievole in casa? (Tranquilla/Socievole)",
        'roommate_ask_bio': "Ottimo! Infine, scrivi una breve biografia su di te (es. i tuoi hobby, cosa studi).",
        'roommate_profile_saved': "✅ Il tuo profilo da coinquilino è stato salvato con successo!",
        'roommate_error_saving': "Si è verificato un errore durante il salvataggio del tuo profilo.",
        'roommate_search_wip': "🔍 La ricerca di coinquilini non è ancora implementata. Per favore, torna più tardi!",
        'error_invalid_budget': "Per favore, inserisci un numero valido per il tuo budget.",
        'roommate_error_no_profile': "Per cercare, devi prima creare il tuo profilo da coinquilino usando il pulsante 'Crea Profilo'.",
        'roommate_no_matches': "Spiacenti, non sono stati trovati coinquilini adatti al tuo profilo.",
        'roommate_no_more_matches': "Nessun altro risultato trovato.",
        'roommate_match_template': """*Trovato un potenziale coinquilino!*

*Su di lui/lei*: {bio}
*Budget*: €{budget}
*Zona*: {location}
*Abitudini*: {habits}

*Per contattarlo/a*: `{contact}`""",
        'roommate_match_template_scored': """*Trovato un potenziale coinquilino!*
*Punteggio di Compatibilità*: {score}/100

*Su di lui/lei*: {bio}
*Budget*: €{budget}
*Zona*: {location}
*Abitudini*: {habits}

*Per contattarlo/a*: `{contact}`""",
        'appt_select_service': "Benvenuto nella sezione prenotazione appuntamenti. Per favore, seleziona il servizio di cui hai bisogno:",
        'appt_select_slot': "Ottimo. Per favore, seleziona uno slot orario disponibile:",
        'appt_confirm_booking': "Hai selezionato lo slot '{slot}'. Confermi questa scelta?",
        'appt_success': "✅ Il tuo appuntamento è stato prenotato con successo! Ti contatteremo se necessario.",
        'appt_canceled': "Prenotazione appuntamento annullata.",
        'error_appointments_unavailable': "Spiacenti, la prenotazione di appuntamenti non è attualmente disponibile.",
        'button_confirm': "✅ Conferma",
        'button_cancel': "❌ Annulla",
        'appt_reminder_24h': "🔔 Promemoria: Hai un appuntamento di consulenza domani alle {slot}.",
        'story_start': "Ci piacerebbe sentire la tua storia di successo! Per favore, scrivi la tua storia in un unico messaggio.",
        'story_ask_photo': "Ottimo! Vorresti aggiungere una foto alla tua storia?",
        'story_success': "✅ La tua storia è stata inviata con successo e sarà pubblicata dopo una revisione. Grazie!",
        'button_yes': "✅ Sì",
        'button_no': "❌ No",
        'qna_ask_question': "Scrivi la tua domanda. Cercheremo prima nelle nostre FAQ.",
        'qna_suggestions_found': "Abbiamo trovato alcune domande simili. La tua risposta è qui?\nIn caso contrario, premi il pulsante qui sotto per inviare la tua domanda.",
        'qna_submit_anyway': "Questa non è la mia domanda, inviala",
        'qna_success': "✅ La tua domanda è stata inviata con successo. Gli amministratori risponderanno presto.",
        'qna_answer_notification': """La tua domanda ha ricevuto una risposta:

*La tua Domanda*: {question}
*Risposta*: {answer}""",
        'migration_checklist_title': "📋 *Checklist per Immigrazione e Residenza*\n\nQuesta è una guida generale. I tuoi passaggi potrebbero variare.",
        'points_display': "🏆 Attualmente hai *{points}* punti. Continua a partecipare per guadagnarne di più!",
    },
    'ar': {
        'welcome': "🇮🇹 أهلاً بك في بوت مساعد الطلاب والمهاجرين في بيروجا!\n\nيرجى التسجيل للوصول إلى الميزات.",
        'main_menu_title': "القائمة الرئيسية:",
        'register_prompt': " لاستخدام البوت، يرجى التسجيل باستخدام الأمر /register.",
        'error_general': "حدث خطأ. يرجى المحاولة مرة أخرى أو الاتصال بالمسؤول.",
        'invalid_input': "إدخال غير صالح. يرجى المحاولة مرة أخرى.",
        'registration_success': "✅ تم تسجيلك بنجاح!",
        'button_register': "📝 تسجيل",
        'button_main_menu': "🏠 القائمة الرئيسية",
        'button_back': "➡️ رجوع",
        'button_res_hub': "📚 مركز الموارد",
        'button_scholarships': "🎓 المنح الدراسية",
        'button_isee': "📊 حاسبة ISEE",
        'button_weather': "🌦 الطقس",
        'button_news': "📰 الأخبار",
        'button_fx': "💱 تحويل العملات",
        'button_profile': "👤 الملف الشخصي",
        'button_roommate': "👥 البحث عن شريك سكن",
        'button_live_chat': "💬 محادثة مباشرة مع المسؤول",
        'register_ask_name': "يرجى إدخال اسمك الكامل:",
        'register_ask_age': "يرجى إدخال عمرك (بين 16 و 100):",
        'register_ask_country': "يرجى إدخال بلدك:",
        'register_ask_major': "يرجى إدخال تخصصك الدراسي:",
        'register_ask_email': "يرجى إدخال بريدك الإلكتروني:",
        'isee_intro': "هذا محاكي تعليمي لحساب ISEE. قد لا تكون النتائج دقيقة.",
        'isee_ask_income': "يرجى إدخال دخل عائلتك السنوي باليورو:",
        'isee_ask_property': "يرجى إدخال الحجم الإجمالي لممتلكات عائلتك بالمتر المربع (0 إذا لم يكن هناك):",
        'isee_ask_family': "كم عدد أفراد عائلتك؟",
        'isee_result': "📊 نتيجة حساب ISEE:\n\n- قيمة ISEE الخاصة بك: `{isee_value:.2f}`\n- حالة المنحة: `{status}`",
        'isee_status_full': "كاملة",
        'isee_status_partial': "جزئية",
        'isee_status_none': "غير مؤهل",
        'cost_select_city': "يرجى تحديد مدينة لمعرفة تكلفة المعيشة التقديرية:",
        'error_cost_data_unavailable': "عذراً، بيانات تكلفة المعيشة غير متوفرة حالياً.",
        'error_city_not_found': "عذراً، لم يتم العثور على معلومات لهذه المدينة.",
        'button_back_to_cities': "⬅️ العودة إلى قائمة المدن",
        'cost_details_template': """💰 *التكاليف الشهرية المقدرة في {city_name}*

🏠 *السكن*:
  - غرفة مفردة: *~€{rent_single}*
  - غرفة مشتركة: *~€{rent_shared}*
  - الفواتير: *~€{utilities}*

🚌 *نمط الحياة*:
  - بطاقة النقل: *€{transport}*
  - البقالة: *~€{groceries}*
  - بيتزا في الخارج: *€{pizza}*

_{notes}_""",
        'discounts_title': "💸 *خصومات الطلاب*\n\n",
        'error_discounts_unavailable': "عذراً، معلومات الخصومات غير متوفرة حالياً.",
        'error_no_more_discounts': "لم يتم العثور على المزيد من الخصومات.",
        'button_previous': "⬅️ السابق",
        'button_next': "➡️ التالي",
        'language_select_category': "يرجى تحديد فئة لتعلم بعض العبارات الإيطالية:",
        'error_language_unavailable': "عذراً، دروس اللغة غير متوفرة حالياً.",
        'error_category_not_found': "الفئة غير موجودة.",
        'button_back_to_categories': "⬅️ العودة إلى الفئات",
        'upload_prompt': "يرجى إرسال الملف الذي ترغب في تحميله (مثل PDF، JPG، PNG).\nالحد الأقصى لحجم الملف: 10 ميغابايت.\n\nاكتب /cancel للإلغاء.",
        'upload_processing': "جاري معالجة ملفك، يرجى الانتظار...",
        'upload_success': "✅ تم تحميل ملفك بنجاح وأمان!",
        'upload_canceled': "تم إلغاء التحميل.",
        'error_upload_no_file': "لا يبدو أن هذا ملف. يرجى إرسال مستند أو صورة.",
        'error_upload_too_large': "الملف كبير جداً. يرجى إرسال ملف أصغر من 10 ميغابايت.",
        'error_upload_mime_type': "نوع الملف '{mime_type}' غير مدعوم.",
        'error_upload_telegram_download': "عذراً، حدث خطأ أثناء تنزيل ملفك من خوادم تيليجرام.",
        'error_upload_drive': "عذراً، حدث خطأ أثناء تحميل ملفك إلى مساحة التخزين لدينا.",
        'error_upload_log_failed': "تم تحميل ملفك، ولكن حدث خطأ في نظامنا. يرجى الاتصال بمسؤول.",
        'weather_prompt': "يرجى إدخال اسم مدينة، أو استخدام الخيار الافتراضي أدناه.",
        'weather_button_perugia': "🌦 الطقس في بيروجا",
        'error_invalid_city': "اسم المدينة غير صالح. يرجى المحاولة مرة أخرى.",
        'error_weather_unavailable': "عذراً، خدمة الطقس غير متوفرة حالياً.",
        'error_weather_city_not_found': "عذراً، لم أتمكن من العثور على مدينة '{city}'. يرجى التحقق من الإملاء والمحاولة مرة أخرى.",
        'weather_details_template': """{emoji} *الطقس في {city}*

*{description}*
🌡️ درجة الحرارة: *{temp:.1f}°م*
🤔 الإحساس الفعلي: *{feels_like:.1f}°م*
💧 الرطوبة: *{humidity}%*
💨 سرعة الرياح: *{wind_speed:.1f} م/ث*""",
        'sim_select_city': "محاكي الميزانية: يرجى تحديد مدينة.",
        'sim_ask_housing': "أي نوع من السكن تفضل؟",
        'sim_housing_single': "غرفة مفردة",
        'sim_housing_shared': "غرفة مشتركة",
        'sim_ask_lifestyle': "كيف تصف نمط حياتك وعاداتك الترفيهية؟",
        'sim_results_template': """✅ *نتائج محاكاة الميزانية الشهرية*

- الإيجار: *€{rent}*
- الفواتير (ماء، كهرباء، ...): *€{utilities}*
- النقل: *€{transport}*
- البقالة: *€{groceries}*
- الترفيه وغيرها: *€{leisure}*

- *المجموع التقديري: €{total}*""",
        'consult_start': "أهلاً بك في خدمة الاستشارات الأكاديمية.\nسنطرح بعض الأسئلة لفهم ملفك الشخصي.\n\nأولاً، ما هو مجال دراستك المقصود؟",
        'consult_ask_gpa': "ما هو معدلك التراكمي الحالي؟ يرجى تحديد المقياس.",
        'consult_ask_budget': "ما هي ميزانيتك السنوية المقدرة للدراسة باليورو؟",
        'consult_ask_language': "ما هو مستواك الحالي في اللغة الإيطالية أو الإنجليزية (مثل B1، IELTS 6.5)؟",
        'consult_ask_cv': "أخيراً، يرجى تحميل سيرتك الذاتية كملف PDF أو DOCX.",
        'consult_uploading_cv': "جاري تحميل سيرتك الذاتية، يرجى الانتظار...",
        'consult_error_cv_upload': "حدث خطأ أثناء تحميل سيرتك الذاتية. يرجى المحاولة مرة أخرى أو الاتصال بمسؤول.",
        'consult_error_cv_format': "لا يبدو أن هذا ملف سيرة ذاتية صالح. يرجى إرسال مستند PDF أو DOCX.",
        'consult_success': "✅ شكراً لك! تم تقديم طلب الاستشارة الخاص بك. سنتصل بك قريباً.",
        'consult_error_saving': "حدث خطأ أثناء حفظ طلبك. يرجى الاتصال بمسؤول.",
        'roommate_welcome': "أهلاً بك في مكتشف شركاء السكن! ماذا تود أن تفعل؟",
        'roommate_button_create': "📝 إنشاء / تحديث الملف الشخصي",
        'roommate_button_search': "🔍 البحث عن شركاء سكن",
        'roommate_create_start': "لنقم بإنشاء ملفك الشخصي للبحث عن شريك سكن.\n\nما هي ميزانيتك الشهرية للإيجار باليورو؟",
        'roommate_ask_location': "في أي منطقة تبحث عن سكن؟ (مثل Centro، Elce)",
        'roommate_ask_habits': "هل أنت شخص هادئ أم اجتماعي في المنزل؟ (هادئ/اجتماعي)",
        'roommate_ask_bio': "ممتاز! أخيراً، اكتب نبذة مختصرة عن نفسك (هواياتك، ماذا تدرس).",
        'roommate_profile_saved': "✅ تم حفظ ملفك الشخصي للبحث عن شريك سكن بنجاح!",
        'roommate_error_saving': "حدث خطأ أثناء حفظ ملفك الشخصي.",
        'roommate_search_wip': "🔍 البحث عن شركاء سكن لم يتم تنفيذه بعد. يرجى العودة لاحقاً!",
        'error_invalid_budget': "يرجى إدخال رقم صالح لميزانيتك.",
        'roommate_error_no_profile': "للبحث، يجب عليك أولاً إنشاء ملفك الشخصي للبحث عن شريك سكن باستخدام زر 'إنشاء ملف شخصي'.",
        'roommate_no_matches': "عذراً، لم يتم العثور على مطابقات مناسبة لملفك الشخصي.",
        'roommate_no_more_matches': "لم يتم العثور على المزيد من المطابقات.",
        'roommate_match_template': """*تم العثور على شريك سكن محتمل!*

*عنه/عنها*: {bio}
*الميزانية*: €{budget}
*المنطقة*: {location}
*العادات*: {habits}

*للتواصل*: `{contact}`""",
        'roommate_match_template_scored': """*تم العثور على شريك سكن محتمل!*
*درجة التطابق*: {score}/100

*عنه/عنها*: {bio}
*الميزانية*: €{budget}
*المنطقة*: {location}
*العادات*: {habits}

*للتواصل*: `{contact}`""",
        'appt_select_service': "أهلاً بك في قسم حجز المواعيد. يرجى تحديد الخدمة التي تحتاجها:",
        'appt_select_slot': "ممتاز. يرجى تحديد موعد متاح:",
        'appt_confirm_booking': "لقد اخترت الموعد '{slot}'. هل تؤكد هذا الاختيار؟",
        'appt_success': "✅ تم حجز موعدك بنجاح! سنتصل بك إذا لزم الأمر.",
        'appt_canceled': "تم إلغاء حجز الموعد.",
        'error_appointments_unavailable': "عذراً، حجز المواعيد غير متاح حالياً.",
        'button_confirm': "✅ تأكيد",
        'button_cancel': "❌ إلغاء",
        'appt_reminder_24h': "🔔 تذكير: لديك موعد استشارة غداً في الساعة {slot}.",
        'story_start': "نود أن نسمع قصة نجاحك! يرجى كتابة قصتك في رسالة واحدة.",
        'story_ask_photo': "ممتاز! هل ترغب في إضافة صورة إلى قصتك؟",
        'story_success': "✅ تم إرسال قصتك بنجاح وسيتم نشرها بعد المراجعة. شكراً لك!",
        'button_yes': "✅ نعم",
        'button_no': "❌ لا",
        'qna_ask_question': "اكتب سؤالك. سنبحث أولاً في الأسئلة الشائعة.",
        'qna_suggestions_found': "وجدنا بعض الأسئلة المشابهة. هل إجابتك هنا؟\nإذا لم تكن كذلك، فاضغط على الزر أدناه لإرسال سؤالك.",
        'qna_submit_anyway': "هذا ليس سؤالي، أرسله",
        'qna_success': "✅ تم إرسال سؤالك بنجاح. سيجيب المسؤولون عليه قريباً.",
        'qna_answer_notification': """تمت الإجابة على سؤالك:

*سؤالك*: {question}
*الإجابة*: {answer}""",
        'migration_checklist_title': "📋 *قائمة التحقق من الهجرة والإقامة*\n\nهذا دليل عام. قد تختلف خطواتك.",
        'points_display': "🏆 لديك حالياً *{points}* نقطة. استمر في المشاركة لكسب المزيد!",
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
