from frontend.Error import Error
from TerminalRedirect import TerminalRedirect
from Dropdown import Dropdown
from Dialog import Dialog
import shell

import json
import sys, os
import re
import time
import customtkinter as ctk
import threading

# Checks if the settings file exists
if os.path.exists("settings.json"):
    with open("settings.json", "r") as f:
        settings = json.load(f)
else:
    sys.exit(0)

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
        self.help_window_font = ctk.CTkFont(
            family=settings["help_window-font-family"],
            size=settings["help_window-font-size"],
            weight=settings["help_window-font-weight"],
            slant=settings["help_window-font-slant"],
            overstrike=settings["help_window-font-overstrike"],
            underline=settings["help_window-font-underline"],
        )
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.screen_ratio = 0.65
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
        self.snippets = []
        self.tab_names_paths = {}
        self.cursors = []
        self.variables = []
        self.menu_open = False
        self.right_menu_open = False

        # Frames
        self.left_panel = ctk.CTkFrame(self, width=200)
        self.right_panel = ctk.CTkScrollableFrame(self)
        self.bottom_panel = ctk.CTkFrame(self)
        self.center_panel = ctk.CTkFrame(self)
        self.goto_panel = ctk.CTkFrame(self.right_panel)
        self.find_and_replace_panel = ctk.CTkFrame(self.right_panel)
        self.menu_bar = ctk.CTkFrame(self, height=20)
        self.available_modules_panel = ctk.CTkFrame(self.right_panel)
        # Tabviews
        self.center_tabview = ctk.CTkTabview(
            self.center_panel,
            int(self.width*self.screen_ratio),
            int(self.height*self.screen_ratio)
        )
        self.bottom_tabview = ctk.CTkTabview(
            self.bottom_panel,
            int(self.width*self.screen_ratio)
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

        self.pack()
        self.bind_keys()

        if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
            self.add_tab(os.path.basename(sys.argv[1]))

    def bind_keys(self) -> None:
        # Bindings
# Single Character Sequence
        self.bind("<F1>", self.show_help)
        self.bind("<F5>", self.run_file)
        self.bind("<Return>", self.enter_commands)
        self.bind("<Escape>", self.escape_key_press)
        self.bind("<(>", self.auto_parenthesis)
        self.bind("<[>", self.auto_bracket)
        self.bind("<{>", self.auto_brace)
        self.bind("<\">", self.auto_double_quote)
        self.bind("<'>", self.auto_single_quote)
        self.bind("<KeyPress>", self.key_press_update)
        self.bind("<Down>", self.down_key_press)
        self.bind("<Up>", self.up_key_press)

# Double Character Sequence
        self.bind("<Control-F4>", self.close_file)
        self.bind("<Control-BackSpace>", self.backspace_entire_word)
        self.bind("<Control-space>", self.show_intelli_sense)
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
        self.bind("<Control-m>", self.toggle_available_modules)
        self.bind("<Control-Home>", self.page_top)
        self.bind("<Control-End>", self.page_bottom)
# Triple Character Sequence
        self.bind("<Control-Shift-z>", self.redo)
        self.bind("<Control-Shift-Tab>", self.previous_tab)
# Mouse Click
        self.bind("<Button-1>", self.mouse_click_update)
        self.bind("<ButtonRelease-1>", self.highlight_selected)
        self.bind("<Button-3>", self.right_click_menu_click)

    def pack(self) -> None:
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

    def run(self) -> None:
        self.mainloop()

    @property
    def current_tab(self) -> ctk.CTkTextbox|None:
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
        _, self.current_language = os.path.splitext(path)
        self.current_language_combo.set(self.current_language)

        tab_name = os.path.basename(path)

        if tab_name not in self.center_tabview._tab_dict:
            self.add_new_tab(path, tab_name)
                
        else:
            error = Dialog(self, "Error", "Cannot open two files with the same name.",
                   self.center_x, self.center_y, self.editor_font)
            error.show()
            self.bell()

    def add_new_tab(self, path: str, tab_name: str):
        if self.current_language not in self.language_syntax_patterns:
            error = Dialog(self, "Error", "File extention not supported.",
                       self.center_x, self.center_y, self.editor_font)
            error.show()
            self.bell()
            return
        
        tab = self.center_tabview.add(tab_name)

        update_syntax_thread = threading.Thread(target=self.update_syntax)
        update_syntax_thread.daemon = True
        update_syntax_thread.start()

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
                editor, 300, 100, [], self.snippet_click_insert, 2, 2, settings["snippet-menu-color"], self.editor_font)
        editor.bind("<KeyPress>", self.editor_press)

        self.open_editors[tab_name] = editor
        self.tab_names_paths[tab_name] = path

        with open(path, "r") as f:
            for line in f.readlines():
                editor.insert("end", line)

        self.code = editor.get("0.0", "end")
        self.load_snippets()

# Updates
    def key_press_update(self, event=None) -> None:
        self.current_language = self.current_language_combo.get()

        if not (editor := self.current_tab):
            return
        
        self.line, self.column = editor.index("insert").split(".")
        self.status_bar.configure(text=f"Ln {self.line}, Col {self.column}")

        current_code = editor.get("0.0", "end")
        self.get_warnings(editor, current_code)

        if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
            self.show_intelli_sense()
        elif self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
            self.show_snippets()

    def get_warnings(self, editor : ctk.CTkTextbox, current_code: str):
        if self.current_language != ".phi":
            return
        
        self.warnings.configure(state="normal")
        self.warnings.delete("0.0", "end")

        parser_warnings = shell.incremental_parsing(current_code, self.current_path)

        if isinstance(parser_warnings, list) and len(parser_warnings) > 0:
            for warning in parser_warnings:
                warning: Error = warning
                line = warning.line

                editor.tag_add("warning", f"{line}.0", f"{line}.end")
                program_line = editor.get(f"{line}.0", f"{line}.end")
                self.warnings.insert("end", f"{program_line}\n{repr(warning)}\n")

            # Update warning tab's name to match total warnings
            new_name = f"Warnings({len(parser_warnings)})"
        else:
            editor.tag_remove("warning", "0.0", "end")
            new_name = "Warnings"

        self.warnings.configure(state="disabled")
        tabs = list(self.bottom_tabview._tab_dict.keys())
        current_name = tabs[1]

        if new_name not in self.bottom_tabview._tab_dict.keys():
            self.bottom_tabview.rename(current_name, new_name)

    def editor_press(self, _=None) -> None:
        if editor := self.current_tab:
            name = self.center_tabview.get()
            current_code = editor.get("0.0", "end")

            if current_code != self.code:
                self.code = current_code
                self.title(f"{name}*")
            else:
                self.title(name)

            self.variables = re.findall(r"\b[^\d\W]+\b", current_code)

            if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
                self.show_intelli_sense()

            editor.tag_remove("error", "0.0", "end")
            self.get_warnings(editor, current_code)

    def mouse_click_update(self, _=None) -> None:
        if editor := self.current_tab:
            editor.tag_remove("similar", "0.0", "end")

    def highlight_selected(self, _=None) -> None:
        if not (editor := self.current_tab):
            return
        
        if editor.tag_ranges("sel"):
            word = editor.get(ctk.SEL_FIRST, ctk.SEL_LAST)
            text = editor.get("0.0", "end").split("\n")
            pattern = f"({re.escape(word)})"

            for line_number, line in enumerate(text):
                matches = [(match.start(), match.end())
                           for match in re.finditer(pattern, line)]
                for start, end in matches:
                    editor.tag_add(
                        "similar", f"{line_number+1}.{start}", f"{line_number+1}.{end}")

    def enter_commands(self, _=None) -> None:
        self.intelli_sense_enter_insert()
        self.snippets_enter_insert()

# Snippets
    def snippets_enter_insert(self) -> None:
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
                self.snippet_menus[self.center_tabview.get()].place_forget()

    def snippet_click_insert(self, snippet_name: str) -> None:
        if not (editor := self.current_tab):
            return
        
        current_index = editor.index("insert -1l lineend")
        word_start = editor.search(
            r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", current_index, backwards=True, regexp=True)
        word = editor.get(word_start, current_index).strip(" \n\t\r({[]})")
        start_position = f"{current_index.split('.')[0]}.{int(current_index.split('.')[1]) - len(word)}"
        snippet = self.snippets_dictionary[snippet_name]
        editor.delete(start_position, "insert")
        editor.insert(start_position, snippet)
        self.snippet_menus[self.center_tabview.get()].place_forget()

    def show_snippets(self, _=None) -> None:
        if not (editor := self.current_tab) or not self.snippets:
            return

        self.snippet_menus[self.center_tabview.get()].place_forget()
        self.snippets = list(self.snippets_dictionary.keys())
        current_index = editor.index("insert")
        word_start = editor.search(
            r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", current_index, backwards=True, regexp=True)

        if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
            self.intelli_sense_boxes[self.center_tabview.get(
            )].place_forget()

        size = 4
        selected_snippet_index = self.snippet_menus[self.center_tabview.get()].current_selected_index
        word = editor.get(word_start, current_index).strip(" \n\t\r{[()]}")

        if word:
            self.snippets = [w for w in self.snippets if w.startswith(word)]

        start_index = max(0, selected_snippet_index)
        end_index = min(len(self.snippets), selected_snippet_index + size + 1)
        self.snippet_menus[self.center_tabview.get(
        )].items = self.snippets[start_index:end_index]
        x, y, _, _ = editor.bbox(editor.index("insert"))
        self.snippet_menus[self.center_tabview.get()].place(x=x, y=y+30)

    def load_snippets(self) -> None:
        path = f"snippets/{self.current_language[1:]}.json"

        if os.path.exists(path):
            with open(path, "r") as f:
                self.snippets_dictionary = json.load(f)
                self.snippets = list(self.snippets_dictionary.keys())
        else:
            error = Dialog(self, "Error", "Failed to load snippets.",
                   self.center_x, self.center_y, self.editor_font)
            error.show()
            self.bell()

# Syntax
    def load_language_syntax(self) -> None:
        path = f"Themes/{settings['theme']}/syntax.json"

        if os.path.exists(path):
            with open(path, "r") as f:
                self.language_syntax_patterns = json.load(f)
            self.current_language_combo.configure(
                values=self.language_syntax_patterns)
        else:
            error = Dialog(self, "Error", "Failed to open syntax file.",
                   self.center_x, self.center_y, self.editor_font)
            error.show()
            self.bell()

    def update_syntax(self) -> None:
        while True:
            if not (editor := self.current_tab):
                continue
            
            current_code = editor.get("0.0", "end")
            
            if self.code == current_code:
                continue

            self.code = current_code
            self.get_warnings(editor, current_code)

            for tag in self.language_syntax_patterns[self.current_language]:
                pattern = self.language_syntax_patterns[self.current_language][tag][1]
                editor.tag_remove(tag, "0.0", "end")

                first_visible_index = editor.index("@0, 0")
                last_visible_index = editor.index(f"@0, {str(editor.winfo_height())}")

                for line_number in range(int(first_visible_index.split(".")[0]), int(last_visible_index.split(".")[0]) + 1):
                    text = editor.get(f"{line_number}.0", f"{line_number}.end")
                    matches = [(match.start(), match.end())
                            for match in re.finditer(pattern, text, re.MULTILINE)]

                    for start, end in matches:
                        editor.tag_add(
                            tag, f"{line_number}.{start}", f"{line_number}.{end}")
            time.sleep(0.1)

# IntelliSense
    def up_key_press(self, _=None) -> None:
        if not (editor := self.current_tab):
            return

        if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
            # move the cursor back to previous position to reverse key press
            if int(editor.index("insert").split('.')[0]) != 1:
                editor.mark_set("insert", editor.index("insert +1l lineend"))

            selected_index = self.intelli_sense_boxes[self.center_tabview.get()].current_selected_index
            self.intelli_sense_boxes[self.center_tabview.get()].current_selected_index = (selected_index - 1) % len(self.intelli_sense_words)
            self.show_intelli_sense()

        elif self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
            # move the cursor back to previous position to reverse key press
            if int(editor.index("insert").split('.')[0]) != 1:
                editor.mark_set("insert", editor.index("insert +1l lineend"))

            selected_index = self.snippet_menus[self.center_tabview.get()].current_selected_index
            self.snippet_menus[self.center_tabview.get()].current_selected_index = (selected_index - 1) % len(self.snippets)
            self.show_snippets()

    def down_key_press(self, _=None) -> None:
        if not (editor := self.current_tab):
            return

        if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
            # move the cursor back to previous position to reverse key press
            if int(editor.index("insert").split('.')[0]) != len(self.code.split('\n')) - 1:
                editor.mark_set("insert", editor.index("insert -1l lineend"))

            selected_index = self.intelli_sense_boxes[self.center_tabview.get()].current_selected_index
            self.intelli_sense_boxes[self.center_tabview.get()].current_selected_index = (selected_index + 1) % len(self.intelli_sense_words)
            self.show_intelli_sense()

        elif self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
            # move the cursor back to previous position to reverse key press
            if int(editor.index("insert").split('.')[0]) != len(self.code.split('\n')) - 1:
                editor.mark_set("insert", editor.index("insert -1l lineend"))

            selected_index = self.snippet_menus[self.center_tabview.get()].current_selected_index
            self.snippet_menus[self.center_tabview.get()].current_selected_index = (selected_index + 1) % len(self.snippets)
            self.show_snippets()

    def show_intelli_sense(self, _=None) -> None:
        if not (editor := self.current_tab):
            return
        
        self.intelli_sense_boxes[self.center_tabview.get()].place_forget()
        self.intelli_sense_words = list(sorted(list(set(
            self.language_syntax_patterns[self.current_language]["keywords"][2] + self.variables + self.language_syntax_patterns[self.current_language]["errors"][2]))))
        current_index = editor.index("insert")
        word_start = editor.search(
            r"(\s|\.|,|\)|\(|\[|\]|\{|\}|\t)", current_index, backwards=True, regexp=True)
        word = editor.get(word_start, current_index).strip(" \n\t\r({[.]})")

        size = 4
        i = self.intelli_sense_boxes[self.center_tabview.get(
        )].current_selected_index
        end_index = start_index = max(0, i)

        if word:
            self.intelli_sense_words = [w for w in self.intelli_sense_words if w.startswith(word)]
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
        x, y, _, _ = editor.bbox(editor.index("insert"))
        self.intelli_sense_boxes[self.center_tabview.get()].place(x=x, y=y+30)

    def intelli_sense_enter_insert(self, _=None) -> None:
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
            self.intelli_sense_boxes[self.center_tabview.get()].place_forget()

# Menu Bar
    def right_click_menu_click(self, event) -> None:
        if self.right_menu_open:
            self.right_click_popup.place_forget()
            self.right_menu_open = False
        else:
            self.right_click_popup.place(x=event.x, y=event.y)
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
        self.file_menu_click()
        self.edit_menu_click()
        self.run_menu_click()
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
                self.run_file()

    # Tab switching

    def previous_tab(self, _=None) -> None:
        tabs = list(self.center_tabview._tab_dict.keys())
        if tabs:
            new_tab_index = (self.center_tabview.index(self.center_tabview.get()) - 1) % len(self.center_tabview._tab_dict)         # wrap the tab index
            new_tab_name = tabs[new_tab_index]
            self.center_tabview.set(new_tab_name)

    def next_tab(self, _=None) -> None:
        tabs = list(self.center_tabview._tab_dict.keys())
        if tabs:
            new_tab_index = (self.center_tabview.index(self.center_tabview.get()) + 1) % len(self.center_tabview._tab_dict)         # wrap the tab index
            new_tab_name = tabs[new_tab_index]
            self.center_tabview.set(new_tab_name)

    # automation
    def auto_single_quote(self, _=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", "'")
            editor.mark_set("insert", "insert -1c")

    def auto_double_quote(self, _=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", "\"")
            editor.mark_set("insert", "insert -1c")

    def auto_parenthesis(self, _=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", ")")
            editor.mark_set("insert", "insert -1c")

    def auto_bracket(self, _=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", "]")
            editor.mark_set("insert", "insert -1c")

    def auto_brace(self, _=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", "}")
            editor.mark_set("insert", "insert -1c")

    # Shortcuts
    def toggle_goto_menu(self, _=None) -> None:
        if self.goto_panel.winfo_ismapped():
            self.goto_panel.pack_forget()
        else:
            self.goto_panel.pack(padx=self.pad_x, pady=self.pad_y*5)
            self.goto_entry.focus_set()

    def goto_click(self) -> None:
        if editor := self.current_tab:
            line_number = int(self.goto_entry.get())
            editor.see(f"{line_number}.0")

    def toggle_find_and_replace(self, _=None) -> None:
        if self.find_and_replace_panel.winfo_ismapped():
            self.find_and_replace_panel.pack_forget()
        else:
            self.find_and_replace_panel.pack(padx=self.pad_x, pady=self.pad_y*5)
            self.find_entry.focus_set()

    def find_and_replace(self, _=None) -> None:
        if not (editor := self.current_tab):
            return
        
        editor.delete("1.0", "end")
        editor_text = editor.get("1.0", "end")
        find_text = self.find_entry.get()
        replace_with_text = self.replace_entry.get()
        updated_text = editor_text.replace(find_text, replace_with_text)
        editor.insert("1.0", updated_text)

    def escape_key_press(self, _=None) -> None:
        if self.current_tab:
            if self.intelli_sense_boxes[self.center_tabview.get()].winfo_ismapped():
                self.intelli_sense_boxes[self.center_tabview.get()].place_forget()

            elif self.snippet_menus[self.center_tabview.get()].winfo_ismapped():
                self.snippet_menus[self.center_tabview.get()].place_forget()

    def indent(self, _=None) -> None:
        if not (editor := self.current_tab):
            return
        
        # indent selected text
        if selected := editor.tag_ranges("sel"):
            start_position, end_position = selected[0].string, selected[1].string
            start_line = int(start_position.split(".")[0])
            endLine = int(end_position.split(".")[0])

            while start_line != endLine:
                editor.insert(f"{start_line}.0", "\t")
                start_line += 1
        # indent current line
        else:
            line = editor.index("insert").split(".")[0]
            editor.insert(f"{line}.0", "\t")

    def dedent(self, _=None) -> None:
        if not (editor := self.current_tab):
            return
        
        # dedent selected text
        if selected := editor.tag_ranges("sel"):
            start_position, end_position = selected[0].string, selected[1].string
            start_line = int(start_position.split(".")[0])
            end_line = int(end_position.split(".")[0])

            while start_line != end_line:
                curr = editor.get(f"{start_line}.0", f"{start_line}.1")

                if curr == "\t":
                    editor.delete(f"{start_line}.0", f"{start_line}.1")
                start_line += 1
        # dedent current line
        else:
            line = editor.index("insert").split(".")[0]
            curr = editor.get(f"{line}.0", f"{line}.1")

            if curr == "\t":
                editor.delete(f"{line}.0", f"{line}.1")

    def open_folder(self, _=None) -> None:
        directory_path = ctk.filedialog.askdirectory(title="Select a folder")
        if files := [
            os.path.join(root, file)
            for root, _, files in os.walk(directory_path)
            for file in files
        ]:
            for file in files:
                self.add_tab(file)

    def open_files(self, _=None) -> None:
        if file_paths := ctk.filedialog.askopenfilenames(
            title="Select a file",
            filetypes=[("Phi File", "*.phi"), ("All Files", "*.*")],
        ):
            for file in file_paths:
                self.add_tab(file)

    def page_top(self, _=None) -> None:
        """Scroll to the top of the text widget."""
        if editor := self.current_tab:
            editor.see("1.0")

    def page_bottom(self, _=None) -> None:
        """Scroll to the bottom of the text widget."""
        if editor := self.current_tab:
            editor.see("end")

    def toggle_available_modules(self, _=None) -> None:
        """Toggle the visibility of available modules."""

        available_modules = os.listdir("Modules")
        self.available_modules_textbox.configure(state="normal")
        self.available_modules_textbox.delete("1.0", "end")
        self.available_modules_textbox.insert("end", "\n".join(available_modules))
        self.available_modules_textbox.configure(state="disabled")

        if self.available_modules_panel.winfo_ismapped():
            self.available_modules_panel.pack_forget()
        else:
            self.available_modules_panel.pack(padx=self.pad_x, pady=self.pad_y*5)
            self.find_entry.focus_set()

    def show_help(self, _=None) -> None:
        text = """\
F1                  Show this menu
F5                  Run file
Enter               Select first intellisense word
Ctrl + Backspace    Deletes entire word
Ctrl + Space        Open intellisense
Ctrl + ;            Snippet menu
Ctrl + /            Comment  line
Ctrl + K            Open folder
Ctrl + O            Open file
Ctrl + S            Save file
Ctrl + N            Creates a new file
Ctrl + F4           Close file
Ctrl + C            Copy
Ctrl + V            Paste
Ctrl + Z            Undo
Ctrl + Shift + Z    Redo
Ctrl + H            Rind and replace menu
Ctrl + G            Go to menu
Ctrl + M            Available module menu
Ctrl + [            Dedent line
Ctrl + ]            Indent line
Ctrl + Tab          Next tab
Ctrl + Shift + Tab  Previous Tab
Ctrl + Left Click   Add/remove cursor
Middle Click        Add/remove cursor
Esc                 Hide intelliSense
        """
        
        help_dialog = Dialog(self, "Help", text, self.center_x, self.center_y, self.help_window_font)
        help_dialog.show()

    def copy(self, _=None) -> None:
        if editor := self.current_tab:
            self.clipboard = editor.selection_get()

    def paste(self, _=None) -> None:
        if editor := self.current_tab:
            editor.insert("insert", self.clipboard)

    def undo(self, _=None) -> None:
        if editor := self.current_tab:
            try:
                editor.edit_undo()
            except:
                self.bell()

    def redo(self, _=None) -> None:
        if editor := self.current_tab:
            try:
                editor.edit_redo()
            except:
                self.bell()

    def comment_line(self, _=None) -> None:
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

    def backspace_entire_word(self, _=None) -> None:
        if editor := self.current_tab:
            current_index = editor.index("insert")
            word_start = editor.search(
                r"\s", current_index, backwards=True, regexp=True)
            editor.delete(word_start, current_index)

    def close_file(self, _=None) -> None:
        self.save_file()
        tab_name = self.center_tabview.get()
        self.center_tabview.delete(tab_name)
        self.title("phIDE")

        if settings["auto-clear-console-on-close"]:
            self.clear_console()

    def run_file(self, _=None) -> None:
        if editor := self.current_tab:
            self.save_file()

            if self.current_language == ".phi":
                if self.current_path != "":

                    with open(self.current_path, "r") as f:
                        source_code = ''.join(f.readlines())

                    self.console["state"] = "normal"
                    error = shell.run(source_code, self.current_path)

                    if error:
                        line = error.line
                        editor.tag_add("error", f"{line}.0", f"{line}.end")
                        text = editor.get(f"{line}.0", f"{line}.end")
                        print(text)
                        print(error)
                        self.error = str(error)

                    self.console["state"] = "disabled"
            else:
                error = Dialog(self, "Error", "Run only supports .phi files",
                    self.center_x, self.center_y, self.editor_font)
                error.show()
                self.bell()

    def save_file(self, _=None) -> None:
        self.current_path = self.tab_names_paths[self.center_tabview.get()] or ctk.filedialog.asksaveasfilename(
                        title="Save", filetypes=[("Phi File", "*.phi"), ("All Files", "*.*")])

        if editor := self.current_tab:
            text = editor.get("0.0", "end")

            with open(self.current_path, "w") as f:
                f.write(text)

            name = self.center_tabview.get()
            self.title(name)

    def new_file(self, _=None) -> None:
        path = ctk.filedialog.asksaveasfilename(
            title="Save As", filetypes=[("Phi File", "*.phi"), ("All Files", "*.*")])
        
        self.current_path = path
        with open(self.current_path, "w") as f:
            f.write("")

        self.add_tab(self.current_path)


if __name__ == "__main__":
    app = App()
    app.run()