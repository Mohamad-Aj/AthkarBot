import telebot
import logging
import threading
import time
import random
import os
import datetime


# Get the bot token from .env
BOT_TOKEN = os.getenv("ATHKAR_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

# Athkar from the **Quran, Sahih Al-Bukhari, and Sahih Muslim**
DEFAULT_ATHKAR_LIST = [
    # 📖 أدعية من القرآن الكريم
    "﴿ وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً ﴾ (الروم: 21)",
    "﴿ رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا ﴾ (الفرقان: 74)",
    "﴿ وَأَنكِحُوا ٱلْأَيَٰمَىٰ مِنكُمْ وَٱلصَّٰلِحِينَ مِنْ عِبَادِكُمْ وَإِمَآئِكُمْ ﴾ (النور: 32)",
    "﴿ فَإِن طِبْنَ لَكُم عَن شَىْءٍۢ مِّنْهُ نَفْسًۭا فَكُلُوهُ هَنِيٓـًۭٔا مَّرِيٓـًۭٔا ﴾ (النساء: 4)",
    "﴿ وَإِن يَتَفَرَّقَا يُغْنِ ٱللَّهُ كُلًّۢا مِّن سَعَتِهِۦ ﴾ (النساء: 130)",
    "﴿ وَلَا تَنكِحُوا ٱلْمُشْرِكَٰتِ حَتَّىٰ يُؤْمِنَّ ﴾ (البقرة: 221)",
    "﴿ رَبِّ إِنِّي لِمَا أَنْزَلْتَ إِلَيَّ مِنْ خَيْرٍ فَقِيرٌ ﴾ (القصص: 24)", 
    "﴿ رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الْآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ ﴾ (البقرة: 201)",
    "﴿ رَبِّ زِدْنِي عِلْمًا ﴾ (طه: 114)",
    "﴿ وَقُلْ رَبِّ أَعُوذُ بِكَ مِنْ هَمَزَاتِ الشَّيَاطِينِ ﴾ (المؤمنون: 97)",
    "﴿ رَبِّ اشْرَحْ لِي صَدْرِي ﴾ (طه: 25)",
    "﴿ رَبِّ اغْفِرْ لِي وَلِوَالِدَيَّ وَلِلْمُؤْمِنِينَ ﴾ (إبراهيم: 41)",

    # 📜 أحاديث نبوية عن الزواج
  
    # 📌 دعاء النبي ﷺ ليلة الزواج
    "كان النبي ﷺ إذا تزوج قال: اللهم إني أسألك خيرها وخير ما جبلتها عليه، وأعوذ بك من شرها وشر ما جبلتها عليه. (رواه أبو داود وابن ماجه وصححه الألباني)",

    # 📌 فضل الزوجة الصالحة
    "قال رسول الله ﷺ: الدنيا متاع، وخير متاع الدنيا المرأة الصالحة. (رواه مسلم)",
    "قال رسول الله ﷺ: أربع من السعادة: المرأة الصالحة، والمسكن الواسع، والجار الصالح، والمركب الهنيء. (رواه ابن حبان وصححه الألباني)",

    # 📌 الحث على الزواج
    "قال رسول الله ﷺ: يا معشر الشباب، من استطاع منكم الباءة فليتزوج، فإنه أغض للبصر وأحصن للفرج. (رواه البخاري ومسلم)",

    # 📌 دعاء عند الجماع
    "قال رسول الله ﷺ: لو أن أحدكم إذا أتى أهله قال: بسم الله، اللهم جنبنا الشيطان، وجنب الشيطان ما رزقتنا، فإنه إن يُقدّر بينهما ولد، لم يضره الشيطان أبدًا. (رواه البخاري ومسلم)",

    # 📌 حسن المعاشرة بين الزوجين
    "قال رسول الله ﷺ: خيرُكم خيرُكم لأهلِهِ وأنا خيرُكم لأهلِي. (رواه الترمذي وصححه الألباني)",
    "قال رسول الله ﷺ: أكمَلُ المؤمنينَ إيمانًا أحسنُهم خُلقًا، وخيارُكم خيارُكم لنسائِهِم. (رواه الترمذي وصححه الألباني)",
    "قال رسول الله ﷺ: استوصوا بالنساء خيرًا، فإنهن خُلقن من ضلع. (رواه البخاري ومسلم)",

    # 📌 الحث على الزواج من المرأة الصالحة
    "قال رسول الله ﷺ: تُنكح المرأة لأربع: لمالها، ولحسبها، ولجمالها، ولدينها، فاظفر بذات الدين تَرِبَت يداك. (رواه البخاري ومسلم)",

    # 📌 دعاء التوفيق بين الزوجين
    "قال رسول الله ﷺ: ثلاثة حق على الله عونهم: المجاهد في سبيل الله، والمكاتب الذي يريد الأداء، والناكح الذي يريد العفاف. (رواه الترمذي وصححه الألباني)",

    # 📌 دعاء للألفة والمودة بين الزوجين
    "اللهم ألف بين قلوبنا، وأصلح ذات بيننا، واهدنا سبل السلام، ونجنا من الظلمات إلى النور. (حديث حسن رواه أبو داود وصححه الألباني)",

    # 📌 دعاء لحفظ العلاقة الزوجية من الشيطان
    "قال رسول الله ﷺ: إن الشيطان يجري من ابن آدم مجرى الدم، فاجعلوا بينكم وبينه سترًا بالصلاة والدعاء. (رواه البخاري ومسلم)",

    # 📌 دعاء لحفظ الزوج والزوجة من الفتنة
    "اللهم احفظني بحلالك عن حرامك، واغنني بفضلك عمّن سواك. (رواه الترمذي وصححه الألباني)",

      # 📌 دعاء عند الحاجة إلى الصبر على الزوج/الزوجة
    "اللهم ارزقني الصبر، وأعني على حسن العشرة، واهدنا لما تحب وترضى. (رواه البخاري ومسلم بمعناه)",

    # 📌 دعاء عند فقدان الزوج أو الزوجة
    "اللهم أجرني في مصيبتي، واخلفني خيرًا منها. (رواه مسلم)",

    # 📌 دعاء عند الطلاق أو الانفصال
    "اللهم إن كان خيرًا لنا فاجمعنا، وإن كان شرًا لنا فاصرفه عنا، ووفقنا لما فيه الخير لنا في ديننا ودنيانا. (مستنبط من أدعية النبي ﷺ في الفتن والشدائد)",   

    # 📜 الأربعون النووية (40 Nawawi Hadiths)
    "إنما الأعمال بالنيات، وإنما لكل امرئ ما نوى. (رواه البخاري ومسلم)",
    "من حسن إسلام المرء تركه ما لا يعنيه. (رواه الترمذي وصححه الألباني)",
    "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه. (رواه البخاري ومسلم)",
    "إن الحلال بيّن وإن الحرام بيّن وبينهما أمور مشتبهات. (رواه البخاري ومسلم)",
    "الدين النصيحة. (رواه مسلم)",
    "الحلال بيّن والحرام بيّن وبينهما أمور مشتبهات. (رواه البخاري ومسلم)",
    "الدعاء هو العبادة. (رواه الترمذي وصححه الألباني)",
    "إن الله طيب لا يقبل إلا طيبًا. (رواه مسلم)",
    "دع ما يريبك إلى ما لا يريبك. (رواه الترمذي والنسائي وصححه الألباني)",
    "من كان يؤمن بالله واليوم الآخر فليقل خيرًا أو ليصمت. (رواه البخاري ومسلم)",
    "لا تغضب. (رواه البخاري)",
    "أحب الأعمال إلى الله أدومها وإن قل. (رواه البخاري ومسلم)",
    "من حسن إسلام المرء تركه ما لا يعنيه. (رواه الترمذي وصححه الألباني)",
    "إن الله كتب الإحسان على كل شيء. (رواه مسلم)",
    "اتق الله حيثما كنت. (رواه الترمذي وصححه الألباني)",
    "لا تحقرن من المعروف شيئًا ولو أن تلقى أخاك بوجه طلق. (رواه مسلم)",
    "إن الله يغفر الذنوب جميعًا. (رواه مسلم)",
    "من دل على خير فله مثل أجر فاعله. (رواه مسلم)",
    "الدنيا سجن المؤمن وجنة الكافر. (رواه مسلم)",
    "من سلك طريقًا يلتمس فيه علمًا سهل الله له طريقًا إلى الجنة. (رواه مسلم)",
    "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه. (رواه البخاري ومسلم)",
    "من صلى الفجر في جماعة فهو في ذمة الله. (رواه مسلم)",
    "خيركم من تعلم القرآن وعلمه. (رواه البخاري)",
    "من كان في حاجة أخيه كان الله في حاجته. (رواه مسلم)",
    "ليس الشديد بالصرعة، إنما الشديد الذي يملك نفسه عند الغضب. (رواه البخاري ومسلم)",
    "من صام رمضان إيمانًا واحتسابًا غفر له ما تقدم من ذنبه. (رواه البخاري ومسلم)",
    "من غشنا فليس منا. (رواه مسلم)",
    "ازهد في الدنيا يحبك الله. (رواه ابن ماجه وصححه الألباني)",
    "من توضأ فأحسن الوضوء خرجت خطاياه. (رواه مسلم)",
    "الظلم ظلمات يوم القيامة. (رواه البخاري ومسلم)",
    "من سمع النداء ولم يجب فلا صلاة له إلا من عذر. (رواه ابن ماجه وصححه الألباني)",
    "من صلى العشاء في جماعة فكأنما قام نصف الليل. (رواه مسلم)",
    "من سلك طريقًا يلتمس فيه علمًا سهل الله له طريقًا إلى الجنة. (رواه مسلم)",
    "الدين النصيحة. (رواه مسلم)",
    "من لا يشكر الناس لا يشكر الله. (رواه الترمذي وصححه الألباني)",
    "إن الله كتب الإحسان على كل شيء. (رواه مسلم)",
    "إنما الأعمال بالخواتيم. (رواه البخاري)",

    # 🌿 الأذكار اليومية من السنة النبوية
    "سبحان الله الحمد لله لا اله الا الله والله اكبر",
    "لا حول ولا قوة إلا بالله",
    "سبحان الله وبحمده، سبحان الله العظيم",
    "أستغفلر الله وأتوب اليه",
    "اللهم صلِّ وسلم وبارك على نبينا محمد",

    #  🌅 أذكار الصباح والمساء
    "اللهم بك أصبحنا وبك أمسينا، وبك نحيا وبك نموت وإليك النشور. (رواه الترمذي)",
    "اللهم إني أعوذ بك من الهم والحزن، والعجز والكسل، والجبن والبخل، وغلبة الدين وقهر الرجال. (رواه البخاري)",
    "اللهم أنت ربي لا إله إلا أنت، خلقتني وأنا عبدك، وأنا على عهدك ووعدك ما استطعت. (رواه البخاري)",

      # 🏆 دعاء تحقيق الأمنيات
    "اللهم يسر لي أمري، واشرح لي صدري، واحلل عقدة من لساني يفقهوا قولي. (طه: 25-28)",
    "اللهم لا سهل إلا ما جعلته سهلاً، وأنت تجعل الحزن إذا شئت سهلاً. (رواه ابن حبان)",

    # 📖 دعاء طلب العلم
    "اللهم انفعني بما علمتني، وعلمني ما ينفعني، وزدني علما. (رواه الترمذي وصححه الألباني)",

    # 💪 دعاء القوة والصبر
    "اللهم إني أسألك العزيمة على الرشد، والغنيمة من كل بر، والسلامة من كل إثم، والفوز بالجنة، والنجاة من النار. (رواه الترمذي)",

    # 🤲 أدعية الاستغفار والتوبة
    "أستغفر الله الذي لا إله إلا هو الحي القيوم وأتوب إليه. (رواه الترمذي)",
    "اللهم اغفر لي ذنبي كله، دقه وجله، وأوله وآخره، وعلانيته وسره. (رواه مسلم)",
]

athkar_list = DEFAULT_ATHKAR_LIST.copy()


# Store user Quran reading plans and timers
user_werd_settings = {}
user_werd_timers = {}
user_timers = {}
user_intervals = {}  # Store custom intervals per user (in seconds)


JUZ_STRUCTURE = [
    {"juz": 1, "start": {"surah": "الفاتحة", "page": 1}, "end": {"surah": "البقرة", "page": 21}},
    {"juz": 2, "start": {"surah": "البقرة", "page": 22}, "end": {"surah": "البقرة", "page": 41}},
    {"juz": 3, "start": {"surah": "البقرة", "page": 42}, "end": {"surah": "آل عمران", "page": 61}},
    {"juz": 4, "start": {"surah": "آل عمران", "page": 62}, "end": {"surah": "النساء", "page": 81}},
    {"juz": 5, "start": {"surah": "النساء", "page": 82}, "end": {"surah": "النساء", "page": 101}},
    {"juz": 6, "start": {"surah": "النساء", "page": 102}, "end": {"surah": "المائدة", "page": 121}},
    {"juz": 7, "start": {"surah": "المائدة", "page": 122}, "end": {"surah": "الأنعام", "page": 141}},
    {"juz": 8, "start": {"surah": "الأنعام", "page": 142}, "end": {"surah": "الأعراف", "page": 161}},
    {"juz": 9, "start": {"surah": "الأعراف", "page": 162}, "end": {"surah": "الأنفال", "page": 181}},
    {"juz": 10, "start": {"surah": "الأنفال", "page": 182}, "end": {"surah": "التوبة", "page": 201}},
    {"juz": 11, "start": {"surah": "التوبة", "page": 202}, "end": {"surah": "هود", "page": 221}},
    {"juz": 12, "start": {"surah": "هود", "page": 222}, "end": {"surah": "يوسف", "page": 241}},
    {"juz": 13, "start": {"surah": "يوسف", "page": 242}, "end": {"surah": "إبراهيم", "page": 261}},
    {"juz": 14, "start": {"surah": "الحجر", "page": 262}, "end": {"surah": "النحل", "page": 281}},
    {"juz": 15, "start": {"surah": "الإسراء", "page": 282}, "end": {"surah": "الكهف", "page": 301}},
    {"juz": 16, "start": {"surah": "الكهف", "page": 302}, "end": {"surah": "طه", "page": 321}},
    {"juz": 17, "start": {"surah": "الأنبياء", "page": 322}, "end": {"surah": "الحج", "page": 341}},
    {"juz": 18, "start": {"surah": "المؤمنون", "page": 342}, "end": {"surah": "الفرقان", "page": 361}},
    {"juz": 19, "start": {"surah": "الفرقان", "page": 362}, "end": {"surah": "النمل", "page": 381}},
    {"juz": 20, "start": {"surah": "النمل", "page": 382}, "end": {"surah": "العنكبوت", "page": 401}},
    {"juz": 21, "start": {"surah": "العنكبوت", "page": 402}, "end": {"surah": "الأحزاب", "page": 421}},
    {"juz": 22, "start": {"surah": "الأحزاب", "page": 422}, "end": {"surah": "يس", "page": 441}},
    {"juz": 23, "start": {"surah": "يس", "page": 442}, "end": {"surah": "الزمر", "page": 461}},
    {"juz": 24, "start": {"surah": "الزمر", "page": 462}, "end": {"surah": "فصلت", "page": 481}},
    {"juz": 25, "start": {"surah": "فصلت", "page": 482}, "end": {"surah": "الجاثية", "page": 501}},
    {"juz": 26, "start": {"surah": "الأحقاف", "page": 502}, "end": {"surah": "الذاريات", "page": 521}},
    {"juz": 27, "start": {"surah": "الذاريات", "page": 522}, "end": {"surah": "الحديد", "page": 541}},
    {"juz": 28, "start": {"surah": "المجادلة", "page": 542}, "end": {"surah": "التحريم", "page": 561}},
    {"juz": 29, "start": {"surah": "الملك", "page": 562}, "end": {"surah": "المرسلات", "page": 581}},
    {"juz": 30, "start": {"surah": "النبأ", "page": 582}, "end": {"surah": "الناس", "page": 604}},
]


def generate_quran_schedule(days):
    """Distribute Quran reading plan evenly over a given number of days."""
    total_juz = 30

    # Distribute Juz' as evenly as possible
    base_juz_per_day = total_juz // days  # Minimum Juz' per day
    extra_juz = total_juz % days  # Extra Juz' to distribute
    
    schedule = []
    start_index = 0

    for day in range(1, days + 1):
        # Assign an extra Juz' to some days until they are exhausted
        juz_for_today = base_juz_per_day + (1 if extra_juz > 0 else 0)
        extra_juz -= 1

        # Determine the start and end of today's Werd
        start_surah = JUZ_STRUCTURE[start_index]["start"]["surah"]
        start_page = JUZ_STRUCTURE[start_index]["start"]["page"]
        
        end_index = start_index + juz_for_today - 1
        if end_index >= len(JUZ_STRUCTURE):
            end_index = len(JUZ_STRUCTURE) - 1

        end_surah = JUZ_STRUCTURE[end_index]["end"]["surah"]
        end_page = JUZ_STRUCTURE[end_index]["end"]["page"]

        # Store the day's Werd
        schedule.append(
            f"📖 يوم {day}:\n"
            f"🔹 يبدأ من: {start_surah} (صفحة {start_page})\n"
            f"🔹 ينتهي عند: {end_surah} (صفحة {end_page})"
            f"\n📚 عدد الأجزاء لهذا اليوم: {juz_for_today}"
        )

        # Move to the next Juz'
        start_index = end_index + 1

    return "\n\n".join(schedule)
        


@bot.message_handler(commands=["setwerd"])
def set_werd_system(message: telebot.types.Message):
    """Allow users to set their completion goal (number of days)."""
    chat_id = message.chat.id
    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ يرجى إدخال عدد الأيام، مثال: **/setwerd 7**")
        return

    days = int(args[1])
    if days < 1:
        bot.reply_to(message, "⚠️ الحد الأدنى هو يوم واحد!")
        return

    # Generate Quran schedule
    quran_schedule = generate_quran_schedule(days)
    schedule_list = quran_schedule.split("\n\n")

    user_werd_settings[chat_id] = {
        "days": days,
        "schedule": schedule_list,
        "finished_today": False,
        "start_date": datetime.datetime.now()  # Track when the schedule started
    }

    today_index = 0  # Always start with the first day's Werd
    today_werd = schedule_list[today_index] if today_index < len(schedule_list) else "⚠️ لا يوجد ورد محدد لليوم."

    full_schedule_text = "\n\n".join(schedule_list)

    bot.reply_to(message, f"✅ تم ضبط الورد على {days} أيام!\n\n📖 **جدول الورد بالكامل:**\n{full_schedule_text}")

    # Start reminders
    start_hourly_reminders(chat_id)



@bot.message_handler(commands=["werd"])
def send_werd(message: telebot.types.Message):
    """Send today's Quran Werd based on the user's schedule."""
    chat_id = message.chat.id

    if chat_id not in user_werd_settings:
        bot.reply_to(message, "⚠️ لم تحدد بعد جدول ورد، استخدم **/setwerd <عدد الأيام>**.")
        return

    days = user_werd_settings[chat_id]["days"]
    schedule_list = user_werd_settings[chat_id]["schedule"]

    start_date = user_werd_settings[chat_id]["start_date"]
    elapsed_days = (datetime.datetime.now() - start_date).days
    today_index = elapsed_days % days  # Ensure cycling within range
    # Get today's index
    today_werd = schedule_list[today_index] if today_index < len(schedule_list) else "⚠️ لا يوجد ورد محدد لليوم."

    bot.reply_to(message, f"📖 **ورد اليوم:**\n{today_werd}")


def send_werd_reminder(chat_id):
    """Send daily Quran Werd reminder only if not marked as done."""
    if chat_id not in user_werd_settings:
        return

    # If the user already finished today’s Werd, do nothing
    if user_werd_settings[chat_id]["finished_today"]:
        return

    # Calculate the Werd for today
    start_date = user_werd_settings[chat_id]["start_date"]
    elapsed_days = (datetime.datetime.now() - start_date).days

    # Keep the same Werd until the user marks it as done
    today_index = elapsed_days % user_werd_settings[chat_id]["days"]

    schedule = user_werd_settings[chat_id]["schedule"]

    if today_index < len(schedule):
        today_werd = schedule[today_index]
        bot.send_message(chat_id, f"📖 ورد اليوم:\n{today_werd}")
    else:
        bot.send_message(chat_id, "⚠️ لا يوجد ورد محدد لليوم.")

    # Schedule the next reminder for the next day at midnight
    next_reminder_time = datetime.datetime.now().replace(hour=0, minute=0, second=1) + datetime.timedelta(days=1)
    delay = (next_reminder_time - datetime.datetime.now()).total_seconds()

    user_werd_timers[chat_id] = threading.Timer(delay, send_werd_reminder, [chat_id])
    user_werd_timers[chat_id].start()



def start_hourly_reminders(chat_id):
    """Starts the hourly reminder system for the user."""
    if chat_id in user_werd_timers:
        user_werd_timers[chat_id].cancel()  # Cancel any existing reminders

    user_werd_timers[chat_id] = threading.Timer(1, send_werd_reminder, [chat_id])
    user_werd_timers[chat_id].start()

@bot.message_handler(commands=["donewerd"])
def mark_werd_done(message: telebot.types.Message):
    """Mark today's Werd as finished and schedule reminders for the next day."""
    chat_id = message.chat.id
    if chat_id in user_werd_settings:
        # Mark today as finished
        user_werd_settings[chat_id]["finished_today"] = True

        # Cancel current reminders
        if chat_id in user_werd_timers:
            user_werd_timers[chat_id].cancel()
        
        bot.reply_to(message, "✅ تم تسجيل ورد اليوم كمقروء! سيتم تذكيرك غدًا 📖")

        # Start a new reminder at the beginning of the next day
        next_reminder_time = datetime.datetime.now().replace(hour=0, minute=0, second=1) + datetime.timedelta(days=1)
        delay = (next_reminder_time - datetime.datetime.now()).total_seconds()

        user_werd_timers[chat_id] = threading.Timer(delay, send_werd_reminder, [chat_id])
        user_werd_timers[chat_id].start()
    else:
        bot.reply_to(message, "⚠️ لم تحدد بعد جدول ورد، استخدم **/setwerd <عدد الأيام>**.")


def send_athkar_to_user(chat_id):
    """Send a random Athkar to the user and restart the timer."""
    if chat_id in user_timers and athkar_list:
        athkar = random.choice(athkar_list)
        try:
            bot.send_message(chat_id, athkar)
        except Exception as e:
            logger.error(f"Failed to send Athkar to {chat_id}: {e}")

        # Restart timer with user's custom interval
        interval = user_intervals.get(chat_id, 1800)  # Default to 30 minutes if not set
        user_timers[chat_id] = threading.Timer(interval, send_athkar_to_user, [chat_id])
        user_timers[chat_id].start()

@bot.message_handler(commands=["resetlist"])
def reset_athkar_list(message: telebot.types.Message):
    """Reset the Athkar list to the default values."""
    global athkar_list
    athkar_list = DEFAULT_ATHKAR_LIST.copy()
    bot.reply_to(message, "🔄 تم إعادة ضبط قائمة الأذكار إلى الإعدادات الافتراضية.")

@bot.message_handler(commands=["addthikr"])
def add_thikr(message: telebot.types.Message):
    """Allow a user to add a new Thikr to the list."""
    global athkar_list
    new_thikr = message.text.replace("/addthikr", "").strip()

    if not new_thikr:
        bot.reply_to(message, "⚠️ يرجى كتابة الذكر بعد الأمر، مثال: **/addthikr سبحان الله**")
        return

    athkar_list.append(new_thikr)
    bot.reply_to(message, f"✅ تم إضافة الذكر بنجاح!\n\n🔢 رقم الذكر: **{len(athkar_list)}**")

@bot.message_handler(commands=["listthikr"])
def list_thikr(message: telebot.types.Message):
    """List all the Athkar with their numbers in multiple messages if needed."""
    if not athkar_list:
        bot.reply_to(message, "📭 قائمة الأذكار فارغة حاليًا.")
        return

    response = "📜 قائمة الأذكار:\n\n"
    messages = []
    
    for i, thikr in enumerate(athkar_list, start=1):
        thikr_text = f"**{i}.** {thikr}\n"
        
        if len(response) + len(thikr_text) > 4000:  # If message is too long, store and start a new one
            messages.append(response)
            response = "📜 تابع قائمة الأذكار:\n\n"
        
        response += thikr_text

    messages.append(response)  # Add the last batch

    for msg in messages:
        bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=["delthikr"])
def delete_thikr(message: telebot.types.Message):
    """Delete a Thikr from the list by number."""
    global athkar_list
    args = message.text.split()

    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ يرجى إدخال رقم الذكر الذي تريد حذفه، مثال: **/delthikr 2**")
        return

    index = int(args[1]) - 1

    if index < 0 or index >= len(athkar_list):
        bot.reply_to(message, "❌ الرقم غير صحيح. استخدم **/listthikr** لرؤية الأذكار المتاحة.")
        return

    removed_thikr = athkar_list.pop(index)
    bot.reply_to(message, f"🗑️ تم حذف الذكر:\n\n_{removed_thikr}_")

@bot.message_handler(commands=["start","help"])
def send_welcome(message: telebot.types.Message):
    """Send welcome message with instructions."""
    logger.info(f"- User started: {message.chat.username}")
    welcome_text = (
        "👋 مرحبًا بك في **بوت الأذكار والورد القرآني**! 🤲📖\n\n"
        
        "📖 **قسم ورد القرآن:**\n"
        "🔹 **/setwerd <عدد الأيام>** - حدد عدد الأيام التي تريد إنهاء القرآن فيها، وسيقوم البوت بتقسيم القراءة يوميًا.\n"
        "🔹 **/werd** - احصل على ورد اليوم (يتم تحديثه تلقائيًا كل ساعة).\n"
        "🔹 **/donewerd** - أبلغ البوت أنك أنهيت ورد اليوم، ولن يتم إرسال تذكيرات حتى الغد.\n\n"

        "🕌 **قسم الأذكار:**\n"
        "🔹 **/subscribe** - اشترك لاستقبال الأذكار العشوائية كل 30 دقيقة (أو حسب تفضيلاتك).\n"
        "🔹 **/unsubscribe** - إلغاء الاشتراك في الأذكار.\n"
        "🔹 **/settime <عدد الدقائق>** - تغيير فترة إرسال الأذكار.\n"
        "🔹 **/resetlist** - إعادة ضبط قائمة الأذكار إلى القائمة الافتراضية.\n"
        "🔹 **/addthikr <ذكر جديد>** - أضف ذكرًا خاصًا بك إلى القائمة.\n"
        "🔹 **/listthikr** - عرض قائمة الأذكار المتاحة.\n"
        "🔹 **/delthikr <رقم الذكر>** - حذف ذكر من القائمة.\n\n"

        "📌 **معلومات إضافية:**\n"
        "✅ سيتم إرسال **تذكيرات الورد القرآني كل ساعة** حتى تقوم بإنهائه.\n"
        "✅ يمكنك اختيار **المدة التي تناسبك لإنهاء القرآن**.\n"
        "✅ استخدم **/werd** في أي وقت لمعرفة ورد اليوم.\n"
        "✅ استخدم **/donewerd** عند انتهاء القراءة اليومية لإيقاف التذكيرات.\n\n"

        "🌟 **ابدأ الآن بكتابة /setwerd 7 مثلًا لإنهاء القرآن في 7 أيام!** 🌟"
    )
    bot.reply_to(message, welcome_text)


@bot.message_handler(commands=["subscribe"])
def subscribe_user(message: telebot.types.Message):
    """Subscribe a user and start sending Athkar at their chosen interval."""
    chat_id = message.chat.id
    if chat_id not in user_timers:
        bot.reply_to(message, "✅ تم تسجيلك لاستقبال الأذكار كل 30 دقيقة (افتراضيًا).")

        # Default interval 30 minutes (1800 seconds)
        user_intervals[chat_id] = 1800
        user_timers[chat_id] = threading.Timer(1, send_athkar_to_user, [chat_id])  # Send first Athkar in 1 second
        user_timers[chat_id].start()
    else:
        bot.reply_to(message, "📌 أنت مشترك بالفعل!")

@bot.message_handler(commands=["unsubscribe"])
def unsubscribe_user(message: telebot.types.Message):
    """Unsubscribe a user and stop their Athkar timer."""
    chat_id = message.chat.id
    if chat_id in user_timers:
        user_timers[chat_id].cancel()  # Stop the timer
        del user_timers[chat_id]  # Remove from tracking
        del user_intervals[chat_id]  # Remove interval setting
        bot.reply_to(message, "❌ تم إلغاء اشتراكك ولن تستقبل الأذكار بعد الآن.")
    else:
        bot.reply_to(message, "⚠️ أنت غير مشترك حاليًا.")

@bot.message_handler(commands=["settime"])
def set_user_interval(message: telebot.types.Message):
    """Allow a user to change their Athkar interval (in minutes)."""
    chat_id = message.chat.id
    args = message.text.split()
    
    if len(args) < 2 or not args[1].isdigit():
        bot.reply_to(message, "⚠️ يرجى إدخال عدد الدقائق بشكل صحيح، مثال: **/settime 15**")
        return

    minutes = int(args[1])
    if minutes < 1:
        bot.reply_to(message, "⚠️ الحد الأدنى هو دقيقة واحدة!")
        return

    interval_seconds = minutes * 60  # Convert minutes to seconds
    user_intervals[chat_id] = interval_seconds

    # Restart user's timer with new interval
    if chat_id in user_timers:
        user_timers[chat_id].cancel()
    
    user_timers[chat_id] = threading.Timer(interval_seconds, send_athkar_to_user, [chat_id])
    user_timers[chat_id].start()

    bot.reply_to(message, f"✅ تم ضبط التوقيت! ستتلقى الأذكار كل **{minutes} دقيقة**.")

# Start the bot
print("* Bot is running...")
bot.polling(none_stop=True)
