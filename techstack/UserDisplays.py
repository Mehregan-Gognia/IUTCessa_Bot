
def get_state_keyboard(state: str):
    if state == "main-menu":
        return [["🎓 طرح کمک‌یار", "🛠️ تک‌استک"],
                ["📞 تماس با ما", "❓ درباره ما"]]
    elif state == "kmk-yar-main":
        return [["👥 عضویت در گروه", "📝 ثبت‌نام"],
                ["🔙 بازگشت"]]
    elif state == "kmk-yar-get-link":
        return [["توسعه و هم‌افزایی", "امور علمی و پژوهشی"],
                ["امور فنی", "مستندات"],
                ["🔙 بازگشت"]]
    elif state == "tech-stack-main":
        return [["🔔 به من یادآوری کن", "📓 مشاهده اطلاعات ثبت‌شده", "📝 ثبت‌نام اولیه"],
                ["🔙 بازگشت", "💫 مشاهده نتایج مصاحبه و پرداخت شهریه"]]
    elif state == "tech-stack-first-forum":
        return [["🔙 بازگشت"]]
    elif state == "tech-stack-user-info-confirm":
        return [["❌ خیر","✅ بله"]]
    elif state == "tech-stack-decision":
        return [["Back-End", "Front-End"],
                ["DevOps", "Graphic Design", "AI"],
                ["Game", "Blockchain"],
                ["🔙 بازگشت", "❌ حذف"]]
    elif state == "tech-stack-pay":
        return [["🔙 بازگشت"]]
    elif state == "tach-stack-remind":
        return [["❌ حذف کردن","✅ اضافه کردن"],
                ["🔙 بازگشت"]]
    elif state == "remind-add":
        return [["Back-End", "Front-End"],
                ["DevOps", "Graphic Design", "AI"],
                ["Game", "Blockchain"],
                ["🔙 بازگشت"]]
    elif state == "remind-remove":
        return [["Back-End", "Front-End"],
                ["DevOps", "Graphic Design", "AI"],
                ["Game", "Blockchain"],
                ["🔙 بازگشت"]]

def get_state_text(state: str) -> str:
    if state == "main-menu":
        return "بازگشت به منوی اصلی"
    elif state == "kmk-yar-main":
        return "یکی از گزینه‌های زیر را انتخاب کنید:"
    elif state == "kmk-yar-get-link":
        return "لطفا حوزه‌ی مورد نظر را انتخاب کنید:"
    elif state == "tech-stack-main":
        return "یکی از گزینه‌های زیر را انتخاب کنید:"
    elif state == "tech-stack-first-forum":
        return ("لطفا اطلاعات مورد نیاز را به این ترتیب وارد کنید" + "\n" +
                "نام: (فارسی)" + "\n" +
                "نام خانوادگی: (فارسی)" + "\n" +
                "شهر محل زندگی: (فارسی)" + "\n" +
                "شماره تلفن: (اعداد انگلیسی)" + "\n" +
                "شماره دانشجویی: (اعداد انگلیسی)" + "\n" +
                "سال ورودی: (اعداد انگلیسی)" + "\n" + "\n" +
                "مثال: " + "\n" +
                "امیرمحمد" + "\n" +
                "میرزایی" + "\n" +
                "اصفهان" + "\n" +
                "09987515432" + "\n" +
                "40143203" + "\n" +
                "1401" + "\n\n" +
                "نکته: درصورتی که دانشجوی دانشگاه صنعتی اصفهان نیستید، می‌توانید با مراجعه به اکانت پشتیبانی انجمن یک شماره دانشجویی موقت بگیرید." + "\n"
        )
    elif state == "tech-stack-user-info-confirm":
        return "آیا اطلاعات بالا را تایید می‌کنید؟ (توجه کنید که این اطلاعات را نمی‌توانید در آینده تغییر دهید)"
    elif state == "tech-stack-decision":
        return "لطفا حوزه‌ی مورد نظر را انتخاب کنید:"
    elif state == "tech-stack-pay":
        return (
            "لطفاً فیش واریزی خود را در اینجا ارسال کنید (حتماً به صورت عکس)." + "\n\n"
            "💳 شماره کارت جهت واریز:\n\n"
            "`6037 9982 6388 2192`"
            "\nمبلغ 150 هزار تومان مختص دانشجویان صنعتی، و 300 هزار تومان برای دانشجوهای دیگر\n"
            "محمد بزاززاده\n"
        )
    elif state == "tach-stack-remind":
        return ("در این قسمت می‌توانید دوره‌های مدنظر خود را انتخاب کنید تا هنگام برگزاری جلسه معارفه از طریق ربات مطلع شوید." + "\n" +
                "(⚠️ نیاز به یادآوری است که این قسمت جزو دوره اصلی و ثبت‌نام شما محاسبه نمی‌شود ⚠️)")
    elif state == "remind-add":
        return "لطفا حوزه‌ی مورد نظر را انتخاب کنید:"
    elif state == "remind-remove":
        return "لطفا حوزه‌ی مورد نظر را انتخاب کنید:"
