import customtkinter as ctk
from customtkinter import filedialog
import re
import sys
import main

currentLanguage = ''
languageSyntaxPatterns = {
    'txt': r'',
    'phi': r'(in|out|while|if|var|const|now|length|wait|root|fn)' # (in|out|while|if|var|const|now|length|wait|root|fn)|\d+|\"(.*?)\"|(==|<|>|!=|\+|-|\*|\/|%|^)
}
editorTags = {
    'keyword': '#38ff3f',
    'symbols': '#00ffff',
    'numbers': '#123456',
    'strings': '#ff00ff'
}
openEditors = {}

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


def clearOutput() -> None:
    output.delete('0.0', 'end')

window = ctk.CTk()
window.title("phIDE")
window.state('zoomed')
font = ctk.CTkFont(family="Courier", size=16)

leftPanel = ctk.CTkFrame(window)
rightPanel = ctk.CTkFrame(window)
bottomPanel = ctk.CTkFrame(window)
centerPanel = ctk.CTkFrame(window)
centerTabWindow = ctk.CTkTabview(centerPanel)
bottomTabWindow = ctk.CTkTabview(bottomPanel)

outputTab = bottomTabWindow.add('Output')
output = ctk.CTkTextbox(outputTab, font=font)
btnClearOutput = ctk.CTkButton(outputTab, command=clearOutput, text='x', width=10, height=10)

btnClearOutput.pack(anchor='ne')
output.pack(expand=True, fill='both')

sys.stdout = TerminalRedirect(output)
sys.stdin = TerminalRedirect(output)

def currentTab() -> ctk.CTkTextbox|None:
    tabName = centerTabWindow.get()
    if tabName != '':
        return openEditors[tabName]
    

def updateSyntax(e) -> None:
    editor = currentTab()
    if editor:
        ypos = editor.yview()[0]
        cursorPos = editor.index(ctk.INSERT)
        text = editor.get('0.0', 'end')
        matches = [(match.start(), match.end()) for match in re.finditer(languageSyntaxPatterns[currentLanguage], text)]
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

def addTab(path:str) -> None:
    global currentLanguage
    currentLanguage = path.split('/')[-1].split('.')[-1]
    tabName = path.split('/')[-1]
    tab = centerTabWindow.add(tabName)
    editor = ctk.CTkTextbox(tab, font=font)
    for tag in editorTags:
        editor.tag_config(tag, foreground=editorTags[tag])
    editor.pack(expand=True, fill='both')

    with open(path, 'r') as f:
        for line in f.readlines():
            editor.insert('end', line)

    openEditors[tabName] = editor
    updateSyntax('')   

def openFile(e) -> None:
    filePath = filedialog.askopenfilename(title='Select a file', filetypes=[('Phi File', '*.phi'), ('All Files', '*.*')])
    if filePath:
        addTab(filePath)

def run(e) -> None:
    editor = currentTab()
    if editor:
        sourceCode = editor.get('0.0', 'end')
        main.run(sourceCode)

def commentLine(e) -> None:
    print('hi')
    editor = currentTab()
    if editor:
        cursor_position = editor.index(ctk.CURRENT)
        line_number = cursor_position.split('.')[0]
        start_position = f"{line_number}.0"
        editor.insert(start_position, '# ')

leftPanel.grid(sticky='nesw', row=0, column=0, rowspan=2)
rightPanel.grid(sticky='nesw', row=0, column=2, rowspan=2)
centerPanel.grid(sticky='nesw', row=0, column=1)
bottomPanel.grid(sticky='nesw', row=1, column=1)
centerTabWindow.pack(expand=True, fill='both')
bottomTabWindow.pack(expand=True, fill='both')

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=1)

window.bind('<Control-o>', openFile)
window.bind('<F5>', run)
window.bind('<Control-/>', commentLine)
window.bind('<KeyPress>', updateSyntax)

window.mainloop()
