import customtkinter as ctk

class Dropdown:
    def __init__(self, master, width: int, height: int, items: list, command, item_pad_x: int, item_pad_y: int, bg_color: str, item_font: ctk.CTkFont):
        self.master = master
        self.width = width
        self.height = height
        self.items = items
        self.command = command
        self.item_pad_x = item_pad_x
        self.item_pad_y = item_pad_y
        self.item_font = item_font
        self.bg_color = bg_color

        self.ismapped = False
        self.current_selected_index = 0

        self.frame = ctk.CTkFrame(self.master, width=self.width, height=self.height, bg_color=self.bg_color)

    def winfo_ismapped(self) -> bool:
        return self.ismapped

    def update(self) -> None:
        for child in self.frame.winfo_children():
            child.destroy()

    def place(self, x, y) -> None:
        self.update()
        for i, item in enumerate(self.items):
            btn = ctk.CTkButton(self.frame, text=item, command=lambda item=item: self.command(str(item)), font=self.item_font,
                                height=14, anchor="w", fg_color="#262626" if i == 0 else "#333333", hover_color="#262626")
            btn.pack(fill="both", expand=True,
                     padx=self.item_pad_x, pady=self.item_pad_y)
        self.frame.place(x=x, y=y)
        self.ismapped = True

    def place_forget(self) -> None:
        self.update()
        self.frame.place_forget()
        self.ismapped = False