import telebot
import logging
import threading
import time
import random
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the bot token from .env
BOT_TOKEN = os.getenv("ATHKAR_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

# Athkar from the **Quran, Sahih Al-Bukhari, and Sahih Muslim**
athkar_list = [
    # 📖 أدعية من القرآن الكريم
    " وَمِنْ آيَاتِهِ أَنْ خَلَقَ لَكُم مِّنْ أَنفُسِكُمْ أَزْوَاجًا لِّتَسْكُنُوا إِلَيْهَا وَجَعَلَ بَيْنَكُم مَّوَدَّةً وَرَحْمَةً ﴾ (الروم: 21) ﴿" ,
    " رَبَّنَا هَبْ لَنَا مِنْ أَزْوَاجِنَا وَذُرِّيَّاتِنَا قُرَّةَ أَعْيُنٍ وَاجْعَلْنَا لِلْمُتَّقِينَ إِمَامًا ﴾ (الفرقان: 74) ﴿" ,
    " وَأَنكِحُوا ٱلْأَيَٰمَىٰ مِنكُمْ وَٱلصَّٰلِحِينَ مِنْ عِبَادِكُمْ وَإِمَآئِكُمْ ﴾ (النور: 32) ﴿",
    " نِسَآؤُكُمْ حَرْثٌ لَّكُمْ فَأْتُوا۟ حَرْثَكُمْ أَنَّىٰ شِئْتُمْ ﴾ (البقرة: 223) ﴿",
    " وَلَهُنَّ مِثْلُ ٱلَّذِى عَلَيْهِنَّ بِٱلْمَعْرُوفِ ﴾ (البقرة: 228) ﴿",
    " وَٱلْمُحْصَنَٰتُ مِنَ ٱلْمُؤْمِنَٰتِ وَٱلْمُحْصَنَٰتُ مِنَ ٱلَّذِينَ أُوتُواْ ٱلْكِتَٰبَ ﴾ (المائدة: 5) ﴿",
    " فَإِن طِبْنَ لَكُم عَن شَىْءٍۢ مِّنْهُ نَفْسًۭا فَكُلُوهُ هَنِيٓـًۭٔا مَّرِيٓـًۭٔا ﴾ (النساء: 4) ﴿",
    " وَإِن يَتَفَرَّقَا يُغْنِ ٱللَّهُ كُلًّۢا مِّن سَعَتِهِۦ ﴾ (النساء: 130) ﴿",
    " وَلَا تَنكِحُوا ٱلْمُشْرِكَٰتِ حَتَّىٰ يُؤْمِنَّ ﴾ (البقرة: 221) ﴿",
    " رَبِّ إِنِّي لِمَا أَنْزَلْتَ إِلَيَّ مِنْ خَيْرٍ فَقِيرٌ ﴾ (القصص: 24) ﴿",  

    # 📜 أحاديث نبوية عن الزواج
    # 📌 أدعية عند الزواج والعقد
    "قال رسول الله ﷺ: إذا تزوَّجَ أحدُكُمُ امرأةً فليأخذْ بناصيتِها، وليُسمِّ اللهَ، ولْيَدْعُ بالبرَكةِ. (رواه أبو داود وصححه الألباني)",
    "قال رسول الله ﷺ: بارك الله لك، وبارك عليك، وجمع بينكما في خير. (رواه الترمذي وأبو داود وصححه الألباني)",

    # 📌 دعاء النبي ﷺ ليلة الزواج
    "كان النبي ﷺ إذا تزوج قال: اللهم إني أسألك خيرها وخير ما جبلتها عليه، وأعوذ بك من شرها وشر ما جبلتها عليه. (رواه أبو داود وابن ماجه وصححه الألباني)",

    # 📌 دعاء عند الدخول بالزوجة
    "قال رسول الله ﷺ: إذا تزوّج أحدكم امرأة، أو اشترى خادمًا، فليقل: اللهم إني أسألك خيرها، وخير ما جبلتها عليه، وأعوذ بك من شرها، وشر ما جبلتها عليه. (رواه أبو داود وابن ماجه وصححه الألباني)",

    # 📌 فضل الزوجة الصالحة
    "قال رسول الله ﷺ: الدنيا متاع، وخير متاع الدنيا المرأة الصالحة. (رواه مسلم)",
    "قال رسول الله ﷺ: أربع من السعادة: المرأة الصالحة، والمسكن الواسع، والجار الصالح، والمركب الهنيء. (رواه ابن حبان وصححه الألباني)",

    # 📌 دعاء البركة للمتزوجين
    "قال رسول الله ﷺ: اللهم بارك لهما، وبارك عليهما، واجمع بينهما في خير. (رواه الترمذي وأبو داود وصححه الألباني)",

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

    # 📌 دعاء للبركة في الحياة الزوجية
    "اللهم اجعل بيني وبين زوجي مودة ورحمة كما أمرت، وبارك لنا في حياتنا الزوجية. (رواه البخاري ومسلم بمعناه)",

    # 📌 دعاء لحفظ العلاقة الزوجية من الشيطان
    "قال رسول الله ﷺ: إن الشيطان يجري من ابن آدم مجرى الدم، فاجعلوا بينكم وبينه سترًا بالصلاة والدعاء. (رواه البخاري ومسلم)",

    # 📌 دعاء عند الخلاف بين الزوجين
    "اللهم أصلح بيني وبين زوجي، واهدنا لما تحب وترضى، وبارك لنا في حياتنا الزوجية. (مستنبط من أدعية النبي ﷺ في إصلاح ذات البين)",

    # 📌 دعاء لحفظ الزوج والزوجة من الفتنة
    "اللهم احفظني بحلالك عن حرامك، واغنني بفضلك عمّن سواك. (رواه الترمذي وصححه الألباني)",

    # 📌 دعاء لجلب الحب والمودة بين الزوجين
    "اللهم اجعلني قرة عين لزوجي، واجعله قرة عين لي، وارزقنا الذرية الصالحة. (رواه مسلم بمعناه)",

    # 📌 دعاء لحسن العشرة والمعاشرة الطيبة
    "اللهم ارزقني حسن العشرة، وبارك لي في زوجي، وأصلح بيننا، واجعلنا من عبادك الصالحين. (حديث حسن بمعناه)",

    # 📌 دعاء عند رؤية الزوج أو الزوجة لأول مرة بعد العقد
    "اللهم اجعلها مباركة لي، وبارك لي فيها، وارزقنا التوفيق والذرية الصالحة. (رواه البخاري بمعناه)",

    # 📌 دعاء عند وجود مشاكل زوجية
    "اللهم اهدني لأحسن الأخلاق، واصرف عني سيئها، واهدني إلى الحق، وارزقني الحكمة في التعامل مع زوجي (أو زوجتي). (رواه مسلم بمعناه)",

    # 📌 دعاء عند قدوم المولود بعد الزواج
    "اللهم اجعله مباركًا، وأصلحه، وانبته نباتًا حسنًا، واجعله قرة عين لنا. (رواه البخاري ومسلم بمعناه)",

    # 📌 دعاء لحفظ البيت والأسرة
    "اللهم احفظ بيتي، واجعلنا في رعايتك وحفظك، وبارك لنا في زواجنا وأولادنا. (رواه مسلم بمعناه)",

    # 📌 دعاء عند الحاجة إلى الصبر على الزوج/الزوجة
    "اللهم ارزقني الصبر، وأعني على حسن العشرة، واهدنا لما تحب وترضى. (رواه البخاري ومسلم بمعناه)",

    # 📌 دعاء عند فقدان الزوج أو الزوجة
    "اللهم أجرني في مصيبتي، واخلفني خيرًا منها. (رواه مسلم)",

    # 📌 دعاء عند الطلاق أو الانفصال
    "اللهم إن كان خيرًا لنا فاجمعنا، وإن كان شرًا لنا فاصرفه عنا، ووفقنا لما فيه الخير لنا في ديننا ودنيانا. (مستنبط من أدعية النبي ﷺ في الفتن والشدائد)",   
]


user_timers = {}
user_intervals = {}  # Store custom intervals per user (in seconds)

def send_athkar_to_user(chat_id):
    """Send a random Athkar to the user and restart the timer."""
    if chat_id in user_timers:
        athkar = random.choice(athkar_list)
        try:
            bot.send_message(chat_id, athkar)
        except Exception as e:
            logger.error(f"Failed to send Athkar to {chat_id}: {e}")

        # Restart timer with user's custom interval
        interval = user_intervals.get(chat_id, 1800)  # Default to 30 minutes if not set
        user_timers[chat_id] = threading.Timer(interval, send_athkar_to_user, [chat_id])
        user_timers[chat_id].start()

@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    """Send welcome message with instructions."""
    logger.info(f"- User started: {message.chat.username}")
    welcome_text = (
        "👋 مرحبًا بك في بوت الأذكار!\n\n"
        "📌 للاشتراك في الأذكار، أرسل: **/subscribe**\n"
        "📌 لإلغاء الاشتراك، أرسل: **/unsubscribe**\n"
        "📌 لتغيير التوقيت، أرسل: **/settime <عدد الدقائق>**\n"
        "📌 ستتلقى الأذكار حسب المدة التي تحددها."
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
