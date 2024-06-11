import customtkinter as ctk

class TerminalRedirect:
    def __init__(self, text_widget: ctk.CTkBaseClass) -> None:
        self.widget = text_widget

    def write(self, message) -> None:
        self.widget.configure(state="normal")
        self.widget.insert("end", message)
        self.widget.yview_moveto(1)
        self.widget.update_idletasks()
        self.widget.configure(state="disabled")

    def readline(self, prompt="") -> str:
        self.widget.configure(state="normal")
        self.widget.insert("end", prompt)
        self.widget.mark_set("input_start", "end-1c")
        self.widget.mark_set("input_end", "end-1c + 1l")
        line = self.widget.get("input_start", "input_end")
        self.widget.delete("input_start", "input_end")
        self.widget.configure(state="disabled")
        return line