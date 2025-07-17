from telegram import Update
from telegram.ext import ContextTypes
from interface.DisplayManager import set_user_display
from .DBInteract import load_registered_users, save_registered_users
from .Validations import is_valid_positive_integer
from core.AccessLevels import (save_user_access, user_access_keys,
                                get_user_access, set_user_access)
from .main import (parse_edit_input, filter_input, message_input, start_filter, user_matches,
                            render_user_summary, USERS_PER_MSG)
from core.Tokens import SALATIN

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, state: str):
    text = update.message.text
    user_id = update.effective_user.id
    username = update.message.from_user.username

    if state == "backdoor-panel-head":
        if user_id not in SALATIN:
            await set_user_display(update, context, state="main-menu")
            return

        if text == "👥 تنظیمات ادمین‌ها":
            await set_user_display(update, context, state="admin-list")
        elif text == "📩 ویرایش ثبت‌نامی‌ها":
            await set_user_display(update, context, state="registrant-panel")
        elif text == "💸 لیست پرداختی‌ها":
            await set_user_display(update, context, state="pay-panel")
        elif text == "🗨️ لیست مصاحبه‌ای‌ها":
            await set_user_display(update, context, state="interview-panel")
        elif text == "📢 ارسال پیام همگانی":
            start_filter(update, context, "broadcast")
            await set_user_display(update, context, state="filter-panel")
        elif text == "🔎 جستجو در دیتابیس":
            await set_user_display(update, context, state="search-choose")
        elif text == "🔙 بازگشت":
            await set_user_display(update, context, state="main-menu")

    elif state == "backdoor-panel":
        if get_user_access(user_id) != "admin" and user_id not in SALATIN:
            await set_user_display(update, context, state="main-menu")
            return

        if text == "💸 لیست پرداختی‌ها":
            await set_user_display(update, context, state="pay-panel")
        elif text == "🗨️ لیست مصاحبه‌ای‌ها":
            await set_user_display(update, context, state="interview-panel")
        elif text == "📢 ارسال پیام همگانی":
            start_filter(update, context, "broadcast")
            await set_user_display(update, context, state="filter-panel")
        elif text == "🔎 جستجو در دیتابیس":
            await set_user_display(update, context, state="search-choose")
        elif text == "🔙 بازگشت":
            await set_user_display(update, context, state="main-menu")

    elif state == "backdoor-access-denied":
        if text == "🔢 دریافت آیدی عددی":
            await update.message.reply_text("آیدی عددی شما:")
            await update.message.reply_text(user_id)
            await set_user_display(update, context, state="main-menu")
        elif text == "🔙 بازگشت":
            await set_user_display(update, context, state="main-menu")

    elif state == "registrant-panel":
        if text == "✍️ ویرایش کردن":
            await set_user_display(update, context, state="registrant-edit")
        elif text == "❌ حذف کردن":
            await set_user_display(update, context, state="registrant-remove")
        elif text == "🔙 بازگشت":
            if user_id in SALATIN:
                await set_user_display(update, context, state="backdoor-panel-head")
            else:
                await set_user_display(update, context, state="backdoor-panel")

    elif state == "registrant-edit":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="registrant-panel")
        elif is_valid_positive_integer(text):
            target_id = str(int(text))
            registered_users = load_registered_users()
            if target_id not in registered_users:
                await update.message.reply_text("❌ کاربری با این آیدی یافت نشد.")
            else:
                data = registered_users.get(target_id)
                context.user_data["temp-id-slot"] = target_id

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
                                                    f"📄 <b>اطلاعات هدف: (شناسه کاربری \"</b><code>{target_id}</code><b>\")</b> 🆔\n\n"
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
                                                    f"📄 <b>اطلاعات هدف: (شناسه کاربری \"</b><code>{target_id}</code><b>\")</b> 🆔\n\n"
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
                    await set_user_display(update, context, state="registrant-edit-input")
        else:
            await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "registrant-edit-input":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="registrant-panel")
        else:
            try:
                updates = parse_edit_input(text)
                registered_users = load_registered_users()
                target_id = context.user_data["temp-id-slot"]
                context.user_data.pop("temp-id-slot", None)

                if target_id not in registered_users:
                    await update.message.reply_text("❌ کاربر موردنظر یافت نشد.")
                else:
                    registered_users[target_id].update(updates)
                    save_registered_users(registered_users)
                    await update.message.reply_text("✅ اطلاعات با موفقیت به‌روزرسانی شد.")
                    await set_user_display(update, context, state="registrant-panel")

            except ValueError as e:
                await update.message.reply_text(f"❌ خطا: {str(e)}")

    elif state == "registrant-remove":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="registrant-panel")
        elif is_valid_positive_integer(text):
            target_id = str(int(text))
            registered_users = load_registered_users()
            if target_id not in registered_users:
                await update.message.reply_text("❌ کاربری با این آیدی یافت نشد.")
                await set_user_display(update, context, state="registrant-panel")
            else:
                data = registered_users.get(target_id)
                context.user_data["temp-id-slot"] = target_id
                await update.message.reply_text(
                                                f"📄 <b>اطلاعات هدف: (شناسه کاربری \"</b><code>{target_id}</code><b>\")</b> 🆔\n\n"
                                                f"👤 <b>نام:</b> {data['name']}\n"
                                                f"👥 <b>نام خانوادگی:</b> {data['surname']}\n"
                                                f"🔗 <b>آیدی تلگرام:</b> {data['username']}\n"
                                                ,parse_mode='HTML'
                                            )
                await set_user_display(update, context, state="registrant-remove-confirm")
        else:
            await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "registrant-remove-confirm":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="registrant-panel")
        elif text == "YES YES YES I AM 100 PERCANT POSETIVE JUST DELETE THIS POOR PERSON":
            if user_id not in SALATIN:
                await update.message.reply_text("شرمنده گلم ولی همچین اجازه‌ای نمیتونم به شما :)")
            else:
                registered_users = load_registered_users()
                target_id = context.user_data["temp-id-slot"]
                context.user_data.pop("temp-id-slot", None)

            if target_id in registered_users:
                del registered_users[target_id]
                save_registered_users(registered_users)
                await update.message.reply_text("✅ اطلاعات کاربر با موفقیت از لیست حذف شد.")
            else:
                await update.message.reply_text("❌ کاربر مورد نظر در لیست وجود نداشت.")

                await set_user_display(update, context, state="interview-panel")

    elif state == "interview-panel":
        if text == "✅ قبول کردن":
            await set_user_display(update, context, state="interviewee-accept")
        elif text == "🕳️ حذف کردن":
            await set_user_display(update, context, state="interviewee-remove")
        elif text == "❌ رد کردن":
            await set_user_display(update, context, state="interviewee-reject")
        elif text == "🔙 بازگشت":
            if user_id in SALATIN:
                await set_user_display(update, context, state="backdoor-panel-head")
            else:
                await set_user_display(update, context, state="backdoor-panel")

    elif state == "interviewee-accept":
        registered_users = load_registered_users()

        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="interview-panel")
        elif is_valid_positive_integer(text):
            target_id = str(int(text))
            if target_id not in registered_users:
                await update.message.reply_text("❌ کاربری با این آیدی یافت نشد.")
            elif registered_users[target_id].get("is_passed") is True:
                await update.message.reply_text("❇️ قبولی این کاربر قبلا ثبت شده است.")
            else:
                registered_users[target_id]["is_passed"] = True
                save_registered_users(registered_users)
                await update.message.reply_text(f"✅ وضعیت قبولی کاربر {target_id} ثبت شد.")
            await set_user_display(update, context, state="interview-panel")
        else:
            await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "interviewee-remove":
        registered_users = load_registered_users()

        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="interview-panel")
        elif text == "DELETE THE WHOLE DATABASE FOR THOSE POOR SOULS WHO DID OR DID NOT PASS THE INTERVIEW":
            if user_id not in SALATIN:
                await update.message.reply_text("شرمنده گلم ولی همچین اجازه‌ای نمیتونم به شما :)")
            else:
                removed = 0
                for uid, info in registered_users.items():
                    if info.get("is_passed") is not None:
                        info["is_passed"] = None
                        removed += 1
                save_registered_users(registered_users)
                await update.message.reply_text(f"✅ وضعیت مصاحبه {removed} کاربر پاک شد.")
                await set_user_display(update, context, state="interview-panel")
        elif is_valid_positive_integer(text):
            target_id = str(int(text))
            if target_id not in registered_users:
                await update.message.reply_text("❌ کاربری با این آیدی یافت نشد.")
            elif registered_users[target_id].get("is_passed") is None:
                await update.message.reply_text("❌ این کاربر وضعیت مصحابه ندارد.")
            else:
                registered_users[target_id]["is_passed"] = None
                save_registered_users(registered_users)
                await update.message.reply_text(f"✅ وضعیت مصاحبه کاربر {target_id} حذف شد.")
            await set_user_display(update, context, state="interview-panel")
        else:
            await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "interviewee-reject":
        registered_users = load_registered_users()

        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="interview-panel")
        elif is_valid_positive_integer(text):
            target_id = str(int(text))
            if target_id not in registered_users:
                await update.message.reply_text("❌ کاربری با این آیدی یافت نشد.")
            elif registered_users[target_id].get("is_passed") is False:
                await update.message.reply_text("❇️ ردی این کاربر قبلا ثبت شده است.")
            else:
                registered_users[target_id]["is_passed"] = False
                save_registered_users(registered_users)
                await update.message.reply_text(f"✅ وضعیت ردی کاربر {target_id} ثبت شد.")
            await set_user_display(update, context, state="interview-panel")
        else:
            await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "pay-panel":
        if text == "👁️ مشاهده لیست":
            await set_user_display(update, context, state="pay-list")
        elif text == "✅ اضافه کردن":
            await set_user_display(update, context, state="payer-add")
        elif text == "❌ حذف کردن":
            await set_user_display(update, context, state="payer-remove")
        elif text == "🔙 بازگشت":
            if user_id in SALATIN:
                await set_user_display(update, context, state="backdoor-panel-head")
            else:
                await set_user_display(update, context, state="backdoor-panel")

    elif state == "pay-list":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="pay-panel")
            return

        registered_users = load_registered_users()
        result_txt = ""
        count = 0

        if text == "همه":
            for uid, info in registered_users.items():
                if info.get("has_paid") is True:
                    full_name = f"{info.get('name', '')} {info.get('surname', '')}"
                    username = info.get('username', 'نامشخص')
                    course = info.get('course', '-')
                    result_txt += f"• {full_name}\n{username}\n<code>{uid}</code>\n({course})\n\n"
                    count += 1
        else:
            for uid, info in registered_users.items():
                if info.get("has_paid") is True and info.get("course") == text:
                    full_name = f"{info.get('name', '')} {info.get('surname', '')}"
                    username = info.get('username', 'نامشخص')
                    result_txt += f"• {full_name}\n{username}\n<code>{uid}</code>\n\n"
                    count += 1

        if count == 0:
            await update.message.reply_text("❌ هیچ کاربری برای این دسته‌بندی پرداخت نکرده است.")
        else:
            await update.message.reply_text(
                f"✅ لیست پرداخت‌کنندگان ({text}):\n\n{result_txt}",
                parse_mode='HTML'
            )

    elif state == "payer-add":
        registered_users = load_registered_users()

        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="pay-panel")
        else:
            lines = text.splitlines()
            stripped_lines = [line.strip() for line in lines if line.strip()]
            for mini_texts in stripped_lines:
                if is_valid_positive_integer(mini_texts):
                    target_id = str(int(mini_texts))
                    if target_id not in registered_users:
                        await update.message.reply_text(f"❌ کاربری با آیدی {target_id} یافت نشد.")
                    elif registered_users[target_id].get("is_passed") is not True:
                        await update.message.reply_text(f"❌ کاربر {target_id} مصاحبه را قبول نشده.")
                    elif registered_users[target_id].get("has_paid") is True:
                        await update.message.reply_text(f"❇️ پرداخت کاربر {target_id} قبلا ثبت شده است.")
                    else:
                        registered_users[target_id]["has_paid"] = True
                        save_registered_users(registered_users)
                        await update.message.reply_text(f"✅ وضعیت پرداخت کاربر {target_id} ثبت شد.")
                else:
                    await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "payer-remove":
        registered_users = load_registered_users()

        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="pay-panel")
        elif text == "DELETE THE WHOLE DATABASE FOR THOSE POOR SOULS WHO HAVE PAID":
            if user_id not in SALATIN:
                await update.message.reply_text("شرمنده گلم ولی همچین اجازه‌ای نمیتونم به شما :)")
            else:
                removed = 0
                for uid, info in registered_users.items():
                    if info.get("has_paid") is True:
                        info["has_paid"] = False
                        removed += 1
                save_registered_users(registered_users)
                await update.message.reply_text(f"✅ وضعیت پرداخت {removed} کاربر پاک شد.")
        else:
            lines = text.splitlines()
            stripped_lines = [line.strip() for line in lines if line.strip()]
            for mini_texts in stripped_lines:
                if is_valid_positive_integer(mini_texts):
                    target_id = str(int(mini_texts))
                    if target_id not in registered_users:
                        await update.message.reply_text(f"❌ کاربری با آیدی {target_id} یافت نشد.")
                    elif registered_users[target_id].get("has_paid") is not True:
                        await update.message.reply_text(f"❌ کاربر {target_id} وضعیت پرداخت ندارد.")
                    else:
                        registered_users[target_id]["has_paid"] = False
                        save_registered_users(registered_users)
                        await update.message.reply_text(f"✅ پرداخت کاربر {target_id} حذف شد.")
            else:
                await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "admin-list":
        if text == "✅ اضافه کردن":
            await set_user_display(update, context, state="admin-add")
        elif text == "❌ حذف کردن":
            await set_user_display(update, context, state="admin-remove")
        elif text == "🔙 بازگشت":
            await set_user_display(update, context, state="backdoor-panel-head")

    elif state == "admin-add":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="admin-list")
        elif is_valid_positive_integer(text):
            target_id = int(text)
            if get_user_access(target_id) == "admin":
                await update.message.reply_text("❇️ این کاربر هم‌اکنون ادمین است.")
            else:
                set_user_access(user_id= target_id, access= "admin", update= update)
                save_user_access()
                await update.message.reply_text(f"✅ کاربر با آیدی {target_id} با موفقیت به ادمین‌ها اضافه شد.")
            await set_user_display(update, context, state="admin-list")
        else:
            await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "admin-remove":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="admin-list")
        elif text in ["ALL", "All", "all", "همه"]:
            removed = 0
            for uid in list(user_access_keys()):
                if get_user_access(uid) == "admin":
                    set_user_access(user_id= uid, access= "user", update= update)
                    removed += 1

            save_user_access()
            await update.message.reply_text(f"✅ {removed} ادمین با موفقیت حذف شدند.")
            await set_user_display(update, context, state="admin-list")
        elif is_valid_positive_integer(text):
            target_id = int(text)
            if get_user_access(target_id) != "admin":
                await update.message.reply_text("❌ این کاربر ادمین نیست.")
            else:
                set_user_access(user_id= target_id, access= "user", update= update)
                save_user_access()
                await update.message.reply_text(f"✅ کاربر با آیدی {target_id} از لیست ادمین‌ها حذف شد.")
            await set_user_display(update, context, state="admin-list")
        else:
            await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")

    elif state == "filter-panel":
        if text == "✅ تایید":
            await update.message.reply_text(str(context.user_data.get('filters', [])))
            if (context.user_data['filter-mode'] == "broadcast"):
                await set_user_display(update, context, state="message-panel")
            elif (context.user_data['filter-mode'] == "search"):
                registered_users = load_registered_users()
                filtered = {
                            uid: info for uid, info in registered_users.items()
                            if user_matches(info, context.user_data.get('filters', []), uid)
                            }
                count = len(filtered)
                await update.message.reply_text(f"تعداد کاربران انتخاب‌شده: {count}")
                await set_user_display(update, context, state="search-confirm")
        elif text == "🔙 بازگشت":
            if (context.user_data['filter-mode'] == "broadcast"):
                if user_id in SALATIN:
                    await set_user_display(update, context, state="backdoor-panel-head")
                else:
                    await set_user_display(update, context, state="backdoor-panel")
            elif (context.user_data['filter-mode'] == "search"):
                await set_user_display(update, context, state="search-choose")
        else:
            await filter_input(update, context)

    elif state == "message-panel":
        if text == "🔙 بازگشت":
            if user_id in SALATIN:
                await set_user_display(update, context, state="backdoor-panel-head")
            else:
                await set_user_display(update, context, state="backdoor-panel")
        else:
            if (await message_input(update, context)):
                await set_user_display(update, context, state="broadcast-confirm")

    elif state == "broadcast-confirm":
        if text == "❌ خیر":
            await update.message.reply_text("لغو شد.")
            next_state = "backdoor-panel-head" if user_id in SALATIN else "backdoor-panel"
            await set_user_display(update, context, state=next_state)
            return

        elif text == "✅ بله":
            registered_users = load_registered_users()
            users = {
                uid: info for uid, info in registered_users.items()
                if user_matches(info, context.user_data.get('filters', []), uid)
            }

            btype = context.user_data.get('broadcast_type')
            sent = 0

            for uid, info in users.items():
                try:
                    if btype == 'text':
                        msg = context.user_data['template'].format(**info, id=uid)
                        await context.bot.send_message(chat_id=int(uid), text=msg, parse_mode='HTML')

                    elif btype == 'photo':
                        caption = context.user_data['caption'].format(**info, id=uid)
                        await context.bot.send_photo(
                            chat_id=int(uid),
                            photo=context.user_data['photo_file_id'],
                            caption=caption,
                            parse_mode='HTML'
                        )

                    elif btype == 'forward':
                        await context.bot.forward_message(
                            chat_id=int(uid),
                            from_chat_id=context.user_data['from_chat_id'],
                            message_id=context.user_data['from_message_id']
                        )

                    sent += 1
                except Exception:
                    continue

            await update.message.reply_text(f"✅ ارسال انجام شد به {sent} کاربر.")
            next_state = "backdoor-panel-head" if user_id in SALATIN else "backdoor-panel"
            await set_user_display(update, context, state=next_state)

    elif state == "search-confirm":
        if text == "❌ خیر":
            await update.message.reply_text("لغو شد.")
            await set_user_display(update, context, state="search-choose")
        elif text == "✅ بله":
            registered_users = load_registered_users()
            users = {
                    uid: info for uid, info in registered_users.items()
                    if user_matches(info, context.user_data.get('filters', []), uid)
                    }

            if not users:
                await update.message.reply_text("هیچ کاربری با این مشخصات یافت نشد.")
            else:
                items = list(users.items())

                for i in range(0, len(items), USERS_PER_MSG):
                    chunk = items[i:i + USERS_PER_MSG]
                    result = f"👥 <b>نتایج جست‌وجو ({i+1}-{min(i+USERS_PER_MSG, len(items))}):</b>\n\n"
                    for uid, info in chunk:
                        try:
                            result += render_user_summary(uid, info) + "\n\n"
                        except Exception as e:
                            result += f"❗️خطا در نمایش کاربر {uid}: {e}\n\n"
                    await update.message.reply_text(result.strip(), parse_mode='HTML')

            await set_user_display(update, context, state="search-choose")

    elif state == "search-choose":
        if get_user_access(user_id) != "admin" and user_id not in SALATIN:
            await update.message.reply_text("دسترسی ندارید.")
            return
        if text == "🌐 اعمال فیلتر":
            start_filter(update, context, "search")
            await set_user_display(update, context, state="filter-panel")
        elif text == "📃 اطلاعات کاربر":
            await set_user_display(update, context, state="user-search")
        elif text == "🔙 بازگشت":
            if user_id in SALATIN:
                await set_user_display(update, context, state="backdoor-panel-head")
            else:
                await set_user_display(update, context, state="backdoor-panel")

    elif state == "user-search":
        if text == "🔙 بازگشت":
            await set_user_display(update, context, state="search-choose")
        elif is_valid_positive_integer(text):
            target_id = str(int(text))
            registered_users = load_registered_users()
            if target_id not in registered_users:
                await update.message.reply_text("❌ کاربری با این آیدی یافت نشد.")
            else:
                data = registered_users.get(target_id)

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
                                                    f"📄 <b>اطلاعات هدف: (شناسه کاربری \"</b><code>{target_id}</code><b>\")</b> 🆔\n\n"
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
                                                    f"📄 <b>اطلاعات هدف: (شناسه کاربری \"</b><code>{target_id}</code><b>\")</b> 🆔\n\n"
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
        else:
            await update.message.reply_text("❌ لطفاً یک عدد صحیح مثبت وارد کنید.")
