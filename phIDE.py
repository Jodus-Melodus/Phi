import json
import sys
import re
import shell
import time
import customtkinter as ctk
import os
import threading

# Checks if the settings file exists
if os.path.exists("settings.json"):
    with open("settings.json", "r") as f:
        settings = json.load(f)
else:
    exit("Settings file not found")

class TerminalRedirect:
    def __init__(self, textWidget) -> None:
        self.widget = textWidget

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

# Custom dropdown menu
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

# Custom dialog
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
        title = ctk.CTkLabel(self.dialog, anchor="nw", text=self.title, font=self.font, text_color="#ee0000")
        msg = ctk.CTkTextbox(self.dialog, font=self.font)
        close = ctk.CTkButton(self.dialog, text="Close", command=self._close, font=self.font)

        msg.insert("0.0", self.message)
        msg.configure(wrap="word", state="disabled")

        title.pack(fill="both", anchor="nw", padx=10, pady=10)
        msg.pack(fill="both", expand=True, anchor="s", padx=10, pady=10)
        close.pack(expand=True, anchor="se", padx=10, pady=10)

        self.dialog.place(x=self.x-self.width//4, y=self.y-self.height//2)

    def _close(self) -> None:
        self.dialog.destroy()

# Main application
class App(ctk.CTk):
    def __init__(self) -> None:
        ctk.set_default_color_theme(f"Themes/{settings['theme']}/theme.json")
        super().__init__()
        self.title("phIDE")
        self.state("zoomed")
        self.iconbitmap("phi.ico")
        # Fonts
        self.editor_font = ctk.CTkFont(
            family=settings["editor-font-family"],
            size=settings["editor-font-size"],
            weight=settings["editor-font-weight"],
            slant=settings["editor-font-slant"],
            overstrike=settings["editor-font-overstrike"],
            underline=settings["editor-font-underline"]
        )
        self.console_font = ctk.CTkFont(
            family=settings["console-font-family"],
            size=settings["console-font-size"],
            weight=settings["console-font-weight"],
            slant=settings["console-font-slant"],
            overstrike=settings["console-font-overstrike"],
            underline=settings["console-font-underline"]
        )
        self.button_font = ctk.CTkFont(
            family=settings["button-font-family"],
            size=settings["button-font-size"],
            weight=settings["button-font-weight"],
            slant=settings["button-font-slant"],
            overstrike=settings["button-font-overstrike"],
            underline=settings["button-font-underline"]
        )
        self.label_font = ctk.CTkFont(
            family=settings["label-font-family"],
            size=settings["label-font-size"],
            weight=settings["label-font-weight"],
            slant=settings["label-font-slant"],
            overstrike=settings["label-font-overstrike"],
            underline=settings["label-font-underline"]
        )
        self.entry_font = ctk.CTkFont(
            family=settings["entry-font-family"],
            size=settings["entry-font-size"],
            weight=settings["entry-font-weight"],
            slant=settings["entry-font-slant"],
            overstrike=settings["entry-font-overstrike"],
            underline=settings["entry-font-underline"]
        )
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.center_x = self.width // 2
        self.screen_ratio = 0.65
        self.center_y = self.height // 2
        self.pad_x = settings["x-padding"]
        self.pad_y = settings["y-padding"]
        self.line = 1
        self.column = 1
        self.current_path = ""
        self.current_language = ""
        self.clipboard = ""
        self.code = ""
        self.error = ""
        self.open_editors = {}
        self.intelli_sense_boxes = {}
        self.snippet_menus = {}
        self.tab_names_paths = {}
        self.menu_open = False
        self.right_menu_open = False
        self.saved = False
        self.cursors = []
        self.variables = []

        # Frames
        self.left_panel = ctk.CTkFrame(self, width=200)
        self.right_panel = ctk.CTkScrollableFrame(self)
        self.bottom_panel = ctk.CTkFrame(self)
        self.center_panel = ctk.CTkFrame(self)
        self.goto_panel = ctk.CTkFrame(self.right_panel)
        self.find_and_replace_panel = ctk.CTkFrame(self.right_panel)
        self.multi_cursor_panel = ctk.CTkFrame(self.right_panel)
        self.menu_bar = ctk.CTkFrame(self, height=20)
        self.available_modules_panel = ctk.CTkFrame(self.right_panel)
        # Tabviews
        self.center_tabview = ctk.CTkTabview(
            self.center_panel,
            self.width*self.screen_ratio,
            height=self.height*self.screen_ratio
        )
        self.bottom_tabview = ctk.CTkTabview(
            self.bottom_panel,
            width=self.width*self.screen_ratio
        )
        self.console_tab = self.bottom_tabview.add("Console")
        self.warning_tab = self.bottom_tabview.add("Warnings")
        # Frames
        self.console_buttons = ctk.CTkFrame(self.console_tab)
        # Textboxes
        self.console = ctk.CTkTextbox(
            self.console_tab,
            font=self.console_font,
            state="disabled"
        )
        self.warnings = ctk.CTkTextbox(
            self.warning_tab,
            font=self.editor_font,
            state="disabled"
        )
        self.multi_cursor_textbox = ctk.CTkTextbox(
            self.multi_cursor_panel,
            font=self.editor_font
        )
        self.available_modules_textbox = ctk.CTkTextbox(
            self.available_modules_panel,
            font=self.editor_font
        )
        # Buttons
        self.clear_console_button = ctk.CTkButton(
            self.console_buttons,
            text="Clear",
            command=self.clear_console,
            font=self.button_font,
            width=50,
            height=20
        )
        self.goto_button = ctk.CTkButton(
            self.goto_panel,
            text="Go to",
            command=self.goto_click,
            font=self.button_font
        )
        self.copy_error_button = ctk.CTkButton(
            self.console_buttons,
            text="Copy",
            command=self.copy_error_message,
            font=self.button_font,
            width=50,
            height=20
        )
        self.find_and_replace_button = ctk.CTkButton(
            self.find_and_replace_panel,
            text="Find & Replace",
            command=self.find_and_replace,
            font=self.button_font
        )
        # Menu Buttons & Popups
        self.file_menu = ctk.CTkButton(
            self.menu_bar,
            text="File",
            height=20,
            width=50,
            command=self.file_menu_click,
            font=self.button_font
        )
        self.edit_menu = ctk.CTkButton(
            self.menu_bar,
            text="Edit",
            height=20,
            width=50,
            command=self.edit_menu_click,
            font=self.button_font
        )
        self.run_menu = ctk.CTkButton(
            self.menu_bar,
            text="Run",
            height=20,
            width=50,
            command=self.run_menu_click,
            font=self.button_font
        )
        self.file_menu_popup = ctk.CTkSegmentedButton(
            self,
            values=["New File", "Open File", "Save File", "Close File"],
            command=self.process_menu_shortcuts,
            height=20,
            font=self.button_font
        )
        self.edit_menu_popup = ctk.CTkSegmentedButton(
            self,
            values=["Undo", "Redo", "Copy", "Paste", "Replace", "Comment"],
            command=self.process_menu_shortcuts,
            height=20,
            font=self.button_font
        )
        self.run_menu_popup = ctk.CTkSegmentedButton(
            self,
            values=["Run"],
            command=self.process_menu_shortcuts,
            height=20,
            font=self.button_font
        )
        self.right_click_popup = Dropdown(
            self,
            width=300,
            height=100,
            items=["New File", "Open File", "Save File", "Close File", "Run","Undo", "Redo", "Copy", "Paste", "Replace", "Comment"],
            command=self.process_menu_shortcuts,
            item_pad_x=2,
            item_pad_y=2,
            bg_color=settings["intelli-sense-menu-color"],
            item_font=self.button_font
        )
        # Labels
        self.status_bar = ctk.CTkLabel(
            self,
            text="",
            height=20,
            font=self.label_font
        )
        self.multi_cursor_abel = ctk.CTkLabel(
            self.multi_cursor_panel,
            text="Multi-Cursor",
            font=self.label_font,
            anchor="nw"
        )
        self.goto_label = ctk.CTkLabel(
            self.goto_panel,
            text="Go To",
            font=self.label_font,
            anchor="nw"
        )
        self.find_label = ctk.CTkLabel(
            self.find_and_replace_panel,
            text="Find",
            font=self.label_font
        )
        self.replace_label = ctk.CTkLabel(
            self.find_and_replace_panel,
            text="Replace",
            font=self.label_font
        )
        self.available_modules_label = ctk.CTkLabel(
            self.available_modules_panel,
            text="Available Modules",
            font=self.label_font
        )
        # Entries
        self.goto_entry = ctk.CTkEntry(
            self.goto_panel,
            placeholder_text="Go to line",
            font=self.entry_font
        )
        self.find_entry = ctk.CTkEntry(
            self.find_and_replace_panel,
            placeholder_text="Find",
            font=self.entry_font
        )
        self.replace_entry = ctk.CTkEntry(
            self.find_and_replace_panel,
            placeholder_text="Replace",
            font=self.entry_font
        )
        # ComboBox
        self.current_language_combo = ctk.CTkOptionMenu(
            self.menu_bar,
            height=20,
            font=self.button_font,
            values=[""]
        )
        # Other
        sys.stdin = TerminalRedirect(self.console)
        sys.stdout = TerminalRedirect(self.console)
        sys.stderr = TerminalRedirect(self.console)

        # Pack all the components
        self.available_modules_label.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            side="top",
            anchor="nw"
        )
        self.available_modules_textbox.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            expand=True
        )
        self.available_modules_textbox.configure(
            state="disabled"
        )
        self.multi_cursor_abel.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            side="top",
            anchor="nw"
        )
        self.multi_cursor_textbox.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            expand=True
        )
        self.multi_cursor_textbox.configure(
            state="disabled"
        )

        self.menu_bar.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            anchor="w"
        )
        self.current_language_combo.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            expand=True,
            anchor="e",
            side="right"
        )
        self.file_menu.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            expand=True,
            anchor="w",
            side="left"
        )
        self.edit_menu.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            expand=True,
            anchor="w",
            side="left"
        )
        self.run_menu.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            expand=True,
            anchor="w",
            side="left"
        )

        self.goto_label.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            side="top",
            anchor="nw"
        )
        self.goto_button.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            side="bottom"
        )
        self.goto_entry.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            side="top",
            expand=True
        )

        self.find_label.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            anchor="nw"
        )
        self.find_entry.pack(
            padx=self.pad_x,
            pady=self.pad_y
        )
        self.replace_label.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            anchor="nw"
        )
        self.replace_entry.pack(
            padx=self.pad_x,
            pady=self.pad_y
        )
        self.find_and_replace_button.pack(
            padx=self.pad_x,
            pady=self.pad_y
        )

        self.status_bar.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            side="bottom",
            anchor="se",
            expand=True
        )
        self.console_buttons.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            side="right",
            anchor="n"
        )
        self.console.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            fill="both",
            expand=True
        )
        self.warnings.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            fill="both",
            expand=True
        )
        self.clear_console_button.pack(
            padx=self.pad_x,
            pady=self.pad_y
        )
        self.copy_error_button.pack(
            padx=self.pad_x,
            pady=self.pad_y
        )

        self.right_panel.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            fill="both",
            side="right",
            anchor="e"
        )
        self.left_panel.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            fill="both",
            side="left",
            anchor="w"
        )
        self.center_panel.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            fill="both",
            expand=True
        )
        self.bottom_panel.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            fill="both",
            expand=True,
            anchor="s"
        )

        self.center_tabview.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            expand=True,
            fill="both"
        )
        self.bottom_tabview.pack(
            padx=self.pad_x,
            pady=self.pad_y,
            expand=True,
            fill="both"
        )

# Bindings
# Single Character Sequence
        self.bind("<F1>", self.show_help)
        self.bind("<F5>", self.run)
        self.bind("<Return>", self.enter_commands)
        self.bind("<Escape>", self.escape_key_press)
        self.bind("<(>", self.auto_parenthesis)
        self.bind("<[>", self.auto_bracket)
        self.bind("<{>", self.auto_brace)
        self.bind("<\">", self.auto_double_quote)
        self.bind("<'>", self.auto_single_quote)
        self.bind("<KeyPress>", self.key_press_update)
        self.bind("<Down>", self.intelli_sense_down_key_press)
        self.bind("<Up>", self.intelli_sense_up_key_press)

# Double Character Sequence
        self.bind("<Control-F4>", self.close_file)
        self.bind("<Control-BackSpace>", self.backspace_entire_word)
        self.bind("<Control-space>", self.intelli_sense_trigger)
        self.bind("<Control-Tab>", self.next_tab)
        self.bind("<Control-/>", self.comment_line)
        self.bind("<Control-;>", self.show_snippets)
        self.bind("<Control-]>", self.indent)
        self.bind("<Control-[>", self.dedent)
        self.bind("<Control-k>", self.open_folder)
        self.bind("<Control-o>", self.open_files)
        self.bind("<Control-s>", self.save_file)
        self.bind("<Control-n>", self.new_file)
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-h>", self.toggle_find_and_replace)
        self.bind("<Control-g>", self.toggle_goto_menu)
        self.bind("<Control-m>", self.toggle_multi_cursor_menu)
        self.bind("<Control-Home>", self.page_top)
        self.bind("<Control-End>", self.page_bottom)
# Triple Character Sequence
        self.bind("<Control-Shift-z>", self.redo)
        self.bind("<Control-Shift-Tab>", self.previous_tab)
        self.bind("<Control-Alt-m>", self.toggle_available_modules)
# Mouse Click
        self.bind("<Button-1>", self.mouse_click_update)
        self.bind("<ButtonRelease-1>", self.highlight_selected)
        self.bind("<Button-2>", self.multi_cursor)
        self.bind("<Control-Button-1>", self.multi_cursor)
        self.bind("<Button-3>", self.right_click_menu_click)

        self.mainloop()

    def page_top(self, e=None) -> None:
        """Scroll to the top of the text widget."""
        if editor := self.current_tab:
            editor.see("1.0")

    def page_bottom(self, e=None) -> None:
        """Scroll to the bottom of the text widget."""
        if editor := self.current_tab:
            editor.see("end")

    def toggle_available_modules(self, e=None) -> None:
        """Toggle the visibility of available modules."""

        available_modules = os.listdir("Modules")
        self.available_modules_textbox.configure(state="normal")
        self.available_modules_textbox.delete("1.0", "end")
        self.available_modules_textbox.insert("end", "\n".join(available_modules))
        self.available_modules_textbox.configure(state="disabled")

        if self.available_modules_panel.winfo_ismapped():
            self.available_modules_panel.pack_forget()
            if editor := self.current_tab:
                editor.focus_set()
        else:
            self.available_modules_panel.pack(padx=self.pad_x, pady=self.pad_y*5)
            self.find_entry.focus_set()

    def show_help(self, e=None) -> None:
        help_window = ctk.CTkToplevel()
        help_window.title("phIDE - Help")
        help_text = ctk.CTkTextbox(help_window, font=self.editor_font)
        help_text.pack(expand=True, fill="both")
        text = """\
        F1 -                    Show this menu
        F5 -                    Run current file
        Enter -                 Select first intellisense word
        Ctrl + Backspace -      Deletes entire word
        Ctrl + Space -          Manually open intellisense
        Ctrl + ; -              Show Snippet menu
        Ctrl + / -              Comment current line
        Ctrl + K -              Open folder
        Ctrl + O -              Open file
        Ctrl + S -              Save current file
        Ctrl + N -              Creates a new file
        Ctrl + F4 -             Close current tab
        Ctrl + C -              Copy selected text
        Ctrl + V -              Paste last copied word
        Ctrl + Z -              Undo action
        Ctrl + Shift + Z -      Redo action
        Ctrl + H -              Toggle the find and replace panel
        Ctrl + G -              Toggle the go to panel
        Ctrl + M -              Toggle the multi-cursor panel
        Ctrl + [ -              Dedent line or selected text
        Ctrl + ] -              Indent line or selected text
        Ctrl + Tab -            Next tab
        Ctrl + Shift + Tab -    Previous Tab
        Ctrl + Left Click -     Add/remove cursor
        Middle Click -          Add/remove cursor
        Esc -                   Hide intelliSense
        """
        help_text.insert("0.0", text)
        help_text.configure(wrap="none", state="disabled")

    @property
    def current_tab(self) -> ctk.CTkTextbox:
        tab_name = self.center_tabview.get()
        if (tab_name != "") and (tab_name in self.open_editors):
            return self.open_editors[tab_name]

    def copy_error_message(self) -> None:
        if editor := self.current_tab:
            editor.clipboard_append(self.error)

    def clear_console(self) -> None:
        self.console.configure(state="normal")
        self.console.delete("0.0", "end")
        self.console.configure(state="disabled")

    def add_tab(self, path: str) -> None:
        self.current_path = path
        self.load_language_syntax()
        self.current_language = "." + path.split("/")[-1].split(".")[-1]
        self.current_language_combo.set(self.current_language)

        tab_name = path.split("/")[-1]
        if tab_name not in self.center_tabview._tab_dict:
            tab = self.center_tabview.add(tab_name)

            editor = ctk.CTkTextbox(
                tab,
                font=self.editor_font,
                undo=True,
                maxundo=-1,
                spacing1=2,
                spacing3=2,
                wrap="none",
                tabs="1c"
            )
            
            t = threading.Thread(target=self.update_syntax)
            t.daemon = True
            t.start()

            if self.current_language in self.language_syntax_patterns:
                for tag in self.language_syntax_patterns[self.current_language]:
                    editor.tag_config(
                        tag, foreground=self.language_syntax_patterns[self.current_language][tag][0])
                editor.tag_config("error", foreground=settings["error-tag-foreground-color"],
                                  background=settings["error-tag-background-color"], underline=settings["error-tag-underline"])
                editor.tag_config("similar", foreground=settings["similar-tag-foreground-color"],
                                  background=settings["similar-tag-background-color"], underline=settings["similar-tag-underline"])
                editor.tag_config("sel", foreground=settings["selected-tag-foreground-color"],
                                  background=settings["selected-tag-background-color"], underline=settings["selected-tag-underline"])
                editor.tag_config("warning", foreground=settings["warning-tag-foreground-color"],
                                  background=settings["warning-tag-background-color"], underline=settings["warning-tag-underline"])

                editor.pack(expand=True, fill="both")

                self.intelli_sense_boxes[tab_name] = Dropdown(editor, 300, 100, [
                ], self.intelli_sense_click_insert, 2, 2, settings["intelli-sense-menu-color"], self.editor_font)
                self.snippet_menus[tab_name] = Dropdown(
                    editor, 300, 100, [], self.insert_snippet, 2, 2, settings["snippet-menu-color"], self.editor_font)
                editor.bind("<KeyPress>", self.editor_press)

                self.open_editors[tab_name] = editor
                self.tab_names_paths[tab_name] = path

                with open(path, "r") as f:
                    for line in f.readlines():
                        editor.insert("end", line)

                self.code = editor.get("0.0", "end")
                self.load_snippets()
            else:
                Dialog(self, "Error", "File extention not supported.",
                       self.center_x, self.center_y)
        else:
            Dialog(self, "Error", "Cannot open two files with the same name.",
                   self.center_x, self.center_y)

# Updates
    def increment_index(self, cursor: str) -> str:
        line, char = cursor.split(".")

        return f"{line}.{str(int(char) + 1)}"

    def decrement_index(self, cursor: str) -> str:
        line, char = cursor.split(".")

        if char == "0":
            return f"{str(int(line) - 1)}.lineend"

        return f"{line}.{str(int(char) - 1)}"

    def update_multi_cursors(self, e) -> None:
        if not (editor := self.current_tab):
            return
        for cursor in self.cursors:
            editor.delete(cursor)
            editor.insert(cursor, "|")

        new = []
        for index in self.cursors:
            if index != editor.index("insert"):
                key = e.keysym.lower()
                if key not in ["control_l", "control_r", "shift_L", "shift_r", "alt_L", "alt_r"]:
                    if key == "left":
                        new.append(self.decrement_index(index))
                    elif key == "right":
                        new.append(self.increment_index(index))
                    elif key == "backspace":
                        editor.delete(f"{index}-1c", index)
                        new.append(self.decrement_index(index))
                    elif key == "space":
                        editor.insert(index, " ")
                        new.append(self.increment_index(index))
                    else:
                        editor.insert(index, key)
                        new.append(self.increment_index(index))

        self.cursors = new
        self.multi_cursor_textbox.configure(state="normal")
        self.multi_cursor_textbox.delete("0.0", "end")
        self.multi_cursor_textbox.insert("0.0", "\n".join(self.cursors))
        self.multi_cursor_textbox.configure(state="disabled")

    def key_press_update(self, e=None) -> None:
        self.current_language = self.current_language_combo.get()
        if editor := self.current_tab:
            self.line, self.column = editor.index("insert").split(".")
            self.status_bar.configure(text=f"Ln {self.line}, Col {self.column}")

            current_code = editor.get("0.0", "end")

            if self.current_language == ".phi":
                warning = shell.incremental_parsing(
                    current_code, self.current_path)
                self.warnings.configure(state="normal")
                self.warnings.delete("0.0", "end")
                self.warnings.configure(state="disabled")
                if warning != "":
                    line = warning.line
                    editor.tag_add("warning", f"{line}.0", f"{line}.end")
                    if warning.warning_message() not in self.warnings.get("0.0", "end"):
                        self.warnings.configure(state="normal")
                        self.warnings.insert("end", warning.warning_message())
                        self.warnings.configure(state="disabled")

                warnings = self.warnings.get("0.0", "end").strip().split("\n")
                tabs = list(self.bottom_tabview._tab_dict.keys())
                current_name = tabs[1]
                if (len(warnings) > 0) and (warnings[0] != ""):
                    new_name = f"Warnings({len(warnings)})"
                else:
                    new_name = "Warnings"
                if new_name not in self.bottom_tabview._tab_dict.keys():
                    self.bottom_tabview.rename(current_name, new_name)

        self.update_multi_cursors(e)

        if hasattr(self, "intelliSenseBox") and self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
            self.intelli_sense_trigger()
        if hasattr(self, "snippetMenu") and self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
            self.show_snippets()

    def editor_press(self, e=None) -> None:
        self.saved = False

        if editor := self.current_tab:
            editor.tag_remove("warning", "0.0", "end")
            current_code = editor.get("0.0", "end")
            name = self.center_tabview.get()
            if current_code != self.code:
                self.code = current_code
                self.title(f"{name}*")
            else:
                self.title(name)

            self.variables = re.findall(r"\b[^\d\W]+\b", current_code)

            if hasattr(self, "intelliSenseBox") and self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
                self.intelli_sense_trigger()

            warning = shell.incremental_parsing(current_code, self.current_path)
            self.warnings.configure(state="normal")
            self.warnings.delete("0.0", "end")
            self.warnings.configure(state="disabled")
            if warning != "":
                line = warning.line
                editor.tag_add("warning", f"{line}.0", f"{line}.end")
                if warning.warning_message() not in self.warnings.get("0.0", "end"):
                    self.warnings.configure(state="normal")
                    self.warnings.insert("end", warning.warning_message())
                    self.warnings.configure(state="disabled")

            warnings = self.warnings.get("0.0", "end").strip().split("\n")
            tabs = list(self.bottom_tabview._tab_dict.keys())
            current_name = tabs[1]
            if (len(warnings) > 0) and (warnings[0] != ""):
                new_name = f"Warnings({len(warnings)})"
            else:
                new_name = "Warnings"
            if new_name not in self.bottom_tabview._tab_dict.keys():
                self.bottom_tabview.rename(current_name, new_name)

    def mouse_click_update(self, e=None) -> None:
        if editor := self.current_tab:
            editor.tag_remove("similar", "0.0", "end")

    def highlight_selected(self, e=None) -> None:
        if not (editor := self.current_tab):
            return
        text = editor.get("0.0", "end").split("\n")
        if editor.tag_ranges("sel"):
            w = editor.get(ctk.SEL_FIRST, ctk.SEL_LAST)
            word = re.escape(w)
            pattern = f"({word})"
            for ln, line in enumerate(text):
                matches = [(match.start(), match.end())
                           for match in re.finditer(pattern, line)]
                for start, end in matches:
                    editor.tag_add(
                        "similar", f"{ln+1}.{start}", f"{ln+1}.{end}")
                    editor.tag_remove("error", f"{ln}.0", f"{ln}.end")

    def enter_commands(self, e=None) -> None:
        self.intelli_sense_enter_insert()
        self.enter_snippets()

# Snippets
    def enter_snippets(self) -> None:
        if self.snippet_menus[self.center_tabview.get()].winfo_ismapped() and len(self.snippet_menus[self.center_tabview.get()].items) > 0:
            if editor := self.current_tab:
                snippet = self.snippets_dictionary[self.snippets[self.snippet_menus[self.center_tabview.get(
                )].current_selected_index]]
                currentIndex = editor.index("insert -1l lineend")
                wordStart = editor.search(
                    r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", currentIndex, backwards=True, regexp=True)
                word = editor.get(wordStart, currentIndex).strip(
                    " \n\t\r({[]})")
                startPos = f"{currentIndex.split('.')[0]}.{int(currentIndex.split('.')[1]) - len(word)}"
                editor.delete(startPos, "insert")
                editor.insert(startPos, snippet)
                editor.focus_set()
                self.snippet_menus[self.center_tabview.get()].place_forget()

    def insert_snippet(self, snippet_name: str) -> None:
        if editor := self.current_tab:
            snippet = self.snippets_dictionary[snippet_name]
            current_index = editor.index("insert -1l lineend")
            word_start = editor.search(
                r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", current_index, backwards=True, regexp=True)
            word = editor.get(word_start, current_index).strip(" \n\t\r({[]})")
            start_position = f"{current_index.split('.')[0]}.{int(current_index.split('.')[1]) - len(word)}"
            editor.delete(start_position, "insert")
            editor.insert(start_position, snippet)
            editor.focus_set()
            self.snippet_menus[self.center_tabview.get()].place_forget()

    def show_snippets(self, e=None) -> None:
        if not (editor := self.current_tab):
            return
        self.snippet_menus[self.center_tabview.get()].place_forget()
        self.snippets = list(self.snippets_dictionary.keys())
        x, y, _, _ = editor.bbox(editor.index("insert"))
        current_index = editor.index("insert")
        word_start = editor.search(
            r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", current_index, backwards=True, regexp=True)
        word = editor.get(word_start, current_index).strip(" \n\t\r{[()]}")

        size = 4
        i = self.snippet_menus[self.center_tabview.get()
                              ].current_selected_index
        start_index = max(0, i)
        if word:
            words = [w for w in self.snippets if w.startswith(word)]
            self.snippets = words
            if self.snippets:
                if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
                    self.intelli_sense_boxes[self.center_tabview.get(
                    )].place_forget()
                end_index = min(len(self.snippets), i + size + 1)
        else:
            if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
                self.intelli_sense_boxes[self.center_tabview.get(
                )].place_forget()
            end_index = min(len(self.snippets), i + size + 1)

        self.snippet_menus[self.center_tabview.get(
        )].items = self.snippets[start_index:end_index]
        self.snippet_menus[self.center_tabview.get()].place(x=x, y=y+30)

    def load_snippets(self) -> None:
        path = f"snippets/{self.current_language[1:]}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                self.snippets_dictionary = json.load(f)
                self.snippets = list(self.snippets_dictionary.keys())
        else:
            Dialog(self, "Error", "Failed to load snippets.",
                   self.center_x, self.center_y)

# Syntax
    def load_language_syntax(self) -> None:
        path = f"Themes/{settings['theme']}/syntax.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                self.language_syntax_patterns = json.load(f)
            self.current_language_combo.configure(
                values=self.language_syntax_patterns)
        else:
            Dialog(self, "Error", "Failed to open syntax file.",
                   self.center_x, self.center_y)

    def update_syntax(self, line: str = None, lnIndex: int = None) -> None:
        if editor := self.current_tab:
            for tag in self.language_syntax_patterns[self.current_language]:
                pattern = self.language_syntax_patterns[self.current_language][tag][1]
                editor.tag_remove(tag, "0.0", "end")

                first_visible_index = editor.index("@0,0")
                last_visible_index = editor.index(f"@0,{str(editor.winfo_height())}")

                for ln in range(int(first_visible_index.split(".")[0]), int(last_visible_index.split(".")[0]) + 1):
                    text = editor.get(f"{ln}.0", f"{ln}.end")
                    matches = [(match.start(), match.end())
                               for match in re.finditer(pattern, text, re.MULTILINE)]

                    for start, end in matches:
                        editor.tag_add(
                            tag, f"{ln}.{start}", f"{ln}.{end}")

        time.sleep(0.1)
        self.update_syntax()

# IntelliSense
    def intelli_sense_up_key_press(self, e=None) -> None:
        if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped() and self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
            if editor := self.current_tab:
                editor.mark_set(
                    "insert", editor.index("insert +1l lineend"))
            self.intelli_sense_boxes[self.center_tabview.get(
            )].current_selected_index -= 1
            if self.intelli_sense_boxes[self.center_tabview.get()].current_selected_index < 0:
                self.intelli_sense_boxes[self.center_tabview.get()].current_selected_index = len(
                    self.intelli_sense_words) - 1
            self.intelli_sense_trigger()

        if self.snippet_menus[self.center_tabview.get()].winfo_ismapped() and self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
            if editor := self.current_tab:
                editor.mark_set(
                    "insert", editor.index("insert +1l lineend"))
            self.snippet_menus[self.center_tabview.get()
                              ].current_selected_index -= 1
            if self.snippet_menus[self.center_tabview.get()].current_selected_index < 0:
                self.snippet_menus[self.center_tabview.get()].current_selected_index = len(
                    self.snippets) - 1
            self.show_snippets()

    def intelli_sense_down_key_press(self, e=None) -> None:
        if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped() and self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
            if editor := self.current_tab:
                editor.mark_set(
                    "insert", editor.index("insert -1l lineend"))
            self.intelli_sense_boxes[self.center_tabview.get(
            )].current_selected_index += 1
            if self.intelli_sense_boxes[self.center_tabview.get()].current_selected_index >= len(self.intelli_sense_words):
                self.intelli_sense_boxes[self.center_tabview.get(
                )].current_selected_index = 0
            self.intelli_sense_trigger()

        if self.snippet_menus[self.center_tabview.get()].winfo_ismapped() and self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
            if editor := self.current_tab:
                editor.mark_set(
                    "insert", editor.index("insert -1l lineend"))
            self.snippet_menus[self.center_tabview.get()
                              ].current_selected_index += 1
            if self.intelli_sense_boxes[self.center_tabview.get()].current_selected_index >= len(self.snippets):
                self.snippet_menus[self.center_tabview.get()
                                  ].current_selected_index = 0
            self.show_snippets()

    def intelli_sense_trigger(self, e=None) -> None:
        if not (editor := self.current_tab):
            return
        self.intelli_sense_boxes[self.center_tabview.get()].place_forget()
        self.intelli_sense_words = list(sorted(list(set(
            self.language_syntax_patterns[self.current_language]["keywords"][2] + self.variables + self.language_syntax_patterns[self.current_language]["errors"][2]))))
        x, y, _, _ = editor.bbox(editor.index("insert"))
        current_index = editor.index("insert")
        word_start = editor.search(
            r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", current_index, backwards=True, regexp=True)
        word = editor.get(word_start, current_index).strip(" \n\t\r({[.]})")

        size = 4
        i = self.intelli_sense_boxes[self.center_tabview.get(
        )].current_selected_index
        start_index = max(0, i)
        if word:
            words = [w for w in self.intelli_sense_words if w.startswith(word)]
            self.intelli_sense_words = words
            if self.intelli_sense_words:
                # Hide snippetMenu if present
                if self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
                    self.snippet_menus[self.center_tabview.get()
                                      ].place_forget()
                end_index = min(len(self.intelli_sense_words), i + size + 1)
        else:
            # Hide snippetMenu if present
            if self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
                self.snippet_menus[self.center_tabview.get()].place_forget()
            end_index = min(len(self.intelli_sense_words), i + size + 1)

        self.intelli_sense_boxes[self.center_tabview.get(
        )].items = self.intelli_sense_words[start_index:end_index]
        self.intelli_sense_boxes[self.center_tabview.get()].place(x=x, y=y+30)

    def intelli_sense_enter_insert(self, e=None) -> None:
        if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped() and len(self.intelli_sense_boxes[self.center_tabview.get()].items) > 0:
            if editor := self.current_tab:
                selected_word = self.intelli_sense_words[self.intelli_sense_boxes[self.center_tabview.get(
                )].current_selected_index]
                current_index = editor.index("insert -1l lineend")
                word_start = editor.search(
                    r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", current_index, backwards=True, regexp=True)
                word = editor.get(word_start, current_index).strip(
                    " \n\t\r({[]})")
                start_position = f"{current_index.split('.')[0]}.{int(current_index.split('.')[1]) - len(word)}"
                editor.delete(start_position, "insert")
                editor.insert(start_position, selected_word)
                editor.focus_set()
                self.intelli_sense_boxes[self.center_tabview.get(
                )].place_forget()

    def intelli_sense_click_insert(self, selected) -> None:
        if editor := self.current_tab:
            current_index = editor.index("insert")
            word_start = editor.search(
                r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", current_index, backwards=True, regexp=True)
            word = editor.get(word_start, current_index).strip(" \n\t\r({[]})")
            start_position = f"{current_index.split('.')[0]}.{int(current_index.split('.')[1]) - len(word)}"
            editor.delete(start_position, "insert")
            editor.insert(start_position, selected)
            editor.focus_set()
            self.intelli_sense_boxes[self.center_tabview.get()].place_forget()

# Menu Bar
    def right_click_menu_click(self, e=None) -> None:
        if self.right_menu_open:
            self.right_click_popup.place_forget()
            self.right_menu_open = False
        else:
            self.right_click_popup.place(x=e.x, y=e.y)
            self.right_menu_open = True

    def file_menu_click(self) -> None:
        self.file_menu_popup.set("")
        if self.menu_open:
            self.file_menu_popup.place_forget()
            self.edit_menu_popup.place_forget()
            self.run_menu_popup.place_forget()
            self.menu_open = False
        else:
            self.file_menu_popup.place(
                x=self.file_menu.winfo_x()+5, y=self.file_menu.winfo_y()+30)
            self.menu_open = True

    def edit_menu_click(self) -> None:
        self.edit_menu_popup.set("")
        if self.menu_open:
            self.file_menu_popup.place_forget()
            self.edit_menu_popup.place_forget()
            self.run_menu_popup.place_forget()
            self.menu_open = False
        else:
            self.edit_menu_popup.place(
                x=self.edit_menu.winfo_x()+5, y=self.edit_menu.winfo_y()+30)
            self.menu_open = True

    def run_menu_click(self) -> None:
        self.run_menu_popup.set("")
        if self.menu_open:
            self.file_menu_popup.place_forget()
            self.edit_menu_popup.place_forget()
            self.run_menu_popup.place_forget()
            self.menu_open = False
        else:
            self.run_menu_popup.place(
                x=self.run_menu.winfo_x()+5, y=self.run_menu.winfo_y()+30)
            self.menu_open = True

    def process_menu_shortcuts(self, name: str) -> None:
        self.file_menu_popup.place_forget()
        self.edit_menu_popup.place_forget()
        self.run_menu_popup.place_forget()
        self.right_click_popup.place_forget()
        match name:
            case "New File":
                self.new_file()
            case "Open File":
                self.open_files()
            case "Save File":
                self.save_file()
            case "Close File":
                self.close_file()
            case "Undo":
                self.undo()
            case "Redo":
                self.redo()
            case "Copy":
                self.copy()
            case "Paste":
                self.paste()
            case "Comment":
                self.comment_line()
            case "Run":
                self.run()

# Side Menus
    def toggle_multi_cursor_menu(self, e=None) -> None:
        if self.multi_cursor_panel.winfo_ismapped():
            self.multi_cursor_panel.pack_forget()
        else:
            self.multi_cursor_panel.pack(padx=self.pad_x, pady=self.pad_y*5)

    def toggle_goto_menu(self, e=None) -> None:
        if self.goto_panel.winfo_ismapped():
            self.goto_panel.pack_forget()
            if editor := self.current_tab:
                editor.focus_set()
        else:
            self.goto_panel.pack(padx=self.pad_x, pady=self.pad_y*5)
            self.goto_entry.focus_set()

    def goto_click(self) -> None:
        if editor := self.current_tab:
            line_number = int(self.goto_entry.get())
            index = f"{line_number}.0"
            editor.see(index)

    def toggle_find_and_replace(self, e=None) -> None:
        if self.find_and_replace_panel.winfo_ismapped():
            self.find_and_replace_panel.pack_forget()
            if editor := self.current_tab:
                editor.focus_set()
        else:
            self.find_and_replace_panel.pack(padx=self.pad_x, pady=self.pad_y*5)
            self.find_entry.focus_set()

    def find_and_replace(self, e=None) -> None:
        find = self.find_entry.get()
        replace = self.replace_entry.get()

        if editor := self.current_tab:
            editor_text = editor.get("1.0", "end")
            updated_text = editor_text.replace(find, replace)

            editor.delete("1.0", "end")
            editor.insert("1.0", updated_text)

# Shortcuts
    def multi_cursor(self, e=None) -> None:
        if editor := self.current_tab:
            index = editor.index("current")
            if index in self.cursors:
                self.cursors.remove(index)
            else:
                self.cursors.append(editor.index("current"))

    def indent(self, e=None) -> None:
        if editor := self.current_tab:
            if selected := editor.tag_ranges("sel"):
                start_position, end_position = selected[0].string, selected[1].string
                start_line = int(start_position.split(".")[0])
                endLine = int(end_position.split(".")[0])
                while start_line != endLine:
                    editor.insert(f"{start_line}.0", "\t")
                    start_line += 1
            else:
                line = editor.index("insert").split(".")[0]
                editor.insert(f"{line}.0", "\t")

    def dedent(self, e=None) -> None:
        if not (editor := self.current_tab):
            return
        if selected := editor.tag_ranges("sel"):
            start_position, end_position = selected[0].string, selected[1].string
            start_line = int(start_position.split(".")[0])
            end_line = int(end_position.split(".")[0])
            while start_line != end_line:
                curr = editor.get(f"{start_line}.0", f"{start_line}.1")
                if curr == "\t":
                    editor.delete(f"{start_line}.0", f"{start_line}.1")
                start_line += 1
        else:
            line = editor.index("insert").split(".")[0]
            curr = editor.get(f"{line}.0", f"{line}.1")
            if curr == "\t":
                editor.delete(f"{line}.0", f"{line}.1")

    def escape_key_press(self, e=None) -> None:
        if hasattr(self, "intelliSenseBox") and self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
            self.intelli_sense_boxes[self.center_tabview.get()].place_forget()
        if hasattr(self, "snippetMenu") and self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
            self.snippet_menus[self.center_tabview.get()].place_forget()

    def previous_tab(self, e=None) -> None:
        tabs = list(self.center_tabview._tab_dict.keys())
        new_tab_index = self.center_tabview.index(self.center_tabview.get()) - 1
        if new_tab_index >= 0:
            new_tab_name = tabs[new_tab_index]
            self.center_tabview.set(new_tab_name)

    def next_tab(self, e=None) -> None:
        tabs = list(self.center_tabview._tab_dict.keys())
        new_tab_index = self.center_tabview.index(self.center_tabview.get()) + 1
        if new_tab_index < len(tabs):
            new_tab_name = tabs[new_tab_index]
            self.center_tabview.set(new_tab_name)

    def auto_single_quote(self, e=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", "'")
            editor.mark_set("insert", "insert -1c")

    def auto_double_quote(self, e=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", "\"")
            editor.mark_set("insert", "insert -1c")

    def auto_parenthesis(self, e=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", ")")
            editor.mark_set("insert", "insert -1c")

    def auto_bracket(self, e=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", "]")
            editor.mark_set("insert", "insert -1c")

    def auto_brace(self, e=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", "}")
            editor.mark_set("insert", "insert -1c")

    def close_file(self, e=None) -> None:
        self.save_file()
        tab_name = self.center_tabview.get()
        self.center_tabview.delete(tab_name)
        self.title("phIDE")

    def open_folder(self, e=None) -> None:
        directory_path = ctk.filedialog.askdirectory(title="Select a folder")
        if files := [
            os.path.join(root, file)
            for root, dirs, files in os.walk(directory_path)
            for file in files
        ]:
            for file in files:
                self.add_tab(file.replace("\\", "/"))

    def open_files(self, e=None) -> None:
        if file_paths := ctk.filedialog.askopenfilenames(
            title="Select a file",
            filetypes=[("Phi File", "*.phi"), ("All Files", "*.*")],
        ):
            for file in file_paths:
                self.add_tab(file)

    def backspace_entire_word(self, e=None) -> None:
        if editor := self.current_tab:
            current_index = editor.index("insert")
            word_start = editor.search(
                r"\s", current_index, backwards=True, regexp=True)
            editor.delete(word_start, current_index)

    def run(self, e=None) -> None:
        self.save_file()
        if self.current_language == ".phi":
            if self.current_path != "":
                with open(self.current_path, "r") as f:
                    source_code = "".join(f.readlines())
                start = time.time()
                self.console["state"] = "normal"
                error = shell.run(source_code, self.current_path)
                if error:
                    if editor := self.current_tab:
                        line = error.line
                        editor.tag_add("error", f"{line}.0", f"{line}.end")
                        text = editor.get(f"{line}.0", f"{line}.end")
                        print(text)
                        print(error)
                        self.error = error
                self.console["state"] = "disabled"
                end = time.time()
                print(f"\nProcess finished in {end - start} seconds.")
                print("-"*60)
        else:
            Dialog(self, "Error", "Run only supports .phi files",
                   self.center_x, self.center_y)

    def comment_line(self, e=None) -> None:
        if editor := self.current_tab:
            cursor_position = editor.index("insert")
            line_number = cursor_position.split(".")[0]
            start_position = f"{line_number}.0"
            end_position = f"{line_number}.2"
            commented = editor.get(start_position, end_position)
            if commented == "# ":
                editor.delete(start_position, end_position)
            else:
                editor.insert(start_position, "# ")
            editor.tag_remove("sel", "0.0", "end")

    def save_file(self, e=None) -> None:
        self.current_path = self.tab_names_paths[self.center_tabview.get()] or ctk.filedialog.asksaveasfilename(
                        title="Select a file", filetypes=[("Phi File", "*.phi"), ("All Files", "*.*")])

        if editor := self.current_tab:
            text = editor.get("0.0", "end")
            with open(self.current_path, "w") as f:
                f.write(text)
            name = self.center_tabview.get()
            self.title(name)
        self.saved = True

    def new_file(self, e=None) -> None:
        path = ctk.filedialog.asksaveasfilename(
            title="Select a file", filetypes=[("Phi File", "*.phi"), ("All Files", "*.*")])
        if os.path.exists(path):
            self.current_path = path
            with open(self.current_path, "w") as f:
                f.write("")
            self.add_tab(self.current_path)

    def copy(self, e=None) -> None:
        if editor := self.current_tab:
            self.clipboard = editor.selection_get()

    def paste(self, e=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", self.clipboard)

    def undo(self, e=None) -> None:
        if editor := self.current_tab:
            try:
                editor.edit_undo()
            except:
                pass

    def redo(self, e=None) -> None:
        if editor := self.current_tab:
            try:
                editor.edit_redo()
            except:
                pass

if __name__ == "__main__":
    app = App()