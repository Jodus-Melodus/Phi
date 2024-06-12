import customtkinter as ctk

class Dialog:
    def __init__(self, master, title: str, message: str, x: int, y: int, font: ctk.CTkFont) -> None:
        self.master = master
        self.title = title
        self.message = message
        self.x = x
        self.y = y
        self.width = 500
        self.height = 250
        self.font = font
        self.dialog = ctk.CTkFrame(self.master, width=self.width, height=self.height, corner_radius=5)

    def show(self) -> None:
        title = ctk.CTkLabel(self.dialog, anchor="nw", text=self.title, font=self.font, text_color="#ee0000")
        msg = ctk.CTkTextbox(self.dialog, font=self.font)
        close = ctk.CTkButton(self.dialog, text="Close", command=self._close, font=self.font)

        msg.insert("0.0", self.message)
        msg.configure(wrap="none", state="disabled")

        title.pack(fill="both", anchor="nw", padx=10, pady=10)
        msg.pack(fill="both", expand=True, anchor="s", padx=10, pady=10)
        close.pack(expand=True, anchor="se", padx=10, pady=10)

        self.dialog.place(x=self.x-self.width//4, y=self.y-self.height//2)

    def _close(self) -> None:
        self.dialog.destroy()