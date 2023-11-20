import customtkinter as ctk
import sys
import re
from customtkinter import filedialog
import main

class TerminalRedirect:
    def __init__(self, textWidget:ctk.CTkTextbox) -> None:
        self.widget = textWidget

    def write(self, message) -> None:
        self.widget.insert('end', message)
        self.widget.yview_moveto(1)

    def readline(self, prompt="") -> str:
        self.widget.insert('end', prompt)
        self.widget.mark_set("input_start", "end-1c")
        self.widget.mark_set("input_end", "end-1c + 1l")
        line = self.widget.get("input_start", "input_end")
        self.widget.delete("input_start", "input_end")
        return line

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title = 'phIDE'
        self.state('zoomed')
        self.font = ctk.CTkFont(family='Courier New', size=16)
        self.screenRatio = 0.8
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.padx = 5
        self.pady = 5
        self.currentPath = ''
        self.currentLanguage = ''
        self.languageSyntaxPatterns = {
            'txt': r'',
            'phi': r'(in|out|while|if|var|const|now|length|wait|root|fn)' # (in|out|while|if|var|const|now|length|wait|root|fn)|\d+|\"(.*?)\"|(==|<|>|!=|\+|-|\*|\/|%|^)
        }
        self.editorTags = {
            'keyword': '#38ff3f',
            'symbols': '#00ffff',
            'numbers': '#123456',
            'strings': '#ff00ff'
        }
        self.openEditors = {}
        # Frames
        self.leftPanel = ctk.CTkFrame(self, width=200)
        self.rightPanel = ctk.CTkFrame(self, width=200)
        self.bottomPanel = ctk.CTkFrame(self)
        self.centerPanel = ctk.CTkFrame(self)
        # Tabviews
        self.centerTabview = ctk.CTkTabview(self.centerPanel, self.width*self.screenRatio, height=self.height*self.screenRatio)
        self.bottomTabview = ctk.CTkTabview(self.bottomPanel, width=self.width*self.screenRatio)
        self.consoleTab = self.bottomTabview.add('Console')
        # Textboxes
        self.console = ctk.CTkTextbox(self.consoleTab, font=self.font)
        # Buttons
        self.clearConsoleButton = ctk.CTkButton(self.consoleTab, text='Clear', font=('courier', 12), command=self.clearConsole, width=50, height=15)
        # Other
        sys.stdin = TerminalRedirect(self.console)
        sys.stdout = TerminalRedirect(self.console)

        self.clearConsoleButton.pack(padx=self.padx, pady=self.pady, side=ctk.RIGHT, anchor='n')
        self.console.pack(padx=self.padx, pady=self.pady, fill='both')
        self.rightPanel.pack(padx=self.padx, pady=self.pady, fill='y', expand=True, side=ctk.RIGHT, anchor='e')
        self.leftPanel.pack(padx=self.padx, pady=self.pady, fill='y', expand=True, side=ctk.LEFT, anchor='w')
        self.centerPanel.pack(padx=self.padx, pady=self.pady, fill='both', expand=True)
        self.bottomPanel.pack(padx=self.padx, pady=self.pady, fill='both', expand=True, anchor='s')
        self.centerTabview.pack(padx=self.padx, pady=self.pady, expand=True, fill='both')
        self.bottomTabview.pack(padx=self.padx, pady=self.pady, expand=True, fill='both')
        # Bindings
        self.bind('<F5>', self.SCRun)
        self.bind('<KeyPress>', self.updateSyntax)
        self.bind('<Control-/>', self.SCCommentLine)
        self.bind('<Control-o>', self.SCOpenFile)
        self.bind('<Control-s>', self.SCSaveFile)

        self.mainloop()

    @property
    def currentTab(self) -> ctk.CTkTextbox:
        tabName = self.centerTabview.get()
        if tabName != '':
            return self.openEditors[tabName]
        
    def clearConsole(self) -> None:
        self.console.delete('0.0', 'end')

    def updateCurrentPath(self) -> None:
        self.currentPath = ...

    def updateSyntax(self, e='') -> None:
        editor = self.currentTab
        ypos = editor.yview()[0]
        cursorPos = editor.index(ctk.INSERT)
        text = editor.get('0.0', 'end')
        matches = [(match.start(), match.end()) for match in re.finditer(self.languageSyntaxPatterns[self.currentLanguage], text)]
        editor.delete("1.0", 'end')

        prev_end = 0
        for start, end in matches:
            unmatched_text_before = text[prev_end:start]
            editor.insert('end', unmatched_text_before)
            matched_text = text[start:end]
            editor.insert('end', matched_text, 'keyword')
            prev_end = end
        unmatched_text_after = text[prev_end:]
        editor.insert('end', unmatched_text_after[:-1])
        editor.yview_moveto(ypos)
        editor.mark_set(ctk.INSERT, cursorPos)

    def addTab(self, path:str) -> None:
        self.currentLanguage = path.split('/')[-1].split('.')[-1]
        tabName = path.split('/')[-1]
        tab = self.centerTabview.add(tabName)
        editor = ctk.CTkTextbox(tab, font=self.font)
        for tag in self.editorTags:
            editor.tag_config(tag, foreground=self.editorTags[tag])
        editor.pack(expand=True, fill='both')

        with open(path, 'r') as f:
            for line in f.readlines():
                editor.insert('end', line)

        self.openEditors[tabName] = editor
        self.updateSyntax()

    def SCOpenFile(self, e='') -> None:
        filePath = filedialog.askopenfilename(title='Select a file', filetypes=[('Phi File', '*.phi'), ('All Files', '*.*')])
        if filePath:
            self.addTab(filePath)

    def SCRun(self, e='') -> None:
        self.SCSaveFile()
        self.updateCurrentPath()
        if self.currentPath != '':
            with open(self.currentPath, 'r') as f:
                sourceCode = ''.join(f.readlines())
            main.run(sourceCode)

    def SCCommentLine(self, e='') -> None:
        editor = self.currentTab
        cursor_position = editor.index(ctk.CURRENT)
        line_number = cursor_position.split('.')[0]
        start_position = f"{line_number}.0"
        editor.insert(start_position, '# ')

    def SCSaveFile(self, e='') -> None:
        if not self.currentPath:
            self.currentPath = filedialog.asksaveasfilename(title='Select a file', filetypes=[('Phi File', '*.phi'), ('All Files', '*.*')])

        editor = self.currentTab
        text = editor.get('0.0', 'end')
        with open(self.currentPath, 'w') as f:
            f.write(text)

if __name__ == '__main__':
    app = App()

