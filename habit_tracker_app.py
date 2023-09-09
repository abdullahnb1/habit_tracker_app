import tkinter
from tkinter import ttk
import customtkinter
from tkinter.messagebox import showinfo
import habit, user, analytics
import json
from datetime import datetime, timedelta


DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.lists = list() 
        self.id = 0
        self.selected_value = []
        self.datas = []
        self.infos = []
        self.title("Change Frames")
        # remove title bar , page reducer and closing page !!!most have a quit button with app.destroy!!! (this app have a quit button so don't worry about that)
        self.overrideredirect(True)
         
        self.geometry("1000x600")
        # make the app as big as the screen (no mater wich screen you use)
        # "{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight())

        self.main_container = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # left side panel -> for frame selection
        self.left_side_panel = customtkinter.CTkFrame(self.main_container, width=100, corner_radius=10)
        self.left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
    
        self.left_side_panel.grid_columnconfigure(0, weight=1)
        self.left_side_panel.grid_rowconfigure((0, 1, 2, 3,4), weight=0)
        self.left_side_panel.grid_rowconfigure((5), weight=1)
    
    
        # self.left_side_panel WIDGET
        self.logo_label = customtkinter.CTkLabel(self.left_side_panel, text="Welcome! \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
    
        self.scaling_label = customtkinter.CTkLabel(self.left_side_panel, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
    
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.left_side_panel, values=["80%", "90%", "100%", "110%", "120%"],
                                                           command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky = "s")
    
        self.bt_Quit = customtkinter.CTkButton(self.left_side_panel, text="Quit", fg_color= '#EA0000', hover_color = '#B20000', command= self.close_window)
        self.bt_Quit.grid(row=9, column=0, padx=20, pady=10)

        # button to select correct frame IN self.left_side_panel WIDGET
        self.bt_edit = customtkinter.CTkButton(self.left_side_panel, text="Add Habit", command=self.add_habit_func)
        self.bt_edit.grid(row=1, column=0, padx=20, pady=10)

        self.bt_mark_done = customtkinter.CTkButton(self.left_side_panel, text="Mark Done", command=self.mark_done_func)
        self.bt_mark_done.grid(row=2, column=0, padx=20, pady=10)
        
        self.bt_add_habit = customtkinter.CTkButton(self.left_side_panel, text="Edit", command=self.edit_func)
        self.bt_add_habit.grid(row=3, column=0, padx=20, pady=10)

        self.bt_metrics = customtkinter.CTkButton(self.left_side_panel, text="Metrics", command=self.metrics_func)
        self.bt_metrics.grid(row=4, column=0, padx=20, pady=10)
        
        self.bt_dash = customtkinter.CTkButton(self.left_side_panel, text="Dashboard", command=self.dash_func)
        self.bt_dash.grid(row=5, column=0, padx=20, pady=10)
    

        # right side panel -> have self.right_dashboard inside it
        self.right_side_panel = customtkinter.CTkFrame(self.main_container, corner_radius=10, fg_color="#000811")
        self.right_side_panel.pack(side= "left", fill= tkinter.BOTH, expand=True, padx=5, pady=5)
    
        self.right_dashboard = customtkinter.CTkFrame(self.main_container, corner_radius=10, fg_color="#000811")
        self.right_dashboard.pack(in_=self.right_side_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
    
        
    def dash_func(self):
        global lists
        self.clear_frame()
        
        cols = ["Habit", "Description", "Last Done", "Current Streak", "Progress"]
        treescroll = ttk.Scrollbar(self.right_dashboard,)
        treescroll.pack(side = "right", fill = "y")
        treeview = ttk.Treeview(self.right_dashboard,show = "headings", yscrollcommand=treescroll.set, columns = cols, height = 13)
        treeview.pack(side = "top", fill= "both", expand = True, padx=5, pady = 5)
        treescroll.config(command=treeview.yview)
        
        
        treeview.column("Habit", width = 100)
        treeview.column("Description", width = 200)
        treeview.column("Last Done", width = 100)
        treeview.column("Current Streak", width = 100)
        treeview.column("Progress", width = 100)
        
        
        treeview.heading("Habit", text = "Habit")
        treeview.heading("Description", text= "Description")
        treeview.heading("Last Done", text = "Last Done")
        treeview.heading("Current Streak", text = "Current Streak")
        treeview.heading("Progress", text = "Progress")
        self.loaded_data = self.load_data("habits.json")
        self.lists += self.loaded_data
        count = 1
        for record in self.loaded_data:
            lists = [record["title"], record["description"], record["progress_entries"][-1], record["current_streak"], "{}/{}".format(record["successes"],record["days"])]
            treeview.insert(parent="", index=tkinter.END, iid = count, text = "", values= lists)
            count+=1
        
        

        def item_selected(_):
            for selected_item in treeview.selection():
                item = treeview.item(selected_item)
                self.datas = item['values']
                for i in self.loaded_data:
                    if i["title"] == self.datas[0]:
                        self.selected_value.append(i)
                        print(self.selected_value)
                    else: continue
                
        treeview.bind('<<TreeviewSelect>>', item_selected)
    # Uploading datas from json
    def save_data(self,data, filename):
        with open(filename, 'w') as file:
            json.dump(data, file)

    # Downloading datas from json
    def load_data(self,filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data       
    
    #  self.right_dashboard   ----> edit widget  
    def adding_func(self):
        
        category = "habits"
        significance = self.goal_entry.get()
        habit_id = self.id + 1
        self.id = habit_id    
        frequency = self.combobox.get()
        title = self.habit_name_entry.get()
        description = self.habit_description_entry.get()
        progress_entries = [1]
        end_date = ["Have not been marked down"]
        
        habits = habit.Habit(habit_id,title, description, frequency, category, significance, progress_entries, end_date)
        habits.update_next_deadline()
        if frequency == "daily":
            habits.days = int(significance)
        elif frequency == "weekly":
            habits.days = int(significance) * 7
        elif frequency == "monthly":
            habits.days = int(significance) * 30
        self.lists.append({"habit_id": habits.habit_id, 
                           "title": habits.title,
                           "description": habits.description,
                           "active": habits.active,
                           "start_date": habits.start_date,
                           "end_date": habits.end_date,
                           "frequency": habits.frequency,
                           "successes": habits.successes,
                           "current_streak": habits.current_streak,
                           "longest_streak": habits.longest_streak,
                           "category": habits.category,
                           "notify": habits.notify,
                           "significance": habits.significance,
                           "next_deadline": habits.next_deadline,
                           "progress_entries": habits.progress_entries,
                           "days": habits.days})
        self.save_data(self.lists,"habits.json")
    def adding_func_edit(self):
        
        category = "habits"
        significance = self.goal_entry.get()
        habit_id = self.id + 1
        self.id = habit_id    
        frequency = self.combobox.get()
        title = self.habit_name_entry.get()
        description = self.habit_description_entry.get()
        progress_entries = [1]
        end_date = ["Have not been marked down"]

        habits = habit.Habit(habit_id,title, description, frequency, category, significance, progress_entries,end_date)
        habits.update_next_deadline()
        
        
        if frequency == "daily":
            habits.days = int(significance)
        elif frequency == "weekly":
            habits.days = int(significance)*7
        elif frequency == "monthly":
            habits.days = int(significance)*30
       # self.lists.remove(self.selected_value[0])
        self.lists.append({"habit_id": habits.habit_id, 
                           "title": habits.title,
                           "description": habits.description,
                           "active": habits.active,
                           "start_date": habits.start_date,
                           "end_date": habits.end_date,
                           "frequency": habits.frequency,
                           "successes": habits.successes,
                           "current_streak": habits.current_streak,
                           "longest_streak": habits.longest_streak,
                           "category": habits.category,
                           "notify": habits.notify,
                           "significance": habits.significance,
                           "next_deadline": habits.next_deadline,
                           "progress_entries": habits.progress_entries,
                           "days": habits.days})
                           
        self.save_data(self.lists,"habits.json")
    def delete_func(self):
           
        self.selected_value = []
    def save_changes(self):
        self.delete_func()
        self.adding_func_edit()
    def add_habit_func(self):
    
        self.clear_frame()
        #  self.right_left_side_panel   ----> dashboard inside the right side frame 
        self.right_left_side_panel = customtkinter.CTkFrame(self.right_dashboard, width=80, corner_radius=10)
        self.right_left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
    
        self.right_left_side_panel.grid_columnconfigure(0, weight=1)
        self.right_left_side_panel.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.right_left_side_panel.grid_rowconfigure((4, 5), weight=1)
        
        self.logo_label_edit = customtkinter.CTkLabel(self.right_left_side_panel, text="Add Habit Page! \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_edit.grid(row=1, column=0, padx=20, pady=(20, 10))
    
        
                
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, text="Save", command=self.adding_func)
        self.bt_save.grid(row=2, column=0, padx=20, pady=(100, 0))
        
        
        #  option menü 
        def optionmenu_callback(choice):
            return choice

        self.combobox = customtkinter.CTkOptionMenu(master=self.right_left_side_panel,
                                values=["daily", "weekly", "monthly"],
                                command=optionmenu_callback)
        self.combobox.grid(row = 3, column = 0, padx=20, pady=(10,0))
        self.combobox.set("Select Periodicity")  # set initial value
        
        self.bt_cancel = customtkinter.CTkButton(master=self.right_left_side_panel, text="Cancel", command=self.dash_func)
        self.bt_cancel.grid(row=4, column=0, padx=20, pady=(200, 0))
        
        #  self.right_right_side_panel   ----> main inside the right side frame 
        self.right_right_side_panel = customtkinter.CTkFrame(self.right_dashboard, width=580, corner_radius=10)
        self.right_right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
        
        self.habit_name_label = customtkinter.CTkLabel(self.right_right_side_panel, text="Habit Name \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_name_label.grid()
        self.habit_name_entry = customtkinter.CTkEntry(master = self.right_right_side_panel, corner_radius=10, fg_color="black", width = 555, height = 50)
        self.habit_name_entry.grid(padx = 0, pady = 20)
        
        self.logo_label = customtkinter.CTkLabel(self.right_right_side_panel, text="Habit Description \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid()
        self.habit_description_entry = customtkinter.CTkEntry(master = self.right_right_side_panel, corner_radius=10, fg_color="black", width = 555, height = 50)
        self.habit_description_entry.grid(padx = 0, pady = 20)
        
        self.logo_label_edit = customtkinter.CTkLabel(self.right_right_side_panel, text="Goal \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_edit.grid()
        self.goal_entry = customtkinter.CTkEntry(master = self.right_right_side_panel, corner_radius=10, fg_color="black", width = 555, height = 50)
        self.goal_entry.grid(padx = 0, pady = 20)
        
    #  self.right_dashboard   ----> mark done widget
    def mark_done_func(self):
        for i in self.loaded_data:
            if i["title"] == self.datas[0]:   
                i["successes"] += 1
                i["current_streak"] += 1
                i["progress_entries"].append(datetime.now().strftime("%Y-%m-%d"))
                if self.is_completed_today_app():
                    i["longest_streak"] += 1
                else: i["longest_streak"] = 0
                
                if i["current_streak"] >= i["longest_streak"]:
                    i["longest_streak"] = i["current_streak"]
                self.save_data(self.loaded_data,"habits.json")
              
    def parse_date_time(self, date):
        return datetime.strptime(date, "%Y-%m-%d")
    def is_completed_today_app(self):
        if datetime.now() == self.parse_date_time(self.selected_value[0]["progress_entries"][-1]):
            return True
        else: return False
    #  self.right_dashboard   ----> metrics widget
    def metrics_func(self):
        self.clear_frame()
        self.right_left_side_panel = customtkinter.CTkFrame(self.right_dashboard, width=100, corner_radius=10)
        self.right_left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
    
       
        
        self.logo_label_metric = customtkinter.CTkLabel(self.right_left_side_panel, text="Metrics  \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_metric.grid(row=1, column=0, padx=20, pady=(20, 10))
    
        
        self.bt_back = customtkinter.CTkButton(master=self.right_left_side_panel, text="Back", command=self.dash_func)
        self.bt_back.grid(row=2, column=0, padx=20, pady=(100, 0))
        #  self.right_right_side_panel   ----> main inside the right side frame   
        self.right_right_side_panel = customtkinter.CTkFrame(self.right_dashboard, width=580, corner_radius=10)
        self.right_right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
        
        habit_labels = []
        self.selected_value[0]["end_date"] = self.selected_value[0]["progress_entries"][-1]
        
        
        habit_texts = ["Habit name: {}".format(self.selected_value[0]["title"]), "Created on: {}".format(self.selected_value[0]["start_date"]), "First done on: {}".format(self.selected_value[0]["start_date"]), "Last done on: {}".format(self.selected_value[0]["end_date"]), "Current Streak: {}".format(self.selected_value[0]["current_streak"]), "Goal Compliation progress: {}/{}".format(self.selected_value[0]["successes"],self.selected_value[0]["days"]), "Longest streak: {}".format(self.selected_value[0]["longest_streak"])]
        
        for text_ in habit_texts:
            label = customtkinter.CTkLabel(master=self.right_right_side_panel, width=580, height=50, corner_radius=10, text_color="black",fg_color="grey", text=text_, anchor="w")
            label.grid(padx=0, pady=10)
            habit_labels.append(label)
        self.selected_value = []
    
    def edit_func(self):
        self.clear_frame()
        #  self.right_left_side_panel   ----> dashboard inside the right side frame 
        self.right_left_side_panel = customtkinter.CTkFrame(self.right_dashboard, width=100, corner_radius=10)
        self.right_left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
    
        self.right_left_side_panel.grid_columnconfigure(0, weight=1)
        self.right_left_side_panel.grid_rowconfigure((0, 1, 2, 3), weight=0)
        self.right_left_side_panel.grid_rowconfigure((4, 5), weight=1)
        
        self.logo_label_edit = customtkinter.CTkLabel(self.right_left_side_panel, text="Edit Page! \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label_edit.grid(row=1, column=0, padx=20, pady=(20, 10))
    
        
        self.bt_save = customtkinter.CTkButton(master=self.right_left_side_panel, text="Save Changes", command=self.save_changes)
        self.bt_save.grid(row=2, column=0, padx=20, pady=(100, 0))
        
        
        
        
        #  option menü 
        def optionmenu_callback(choice):
            print("optionmenu dropdown clicked:", choice)

        self.combobox = customtkinter.CTkOptionMenu(master=self.right_left_side_panel,
                                values=["daily", "weekly", "monthly"],
                                command=optionmenu_callback)
        self.combobox.grid(row = 3, column = 0, padx=20, pady=(10,0))
        self.combobox.set("Select Periodicity")  # set initial value
        self.bt_delete = customtkinter.CTkButton(master=self.right_left_side_panel, text="Delete", command=self.delete_func)
        self.bt_delete.grid(row=2, column=0, padx=20, pady=(10, 0))
        
        self.bt_cancel = customtkinter.CTkButton(master=self.right_left_side_panel, text="Cancel", command=self.dash_func)
        self.bt_cancel.grid(row=4, column=0, padx=20, pady=(200, 0))
        
        #  self.right_right_side_panel   ----> main inside the right side frame 
        self.right_right_side_panel = customtkinter.CTkFrame(self.right_dashboard, width=580, corner_radius=10)
        self.right_right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)
        
        self.right_right_top_side_panel = customtkinter.CTkFrame(self.right_right_side_panel,width = 580, corner_radius=10,fg_color="grey")
        self.right_right_top_side_panel.pack(side="top", fill = "x")
        
        self.right_right_bottom_side_panel = customtkinter.CTkFrame(self.right_right_side_panel,width = 580, corner_radius=10,)
        self.right_right_bottom_side_panel.pack(side="top", fill = "both")
        
        self.habit_name_label_info = customtkinter.CTkLabel(self.right_right_top_side_panel, text="Habit Name: {} \n".format(self.selected_value[0]["title"]), font=customtkinter.CTkFont(size=10, weight="bold"),anchor = "sw")
        self.habit_name_label_info.grid()
        self.habit_description_label = customtkinter.CTkLabel(self.right_right_top_side_panel, text="Habit Description: {} \n".format(self.selected_value[0]["description"]), font=customtkinter.CTkFont(size=10, weight="bold"),anchor = "sw")
        self.habit_description_label.grid()
        self.goal_label = customtkinter.CTkLabel(self.right_right_top_side_panel, text="Goal: {} \n".format(self.selected_value[0]["significance"]), font=customtkinter.CTkFont(size=10, weight="bold"),anchor = "sw")
        self.goal_label.grid()
        
        self.habit_name_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel, text="Habit Name \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_name_label_edit.grid()
        self.habit_name_entry = customtkinter.CTkEntry(master = self.right_right_bottom_side_panel, corner_radius=10, fg_color="black", width = 580, height = 50)
        self.habit_name_entry.grid(padx = 0, pady = 20)
        
        self.habit_description_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel, text="Habit Description \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.habit_description_label_edit.grid()
        self.habit_description_entry = customtkinter.CTkEntry(master = self.right_right_bottom_side_panel, corner_radius=10, fg_color="black", width = 580, height = 50)
        self.habit_description_entry.grid(padx = 0, pady = 20)
        
        self.goal_label_edit = customtkinter.CTkLabel(self.right_right_bottom_side_panel, text="Goal \n", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.goal_label_edit.grid()
        self.goal_entry = customtkinter.CTkEntry(master = self.right_right_bottom_side_panel, corner_radius=10, fg_color="black", width = 580, height = 50)
        self.goal_entry.grid(padx = 0, pady = 20)
    # Change scaling of all widget 80% to 120%
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    
    # close the entire window    
    def close_window(self): 
        App.destroy(self)
        
        
    # CLEAR ALL THE WIDGET FROM self.right_dashboard(frame) BEFORE loading the widget of the concerned page       
    def clear_frame(self):
        for widget in self.right_dashboard.winfo_children():
            widget.destroy()


a = App()
a.mainloop()