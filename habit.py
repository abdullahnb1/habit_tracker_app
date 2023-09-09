from datetime import datetime, timedelta

class Habit:
    def __init__(self, habit_id: str, title: str, description: str, frequency: str, category: str, significance: int, progress_entries: list, end_date: list):
        self.habit_id = habit_id
        self.title = title
        self.description = description
        self.active = True
        self.start_date = datetime.now().strftime("%Y-%m-%d")
        self.end_date = end_date
        self.frequency = frequency
        self.successes = 0
        self.current_streak = 0
        self.longest_streak = 0
        self.category = category
        self.notify = False
        self.significance = significance
        self.next_deadline = None
        self.progress_entries = progress_entries
        self.days = 0
    def complete_habit(self):
        self.active = False
        self.end_date = datetime.now()

    def add_progress_entry(self, entry_id: str, target_timestamp: datetime, comment: str, satisfaction_level: int):
        progress_entry = ProgressEntry(entry_id, target_timestamp, comment, satisfaction_level)
        self.progress_entries.append(progress_entry)

    def reset_current_streak(self):
        self.current_streak = 0

    def update_longest_streak(self):
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

    def is_completed_today(self) -> bool:
        # Check if the habit is completed today by checking if the latest progress entry was made today
        if not self.progress_entries:
            return False
        latest_entry = self.progress_entries[-1]
        return latest_entry["comment"] and latest_entry["satisfaction_level"] >= 0 and datetime.now().date() == latest_entry.get('timestamp', datetime.now()).date()

    def days_remaining(self) -> int:
        # Calculate the remaining days by subtracting the current date from the next deadline date
        if not self.next_deadline:
            return None
        return (self.next_deadline - datetime.now()).days

    def toggle_notification(self):
        self.notify = not self.notify

    def update_next_deadline(self):
        # Update the next deadline based on frequency
        if self.frequency == 'daily':
            self.next_deadline = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif self.frequency == 'weekly':
            self.next_deadline = (datetime.now() + timedelta(weeks=7)).strftime("%Y-%m-%d")
        elif self.frequency == 'monthly':
            self.next_deadline = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        else:
            raise ValueError(f"Unknown frequency: {self.frequency}")

    def update_success_status(self):
        # Update the success status by checking if the habit is completed today
        if self.is_completed_today():
            self.successes += 1
            self.current_streak += 1
        else:
            self.reset_current_streak()
        self.update_longest_streak()

class ProgressEntry:
    def __init__(self, entry_id: str, target_timestamp: datetime, comment: str, satisfaction_level: int):
        self.entry_id = entry_id
        self.entry_timestamp = datetime.now()
        self.target_timestamp = target_timestamp
        self.completed = False
        self.comment = comment
        self.satisfaction_level = satisfaction_level

    def show_entry_details(self):
        print(f"Entry ID: {self.entry_id}")
        print(f"Entry Timestamp: {self.entry_timestamp}")
        print(f"Target Timestamp: {self.target_timestamp}")
        print(f"Completion Status: {self.completed}")
        print(f"Comment: {self.comment}")
        print(f"Satisfaction Level: {self.satisfaction_level}")
