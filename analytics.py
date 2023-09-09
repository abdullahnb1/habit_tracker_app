from __future__ import annotations
from datetime import datetime, timedelta
from typing import List
from collections import defaultdict


class Analytics:
    @staticmethod
    def active_habits(habits: List['Habit']) -> List['Habit']:
        return [habit for habit in habits if habit.active]

    @staticmethod
    def habits_in_period(habits: List['Habit'], from_date: datetime, to_date: datetime) -> List['Habit']:
        return [habit for habit in habits if from_date <= habit.start_date <= to_date]

    @staticmethod
    def top_streak_habit(habits: List['Habit']) -> str:
        # Return the habit_id of the habit with the highest streak
        max_streak = max(habits, key=lambda habit: habit.longest_streak)
        return max_streak.habit_id if max_streak else None

    @staticmethod
    def highest_success_rate(habits: List['Habit']) -> str:
        # Define success rate as ratio of successes to total progress entries, return habit_id with highest rate
        def success_rate(habit):
            return habit.successes / len(habit.progress_entries) if habit.progress_entries else 0

        success_rate_habit = max(habits, key=success_rate)
        return success_rate_habit.habit_id if success_rate_habit else None


    @staticmethod
    def highest_failure_rate(habits: List[Habit]) -> str:
        # Define failure as number of days since creation that are not covered by progress entries
        def failure_rate(habit):
            days_since_creation = (datetime.now() - habit.start_date).days
            days_with_progress = len(habit.progress_entries)
            return (days_since_creation - days_with_progress) / days_since_creation if days_since_creation else 0

        failure_rate_habit = max(habits, key=failure_rate)
        return failure_rate_habit.habit_id

    @staticmethod
    def overall_successes(habits: List['Habit']) -> int:
        # Return the total number of successes across all habits
        return sum(habit.successes for habit in habits)

    @staticmethod
    def overall_failures(habits: List['Habit']) -> int:
        return sum((datetime.now() - habit.start_date).days - len(habit.progress_entries) for habit in habits)

    @staticmethod
    def top_category_performance(habits: List[Habit]) -> str:
        # Assume performance is measured by success rate
        category_success_rates = defaultdict(list)
        for habit in habits:
            category_success_rates[habit.category].append(habit.successes / len(habit.progress_entries) if habit.progress_entries else 0)

        top_category = max(category_success_rates, key=lambda category: sum(category_success_rates[category]) / len(category_success_rates[category]))
        return top_category
    
    @staticmethod
    def top_interval_performance(habits: List[Habit]) -> str:
        # Assume intervals are daily, weekly, monthly based on the frequency attribute
        interval_success_rates = defaultdict(list)
        for habit in habits:
            interval_success_rates[habit.frequency].append(habit.successes / len(habit.progress_entries) if habit.progress_entries else 0)

        top_interval = max(interval_success_rates, key=lambda interval: sum(interval_success_rates[interval]) / len(interval_success_rates[interval]))
        return top_interval

    @staticmethod
    def average_streak_length(habits: List[Habit]) -> int:
        return sum(habit.longest_streak for habit in habits) // len(habits)

    @staticmethod
    def average_streak_break(habits: List['Habit']) -> int:
        # Assume a streak break is any day without a progress entry since the habit creation
        streak_breaks = []
        for habit in habits:
            streak_breaks.append((datetime.now() - habit.start_date).days - len(habit.progress_entries))
        return sum(streak_breaks) // len(streak_breaks) if streak_breaks else 0

    @staticmethod
    def average_remaining_time(habits: List[Habit]) -> int:
        # Assume the remaining time is the difference between now and the next deadline
        remaining_times = []
        for habit in habits:
            if habit.next_deadline:
                remaining_times.append((habit.next_deadline - datetime.now()).days)
        return sum(remaining_times) // len(remaining_times) if remaining_times else 0