import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
import calendar
import json
import datetime
# set first day of week to Monday
calendar.setfirstweekday(calendar.MONDAY)

# load reminders from file
try:
    with open("reminders.json") as f:
        reminders = json.load(f)
except FileNotFoundError:
    reminders = {}
    with open("reminders.json", "w") as f:
        json.dump(reminders, f)

def add_reminder(day):
    month_name = calendar.month_name[month]
    reminder_file = f"{month_name.lower()}_reminders.json"

    # load existing reminders
    try:
        with open(reminder_file, "r") as f:
            reminders = json.load(f)
    except FileNotFoundError:
        reminders = {}

    # check if there is a reminder for this day
    day_str = f"{month}-{day}"
    if day_str in reminders:
        reminder = reminders[day_str]
        reminder_window = tk.Toplevel(root)
        reminder_window.title("Reminder")
        reminder_window.geometry("300x200")
        reminder_label = tk.Label(reminder_window, text=reminder, font="Helvetica 14 bold")
        reminder_label.pack(pady=20)
        edit_button = tk.Button(reminder_window, text="Edit Reminder", font="Helvetica 12", command=lambda: edit_reminder(day, reminder_window))
        edit_button.pack(pady=10)
        delete_button = tk.Button(reminder_window, text="Delete Reminder", font="Helvetica 12", command=lambda: delete_reminder(day, reminder_window))
        delete_button.pack(pady=10)
    else:
        reminder_text = simpledialog.askstring("Add Reminder", f"Enter a reminder for {month_name} {day}:")
        if reminder_text:
            reminders[day_str] = reminder_text
            with open(reminder_file, "w") as f:
                json.dump(reminders, f)
    draw_calendar()
def delete_reminder(day, reminder_window):
    month_name = calendar.month_name[month]
    reminder_file = f"{month_name.lower()}_reminders.json"

    # load existing reminders
    with open(reminder_file, "r") as f:
        reminders = json.load(f)

    # check if there is a reminder for this day
    day_str = f"{month}-{day}"
    if day_str in reminders:
        del reminders[day_str]
        with open(reminder_file, "w") as f:
            json.dump(reminders, f)
        reminder_window.destroy()
        draw_calendar()

def edit_reminder(day, reminder_window):
    month_name = calendar.month_name[month]
    reminder_file = f"{month_name.lower()}_reminders.json"
    
    # load existing reminders
    with open(reminder_file, "r") as f:
        reminders = json.load(f)
    
    # check if there is a reminder for this day
    day_str = f"{month}-{day}"
    if day_str in reminders:
        reminder_text = simpledialog.askstring("Edit Reminder", f"Enter a new reminder for {month_name} {day}:", initialvalue=reminders[day_str])
        if reminder_text is not None:
            reminders[day_str] = reminder_text
            with open(reminder_file, "w") as f:
                json.dump(reminders, f)
    else:
        messagebox.showerror("Error", "No reminder exists for this day")
def prev_month():
    global cal, month, year, calendar_frame
    calendar_frame.destroy()
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    cal = calendar.monthcalendar(year, month)
    calendar_frame = tk.Frame(root)
    calendar_frame.pack()
    draw_calendar()

def next_month():
    global cal, month, year, calendar_frame
    calendar_frame.destroy()
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    cal = calendar.monthcalendar(year, month)
    calendar_frame = tk.Frame(root)
    calendar_frame.pack()
    draw_calendar()

def draw_calendar():
    global cal, calendar_frame, month_label
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    # create calendar header
    header_frame = tk.Frame(calendar_frame)
    header_frame.grid(row=0, column=0, columnspan=7)
    
    # create "Last Month" button
    prev_button = tk.Button(header_frame, text="Last Month", command=prev_month)
    prev_button.grid(row=0, column=0)

    # create month label
    month_name = calendar.month_name[month]
    month_label = tk.Label(header_frame, text=month_name, font="Helvetica 16 bold")
    month_label.grid(row=0, column=1, columnspan=5)

    # create "Next Month" button
    next_button = tk.Button(header_frame, text="Next Month", command=next_month)
    next_button.grid(row=0, column=6)
    
    # check if calendar_frame exists
    if calendar_frame:
        # create weekday labels
        for i, day in enumerate(days):
            label = tk.Label(calendar_frame, text=day, font="Helvetica 12 bold")
            label.grid(row=1, column=i)

        # create day buttons
        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day != 0:
                    day_button = tk.Button(calendar_frame, text=str(day), font="Helvetica 12", width=3, height=1)

                    # check if there is a reminder for this day
                    month_name = calendar.month_name[month]
                    day_str = f"{month}-{day}"
                    reminder_file = f"{month_name.lower()}_reminders.json"
                    try:
                        with open(reminder_file, "r") as f:
                            reminders = json.load(f)
                            if day_str in reminders:
                                day_button.config(bg='red')
                    except FileNotFoundError:
                        pass

                    day_button.grid(row=r+2, column=c)
                    day_button.config(command=lambda day=day: add_reminder(day))
    else:
        messagebox.showerror("Error", "Calendar frame does not exist")
# create GUI
root = tk.Tk()
root.title("Calendar")
print(calendar.month_name)

# get current date
now = datetime.datetime.now()

# set initial month and year
month = now.month
year = now.year
cal = calendar.monthcalendar(year, month)

# create calendar frame
calendar_frame = tk.Frame(root)
calendar_frame.pack()

# draw calendar
draw_calendar()

# create last month button
last_month_button = tk.Button(root, text="<<", font="Helvetica 12", command=prev_month)
last_month_button.pack(side="left")

# create next month button
next_month_button = tk.Button(root, text=">>", font="Helvetica 12", command=next_month)
next_month_button.pack(side="right")

root.mainloop()