from telegram import Update
from telegram.ext import ContextTypes
from interface.DisplayManager import set_user_display 
from .DBInteract import load_registered_users, save_registered_users
from .Validations import vaildate_info

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, state: str):
    text = update.message.text
    user_id = update.effective_user.id
    username = update.message.from_user.username

    if state == "tech-stack-main":
        if text == "📝 ثبت‌نام اولیه":
            registered_users = load_registered_users()
            if str(user_id) in registered_users:
                await update.message.reply_text("شما قبلا ثبت‌نام کرده‌اید.")
            else:
                await set_user_display(update, context, state="tech-stack-first-forum")
        #elif text == "☑️ انتخاب دوره اصلی":
        #    registered_users = load_registered_users()
        #    if str(user_id) not in registered_users:
        #        await update.message.reply_text("شما ابتدا باید ثبت‌نام کنید.")
        #    else:
        #        userid = str(update.effective_user.id)
        #        data = registered_users.get(userid)
        #        dresult = data["is_passed"]
        #
        #        if dresult == None:
        #            await set_user_display(update, context, state="tech-stack-decision")
        #        else:
        #            await update.message.reply_text("متاسفانه امکان تغییر دوره دیگر مقدور نمی‌باشد.")
        elif text == "📓 مشاهده اطلاعات ثبت‌شده":
            registered_users = load_registered_users()
            if str(user_id) not in registered_users:
                await update.message.reply_text("شما هنوز ثبت‌نام نکردید.")
            else:
                userid = str(update.effective_user.id)
                data = registered_users.get(userid)

                #dcourse = data["course"]
                dcourse = None
                if dcourse == None:
                    dcourse = "انتخاب نشده"

                dresult = data["is_passed"]
                if dresult == True:
                    dresult = "قبول شده"
                    dpay = data["has_paid"]
                    if dpay == False:
                        dpay = "پرداخت نشده"
                    elif dpay == True:
                        dpay = "پرداخت شده"
                    await update.message.reply_text(
                                                    f"📄 <b>اطلاعات شما: (شناسه کاربری \"</b><code>{userid}</code><b>\")</b> 🆔\n\n"
                                                    f"👤 <b>نام:</b> {data['name']}\n"
                                                    f"👥 <b>نام خانوادگی:</b> {data['surname']}\n"
                                                    f"🔗 <b>آیدی تلگرام:</b> {data['username']}\n"
                                                    f"📞 <b>شماره تلفن:</b> {data['phone']}\n"
                                                    f"🏙️ <b>شهر محل زندگی:</b> {data['city']}\n"
                                                    f"🎓 <b>شماره دانشجویی:</b> {data['student_id']}\n"
                                                    f"📅 <b>سال ورودی:</b> {data['entry_year']}\n"
                                                    f"📘 <b>دوره اصلی:</b> {dcourse}\n"
                                                    f"🔔 <b>دوره‌های انتخاب شده جهت یادآوری:</b> {data['interests']}\n"
                                                    f"🗣️ <b>وضعیت مصاحبه:</b> {dresult}\n"
                                                    f"💰 <b>وضعیت شهریه:</b> {dpay}\n"
                                                    ,parse_mode='HTML'
                                                )
                else:
                    if dresult == None:
                        dresult = "نامشخص"
                    elif dresult == False:
                        dresult = "رد شده"
                    await update.message.reply_text(
                                                    f"📄 <b>اطلاعات شما: (شناسه کاربری \"</b><code>{userid}</code><b>\")</b> 🆔\n\n"
                                                    f"👤 <b>نام:</b> {data['name']}\n"
                                                    f"👥 <b>نام خانوادگی:</b> {data['surname']}\n"
                                                    f"🔗 <b>آیدی تلگرام:</b> {data['username']}\n"
                                                    f"📞 <b>شماره تلفن:</b> {data['phone']}\n"
                                                    f"🏙️ <b>شهر محل زندگی:</b> {data['city']}\n"
                                                    f"🎓 <b>شماره دانشجویی:</b> {data['student_id']}\n"
                                                    f"📅 <b>سال ورودی:</b> {data['entry_year']}\n"
                                                    f"📘 <b>دوره اصلی:</b> {dcourse}\n"
                                                    f"🔔 <b>دوره‌های انتخاب شده جهت یادآوری:</b> {data['interests']}\n"
                                                    f"🗣️ <b>وضعیت مصاحبه:</b> {dresult}\n"
                                                    ,parse_mode='HTML'
                                                )
        elif text == "💫 مشاهده نتایج مصاحبه و پرداخت شهریه":
            registered_users = load_registered_users()
            if str(user_id) not in registered_users:
                await update.message.reply_text("شما هنوز ثبت‌نام نکردید.")
            else:
                userid = str(update.effective_user.id)
                data = registered_users.get(userid)
                dresult = data["is_passed"]

                if dresult == None:
                    await update.message.reply_text("نتیجه مصاحبه شما درحال حاضر مشخص نیست.")
                elif dresult == False:
                    await update.message.reply_text("متاسفانه شما در مصاحبه رد شدید.")
                elif dresult == True:
                    if data["has_paid"] == True:
                        await update.message.reply_text("شما قبلا مبلغ شهریه را پرداخت کردید.")
                    elif data["has_paid"] == False:
                        await update.message.reply_text("تبریک! شما در مصاحبه قبول شدید!")
                        await set_user_display(update, context, state="tech-stack-pay")
        elif text == "🔔 به من یادآوری کن":
            await set_user_display(update, context, state="tach-stack-remind")
        elif text == "🔙 بازگشت":
            await set_user_display(update, context, state="main-menu")

    elif state == "tech-stack-first-forum":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="tech-stack-main")
        else:
            lines = text.splitlines()
            stripped_lines = [line.strip() for line in lines if line.strip()]
            cleaned_text = "\n".join(stripped_lines)
            result = vaildate_info(cleaned_text)
            if not result[0]:
                await update.message.reply_text(result[1])
            else:
                context.user_data["temp_user_info"] = result[1]
                await update.message.reply_text(
                    "نام: " + result[1][0] + "\n" +
                    "نام خانوادگی: " + result[1][1] + "\n" +
                    "شهر: " + result[1][2] + "\n" +
                    "شماره تلفن: " + result[1][3] + "\n" +
                    "شماره دانشجویی: " + result[1][4] + "\n" +
                    "سال ورودی: " + result[1][5]
                )
                await set_user_display(update, context, state="tech-stack-user-info-confirm")

    elif state == "tech-stack-user-info-confirm":
        if text == "❌ خیر":
            await set_user_display(update, context, state="tech-stack-first-forum")
        if text == "✅ بله":
            user = update.effective_user
            info = context.user_data.get("temp_user_info")

            user_data = {
                "username": f"@{user.username}",
                "name": info[0],
                "surname": info[1],
                "city": info[2],
                "phone": info[3],
                "student_id": info[4],
                "entry_year": info[5],
                "course": None,
                "is_passed": None,
                "has_paid": False,
                "interests": []
            }

            registered_users = load_registered_users()
            registered_users[str(user.id)] = user_data
            save_registered_users(registered_users)

            await update.message.reply_text("✅ اطلاعات شما با موفقیت ذخیره شد.")
            await set_user_display(update, context, state="tech-stack-main")

    elif state == "tech-stack-decision":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="tech-stack-main")
        elif text == "❌ حذف":
            registered_users = load_registered_users()
            user_id = str(update.effective_user.id)

            if user_id in registered_users:
                registered_users[user_id]["course"] = None
                save_registered_users(registered_users)
                await update.message.reply_text("✅ با موفقیت حذف شد.")
            else:
                await update.message.reply_text("❌ شما ابتدا باید اطلاعات خود را ثبت کنید.")

            await set_user_display(update, context, state="tech-stack-main")
        elif text in ["Back-End", "Front-End", "DevOps", "Graphic Design", "AI", "Game", "Blockchain"]:
            registered_users = load_registered_users()
            user_id = str(update.effective_user.id)

            if user_id in registered_users:
                user_info = registered_users[user_id]
                registered_users[user_id]["course"] = text

                if "interests" not in user_info or not isinstance(user_info["interests"], list):
                    user_info["interests"] = []

                if text not in user_info["interests"]:
                    user_info["interests"].append(text)

                save_registered_users(registered_users)

                await update.message.reply_text("✅ دوره مدنظر شما با موفقیت ثبت شد.")
                await set_user_display(update, context, state="tech-stack-main")
            else:
                await update.message.reply_text("❌ شما ابتدا باید اطلاعات خود را ثبت کنید.")
                await set_user_display(update, context, state="tech-stack-main")

    elif state == "tech-stack-pay":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="tech-stack-main")

    elif state == "tach-stack-remind":
        if text == "✅ اضافه کردن":
            await set_user_display(update, context, state="remind-add")
        elif text == "❌ حذف کردن":
            await set_user_display(update, context, state="remind-remove")
        elif text == "🔙 بازگشت":
            await set_user_display(update, context, state="tech-stack-main")

    elif state == "remind-add":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="tach-stack-remind")
        elif text in ["Back-End", "Front-End", "DevOps", "Graphic Design", "AI", "Game", "Blockchain"]:
            registered_users = load_registered_users()
            user_id = str(update.effective_user.id)

            if user_id in registered_users:
                user_info = registered_users[user_id]

                # اگر قبلاً فیلد interests وجود نداشت، ایجادش کن
                if "interests" not in user_info or not isinstance(user_info["interests"], list):
                    user_info["interests"] = []

                # اگر این علاقه قبلاً ثبت نشده، اضافه‌اش کن
                if text not in user_info["interests"]:
                    user_info["interests"].append(text)
                    save_registered_users(registered_users)
                    await update.message.reply_text("✅ دوره مدنظر شما با موفقیت ثبت شد.")
                else:
                    await update.message.reply_text("ℹ️ این دوره قبلاً ثبت شده است.")

            else:
                await update.message.reply_text("❌ شما ابتدا باید اطلاعات خود را ثبت کنید.")

    elif state == "remind-remove":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="tach-stack-remind")
        elif text in ["Back-End", "Front-End", "DevOps", "Graphic Design", "AI", "Game", "Blockchain"]:
            registered_users = load_registered_users()
            user_id = str(update.effective_user.id)

            if user_id in registered_users:
                user_info = registered_users[user_id]
                interests = user_info.get("interests", [])

                if text in interests:
                    interests.remove(text)
                    user_info["interests"] = interests  # ذخیره لیست جدید
                    save_registered_users(registered_users)
                    await update.message.reply_text("✅ این دوره از علاقه‌مندی‌های شما حذف شد.")
                else:
                    await update.message.reply_text("ℹ️ این دوره در لیست علاقه‌مندی‌های شما وجود ندارد.")
            else:
                await update.message.reply_text("❌ شما ابتدا باید اطلاعات خود را ثبت کنید.")
