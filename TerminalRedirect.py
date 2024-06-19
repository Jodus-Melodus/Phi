import customtkinter as ctk

class TerminalRedirect:
    def __init__(self, text_widget: ctk.CTkTextbox) -> None:
        self.text_widget: ctk.CTkTextbox = text_widget

    def write(self, message) -> None:
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", message)
        self.text_widget.yview_moveto(1)
        self.text_widget.update_idletasks()
        self.text_widget.configure(state="disabled")

    def readline(self, prompt="") -> str:
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", prompt)
        self.text_widget.mark_set("input_start", "end-1c")
        self.text_widget.mark_set("input_end", "end-1c + 1l")
        line = self.text_widget.get("input_start", "input_end")
        self.text_widget.delete("input_start", "input_end")
        self.text_widget.configure(state="disabled")
        
        return line