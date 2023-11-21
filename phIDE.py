import customtkinter as ctk
import sys
import re
from customtkinter import filedialog
from tkinter import colorchooser
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
        self.title('phIDE')
        self.state('zoomed')
        self.font = ctk.CTkFont(family='Courier New', size=16, weight='bold')
        self.screenRatio = 0.65
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.padx = 5
        self.pady = 5
        self.currentPath = ''
        self.currentLanguage = ''
        self.languageSyntaxPatterns = {
            'txt': r'',
            'phi': {
                'keyword':[
                    r'(?<!\w)(in|out|while|if|var|const|now|length|wait|root|fn)(?!\w)',
                    ['in', 'out', 'while', 'if', 'var', 'const', 'now', 'length', 'wait', 'root', 'fn']
                ],
                'symbols':[r'(==|<|>|!=|\+|-|\*|\/|%|^|\[|\]|\(|\)|\{|\})', []],
                'numbers':[r'\d+', []],
                'strings':[r'\"(.*?)\"', []],
                'comments':[r'#.*', []]
                }
        }
        self.editorTags = {
            'keyword': '#6666ff',
            'symbols': '#ffcc00',
            'numbers': '#ff1a75',
            'strings': '#00ff99',
            'comments': '#6b6b6b'
        }
        self.openEditors = {}
        self.tabNamesPaths = {}
        self.line = 1
        self.column = 1
        # Frames
        self.leftPanel = ctk.CTkFrame(self, width=200)
        self.rightPanel = ctk.CTkFrame(self, width=200)
        self.bottomPanel = ctk.CTkFrame(self)
        self.centerPanel = ctk.CTkFrame(self)
        self.findAndReplacePanel = ctk.CTkFrame(self.rightPanel)
        # Tabviews
        self.centerTabview = ctk.CTkTabview(self.centerPanel, self.width*self.screenRatio, height=self.height*self.screenRatio)
        self.bottomTabview = ctk.CTkTabview(self.bottomPanel, width=self.width*self.screenRatio)
        self.consoleTab = self.bottomTabview.add('Console')
        # Textboxes
        self.console = ctk.CTkTextbox(self.consoleTab, font=self.font)
        # Buttons
        self.clearConsoleButton = ctk.CTkButton(self.consoleTab, text='Clear', font=('courier', 12), command=self.clearConsole, width=50, height=15)
        self.findAndReplaceButton = ctk.CTkButton(self.findAndReplacePanel, text='Find & Replace', command=self.findAndReplace)
        # Labels
        self.statusbar = ctk.CTkLabel(self, text='', compound='left', height=20)
        # Entries
        self.find = ctk.CTkEntry(self.findAndReplacePanel, placeholder_text='Find')
        self.replace = ctk.CTkEntry(self.findAndReplacePanel, placeholder_text='Replace')
        # Other
        sys.stdin = TerminalRedirect(self.console)
        sys.stdout = TerminalRedirect(self.console)

        self.find.pack(padx=self.padx, pady=self.pady)
        self.replace.pack(padx=self.padx, pady=self.pady)
        self.findAndReplaceButton.pack(padx=self.padx, pady=self.pady)
        self.statusbar.pack(padx=self.padx, pady=self.pady, side=ctk.BOTTOM, anchor='se')
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
        self.bind('<KeyPress>', self.keyPressUpdate)
        self.bind('<Control-/>', self.SCCommentLine)
        self.bind('<Control-o>', self.SCOpenFile)
        self.bind('<Control-s>', self.SCSaveFile)
        self.bind('<Control-BackSpace>', self.SCBackspaceWord)
        self.bind('<(>', self.autoParenthesis)
        self.bind('<[>', self.autoBracket)
        self.bind('<{>', self.autoBrace)
        self.bind('<Control-space>', self.intelliSense)
        self.bind('<Control-n>', self.SCNewFile)
        self.bind('<Control-F4>', self.closeTab)
        self.bind('<Return>', self.enterInsertIntelliSense)
        self.bind('<Control-h>', self.toggleFindAndReplace)

        self.mainloop()

    def findAndReplace(self) -> None:
        find = self.find.get()
        replace = self.replace.get()
        editor = self.currentTab
        new = []
        if editor:
            text = editor.get('0.0', 'end').split('\n')
            for line in text:
                words = re.findall(r'\S+|\s', line)
                for word in words:
                    if word == find:
                        new.append(replace)
                    else:
                        new.append(word)
                new.append('\n')
        editor.delete('0.0', 'end')
        editor.insert('0.0', ''.join(new))

    def toggleFindAndReplace(self, e='') -> None:
        if self.findAndReplacePanel.winfo_ismapped():
            self.findAndReplacePanel.pack_forget()
        else:
            self.findAndReplacePanel.pack()

    def keyPressUpdate(self, e='') -> None:
        editor = self.currentTab
        if editor:
            self.line, self.column = editor.index('insert').split('.')
            self.statusbar.configure(text=f'Ln {self.line}, Col {self.column}')
        self.updateSyntax()
        self.intelliSense()

    def intelliSense (self, e='') -> None:
        editor = self.currentTab
        if editor:
            intelliSenseWords = self.languageSyntaxPatterns[self.currentLanguage]['keyword'][1]
            x, y, _, _ = editor.bbox(editor.index('insert'))
            self.intelliSenseBox.place(x=x, y=y+30)
            currentIndex = editor.index('insert')
            wordStart = editor.search(r'\s', currentIndex, backwards=True, regexp=True)
            word = editor.get(wordStart, currentIndex).strip(' \n')
            words = []
            for w in intelliSenseWords:
                if word in w:
                    words.append(w)
            self.intelliSenseBox.configure(values=words)
            
    def enterInsertIntelliSense(self, e='') -> None:
        if self.intelliSenseBox.winfo_ismapped():
            if len(self.intelliSenseBox._value_list) > 0:
                editor = self.currentTab
                if editor:
                    line, column = editor.index('insert').split('.')
                    editor.mark_set('insert', f'{int(line) - 1}.end')
                    editor.delete('insert', f'{line}.{column}')

                    word = self.intelliSenseBox._value_list[0]
                    currentIndex = editor.index('insert')
                    wordStart = editor.search(r'\s|^.', currentIndex, backwards=True, regexp=True)
                    column = editor.index('insert').split('.')[1]
                    if column == '1':
                        editor.delete(wordStart, currentIndex)
                    else:
                        editor.delete(wordStart + '+1c', currentIndex)
                    editor.insert('current', word)
                    editor.mark_set('insert', 'current')
                    self.intelliSenseBox.place_forget()
                    editor.focus_force()

    def insertIntelliSense(self, selected) -> None:
        editor = self.currentTab
        if editor:
            currentIndex = editor.index('insert')
            wordStart = editor.search(r'\s', currentIndex, backwards=True, regexp=True)
            editor.delete(wordStart, currentIndex)
            editor.insert('insert', selected)
            self.intelliSenseBox.place_forget()
            editor.focus_force()

    def autoParenthesis(self, e='') -> None:
        editor = self.currentTab
        if editor:
            editor.insert('insert', ')')
            editor.mark_set('insert', 'insert -1c')

    def autoBracket(self, e='') -> None:
        editor = self.currentTab
        if editor:
            editor.insert('insert', ']')
            editor.mark_set('insert', 'insert -1c')

    def autoBrace(self, e='') -> None:
        editor = self.currentTab
        if editor:
            editor.insert('insert', '}')
            editor.mark_set('insert', 'insert -1c')

    @property
    def currentTab(self) -> ctk.CTkTextbox:
        tabName = self.centerTabview.get()
        if tabName != '':
            return self.openEditors[tabName]
        
    def clearConsole(self) -> None:
        self.console.delete('0.0', 'end')

    def updateCurrentPath(self) -> None:
        self.currentPath = ...

    def updateSyntax(self) -> None:
        editor = self.currentTab
        if editor:
            for tag in self.editorTags:
                pattern = self.languageSyntaxPatterns[self.currentLanguage][tag][0]
                currLineEnd = editor.index('insert lineend')
                currLine = currLineEnd.split('.')[0]
                editor.tag_remove(tag, f'{currLine}.0', f'{currLine}.end')
                text = editor.get(f"{currLineEnd.split('.')[0]}.0", currLineEnd)
                matches = [(match.start(), match.end()) for match in re.finditer(pattern, text)]
                for start, end in matches:
                    editor.tag_add(tag, f'{currLine}.{start}', f'{currLine}.{end}')

    def addTab(self, path:str) -> None:
        self.currentPath = path
        self.currentLanguage = path.split('/')[-1].split('.')[-1]
        tabName = path.split('/')[-1]
        tab = self.centerTabview.add(tabName)
        editor = ctk.CTkTextbox(tab, font=self.font)
        editor.configure(tabs=40)
        for tag in self.editorTags:
            editor.tag_config(tag, foreground=self.editorTags[tag])
        editor.pack(expand=True, fill='both')
        self.intelliSenseBox = ctk.CTkSegmentedButton(editor, command=self.insertIntelliSense,width=100)

        length = 0
        with open(path, 'r') as f:
            for line in f.readlines():
                length += 1
                editor.insert('end', line)

        self.openEditors[tabName] = editor
        self.tabNamesPaths[tabName] = path
        self.updateSyntax()

    def closeTab(self, e='') -> None:
        self.SCSaveFile()
        tabName = self.centerTabview.get()
        self.centerTabview.delete(tabName)

    def SCOpenFile(self, e='') -> None:
        filePaths = filedialog.askopenfilenames(title='Select a file', filetypes=[('Phi File', '*.phi'), ('All Files', '*.*')])
        if filePaths:
            for file in filePaths:
                self.addTab(file)

    def SCBackspaceWord(self, e='') -> None:
        editor = self.currentTab
        if editor:
            currentIndex = editor.index('insert')
            wordStart = editor.search(r'\s', currentIndex, backwards=True, regexp=True)
            editor.delete(wordStart, currentIndex)

    def SCRun(self, e='') -> None:
        self.SCSaveFile()
        if self.currentPath != '':
            with open(self.currentPath, 'r') as f:
                sourceCode = ''.join(f.readlines())
            main.run(sourceCode)

    def SCCommentLine(self, e='') -> None:
        editor = self.currentTab
        cursor_position = editor.index('current')
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

    def SCNewFile(self, e='') -> None:
        self.currentPath = filedialog.asksaveasfilename(title='Select a file', filetypes=[('Phi File', '*.phi'), ('All Files', '*.*')])
        with open(self.currentPath, 'w') as f:
            f.write('')
        self.addTab(self.currentPath)

if __name__ == '__main__':
    app = App()

