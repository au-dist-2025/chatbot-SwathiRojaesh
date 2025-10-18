🎓 Student Attendance Tracker Chatbot

This is a rule-based, command-line chatbot built in Python to help students track their class attendance. The chatbot provides a simple, conversational interface to mark attendance, view historical records, and check attendance percentages against a defined eligibility criterion.

The primary goal of this project is to create a user-friendly tool that helps students stay organized and aware of their academic standing.

✨ Features

Interactive Conversation: A friendly, rule-based dialogue system to guide the user.

Dynamic Subject Management: Add, remove, or modify subjects by simply editing the knowledge_base.json file, no code changes needed.

Daily Attendance Tracking: Mark attendance as 'present' or 'absent' for any subject.

Data Persistence: The chatbot saves the user's name and all attendance records to attendance_data.json, so progress is never lost between sessions.

Personalization: Remembers the user's name to create a more engaging experience.

Detailed Analytics:

Calculate percentage for a single subject.

Display a summary of attendance for all subjects.

View a complete, date-wise log of attendance.

Automatically find the subject with the lowest attendance.

Eligibility Calculation: Instantly checks if a student meets the required attendance percentage (e.g., 75%) for a subject.

Helpful Guidance: Includes a help command and provides clear action menus to the user.

🚀 How to Run the Chatbot

To run the chatbot, you must have Python 3 installed on your system.

Clone the repository or download the files into a single folder. Make sure the following files are in the same directory:

attendace_bot.py

knowledge_base.json

Open a terminal or command prompt in that folder.

Run the following command:

python attendace_bot.py


The chatbot will greet you and you can start the conversation. Type quit or bye to exit at any time.

💬 Sample Conversation (Input and Output)

Here is a sample walkthrough of a typical interaction with the chatbot.

============================================================
         🎓 STUDENT ATTENDANCE TRACKER 🎓
============================================================
🎓 Welcome to Student Attendance Tracker!

I'll help you track your attendance for all subjects.
Let's get started! What's your name?

Type 'quit' or 'bye' to exit.

You: my name is Priya
Bot: Nice to meet you, Priya! 😊

📚 Available Subjects:

1. ☁️ Cloud Computing
2. 📊 Big Data
3. 🔐 Cryptography
4. 🤖 Artificial Intelligence
5. ⛓️ Blockchain
6. 🧠 Machine Learning

💡 Say the subject name or number to select it!

You: 1
Bot: ☁️ Cloud Computing selected!

What would you like to do?
• Say 'present' to mark attendance
• Say 'absent' if you missed class
• Say 'percentage' to check attendance
• Say 'record' to view its history
• Say 'change' or 'menu' to select another subject

You: present
Bot: ✓ Marked PRESENT for Cloud Computing on 2025-10-18

✨ What's next?
• Mark another subject (say subject name)
• Check 'percentage'
• View 'record' (all subjects)
• View 'all subjects' summary
• Say 'menu' to see subjects again

You: big data
Bot: 📊 Big Data selected!
...

You: absent
Bot: ✗ Marked ABSENT for Big Data on 2025-10-18
...

You: all subjects summary
Bot: 📚 Overall Attendance Summary:

✓ Cloud Computing: 100.00% (1/1)
⚠️ Big Data: 0.00% (0/1)

📈 Overall Average: 50.00%

✨ What's next?
...

You: bye
Bot: Goodbye, Priya! Keep attending classes! 📚

Attendance data saved! Thank you for using the tracker! 🎓


📁 File Structure

attendace_bot.py: The main Python script containing the chatbot's logic, including intent recognition, state management, and response generation.

knowledge_base.json: A JSON file that stores all the "knowledge" for the bot, such as subject names, icons, and response templates. This makes the bot easy to configure and extend.

attendance_data.json: This file is automatically created by the bot to save the user's name and attendance records. This allows the bot to remember data between sessions.