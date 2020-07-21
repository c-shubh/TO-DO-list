from tkinter import (Tk, ttk, TOP, RIGHT, LEFT, BOTH, X, Y, StringVar, messagebox)
import pickle


class MainWindow:

    def __init__(self, master):
        self.master = master
        self.master.title("TO-DO List")
        self.top_frame = ttk.Frame(self.master, borderwidth=1, relief="solid")
        self.middle_frame = ttk.Frame(self.master, borderwidth=1, relief="flat")

        self.todo_list = []

        # TOP FRAME WIDGETS--------------------------------
        self.add_item_button = ttk.Button(self.top_frame, text="Add Item", command=self.add_item)
        self.delete_all_items_button = ttk.Button(self.top_frame, text="Delete all items", command=self.delete_all_items)
        self.delete_selected_items_button = ttk.Button(self.top_frame, text="Delete selected items", command=self.delete_selected_items)
        self.save_button = ttk.Button(self.top_frame, text="Save", command=self.save)

        # TOP FRAME LAYOUT---------------------------------
        self.top_frame.pack(side=TOP, fill=X)
        self.add_item_button.pack(side=RIGHT)
        self.add_item_button.focus()
        self.delete_all_items_button.pack(side=RIGHT)
        self.delete_selected_items_button.pack(side=RIGHT)
        self.save_button.pack(side=RIGHT)

        for button in self.top_frame.winfo_children():
            button.pack_configure(padx=10)

        # MIDDLE FRAME LAYOUT------------------------------
        self.middle_frame.pack(fill=BOTH)


        # BINDINGS-----------------------------------------
        self.master.bind('<Control-n>', self.add_item)
        self.master.bind('<Control-s>', self.save)

        self.load_items()

    def add_item(self, *args):
        self.item_frame = ttk.Frame(self.middle_frame, borderwidth=1, relief="solid")
        self.item_frame.pack(fill=BOTH, pady=2.5, ipady=2)

        self.checkbuttonvar = StringVar()
        ttk.Checkbutton(self.item_frame, variable=self.checkbuttonvar).pack(side=LEFT, padx=(3.5, 0))
        self.checkbuttonvar.set(0)

        self.entryvar = StringVar()
        self.entry = ttk.Entry(self.item_frame, textvariable=self.entryvar)
        self.entry.pack(side=LEFT, expand=1, fill=X, padx=(0, 3.5))
        self.entry.focus()
        

        self.todo_list.append([self.item_frame, self.checkbuttonvar, self.entryvar])

    def save(self, *args):
        data = []
        for item in self.todo_list:
            data.append([item[1].get(), item[2].get()])
        with open("data.pkl", "wb+") as file_to_save:
            pickle.dump(data, file_to_save)

    def load_items(self):
        try:
            with open("data.pkl", "rb") as file_to_load:
                data = pickle.load(file_to_load)
                for i in range(len(data)):
                    self.add_item()
                    self.todo_list[i][1].set(data[i][0])
                    self.todo_list[i][2].set(data[i][1])
        except FileNotFoundError:
            with open("data.pkl", "wb+") as file_to_save:
                pickle.dump([], file_to_save)


    def delete_all_items(self):
        if messagebox.askyesno("Delete all items", "Are you sure you want to delete all the items?"):
            for item in self.todo_list:
                item[0].destroy()
            self.todo_list = []

            self.destroy_and_add_middle_frame()
            self.add_item_button.focus()

    def delete_selected_items(self):
        if messagebox.askyesno("Delete selected items", "Are you sure you want to delete the selected items?"):
            self.len = len(self.todo_list)
            for i in reversed(range(len(self.todo_list))):
                if self.todo_list[i][1].get() == "1":
                    self.todo_list[i][0].destroy()
                    del self.todo_list[i]
            if self.len == 1:
                self.destroy_and_add_middle_frame()
    
    def destroy_and_add_middle_frame(self):
        self.middle_frame.destroy()
        self.middle_frame = ttk.Frame(self.master, borderwidth=1, relief="flat")
        self.middle_frame.pack(fill=BOTH)
        self.add_item_button.focus()


    def on_closing(self):
        answer = messagebox.askyesnocancel("TO-DO List", "Do you want to save before closing?")
        if answer == True:
            self.save()
            root.destroy()
        if answer == False:
            root.destroy()
        if answer == None:
            pass

        


root = Tk()
app = MainWindow(root)

root.protocol("WM_DELETE_WINDOW", app.on_closing)
root.mainloop()