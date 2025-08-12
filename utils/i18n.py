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
        # --- Appointment Booking ---
        'appt_select_service': "به بخش رزرو وقت خوش آمدید. لطفاً نوع خدمات مورد نظر خود را انتخاب کنید:",
        'appt_select_slot': "عالی. لطفاً یک زمان آزاد را انتخاب کنید:",
        'appt_confirm_booking': "شما زمان '{slot}' را انتخاب کردید. آیا این انتخاب را تایید می‌کنید؟",
        'appt_success': "✅ وقت شما با موفقیت رزرو شد! در صورت نیاز با شما تماس خواهیم گرفت.",
        'appt_canceled': "رزرو وقت لغو شد.",
        'error_appointments_unavailable': "متاسفانه در حال حاضر امکان رزرو وقت وجود ندارد.",
        'button_confirm': "✅ تایید",
        'button_cancel': "❌ لغو",
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
        # --- Appointment Booking ---
        'appt_select_service': "Welcome to the appointment booking section. Please select the service you need:",
        'appt_select_slot': "Great. Please select an available time slot:",
        'appt_confirm_booking': "You selected the time slot '{slot}'. Do you confirm this choice?",
        'appt_success': "✅ Your appointment has been successfully booked! We will contact you if needed.",
        'appt_canceled': "Appointment booking canceled.",
        'error_appointments_unavailable': "Sorry, appointment booking is currently unavailable.",
        'button_confirm': "✅ Confirm",
        'button_cancel': "❌ Cancel",
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
