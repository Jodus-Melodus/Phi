import json
import customtkinter as ctk
import sys
import re
from customtkinter import filedialog
import main, time

class TerminalRedirect:
    def __init__(self, textWidget:ctk.CTkTextbox) -> None:
        self.widget = textWidget

    def write(self, message) -> None:
        self.widget.configure(state='normal')
        self.widget.insert('end', message)
        self.widget.yview_moveto(1)
        self.widget.configure(state='disabled')

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
        self.textBoxFont = ctk.CTkFont(family='Courier New', size=16, weight='bold')
        self.buttonFont = ctk.CTkFont(family='Fira Code', size=12, weight='normal')
        self.screenRatio = 0.65
        self.width = self.winfo_width()
        self.height = self.winfo_height()
        self.padx = 5
        self.pady = 5
        self.currentPath = ''
        self.currentLanguage = ''
        self.openEditors = {}
        self.tabNamesPaths = {}
        self.line = 1
        self.column = 1
        self.clipboard = ''
        self.menuOpen = False
        self.rightMenuOpen = False
        self.loadLanguageSyntax()
        # Frames
        self.leftPanel = ctk.CTkFrame(self, width=200)
        self.rightPanel = ctk.CTkFrame(self, width=200)
        self.bottomPanel = ctk.CTkFrame(self)
        self.centerPanel = ctk.CTkFrame(self)
        self.findAndReplacePanel = ctk.CTkFrame(self.rightPanel)
        self.menuBar = ctk.CTkFrame(self, height=20)
        # Tabviews
        self.centerTabview = ctk.CTkTabview(self.centerPanel, self.width*self.screenRatio, height=self.height*self.screenRatio)
        self.bottomTabview = ctk.CTkTabview(self.bottomPanel, width=self.width*self.screenRatio)
        self.consoleTab = self.bottomTabview.add('Console')
        # Textboxes
        self.console = ctk.CTkTextbox(self.consoleTab, font=self.textBoxFont, state='disabled')
        # Buttons
        self.clearConsoleButton = ctk.CTkButton(self.consoleTab, text='Clear', command=self.clearConsole, width=50, height=20, font=self.buttonFont)
        self.findAndReplaceButton = ctk.CTkButton(self.findAndReplacePanel, command=self.findAndReplace, text='Find & Replace', font=self.buttonFont)
        # Menu Buttons & Popups
        self.fileMenu = ctk.CTkButton(self.menuBar, text='File', height=20, width=50, command=self.fileMenuClick, font=self.buttonFont)
        self.editMenu = ctk.CTkButton(self.menuBar, text='Edit', height=20, width=50, command=self.editMenuClick, font=self.buttonFont)
        self.runMenu = ctk.CTkButton(self.menuBar, text='Run', height=20, width=50, command=self.runMenuClick, font=self.buttonFont)
        self.fileMenuPopup = ctk.CTkSegmentedButton(self, values=['New File', 'Open File', 'Save File', 'Close File'], command=self.handleShortCuts, height=20, font=self.buttonFont)
        self.editMenuPopup = ctk.CTkSegmentedButton(self, values=['Undo', 'Redo', 'Copy', 'Paste', 'Replace', 'Comment'], command=self.handleShortCuts, height=20, font=self.buttonFont)
        self.runMenuPopup = ctk.CTkSegmentedButton(self, values=['Run'], command=self.handleShortCuts, height=20, font=self.buttonFont)
        self.rightClickPopup = ctk.CTkSegmentedButton(self, values=['New File', 'Open File', 'Save File', 'Close File', 'Run', 'Undo', 'Redo', 'Copy', 'Paste', 'Replace', 'Comment'], command=self.handleShortCuts, height=20, font=self.buttonFont)
        # Labels
        self.statusbar = ctk.CTkLabel(self, text='', height=20, font=self.buttonFont)
        # Entries
        self.find = ctk.CTkEntry(self.findAndReplacePanel, placeholder_text='Find', font=self.buttonFont)
        self.replace = ctk.CTkEntry(self.findAndReplacePanel, placeholder_text='Replace', font=self.buttonFont)
        # ComboBox
        self.currentLanguageCombo = ctk.CTkOptionMenu(self.menuBar, height=20, values=[x for x in self.languageSyntaxPatterns], font=self.buttonFont)
        # Other
        sys.stdin = TerminalRedirect(self.console)
        sys.stdout = TerminalRedirect(self.console)
        sys.stderr = TerminalRedirect(self.console)

        self.menuBar.pack(padx=self.padx, pady=self.pady, anchor='w')
        self.currentLanguageCombo.pack(padx=self.padx, pady=self.pady, expand=True, anchor='e', side='right')
        self.fileMenu.pack(padx=self.padx, pady=self.pady, expand=True, anchor='w', side='left')
        self.editMenu.pack(padx=self.padx, pady=self.pady, expand=True, anchor='w', side='left')
        self.runMenu.pack(padx=self.padx, pady=self.pady, expand=True, anchor='w', side='left')
        self.find.pack(padx=self.padx, pady=self.pady, side='top', expand=True)
        self.replace.pack(padx=self.padx, pady=self.pady, expand=True)
        self.findAndReplaceButton.pack(padx=self.padx, pady=self.pady, side='bottom')
        self.statusbar.pack(padx=self.padx, pady=self.pady, side=ctk.BOTTOM, anchor='se', expand=True)
        self.clearConsoleButton.pack(padx=self.padx, pady=self.pady, side=ctk.RIGHT, anchor='n')
        self.console.pack(padx=self.padx, pady=self.pady, fill='both', expand=True)
        self.rightPanel.pack(padx=self.padx, pady=self.pady, fill='both', expand=True, side=ctk.RIGHT, anchor='e')
        self.leftPanel.pack(padx=self.padx, pady=self.pady, fill='both', expand=True, side=ctk.LEFT, anchor='w')
        self.centerPanel.pack(padx=self.padx, pady=self.pady, fill='both', expand=True)
        self.bottomPanel.pack(padx=self.padx, pady=self.pady, fill='both', expand=True, anchor='s')
        self.centerTabview.pack(padx=self.padx, pady=self.pady, expand=True, fill='both')
        self.bottomTabview.pack(padx=self.padx, pady=self.pady, expand=True, fill='both')
        # Bindings
        self.bind('<F5>', self.SCRun)
        self.bind('<KeyPress>', self.keyPressUpdate)
        self.bind('<Return>', self.enterCommands)
        self.bind('<Control-BackSpace>', self.SCBackspaceWord)
        self.bind('<Control-space>', self.intelliSense)
        self.bind('<Control-/>', self.SCCommentLine)
        self.bind('<Control-o>', self.SCOpenFile)
        self.bind('<Control-s>', self.SCSaveFile)
        self.bind('<Control-n>', self.SCNewFile)
        self.bind('<Control-F4>', self.SCCloseFile)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-v>', self.paste)
        self.bind('<Control-z>', self.undo)
        self.bind('<Control-Shift-z>', self.redo)
        self.bind('<Control-h>', self.toggleFindAndReplace)
        self.bind('<(>', self.autoParenthesis)
        self.bind('<[>', self.autoBracket)
        self.bind('<{>', self.autoBrace)
        self.bind('<Button-3>', self.rightClickMenuClick)
        self.bind('<F1>', self.showHelp)
        self.bind('<Control-;>', self.showSnippets)
        self.bind('<Control-[>', self.dedent)
        self.bind('<Control-]>', self.indent)
        self.bind('<ButtonRelease-1>', self.highlightSelected)
        self.bind('<Button-1>', self.mouseClickUpdate)

        self.mainloop()

    def mouseClickUpdate(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            editor.tag_remove('similar', '0.0', 'end')

    def highlightSelected(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            text = editor.get('0.0', 'end').split('\n')
            if editor.tag_ranges('sel'):
                word = editor.get(ctk.SEL_FIRST, ctk.SEL_LAST)
                for ln, line in enumerate(text):
                    matches = [(match.start(), match.end()) for match in re.finditer(word, line)]
                    for start, end in matches:
                        editor.tag_add('similar', f'{ln}.{start}', f'{ln}.{end}')
                        editor.tag_remove('error', f'{ln}.0', f'{ln}.end')

    def indent(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            selected = editor.tag_ranges('sel')
            if selected:
                startPosition, endPosition = selected[0].string, selected[1].string
                startLine = int(startPosition.split('.')[0])
                endLine = int(endPosition.split('.')[0])
                while startLine != endLine:
                    editor.insert(f'{startLine}.0', '\t')
                    startLine += 1
            else:
                line = editor.index('insert').split('.')[0]
                editor.insert(f'{line}.0', '\t')

    def dedent(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            selected = editor.tag_ranges('sel')
            if selected:
                startPosition, endPosition = selected[0].string, selected[1].string
                startLine = int(startPosition.split('.')[0])
                endLine = int(endPosition.split('.')[0])
                while startLine != endLine:
                    curr = editor.get(str(startLine)+'.0', str(startLine)+'.1')
                    if curr == '\t':
                        editor.delete(str(startLine) + '.0', str(startLine)+'.1')
                    startLine += 1
            else:
                line = editor.index('insert').split('.')[0]
                curr = editor.get(line+'.0', line+'.1')
                if curr == '\t':
                    editor.delete(line + '.0', line+'.1')

    def enterCommands(self, e=None) -> None:
        self.enterInsertIntelliSense()
        self.enterSnippets()

    def enterSnippets(self) -> None:
        if self.snippetMenu.winfo_ismapped():
            if len(self.snippetMenu._value_list) > 0:
                editor = self.currentTab
                if editor:
                    line, column = editor.index('insert').split('.')
                    editor.mark_set('insert', f'{int(line) - 1}.end')
                    editor.delete('insert', f'{line}.{column}')

                    snippetName = self.snippetMenu._value_list[0]
                    currentIndex = editor.index('insert')
                    wordStart = editor.search(r'\s|^.', currentIndex, backwards=True, regexp=True)
                    column = editor.index('insert').split('.')[1]
                    editor.delete(wordStart, currentIndex)
                    editor.insert('current', self.snippets[snippetName])
                    editor.mark_set('insert', 'current')
                    self.snippetMenu.place_forget()
                    self.updateSyntax()
                    editor.focus_force()
                    self.updateSyntax()

    def insertSnippet(self, snippetName:str) -> None:
        editor = self.currentTab
        if editor:
            currentIndex = editor.index('insert')
            wordStart = editor.search(r'\s', currentIndex, backwards=True, regexp=True)
            editor.delete(wordStart, currentIndex)
            editor.insert('insert', self.snippets[snippetName])
            self.snippetMenu.place_forget()
            editor.focus_force()
            self.updateSyntax()

    def showSnippets(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            self.snippetMenu.place_forget()
            x, y, _, _ = editor.bbox(editor.index('insert'))
            currentIndex = editor.index('insert')
            wordStart = editor.search(r'\s', currentIndex, backwards=True, regexp=True)
            word = editor.get(wordStart, currentIndex).strip(' \n')
            if word:
                words = []
                for w in self.snippets:
                    if w.startswith(word):
                        words.append(w)
                if len(words) > 0:
                    if self.intelliSenseBox.winfo_ismapped():
                        self.intelliSenseBox.place_forget()
                    self.snippetMenu.place(x=x, y=y+30)
                    self.snippetMenu.configure(values=words)

    def loadSnippets(self) -> None:
        with open(f'snippets/{self.currentLanguage[1:]}.json') as f:
            self.snippets = json.load(f)

    def showHelp(self, e=None) -> None:
        helpWindow = ctk.CTkToplevel()
        helpWindow.title('phIDE - Help')
        helpText = ctk.CTkTextbox(helpWindow, font=self.textBoxFont)
        helpText.pack(expand=True, fill='both')
        text = """        F1 -                Show this menu
        F5 -                Run current file
        Enter -             Select first intellisense word
        Ctrl + Backspace -  Deletes entire word
        Ctrl + Space -      Manually open intellisense
        Ctrl + ; -          Show Snippet menu
        Ctrl + / -          Comment current line
        Ctrl + O -          Open file
        Ctrl + S -          Save current file
        Ctrl + N -          Creates a new file
        Ctrl + F4 -         Close current tab
        Ctrl + C -          Copy selected text
        Ctrl + V -          Paste last copied word
        Ctrl + Z -          Undo action
        Ctrl + Shift + Z -  Redo action
        Ctrl + H -          Open and closes find and replace panel
        Ctrl + [ -          Dedent line or selected text
        Ctrl + ] -          Indent line or selected text"""
        helpText.insert('0.0', text)
        helpText.configure(wrap='none', state='disabled')

    def loadLanguageSyntax(self) -> None:
        with open('syntax.json', 'r') as f:
            self.languageSyntaxPatterns = json.load(f)

    def rightClickMenuClick(self, e=None) -> None:
        self.rightClickPopup.set('')
        if self.rightMenuOpen:
            self.rightClickPopup.place_forget()
            self.rightMenuOpen = False
        else:
            self.rightClickPopup.place(x=e.x, y=e.y)
            self.rightMenuOpen = True

    def fileMenuClick(self) -> None:
        self.fileMenuPopup.set('')
        if self.menuOpen:
            self.fileMenuPopup.place_forget()
            self.editMenuPopup.place_forget()
            self.runMenuPopup.place_forget()
            self.menuOpen = False
        else:
            self.fileMenuPopup.place(x=self.fileMenu.winfo_x()+5, y=self.fileMenu.winfo_y()+30)
            self.menuOpen = True
    
    def editMenuClick(self) -> None:
        self.editMenuPopup.set('')
        if self.menuOpen:
            self.fileMenuPopup.place_forget()
            self.editMenuPopup.place_forget()
            self.runMenuPopup.place_forget()
            self.menuOpen = False
        else:
            self.editMenuPopup.place(x=self.editMenu.winfo_x()+5, y=self.editMenu.winfo_y()+30)
            self.menuOpen = True
    
    def runMenuClick(self) -> None:
        self.runMenuPopup.set('')
        if self.menuOpen:
            self.fileMenuPopup.place_forget()
            self.editMenuPopup.place_forget()
            self.runMenuPopup.place_forget()
            self.menuOpen = False
        else:
            self.runMenuPopup.place(x=self.runMenu.winfo_x()+5, y=self.runMenu.winfo_y()+30)
            self.menuOpen = True

    def handleShortCuts(self, name:str) -> None:
        self.fileMenuPopup.place_forget()
        self.editMenuPopup.place_forget()
        self.runMenuPopup.place_forget()
        self.rightClickPopup.place_forget()
        match name:
            case 'New File':
                self.SCNewFile()
            case 'Open File':
                self.SCOpenFile()
            case 'Save File':
                self.SCSaveFile()
            case 'Close File':
                self.SCCloseFile()
            case 'Undo':
                self.undo()
            case 'Redo':
                self.redo()
            case 'Copy':
                self.copy()
            case 'Paste':
                self.paste()
            case 'Replace':
                self.toggleFindAndReplace()
            case 'Comment':
                self.SCCommentLine()
            case 'Run':
                self.SCRun()

    def copy(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            self.clipboard = editor.selection_get()

    def paste(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            editor.insert('insert', self.clipboard)

    def undo(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            editor.event_generate('<<Undo>>')
    
    def redo(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            editor.event_generate('<<Redo>>')

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
                    w = word
                    if find in word:
                        new.append(w.replace(find, replace))
                    else:
                        new.append(word)
                new.append('\n')
            editor.delete('0.0', 'end')
            editor.insert('0.0', ''.join(new))

    def toggleFindAndReplace(self, e=None) -> None:
        if self.findAndReplacePanel.winfo_ismapped():
            self.findAndReplacePanel.pack_forget()
            editor = self.currentTab
            if editor:
                editor.focus_set()
        else:
            self.findAndReplacePanel.pack()
            self.find.focus_set()

    def keyPressUpdate(self, e=None) -> None:
        self.currentLanguage = self.currentLanguageCombo.get()
        editor = self.currentTab
        if editor:
            self.line, self.column = editor.index('insert').split('.')
            self.statusbar.configure(text=f'Ln {self.line}, Col {self.column}')
        self.updateSyntax()
        self.intelliSense()


    def intelliSense(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            self.intelliSenseBox.place_forget()
            intelliSenseWords = self.languageSyntaxPatterns[self.currentLanguage]['keywords'][2]
            x, y, _, _ = editor.bbox(editor.index('insert'))
            currentIndex = editor.index('insert')
            wordStart = editor.search(r'\s', currentIndex, backwards=True, regexp=True)
            word = editor.get(wordStart, currentIndex).strip(' \n')
            if word:
                words = []
                for w in intelliSenseWords:
                    if w.startswith(word):
                        words.append(w)
                if len(words) > 0:
                    if self.snippetMenu.winfo_ismapped():
                        self.snippetMenu.place_forget()
                    self.intelliSenseBox.place(x=x, y=y+30)
                    self.intelliSenseBox.configure(values=words)
            
    def enterInsertIntelliSense(self, e=None) -> None:
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
                    editor.delete(wordStart, currentIndex)
                    editor.insert('current', word)
                    editor.mark_set('insert', 'current')
                    self.intelliSenseBox.place_forget()
                    self.updateSyntax()
                    editor.focus_force()
                    self.updateSyntax()

    def insertIntelliSense(self, selected) -> None:
        editor = self.currentTab
        if editor:
            currentIndex = editor.index('insert')
            wordStart = editor.search(r'\s', currentIndex, backwards=True, regexp=True)
            editor.delete(wordStart, currentIndex)
            editor.insert('insert', selected)
            self.intelliSenseBox.place_forget()
            editor.focus_force()
            self.updateSyntax()

    def autoParenthesis(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            editor.insert('insert', ')')
            editor.mark_set('insert', 'insert -1c')

    def autoBracket(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            editor.insert('insert', ']')
            editor.mark_set('insert', 'insert -1c')

    def autoBrace(self, e=None) -> None:
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
        self.console.configure(state='normal')
        self.console.delete('0.0', 'end')
        self.console.configure(state='disabled')

    def updateSyntax(self, line:str=None, lnIndex:int=None) -> None:
        editor = self.currentTab
        if editor:
            for tag in self.languageSyntaxPatterns[self.currentLanguage]:
                pattern = self.languageSyntaxPatterns[self.currentLanguage][tag][1]
                if not line:
                    currLineEnd = editor.index('insert lineend')
                    currLine = currLineEnd.split('.')[0]
                    editor.tag_remove(tag, f'{currLine}.0', f'{currLine}.end')
                    text = editor.get(f"{currLineEnd.split('.')[0]}.0", currLineEnd)
                else:
                    text = line
                    currLine = lnIndex
                matches = [(match.start(), match.end()) for match in re.finditer(pattern, text)]
                for start, end in matches:
                    editor.tag_add(tag, f'{currLine}.{start}', f'{currLine}.{end}')
                    editor.tag_remove('error', f'{currLine}.0', f'{currLine}.end')

    def addTab(self, path:str) -> None:
        self.currentPath = path
        self.currentLanguage = '.' + path.split('/')[-1].split('.')[-1]
        self.currentLanguageCombo.set(self.currentLanguage)
        tabName = path.split('/')[-1]
        tab = self.centerTabview.add(tabName)
        editor = ctk.CTkTextbox(tab, font=self.textBoxFont)
        editor.configure(tabs=40)
        
        for tag in self.languageSyntaxPatterns[self.currentLanguage]:
            editor.tag_config(tag, foreground=self.languageSyntaxPatterns[self.currentLanguage][tag][0])
        editor.tag_config('error', background='#990000')
        editor.tag_config('similar', background='#0000ff')

        editor.configure(wrap='none')
        editor.pack(expand=True, fill='both')
        self.intelliSenseBox = ctk.CTkSegmentedButton(editor, command=self.insertIntelliSense, width=100, bg_color='#9908aa')
        self.snippetMenu = ctk.CTkSegmentedButton(editor, command=self.insertSnippet, width=20, bg_color='#3366ff')

        self.openEditors[tabName] = editor
        self.tabNamesPaths[tabName] = path
        length = 0
        with open(path, 'r') as f:
            for line in f.readlines():
                length += 1
                editor.insert('end', line)
                self.updateSyntax(line, length)
        self.loadSnippets()

    def SCCloseFile(self, e=None) -> None:
        self.SCSaveFile()
        tabName = self.centerTabview.get()
        self.centerTabview.delete(tabName)

    def SCOpenFile(self, e=None) -> None:
        filePaths = filedialog.askopenfilenames(title='Select a file', filetypes=[('Phi File', '*.phi'), ('All Files', '*.*')])
        if filePaths:
            for file in filePaths:
                self.addTab(file)

    def SCBackspaceWord(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            currentIndex = editor.index('insert')
            wordStart = editor.search(r'\s', currentIndex, backwards=True, regexp=True)
            editor.delete(wordStart, currentIndex)

    def SCRun(self, e=None) -> None:
        self.SCSaveFile()
        if self.currentPath != '':
            with open(self.currentPath, 'r') as f:
                sourceCode = ''.join(f.readlines())
            start = time.time()
            self.console['state'] = 'normal'
            error = main.run(sourceCode)
            if error:
                editor = self.currentTab
                if editor:
                    line = error.line
                    editor.tag_add('error', f'{line}.0', f'{line}.end')
                    text = editor.get(f'{line}.0', f'{line}.end')
                    print(text)
                    print(error)
            self.console['state'] = 'disabled'
            end = time.time()
            print(f"\nProcess finished in {end - start} seconds.")
            print('-'*60+'\n')

    def SCCommentLine(self, e=None) -> None:
        editor = self.currentTab
        if editor:
            cursor_position = editor.index('insert')
            line_number = cursor_position.split('.')[0]
            startPosition = f"{line_number}.0"
            endPosition = f'{line_number}.2'
            commented = editor.get(startPosition, endPosition)
            if commented == '# ':
                editor.delete(startPosition, endPosition)
            else:
                editor.insert(startPosition, '# ')
            editor.tag_remove('sel', '0.0', 'end')
            self.updateSyntax()

    def SCSaveFile(self, e=None) -> None:
        if not self.currentPath:
            self.currentPath = filedialog.asksaveasfilename(title='Select a file', filetypes=[('Phi File', '*.phi'), ('All Files', '*.*')])

        editor = self.currentTab
        if editor:
            text = editor.get('0.0', 'end')
            with open(self.currentPath, 'w') as f:
                f.write(text)

    def SCNewFile(self, e=None) -> None:
        self.currentPath = filedialog.asksaveasfilename(title='Select a file', filetypes=[('Phi File', '*.phi'), ('All Files', '*.*')])
        with open(self.currentPath, 'w') as f:
            f.write('')
        self.addTab(self.currentPath)

if __name__ == '__main__':
    app = App()

