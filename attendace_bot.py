import re
import json
from datetime import datetime
import os # CHANGED: Added os module to check for file existence

class StudentAttendanceBot:
    def __init__(self):
        self.student_name = None
        self.current_subject = None
        self.conversation_count = 0
        self.attendance = {} # CHANGED: Initialize as empty, will be populated dynamically
        
        self.load_knowledge_base()
        self.load_data() # CHANGED: Load previous attendance data on startup

    def load_knowledge_base(self):
        """Load subjects and responses from knowledge base JSON file"""
        try:
            # CHANGED: Added encoding='utf-8' to prevent UnicodeDecodeError
            with open('knowledge_base.json', 'r', encoding='utf-8') as f:
                kb = json.load(f)
                self.subjects = {k: v['name'] for k, v in kb['subjects'].items()}
                self.subject_icons = {k: v['icon'] for k, v in kb['subjects'].items()}
                self.responses = kb['responses']
                self.messages = kb['messages']
                self.fallback_list = kb['fallback_responses']
                self.eligibility_criteria = kb['settings']['eligibility_criteria']
                print("✓ Knowledge base loaded from knowledge_base.json")
        except (FileNotFoundError, KeyError) as e:
            print(f"⚠️ Error loading knowledge_base.json: {e}. Using default data.")
            # Fallback to hardcoded data if file not found or has errors
            self.subjects = {
                "cloud_computing": "Cloud Computing", "big_data": "Big Data", "cryptography": "Cryptography",
                "artificial_intelligence": "Artificial Intelligence", "blockchain": "Blockchain", "machine_learning": "Machine Learning"
            }
            self.subject_icons = {
                "cloud_computing": "☁️", "big_data": "📊", "cryptography": "🔐",
                "artificial_intelligence": "🤖", "blockchain": "⛓️", "machine_learning": "🧠"
            }
            self.responses = {}
            self.messages = {}
            self.fallback_list = ["I'm not sure what you mean. Try selecting a subject!", "Hmm, I didn't understand that. Say 'help' for commands."]
            self.eligibility_criteria = 75
        
        # CHANGED: Dynamically create the attendance dictionary from the loaded subjects.
        # This means you only need to update your JSON file to add/remove subjects.
        for subject_key in self.subjects.keys():
            if subject_key not in self.attendance:
                self.attendance[subject_key] = {}

    def load_data(self):
        """Load previously saved attendance data from JSON file"""
        if os.path.exists('attendance_data.json'):
            try:
                with open('attendance_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.student_name = data.get("student_name", None)
                    # Only load attendance data if it exists
                    if data.get("attendance"):
                        self.attendance = data["attendance"]
                    print("✓ Previous attendance data loaded.")
            except (json.JSONDecodeError, Exception) as e:
                print(f"⚠️ Could not load attendance_data.json: {e}. Starting fresh.")

    def save_data(self):
        """Save attendance data to JSON file"""
        try:
            data = {
                "student_name": self.student_name,
                "attendance": self.attendance,
                "last_updated": datetime.now().isoformat()
            }
            with open('attendance_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Could not save data: {e}")

    def greet(self):
        """Generate greeting message"""
        if self.student_name:
             return f"🎓 Welcome back, {self.student_name}!\n\n{self.show_subjects()}"
        return ("🎓 Welcome to Student Attendance Tracker!\n\n"
                "I'll help you track your attendance for all subjects.\n"
                "Let's get started! What's your name?")

    def show_subjects(self):
        """Display available subjects"""
        msg = "📚 Available Subjects:\n\n"
        # CHANGED: This now dynamically lists subjects from the knowledge base
        for i, (key, name) in enumerate(self.subjects.items(), 1):
            icon = self.subject_icons.get(key, "•")
            msg += f"{i}. {icon} {name}\n"
        msg += "\n💡 Say the subject name or number to select it!"
        return msg

    def select_subject(self, user_input):
        """Select a subject based on user input (fully dynamic)"""
        user_input = user_input.lower().strip()
        
        # CHANGED: This logic is now fully data-driven.
        # It checks against numbers, short keys, and full names from the JSON.
        subject_list = list(self.subjects.keys())
        
        # Check for number
        if user_input.isdigit() and 1 <= int(user_input) <= len(subject_list):
            self.current_subject = subject_list[int(user_input) - 1]
            return True
            
        # Check for subject name or key
        for key, name in self.subjects.items():
            if name.lower() in user_input or key.lower().replace("_", " ") in user_input:
                self.current_subject = key
                return True
                
        return False

    def get_subject_response(self):
        """Get response after selecting subject"""
        if not self.current_subject:
             return "Something went wrong. Please try selecting a subject again."
        subject_name = self.subjects.get(self.current_subject, "the selected subject")
        # CHANGED: Uses self.subject_icons directly, no more hardcoded dict.
        icon = self.subject_icons.get(self.current_subject, "📚")
        
        msg = f"{icon} {subject_name} selected!\n\n"
        msg += "What would you like to do?\n"
        msg += "• Say 'present' to mark attendance\n"
        msg += "• Say 'absent' if you missed class\n"
        msg += "• Say 'percentage' to check attendance\n"
        msg += "• Say 'record' to view its history\n"
        msg += "• Say 'change' or 'menu' to select another subject"
        return msg
        
    # --- NO CHANGES NEEDED for the functions below this line ---
    # Your core logic for marking, calculating, and showing attendance is solid!
    # I've kept them as they were.

    def show_action_menu(self):
        """Show menu after an action"""
        msg = "\n✨ What's next?\n"
        msg += "• Mark another subject (say subject name)\n"
        msg += "• Check 'percentage'\n"
        msg += "• View 'record' (all subjects)\n"
        msg += "• View 'all subjects' summary\n"
        msg += "• Say 'menu' to see subjects again"
        return msg

    def mark_attendance(self, status):
        """Mark attendance for current subject"""
        if not self.current_subject:
            return "⚠️ Please select a subject first! Say a subject name or number (1-6)."
        
        today = datetime.now().strftime("%Y-%m-%d")
        self.attendance[self.current_subject][today] = status
        
        subject_name = self.subjects[self.current_subject]
        if status == "present":
            response = f"✓ Marked PRESENT for {subject_name} on {today}"
        else:
            response = f"✗ Marked ABSENT for {subject_name} on {today}"
        
        response += self.show_action_menu()
        return response

    def calculate_percentage(self, subject_key):
        """Calculate attendance percentage for a subject"""
        records = self.attendance.get(subject_key, {})
        if not records:
            return 0, 0, 0
        
        total = len(records)
        present = sum(1 for status in records.values() if status == "present")
        percentage = (present / total * 100) if total > 0 else 0
        
        return present, total, percentage

    def show_subject_percentage(self):
        """Show percentage for current subject"""
        if not self.current_subject:
            return "⚠️ Please select a subject first!"
        
        subject_name = self.subjects[self.current_subject]
        present, total, percentage = self.calculate_percentage(self.current_subject)
        
        if total == 0:
            return f"📊 No attendance records for {subject_name} yet!\n{self.show_action_menu()}"
        
        status = "✓ Eligible" if percentage >= self.eligibility_criteria else "⚠️ Not Eligible"
        
        msg = f"📊 {subject_name} Attendance:\n\n"
        msg += f"• Present: {present} days\n"
        msg += f"• Absent: {total - present} days\n"
        msg += f"• Total Classes: {total} days\n"
        msg += f"• Percentage: {percentage:.2f}%\n"
        msg += f"• Status: {status} (Need {self.eligibility_criteria}%)"
        msg += self.show_action_menu()
        
        return msg

    def show_all_percentages(self):
        """Show attendance for all subjects"""
        msg = "📚 Overall Attendance Summary:\n\n"
        
        total_present = 0
        total_classes = 0
        
        for key, name in self.subjects.items():
            present, total, percentage = self.calculate_percentage(key)
            if total > 0:
                status = "✓" if percentage >= self.eligibility_criteria else "⚠️"
                msg += f"{status} {name}: {percentage:.2f}% ({present}/{total})\n"
                total_present += present
                total_classes += total
        
        if total_classes > 0:
            overall = (total_present / total_classes * 100)
            msg += f"\n📈 Overall Average: {overall:.2f}%"
        else:
            msg += "\nNo attendance records yet!"
        
        msg += self.show_action_menu()
        return msg

    def show_complete_record(self):
        """Show attendance record for ALL subjects with dates"""
        msg = "📋 COMPLETE ATTENDANCE RECORD\n"
        msg += "=" * 50 + "\n\n"
        
        has_records = False
        
        for key, name in self.subjects.items():
            records = self.attendance[key]
            if records:
                has_records = True
                present, total, percentage = self.calculate_percentage(key)
                
                msg += f"📚 {name}:\n"
                msg += f"   Percentage: {percentage:.2f}% ({present}/{total})\n"
                msg += "   Date-wise Record:\n"
                
                for date, status in sorted(records.items()):
                    icon = "✓" if status == "present" else "✗"
                    msg += f"   {icon} {date}: {status.upper()}\n"
                msg += "\n"
        
        if not has_records:
            msg += "No attendance records yet!"
        
        msg += self.show_action_menu()
        return msg

    def show_lowest_attendance(self):
        """Find subject with lowest attendance"""
        lowest_percentage = 101 # Start high to ensure first subject is picked
        lowest_subject_info = None
        
        has_any_record = False
        for key, name in self.subjects.items():
            present, total, percentage = self.calculate_percentage(key)
            if total > 0:
                has_any_record = True
                if percentage < lowest_percentage:
                    lowest_percentage = percentage
                    lowest_subject_info = {'name': name, 'key': key, 'present': present, 'total': total}

        if not has_any_record:
             return "No attendance records to compare!" + self.show_action_menu()

        if lowest_subject_info:
            name = lowest_subject_info['name']
            percentage = lowest_percentage
            present = lowest_subject_info['present']
            total = lowest_subject_info['total']
            
            classes_needed = 0
            if percentage < self.eligibility_criteria:
                # Formula to find number of consecutive classes needed to reach the criteria
                needed = (self.eligibility_criteria / 100.0 * total - present) / (1 - self.eligibility_criteria / 100.0)
                if needed > 0:
                    classes_needed = int(needed) + 1 # Round up

            msg = f"⚠️ {name} has the lowest attendance: {percentage:.2f}%"
            if classes_needed > 0:
                msg += f"\nYou need to attend the next {classes_needed} classes consecutively to reach {self.eligibility_criteria}%!"
            msg += self.show_action_menu()
            return msg
        
        return "Not enough data to determine lowest attendance." + self.show_action_menu()
        
    def remember_name(self, user_input):
        """Extract and remember student's name"""
        # Added a simple check to avoid asking for name again if already known
        if self.student_name:
            return None

        patterns = [r"my name is (\w+)", r"i am (\w+)", r"i'm (\w+)", r"name is (\w+)"]
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                self.student_name = match.group(1).capitalize()
                return (f"Nice to meet you, {self.student_name}! 😊\n\n"
                        f"{self.show_subjects()}")
        return None

    def process_input(self, user_input):
        """Process user input and generate response"""
        user_input = user_input.strip().lower()
        self.conversation_count += 1

        # This logic remains largely the same as it's the "brain" of your bot.
        # The key change is that `select_subject` is now smarter.
        
        # Rule: Goodbye (handle first to exit cleanly)
        if re.search(r'\b(bye|goodbye|exit|quit)\b', user_input):
            name_part = f", {self.student_name}" if self.student_name else ""
            return f"Goodbye{name_part}! Keep attending classes! 📚"
        
        # Rule: Remember name
        if not self.student_name:
            name_response = self.remember_name(user_input)
            if name_response:
                return name_response

        # Rule: Change subject / Show menu
        if re.search(r'\b(change|switch|different|another|subject|subjects|list|show|menu|options)\b', user_input):
            self.current_subject = None
            return self.show_subjects()
        
        # Rule: Select subject (This must be checked before actions like 'present')
        if self.select_subject(user_input):
            return self.get_subject_response()
            
        # Action Rules (if a subject is already selected or command is generic)
        if re.search(r'\b(present|attended|attend|came|here)\b', user_input):
            return self.mark_attendance("present")
        
        if re.search(r'\b(absent|missed|skip|bunked|not attended)\b', user_input):
            return self.mark_attendance("absent")

        if re.search(r'\b(percentage|percent|%|check|status)\b', user_input) and not re.search(r'\b(all|overall|total)\b', user_input):
            return self.show_subject_percentage()

        if re.search(r'\b(all|overall|total|summary)\b', user_input) and re.search(r'\b(subject|percentage|attendance)\b', user_input):
            return self.show_all_percentages()
            
        if re.search(r'\b(record|history|view|log|complete)\b', user_input):
            return self.show_complete_record()
        
        if re.search(r'\b(lowest|worst|bad|weak|minimum)\b', user_input):
            return self.show_lowest_attendance()
            
        if re.search(r'\b(help|what can|commands)\b', user_input):
            return self.messages.get('help', "I can help you track attendance.")

        if re.search(r'\b(thank|thanks)\b', user_input):
            name_part = f", {self.student_name}" if self.student_name else ""
            return f"You're welcome{name_part}! Keep up the good attendance! 🎓{self.show_action_menu()}"
            
        # Fallback
        return self.fallback_list[self.conversation_count % len(self.fallback_list)]

    def run(self):
        """Main conversation loop"""
        print("=" * 60)
        print("         🎓 STUDENT ATTENDANCE TRACKER 🎓")
        print("=" * 60)
        print(self.greet())
        print("\nType 'quit' or 'bye' to exit.\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            response = self.process_input(user_input)
            print(f"Bot: {response}\n")
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                break
        
        self.save_data()
        print("Attendance data saved! Thank you for using the tracker! 🎓")

if __name__ == "__main__":
    bot = StudentAttendanceBot()
    bot.run()
