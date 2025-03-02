# Telegram Bot Documentation: Daily Quran Werd and Athkar Bot

## **Overview**

This bot provides daily **Quran Werd reminders** and **random Athkar** to users. Users can set a Quran completion goal and receive scheduled Werds. If a user misses a day, the bot continues sending the same Werd until they mark it as done.

---

## **Features & Behavior**

### **1. Sends the Next Werd at the Start of a New Day**

- When a user completes their Werd (`/donewerd`), the bot **stops** reminders for that day.
- The bot **automatically starts sending the next Werd at midnight (00:00:01).**
- If the bot restarts or the system time changes, it **still calculates the correct Werd**.

### **2. If the User Misses a Day, It Keeps the Same Werd**

- If the user \*\*forgets to send \*\*\`\`, the bot **keeps sending the same Werd** the next day.
- Once the user marks `/donewerd`, the bot **advances to the next day’s Werd automatically.**

### **3. Calculates the Correct Werd Based on Time**

- The bot tracks the start date of the Werd schedule.
- It calculates the current day’s Werd dynamically using:
  ```python
  elapsed_days = (datetime.datetime.now() - start_date).days
  today_index = elapsed_days % days
  ```
- Even if the bot is restarted, the Werd remains **accurate and updated**.

### \*\*4. Stops Reminders After \*\*\`\`

- When a user sends `/donewerd`, the bot **stops sending reminders**.
- The next reminder is **scheduled to start at midnight (00:00:01).**
- Implementation:
  ```python
  next_reminder_time = datetime.datetime.now().replace(hour=0, minute=0, second=1) + datetime.timedelta(days=1)
  delay = (next_reminder_time - datetime.datetime.now()).total_seconds()
  ```

### **5. Supports Hourly Reminders Until Done**

- The bot sends hourly reminders \*\*until the user marks \*\*\`\`.
- This ensures the user does not forget to read their Werd.
- Implementation:
  ```python
  if not user_werd_settings[chat_id]["finished_today"]:
      send_werd_reminder(chat_id)
  ```
- After marking `/donewerd`, reminders **pause until midnight**.

---

## **Command List & Usage**

### **Quran Werd Commands**

| Command                 | Description                                                                    |
| ----------------------- | ------------------------------------------------------------------------------ |
| `/setwerd <عدد الأيام>` | Set the number of days to finish the Quran. The bot divides Werds accordingly. |
| `/werd`                 | Get today’s Werd. Updates automatically based on time.                         |
| `/donewerd`             | Mark today’s Werd as completed. Stops reminders for today.                     |

### **Athkar Commands**

| Command              | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| `/subscribe`         | Subscribe to receive random Athkar every 30 minutes (default). |
| `/unsubscribe`       | Stop receiving random Athkar.                                  |
| `/settime <minutes>` | Change the Athkar interval.                                    |
| `/resetlist`         | Reset the Athkar list to default.                              |
| `/addthikr <text>`   | Add a new Thikr to the list.                                   |
| `/listthikr`         | Show all stored Athkar.                                        |
| `/delthikr <number>` | Delete a specific Thikr by number.                             |

### **General Commands**

| Command  | Description                               |
| -------- | ----------------------------------------- |
| `/start` | Show a welcome message with instructions. |

---

## **Expected Behavior Summary**

| User Action                    | Bot Behavior                                                         |
| ------------------------------ | -------------------------------------------------------------------- |
| `/setwerd 10`                  | Generates a 10-day Quran Werd schedule.                              |
| `/werd`                        | Sends today’s Werd.                                                  |
| *User does nothing for 2 days* | Bot keeps sending the same Werd until `/donewerd` is used.           |
| `/donewerd` on Day 3           | Bot stops today’s reminders and schedules the next Werd at midnight. |
| Next Day (`00:00`)             | Bot automatically sends the next day’s Werd.                         |

---

## **Conclusion**

✅ **Next Werd sends at midnight** after `/donewerd`.\
✅ **Missed days = same Werd keeps sending**.\
✅ **Hourly reminders keep running until done**.\
✅ **Automatically calculates correct Werd based on time**.\
✅ **Reminders properly reset for the next day**.

This bot is fully automated and ensures users stay consistent with their Quran Werd schedule while receiving motivational Athkar. 🚀

