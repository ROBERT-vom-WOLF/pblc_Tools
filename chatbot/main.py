from time import sleep
from random import randint, choice
import tkinter as tk
from tkinter import filedialog
import threading as trd
from src.logger import get_logger
import pyautogui


def send_message(text, chat_x, chat_y, click=True):
    perv_x, prev_y = 0, 0
    if click:
        perv_x, prev_y = pyautogui.position()
        pyautogui.click(x=chat_x, y=chat_y)
    pyautogui.write(text)
    pyautogui.press("enter")
    if click:
        pyautogui.moveTo(perv_x, prev_y)


def get_templates(*files):
    messages = []
    for file_path in files:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return [line.strip() for line in lines]
    return messages


class ChatBot:

    # noinspection PyUnresolvedReferences
    def __init__(self):

        self.log = get_logger("__chat_bot__", "src/log_files/chat_bot_log.log")

        # variables preset to None or the given default
        self.bot_thread = None
        self.cursor_coordinate_x = None
        self.cursor_coordinate_y = None
        self.picked_path = None
        self.messages_list = None
        self.bot_alive = False

        self.min_delay = 1
        self.max_delay = 8

        # setup of the window
        self.root = tk.Tk()
        self.root.geometry("450x700")
        self.root.title("Chat Bot")
        self.root.bind('<Escape>', self.close_window)    # keybind "esc" closes window
        self.root.attributes('-topmost', True)           # sets window always as a top window in foreground

        self.click_every_entry = tk.BooleanVar()         # saves my checkbutton status in a boolean

        # init of every label on the window "root"
        self.lb_selected_template = tk.Label(self.root, text="<no template selected>", justify="left")
        self.lb_selected_cursor_coordinates = tk.Label(self.root, text="<no position selected>", justify="left")
        self.lb_messages_preview = tk.Label(self.root, text="<no messages>", justify="left")
        self.lb_system_debug = tk.Label(self.root, text="", justify="left")
        self.lb_delay = tk.Label(self.root, text=f"min = {self.min_delay} sec. | max = {self.max_delay} sec.", justify="left")  # nopep8

        # init of the buttons and their functions
        btn_msg_file = tk.Button(self.root, text="File ...", command=self.open_file_explorer)
        btn_start = tk.Button(self.root, text="START", command=self.start_bot)
        btn_stop = tk.Button(self.root, text="STOP", command=self.kill_bot)
        btn_reset = tk.Button(self.root, text="RESET", command=self.reset_input)
        btn_exit = tk.Button(self.root, text=" EXIT  ", command=self.close_window, )
        btn_add_cords = tk.Button(self.root, text="+", command=self.entry_coordinates)
        btn_add_max_delay = tk.Button(self.root, text="+", command=self.entry_delay)

        # init checkbox (var=<variable to save checkbutton status>)
        self.ch_box = tk.Checkbutton(self.root, text="repeat Click", var=self.click_every_entry)

        # init of text entries
        self.txt_cursor_coordinates = tk.Entry(self.root)
        self.txt_delay = tk.Entry(self.root)

        # init canvas (red/green big circle)
        self.cv_status = tk.Canvas(self.root, width=65, height=65)

        # positioning of the upper part of the interface
        self.lb_system_debug.place(x=20, y=0)
        btn_start.place(x=20, y=40)
        btn_stop.place(x=80, y=40)
        self.cv_status.place(x=150, y=20)
        btn_reset.place(x=405, y=40)
        btn_exit.place(x=405, y=70)

        # positioning of the first middle part of the interface
        self.ch_box.place(x=15, y=90)
        self.txt_cursor_coordinates.place(x=20, y=120)
        self.lb_selected_cursor_coordinates.place(x=20, y=145)
        btn_add_cords.place(x=145, y=117)

        # positioning of the second middle part of the interface
        self.txt_delay.place(x=20, y=180)
        self.lb_delay.place(x=20, y=200)
        btn_add_max_delay.place(x=145, y=177)

        # positioning of the low part of the interface
        btn_msg_file.place(x=20, y=250)
        self.lb_selected_template.place(x=20, y=275)

        # positioning of the message preview on the interface
        self.lb_messages_preview.place(x=20, y=300)

        self.update_status()

        self.config = {
            "x": self.cursor_coordinate_x,
            "y": self.cursor_coordinate_y,
            "delay_min": self.min_delay,
            "delay_max": self.max_delay,
            "template_file": self.picked_path,
        }

    def update_status(self):
        circle = self.cv_status.create_oval(16.25, 16.25, 48.75, 48.75, fill="red")
        if self.bot_alive:
            self.cv_status.itemconfig(circle, fill="green")
        else:
            self.cv_status.itemconfig(circle, fill="red")

    def update_config(self):
        self.config = {
            "x": self.cursor_coordinate_x,
            "y": self.cursor_coordinate_y,
            "delay_min": self.min_delay,
            "delay_max": self.max_delay,
            "template_file": self.picked_path,
        }

    def close_window(self, _=None):
        self.kill_bot()
        self.root.destroy()

    def print(self, text, log=True):
        self.lb_system_debug.config(text=text)
        if log:
            self.log.debug(text)

    def reset_input(self):
        self.kill_bot()
        self.bot_thread = None
        self.cursor_coordinate_x = None
        self.cursor_coordinate_y = None
        self.picked_path = None
        self.messages_list = None
        self.bot_alive = False

        self.min_delay = 1
        self.max_delay = 8

        self.txt_cursor_coordinates.delete(0, self.txt_cursor_coordinates.get().count(""))
        self.txt_delay.delete(0, self.txt_delay.get().count(""))

        self.set_labels_none()
        self.update_status()
        self.print("", False)
        self.root.geometry("450x700")

    def entry_delay(self):
        entry = str(self.txt_delay.get())
        if not entry:
            self.print("no entry", False)
            return
        entry = entry.split(" ")
        if len(entry) != 2:
            self.print("entry lenght invalid!", False)
            return

        if not entry[0].isnumeric() or not entry[1].isnumeric():
            self.print("entry must be numbers!", False)
            return
        if not entry[1] > entry[0]:
            self.print("max time must be bigger than min time!", False)
            return

        self.min_delay = int(entry[0])
        self.max_delay = int(entry[1])

        self.print(f"delay changed >>> min={self.min_delay}, max={self.max_delay}")
        self.lb_delay.config(text=f"min = {self.min_delay} sec. | max = {self.max_delay} sec.")

    def entry_coordinates(self):
        entry = str(self.txt_cursor_coordinates.get())
        if not entry:
            self.print("no entry", False)
            return
        entry = entry.split(" ")
        if len(entry) != 2:
            self.print("entry lenght invalid!", False)
            return

        if not entry[0].isnumeric() or not entry[1].isnumeric():
            self.print("entry must be numbers!", False)
            return

        self.cursor_coordinate_x = int(entry[0])
        self.cursor_coordinate_y = int(entry[1])
        self.lb_selected_cursor_coordinates.config(text=f"X = {self.cursor_coordinate_x} | Y = {self.cursor_coordinate_y}")  # nopep8
        self.print(f"coordinates changed >>> x={self.cursor_coordinate_x}, y={self.cursor_coordinate_y}")

    def set_labels_none(self):
        self.lb_selected_template.config(text="<no template selected>")
        self.lb_selected_cursor_coordinates.config(text="<no position selected>")
        self.lb_messages_preview.config(text="<no messages>")
        self.lb_delay.config(text=f"min = {self.min_delay} sec. | max = {self.max_delay} sec.")
        self.lb_system_debug.config(text="")

    def kill_bot(self):
        self.bot_alive = False
        self.bot_thread = None
        self.update_status()
        self.print("", False)

    def start_countdown(self, seconds):
        for sec in range(seconds):
            if not self.bot_alive:
                break
            self.print(f"Start in: {seconds - sec}", False)
            sleep(1)

    def message_preview(self):
        char_line_counter = 0
        txt = ""
        for element in self.messages_list:
            element = f"{element}; "
            txt += element
            char_line_counter += element.count("")

            if char_line_counter >= 75:
                txt += "\n"
                char_line_counter = 0
        self.lb_messages_preview.config(text=txt)

    def open_file_explorer(self):
        self.picked_path = filedialog.askopenfilename()
        if not self.picked_path:
            self.picked_path = None
            return
        self.lb_selected_template.config(text=self.picked_path)
        self.print(f"template selected >>> {self.picked_path}")
        self.messages_list = get_templates(self.picked_path)
        self.message_preview()

    def start(self):
        self.log.debug("Startup...")
        self.root.mainloop()

    def start_bot(self):
        if self.bot_alive or not self.messages_list:
            return

        # if not self.cursor_coordinate_x or not self.cursor_coordinate_y:
        #     return

        self.update_config()
        self.log.debug(f"Startup Chat-Bot >>> {self.config}")
        self.kill_bot()
        self.bot_thread = trd.Thread(target=self.bot)
        self.bot_alive = True
        self.bot_thread.start()

    def bot(self):

        self.start_countdown(10)
        self.update_status()
        message_counter = 0

        if len(self.messages_list) > 0:
            while True:

                if not self.bot_alive:
                    return

                rnd_delay = randint(self.min_delay, self.max_delay)
                message = choice(self.messages_list)
                for x in range(rnd_delay):
                    self.print(f"Sending message in {rnd_delay - x} sec. >>> {message}", False)
                    sleep(1)
                    if not self.bot_alive:
                        return

                if (message_counter == 0 or self.click_every_entry.get()) and self.cursor_coordinate_x and self.cursor_coordinate_y:  # nopep8
                    send_message(message, self.cursor_coordinate_x, self.cursor_coordinate_y, True)
                else:
                    send_message(message, self.cursor_coordinate_x, self.cursor_coordinate_y, False)

                self.print(f"Message sent >>> {message}")
                message_counter += 1


if __name__ == '__main__':
    bot = ChatBot()
    bot.start()
