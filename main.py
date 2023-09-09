from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from users_screen import UsersScreen

class TrackerApp(App):
    def build(self):
        self.title = 'Habit Tracker'

        manager = ScreenManager()
        manager.add_widget(UsersScreen(name='Choose an account'))
        
        return manager

if __name__ == '__main__':
    TrackerApp().run()