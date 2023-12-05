import random
import re
import time
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

class APP:
    # Initialize the GUI.
    def __init__(self):
        # Set the main application window.
        self.root = Tk() 

        # Set the running flag and time span for the selection process.
        self.running_flag = False 
        self.time_span = 0.1 
        self.index = 0

        self.initialize_window()

        # Define some methods to create, set and place the widgets within the 
        # main window.
        self.create_widget()
        self.configure_widget()
        self.place_widget()

        # Start the main event loop of the main window.
        self.root.mainloop()


    def initialize_window(self):
        # Set the title of the main window.
        self.root.title('Random Selection')

        # Set the size of the main window and calculate the position to 
        # center it on the screen. 
        width = 700
        height = 500
        left = (self.root.winfo_screenwidth() - width) / 2
        top = (self.root.winfo_screenheight() - height) / 2
        self.root.geometry("%dx%d+%d+%d" %(width, height, left, top))

        # Disable window resizing.
        self.root.resizable(0,0)


    def create_widget(self):      
        # Create a variable for label text and radio button selection.
        self.label_show_name_var = StringVar()
        self.radioBtn_var = IntVar(value = 1)

        # Create label, buttons, and frame widgets.
        self.label_show_name = ttk.Label(self.root, textvariable = 
                                        self.label_show_name_var, font = 
                                        ('Arial', 80, "bold"), foreground = 
                                        "#1E90FF")
        self.btn_start = ttk.Button(self.root, text = "Start", command = lambda: self.thread_it(self.start_point_name))
        self.btn_load_names = ttk.Button(self.root, text = "Load Names", command = self.load_names)
        self.label_frame = ttk.LabelFrame(self.root, text = "How To Make A Selection")
        self.radioBtn_sequence = ttk.Radiobutton(self.label_frame, text = 
                                                "Sequence", variable 
                                                = self.radioBtn_var, value = 1)
        self.radioBtn_random = ttk.Radiobutton(self.label_frame, text = 
                                               "Random", variable = 
                                               self.radioBtn_var, value = 2)
        self.radioBtn_deduplicate = ttk.Radiobutton(self.label_frame, text = 
                                               "Deduplicate", variable = 
                                               self.radioBtn_var, value = 3)
        self.label_show_name_num = ttk.Label(self.root, font = ('Arial', 20), 
                                            foreground = '#FF7F50')



    def configure_widget(self):
        default_name = "Who will be selected?"

        # We have already linked a lavel with self.label_show_name_var 
        # variable, the set method will update the value of the varible.
        self.label_show_name_var.set(default_name)

        # Define a method to adjust the display of the label.
        self.label_show_name_adjust(default_name)

        # When "Start" button was clicked, it will execute the function 
        # self.start_point_name.
        self.btn_start.config(command = lambda : self.thread_it(self.start_point_name))

        # When "Load Names" button was clicked, it will execute the function 
        # self.load_names.
        self.btn_load_names.config(command = self.load_names)

        # When "Close" button was clicked, it will execute self.quit_window 
        # function to end the main function. 
        self.root.protocol('WM_DELETE_WINDOW', self.quit_window)
        # Binding the "Escape" button and self.quit_window function, When we 
        # press the "Escape" button, the main function will also be ended.
        self.root.bind('<Escape>', self.quit_window)

        # Calling the method self.load_names_txt to load names from txt file 
        # and store them in a variable.
        init_names = self.load_names_txt("./names.txt")
        if init_names:
            self.default_names = init_names
            self.label_show_name_num.config(text = f"The Number Of Loading Names: {len(self.default_names)}")
        else:
            self.btn_start.config(state = DISABLED)
            self.label_show_name_num.config(text = f"Please Loading Name List First!")
        

    def place_widget(self):
        self.label_frame.place(x = 200, y = 250, width = 300, height = 50)
        self.radioBtn_sequence.place(x = 20, y = 0)
        self.radioBtn_random.place(x = 105, y = 0)
        self.radioBtn_deduplicate.place(x = 180, y = 0)
        self.btn_start.place(x = 290, y = 150, width = 120, height = 30)
        self.btn_load_names.place(x = 290, y = 200, width = 120, height = 30)
        self.label_show_name_num.place(x = 200, y = 330)



    def label_show_name_adjust(self, the_name):
        label_width = self.label_show_name.winfo_reqwidth()
        window_width = 700  # Width of the main window, adjust as needed

        # Calculate the x-coordinate to center the label text
        x_centered = (window_width - label_width) / 2

        self.label_show_name.place(x = x_centered, y=10)
        

    def start_point_name(self):
        # Check if there is only one person in the name list.
        if len(self.default_names) == 1 and self.index == 0:
        
            # Show a message if there is only one person.
            self.show_warning("Only one person in the name list")

            # Set the label to the single name.
            self.label_show_name_var.set(self.default_names[0])

            # Adjust the label postion.
            self.label_show_name_adjust(self.default_names[0])
            return
        
        # Check if the "Start" button is clicked.
        if self.btn_start["text"] == "Start":

            # Disable the "Load Names"  button.
            self.btn_load_names.config(state = DISABLED)

            # Set the running flag to True.
            self.running_flag = True

            # Check if the loaded names are in a list.
            if isinstance(self.default_names, list):

                # Change the text on the "Start" button.
                self.btn_start.config(text = "That's you")

                # Determine the mode based on the selected radio button.
                if self.radioBtn_var.get() == 1:
                    mode = "sequence"
                elif self.radioBtn_var.get() == 2:
                    mode = "random"
                elif self.radioBtn_var.get() == 3:
                    mode = "deduplicate"

                else:
                    pass

                # Start the name selection process in a separate thread.
                self.thread_it(self.point_name_begin(mode))
            
            # Show a warning if the name list is not loaded.
            else:
                self.show_warning("Please loading name list first")
        
        # If the text is not "Start", stop the process and enable the 
        # "Load Names" button and change the text to "Start".
        else:
            self.running_flag = False
            self.btn_load_names.config(state = NORMAL)
            self.btn_start.config(text = "Start")
            

    def point_name_begin(self, mode):
        if mode == "sequence":
            while True:
                if self.running_flag:
                    self.btn_start.config(text="Next")  # 更改按钮文本为“Next”############
                    self.next_point_name()
                    break
        elif mode == "random":
            while True:
                if self.running_flag:
                    # select a name randomly.
                    random_choice_name = random.choice(self.default_names)

                    # Set the random name as the text to the label.
                    self.label_show_name_var.set(random_choice_name)

                    # Adjust the name's position. 
                    self.label_show_name_adjust(random_choice_name)
                    time.sleep(self.time_span)
                else:
                    break
        elif mode == "deduplicate":
            while True:
                if self.running_flag and self.default_names:

                    # select a name randomly.
                    random_choice_name = random.choice(self.default_names)

                    # Set the random name as the text to the label.
                    self.label_show_name_var.set(random_choice_name)
                    
                    #Record the name on the current label.
                    current_name = self.label_show_name_var.get()#///////////////////

                    # Adjust the name's position. 
                    self.label_show_name_adjust(random_choice_name)
                    time.sleep(self.time_span)

                    
                elif len(self.default_names)==0:
                    self.show_warning("All names have been displayed! Please load a new list.")        
                    break
                else:
                    
                    #Remove the random name"" from name list
                    self.default_names.remove(current_name)
                    self.default_names = list(filter(None, self.default_names))  # 删除空行
                    self.index +=1
                    self.label_show_name_num.config(text = f"The Number Of Loading Names: {len(self.default_names)}")

                    break


    def next_point_name(self):
        if len(self.default_names) > 0:  # 如果还有名字
            current_name = self.default_names.pop(0)  # 移除第一个名字并获取
            self.label_show_name_var.set(current_name)  # 设置标签显示当前名字
            self.label_show_name_adjust(current_name)  # 调整标签位置
            self.btn_start.config(text="Next")  # 更改按钮文本为“Next”############
            self.btn_start.config(command=self.next_point_name)  # 更新按钮命令为下一个名字
        else:
            self.show_warning("All names have been displayed! Please load a new list.")
            self.btn_start.config(text="Start")  # 如果名字全部展示完毕，按钮恢复为“Start”状态
            self.btn_load_names.config(state = NORMAL) 
            self.btn_start.config(command=lambda: self.thread_it(self.start_point_name))  # 更新按钮命令为开始点名


    def always_ergodic(self):
        for i in self.default_names:
            if self.running_flag:
                self.label_show_name_var.set(i)
                self.label_show_name_adjust(i)

                self.btn_start.config(text = "That's you")

                time.sleep(self.time_span)

                # If i is the last name of the list, repeat the loop.
                if i == self.default_names[-1]:
                    self.show_warning("All names have been displayed!Please load a new list.")        
                    break
            else:
                break
    

    def load_names(self):

        # Open the file
        filename = askopenfilename(filetypes= [('files', '.TXT')], title = "Choose a file", initialdir = "./")

        if filename:
            names = self.load_names_txt(filename)
            if names:
                self.default_names = names

                # Update the label to display the number of the name list.
                self.label_show_name_num.config(text = f"the total number of loading names: {len(self.default_names)}" )
                default_name = "Who will be selected?"
                self.label_show_name_var.set(default_name)
                self.label_show_name_adjust(default_name)

                # Enable the "Start" button.
                self.btn_start.config(state = NORMAL)
            else:
                self.show_warning("Fail to loading names. Please check")


    # Loading names list from a txt file.
    def load_names_txt(self, txt_file):
        try:
            with open(txt_file, "r", encoding = "utf-8") as f:
                names = [name.strip() for name in f.readlines()]
                if len(names) == 0:
                    return False
                else:
                    return names
        except:
            return False
    

    def load_names_check(self, name):
        regex = r'[\u4e00-\u9fa5]+'
        if re.match(regex, name):
            return True
        else:
            return False
    

    def reset_name_list(self,mode = None):
        init_names = self.load_names_txt("./names.txt")
        if init_names:
            self.default_names = init_names
            self.label_show_name_num.config(text=f"The Number Of Loading Names: {len(self.default_names)}")
        else:
            self.btn_start.config(state=DISABLED)
            self.label_show_name_num.config(text="Please Loading Name List First!")
        

    def thread_it(self, func, *args):

        # Set a new thread.
        t = threading.Thread(target = func, args = args)

        # Set the new thread as Daemon thread. If the main program was stopped, the Daemon also will be.
        t.daemon = True

        # Start the thread.
        t.start()


    def quit_window(self, *args):
        # Ask for confirmation before closing the application.
        self.root.update()
        ret = self.ask_yes_no("Confirmation", "Are you sure to exit?")
        if ret:
            self.root.destroy()

    
    def show_info(self, message):
        self.root.after(0, lambda: messagebox.showinfo("INFO", message))


    def show_warning(self, message):
        self.root.after(0, lambda: messagebox.showwarning("WARNING", message))


    def ask_yes_no(self, title, message):
        result = messagebox.askyesno(title, message)
        return result
            

if __name__ == "__main__":
    a = APP()
                

