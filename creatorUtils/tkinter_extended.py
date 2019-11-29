import sys
import os
import os.path
from creatorUtils import path
import copy
import datetime
import itertools

if sys.version_info[0] < 3:
    import Tkinter as tk
    import tkFont
    import tkFileDialog as tkFile
else:
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.filedialog as tkFile


DEFAULT_FONT = ('Consolas', 10)
FOLDER = 0 # Selection will be a single folder
FOLDERS = 1 # Selection will be one or more folders
FILE = 2 # Selection will be a single file
FILES = 3 # Selection will be one or more files
EITHER = 4 # Selection will be a single file or a siongle folder
MIXED = 5 # Selection will be one or more files and/or folders

KEY_BACKSPACE = 8
KEY_SHIFT = 16
KEY_CONTROL = 17
KEY_CAPSLOCK = 20
KEY_ESCAPE = 27
KEY_PAGEDOWN = 34
KEY_END = 35
KEY_HOME = 36
KEY_LEFT = 37
KEY_PAGEUP = 33
KEY_UP = 38
KEY_RIGHT = 39
KEY_DOWN = 40
KEY_INSERT = 45
KEY_DELETE = 46
KEY_F1 = 112
KEY_F2 = 113
KEY_F3 = 114
KEY_F4 = 115
KEY_F5 = 116
KEY_F6 = 117
KEY_F7 = 118
KEY_F8 = 119
KEY_F9 = 120
KEY_F10 = 121
KEY_F11 = 122
KEY_F12 = 123
KEY_NUMLOCK = 144
KEY_SCRLOCK = 145
IGNORED = [
    KEY_CONTROL,
    KEY_NUMLOCK,
    KEY_CAPSLOCK,
    KEY_SCRLOCK,
    KEY_END,
    KEY_SHIFT,
    KEY_HOME,
    KEY_PAGEUP,
    KEY_PAGEDOWN,
    KEY_UP,
    KEY_RIGHT,
    KEY_DOWN,
    KEY_LEFT,
    KEY_INSERT
]

def askopenfilename(master = None, **options):
    dest = False
    if master == None:
        master = tk.Tk()
        dest = True
    a = tkFile.Open(master, **options).show()
    if dest:
        master.destroy()
    return a

def asksaveasfilename(master = None, **options):
    dest = False
    if master == None:
        master = tk.Tk()
        dest = True
    a = tkFile.SaveAs(master, **options).show()
    if dest:
        master.destroy()
    return a

def askopenfile(master = None, mode = 'r', **options):
    dest = False
    if master == None:
        master = tk.Tk()
        dest = True
    filename = tkFile.Open(master, **options).show()
    if dest:
        master.destroy()
    if filename:
        return open(filename, mode)
    return None

def askopenfiles(master = None, mode = 'r', **options):
    dest = False
    if master == None:
        master = tk.Tk()
        dest = True
    files = askopenfilenames(master, **options)
    if dest:
        master.destroy()
    if files:
        ofiles = []
        for filename in files:
            ofiles.append(open(filename, mode))
        files = ofiles
    return files

def asksaveasfile(master = None, mode = 'w', **options):
    dest = False
    if master == None:
        master = tk.Tk()
        dest = True
    filename = tkFile.SaveAs(master, **options).show()
    if dest:
        master.destroy()
    if filename:
        return open(filename, mode)
    return None

def askdirectory(master = None, **options):
    dest = False
    if master == None:
        master = tk.Tk()
        dest = True
    a = tkFile.Directory(**options).show()
    if dest:
        master.destroy()
    return a

def askopenfilenames(master = None, **options):
    dest = False
    if master == None:
        master = tk.Tk()
        dest = True
    options['multiple'] = 1
    files = tkFile.Open(master, **options).show()
    if dest:
        master.destroy()
    return files



askdirectory.__doc__ = tkFile.askdirectory.__doc__
askopenfile.__doc__ = tkFile.askopenfile.__doc__
askopenfiles.__doc__ = tkFile.askopenfiles.__doc__
askopenfilename.__doc__ = tkFile.askopenfilename.__doc__
askopenfilenames.__doc__ = tkFile.askopenfilenames.__doc__
asksaveasfile.__doc__ = tkFile.asksaveasfile.__doc__
asksaveasfilename.__doc__ = tkFile.asksaveasfilename.__doc__

askdir = askdirectory

def addSelectAllToWidget(widget):
    def select_all(event = None):
        event.widget.tag_add(tk.SEL, '0.0', tk.END)
        return 'break'
    widget.bind('<Control-a>', select_all)


class AlreadyCreatedError(Exception):
    pass

class DisappearingScrollbar(tk.Scrollbar):
    def __init__(self, *args, **kwargs):
        tk.Scrollbar.__init__(self, *args, **kwargs)
        self._geometryManager = None
        self.grid = grid_configure

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            if self._geometryManager == 'pack':
                self.pack_remove()
            elif self._geometryManager == 'grid':
                self.grid_remove()
            elif self._geometryManager == 'place':
                self.place_remove()
        else:
            if self._geometryManager == 'pack':
                self.pack()
            elif self._geometryManager == 'grid':
                self.grid()
            elif self._geometryManager == 'place':
                self.place()
        tk.Scrollbar.set(self, lo, hi)

    def grid_configure(self, cnf = {}, **kw):
        self._geometryManager = 'grid'
        tk.Scrollbar.grid_configure(self, cnf, **kw)

    def place_configure(self, cnf = {}, **kw):
        self._geometryManager = 'place'
        tk.Scrollbar.place_configure(self, cnf, **kw)

    def pack_configure(self, cnf = {}, **kw):
        self._geometryManager = 'pack'
        tk.Scrollbar.pack_configure(self, cnf, **kw)



class Entry(tk.Entry):
    """
    Base tkinter Entry widget with a select all command bound to '<Control-a>'
    """
    def __init__(self, *args, **kwargs):
        tk.Entry.__init__(self, *args, **kwargs)
        self.bind('<Control-a>', self.select_all)

    def select_all(self, event = None):
        self.tag_add(tk.SEL, '0.0', tk.END)
        return 'break'

class Text(tk.Text):
    """
    Base tkinter Text widget with a select all command bound to '<Control-a>'
    """
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.bind('<Control-a>', self.select_all)

    def select_all(self, event = None):
        self.tag_add(tk.SEL, '0.0', tk.END + '-1c')
        return 'break'

class Text2(Text):
    """
    Extension of Text that allows automatic management of overlapping tags
    """
    def __init__(self, master, *args, **kwargs):
        Text.__init__(self, tk.Frame(master), *args, **kwargs)
        self.frame = self.master
        self.bind('<Key>', self.handleKey)
        self.bind('<Control-Key>', self.handleControlKey)
        self.overlapGuide = OverlapGuide()
        self.backend = tk.Text(self.frame, *args, **kwargs)
        Text.grid(self, row = 0, column = 0, sticky = 'nsew')
        self.backend.grid(row = 0, column = 0, sticky = 'nsew')
        self.backend.lower(self)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.frame.grid_columnconfigure(0, weight = 1)

    def comboTagConfig(self, comboTag, tags):
        """
        Configures a combo tag to be made from the tags in `tags`
        """
        self.overlapGuide.addRule(tags, comboTag)

    def pack(self, cnf = {}, **kw):
        self.frame.pack(cnf, **kw)

    def pack_configure(self, cnf = {}, **kw):
        self.frame.pack_configure(cnf, **kw)

    def forget(self):
        self.frame.forget()

    def pack_forget(self):
        self.frame.pack_forget()

    def lower(self, belowThis = None):
        self.frame.lower(belowThis)

    def lift(self, aboveThis):
        self.frame.lift(aboveThis)

    def place_forget(self):
        self.frame.place_forget()

    def grid_forget(self):
        self.frame.grid_forget()

    def grid_remove(self):
        self.frame.grid_remove()

    def place(self, cnf = {}, **kw):
        self.frame.place(cnf, **kw)

    def place_configure(self, cnf = {}, **kw):
        self.frame.place_configure(cnf, **kw)

    def grid(self, cnf = {}, **kw):
        self.frame.grid(cnf, **kw)

    def grid_configure(self, cnf = {}, **kw):
        self.frame.grid_configure(cnf, **kw)

    def insert(self, index, chars, *args):
        self.backend.insert(index, chars, *args)
        Text.insert(self, index, chars, *args)
        self.manageOverlaps()

    def delete(self, index1, index2 = None):
        Text.delete(self, index1, index2)
        self.backend.delete(index1, index2)
        self.manageOverlaps()

    def tag_bind(self, tagName, sequence, func, add = None):
        self.backend.tag_bind(tagName, sequence, func, add)
        Text.tag_bind(self, tagName, sequence, func, add)

    def tag_unbind(self, tagName, sequence, funcid = None):
        self.backend.tag_unbind(tagName, sequence, funcid)
        Text.tag_unbind(self, tagName, sequence, funcid)

    def tag_add(self, tagName, index1, *args):
        self.backend.tag_add(tagName, index1, *args)
        self.manageOverlaps(tagName != 'sel')

    def tag_remove(self, tagName, index1, index2 = None):
        self.backend.tag_remove(tagName, index1, index2)
        self.manageOverlaps()

    def tag_configure(self, tagName, cnf = None, **kw):
        self.backend.tag_configure(tagName, cnf = None, **kw)
        Text.tag_configure(self, tagName, cnf = None, **kw)

    def tag_config(self, tagName, cnf = None, **kw):
        self.backend.tag_config(tagName, cnf = None, **kw)
        Text.tag_config(self, tagName, cnf = None, **kw)

    def edit(self, *args):
        self.backend.edit(*args)
        self.manageOverlaps()

    def edit_modified(self, arg = None):
        self.backend.edit_modified(arg)
        self.manageOverlaps()

    def edit_redo(self):
        self.backend.edit_redo()
        self.manageOverlaps()

    def edit_separator(self):
        self.backend.edit_separator()
        self.manageOverlaps()

    def edit_undo(self):
        self.backend.edit_undo()
        self.manageOverlaps()

    def mark_gravity(self, markName, direction = None):
        self.backend.mark_gravity(markName, direction)
        self.manageOverlaps()

    def mark_names(self):
        self.backend.mark_names()
        self.manageOverlaps()

    def mark_next(self, index):
        self.manageOverlaps()
        self.backend.mark_next(index)

    def mark_previous(self, index):
        self.manageOverlaps()
        self.backend.mark_previous(index)

    def mark_set(self, markName, index):
        self.backend.mark_set(markName, index)
        self.manageOverlaps()

    def mark_unset(self, *markNames):
        self.backend.mark_unset(*markNames)
        self.manageOverlaps()

    def configure(self, cnf = None, **kw):
        Text.configure(self, cnf, **kw)
        self.backend.configure(cnf, **kw)

    def config(self, cnf = None, **kw):
        Text.config(self, cnf, **kw)
        self.backend.config(cnf, **kw)

    def copyMarksToBackend(self):
        a = self.dump('0.0', tk.END, mark = True)[::-1]
        self.backend.mark_unset(self.backend.mark_names())
        for x in a:
            self.backend.mark_set(x[1], x[2])

    def copySelectionToBackend(self):
        try:
            self.backend.tag_remove('sel', '0.0', tk.END)
        except:
            pass
        try:
            self.backend.tag_add('sel', self.index(tk.SEL_FIRST), self.index(tk.SEL_LAST))
        except:
            pass

    def manageOverlaps(self, copySelection = True):
        self.copyMarksToBackend()
        if copySelection:
            self.copySelectionToBackend()
        a = self.backend.dump('0.0', tk.END, all = True)
        managed = []
        currentReal = []
        currentOverlap = None
        for x in a:
            if x[0] not in ['tagon', 'tagoff']:
                managed.append(x)
            elif self.overlapGuide.hasOverlapRule(x[1]):
                if x[0] == 'tagon':
                    currentReal.append(x[1])
                    if len(currentReal) > 1:
                        c = self.overlapGuide.haveOverlapRule(currentReal)
                        if type(c) == tuple:
                            raise Exception('FATAL: Missing combotag for ' + c)
                        else:
                            managed.append(('tagoff', currentOverlap, x[2]))
                            managed.append(('tagon', c, x[2]))
                            currentOverlap = c
                    else:
                        currentOverlap = x[1]
                        managed.append(x)
                else:
                    managed.append(('tagoff', currentOverlap, x[2]))
                    currentReal.remove(x[1])
                    if len(currentReal) >= 1:
                        currentOverlap = self.overlapGuide.tagOff(currentOverlap, x[1])
                        managed.append(('tagon', currentOverlap, x[2]))
                    else:
                        currentOverlap = None
            else:
                managed.append(x)
        tagStarts = {}
        tagRanges = []
        for x in managed:
            if x[0] == 'tagon':
                tagStarts[x[1]] = x[2]
            elif x[0] == 'tagoff':
                tagRanges.append((x[1], tagStarts.pop(x[1]), x[2]))

        # Everything has been generated, push it to the display
        Text.delete(self, '0.0', tk.END)
        for x in managed:
            if x[0] == 'text':
                Text.insert(self, x[2], x[1])
        for x in managed:
            if x[0] == 'mark':
                Text.mark_set(self, x[1], x[2])
                Text.mark_gravity(self, x[1], self.backend.mark_gravity(x[1]))
        for x in tagRanges:
            Text.tag_add(self, x[0], x[1], x[2])

    def toggleTag(self, tag):
        a = self.tag_ranges(tk.SEL)
        if a != ():
            if rangeWithinRange(a, self.backend.tag_ranges(tag)):
                self.tag_remove(tag, self.index(tk.SEL_FIRST), self.index(tk.SEL_LAST))
            else:
                self.tag_add(tag, self.index(tk.SEL_FIRST), self.index(tk.SEL_LAST))
        return 'break'

    def handleKey(self, event):
        self.copyMarksToBackend()
        if event.keycode in IGNORED:
            return
        elif event.keycode == KEY_BACKSPACE:
            a = self.tag_ranges(tk.SEL)
            if a != ():
                self.delete(a[0], a[1])
            else:
                self.delete(tk.INSERT + '-1c')
            return 'break'
        elif event.keycode == KEY_DELETE:
            a = self.tag_ranges(tk.SEL)
            if a != ():
                self.delete(a[0], a[1])
            else:
                self.delete(tk.INSERT)
            return 'break'
        else:
            a = self.tag_ranges(tk.SEL)
            if a != ():
                self.delete(a[0], a[1])
                self.insert(a[0], event.char)
            else:
                self.insert(self.index(tk.INSERT), event.char)
            return 'break'

    def handleControlKey(self, event):
        pass

    def handleAltKey(self, event):
        pass



class BasicFileExplorer(tk.Frame):
    """
    A file explorer frame.
    A breif description of the keywords that are specific to this class is as follows:
        `master` - The parent container of this Frame
        `returnVariable` - The variable which this widget should set
        `selectionType` - Determines what can be selected
        `new` - Are we creating a new file or are we opening a file that already exists?
    """
    def __init__(self, master, returnVariable = None, selectionType = MIXED, new = False, fileBoxClass = tk.Listbox, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.bind_all('<F5>', self.refreshDirectory)
        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self._new = new
        self._mode = selectionType
        if self._new and self._mode not in [FILE, FOLDER]:
            raise Exception('Cannot create new file or folder if not in FILE or FOLDER mode, respectfully.')
        if returnVariable == None:
            self._returnVariable = ListVariable()
        else:
            self._returnVariable = returnVariable

        self._testReturn = ListVariable()
        self._font = tkFont.Font(font = DEFAULT_FONT)
        self._directory = os.getcwd()
        self._files = []
        self._folders = []
        self.pathbox = Text(master = self, height = 1, font = self._font)
        self.pathbox.bind('<Return>', self.pathEntered)
        self.widgetName = tk.Label(master = self, text = 'File Explorer', font = self._font)
        self._f = tk.Frame(master = self)
        if self._mode in [FILES, FOLDERS, MIXED]:
            self.createFileBox(fileBoxClass, selectmode = tk.EXTENDED, font = self._font, activestyle = tk.NONE)
        else:
            self.createFileBox(fileBoxClass, font = self._font, activestyle = tk.NONE, exportselection = self._testReturn)
        self.filebox.bind('<Double-Button-1>', self._dbClick)
        self.filebox.bind('<Return>', self.returnSelected)
        self.filebox.bind('<<ListboxSelect>>', self.lis)
        self.pathbox.grid(row = 1, column = 0, sticky = 'ew')
        self.widgetName.grid(row = 0, column = 0, sticky = 'ew')
        self._f.grid(row = 2, column = 0, sticky = 'nsew')
        self.refreshDirectory()
        #self.after(1000, self.lis)

    def createFileBox(self, fileboxClass, *args, **kwargs):
        """
        Function to add the filebox to the file explorer.
        """
        try:
            self.filebox
            raise AlreadyCreatedError('`filebox` has already been created.')
        except AttributeError:
            self.filebox = fileboxClass(self._f, *args, **kwargs)
            self.vsb = tk.Scrollbar(self._f, orient = 'vertical', command = self.filebox.yview)
            self.filebox.configure(yscrollcommand = self.vsb.set)
            self.filebox.pack(side = 'left', fill = 'both', expand = True)
            self.vsb.pack(side = 'right', fill = 'y')

    def getFileboxSelection(self):
        """
        Returns the current selection in the filebox.
        Meant to be overriden if filebox class is not tk.Listbox
        and does not have the same get/insert/selection methods.
        """
        return self.filebox.curselection()

    def getFileboxItem(self, index):
        """
        Returns the item at `index`.
        Meant to be overriden if filebox class is not tk.Listbox
        and does not have the same get/insert/selection methods.
        """
        return self.filebox.get(index)

    def addNewFileboxFolder(self, index, *args, **kwargs):
        """

        Meant to be overriden if filebox class is not tk.Listbox
        and does not have the same get/insert/selection methods.
        """
        self.filebox.insert(index, *args, **kwargs)
        self.filebox.itemconfigure(index, background = '#cccccc')

    def lis(self, event = None):
        print(self._returnVariable.get())
        #self.after(1000, self.lis)

    def set_font(self, **kwargs):
        """
        Accepted keyword arguements:
            font -- font specier. If this keyword exists, all others are ignored
            family -- font 'family', e.g. Courier, Times, Helvetica
            size -- font size in points
            weight -- font thickness: NORMAL, BOLD
            slant -- font slant: ROMAN, ITALIC
            underline -- font underlining: false (0), true (1)
            overstrike -- font strikeout: false (0), true (1)
        """
        self._font.configure(**kwargs)

    def _dbClick(self, event = None):
        a = self.getFileboxItem(self.getFileboxSelection()[0])
        if path.isFolder(a):
            self.changeDirectory(a)
        else:
            self._returnVariable.set([os.getcwd() + '\\' + self.getFileboxItem(self.getFileboxSelection()[0])])

    def pathEntered(self, event = None):
        a = os.path.expandvars(self.pathbox.get('0.0', tk.END)[:-1])
        if path.isFolder(a):
            self.changeDirectory(a)
        elif path.isFile(a):
            self._returnVariable.set([os.getcwd() + '\\' + a])
        else:
            self.notfound(a)
        return 'break'

    def changeDirectory(self, dir):
        try:
            os.chdir(dir)
            self._directory = os.getcwd()
            self.pathbox.delete('0.0', tk.END)
            self.pathbox.insert(tk.INSERT, self._directory)
            self.filebox.delete('0', tk.END)
            self._files = []
            self._folders = []
            self._folders.append('..')
            for x in os.listdir('.'):
                if path.isFile(x):
                    self._files.append(x)
                else:
                    self._folders.append(x)
            for x in self._folders:
                self.addNewFileboxFolder(tk.END, x)

            if self._mode in [FILE, FILES, MIXED, EITHER]:
                for x in self._files:
                    self.filebox.insert(tk.END, x)
        except Exception as e:
            global a
            a.append(e)
            print(e)
            #TODO

    def refreshDirectory(self, event = None):
        self.changeDirectory('.')

    def save(self, path):
        if not self._new:
            raise Exception('Not in new mode.')
        #TODO

    def returnSelected(self, event = None):
        a = self.getFileboxSelection()
        if len(a) == 0:
            return
        if event != None:
            if len(a) == 1:
                self._dbClick()
                return
            elif self._mode != MIXED:
                for x in a:
                    if path.isFolder(self.getFileboxItem(x)):
                        return
        b = [os.getcwd() + '\\' + self.getFileboxItem(x) for x in a]
        for x in b:
            try:
                os.stat(x)
            except Exception as e:
                self.fileError(x, e)
        self._returnVariable.set(b)

    def notfound(self, path):
        #TODO code that shows an error message saying that the specified path could not be found
        pass

    def fileerror(self, path, error):
        #TODO code that shows an error message describing the error it encountered
        pass

    @property
    def returnVariable(self):
        """
        Returns the reference for the return variable.
        """
        return self._returnVariable



### INTERNAL CLASSES ###
# These classes are mostly just small subclasses to be used within larger classes
# They can be used as is, but that should be avoided if you do not know what you are doing


class ListItem(object):
    def __init__(self, row, master = None, font = None, name = None):
        object.__init__(self)
        self.__master = master
        if font != None:
            self.__font = font
        else:
            self.__font = tkFont.Font(master, font = DEFAULT_FONT)
        self.__row = row
        self.__propDic = {'Name': tk.StringVar(self.__master)}
        self.__props = {'Name': 'v'}
        self.__propDicInvisible = {}
        self.__override = {'Name': None}
        if name != None:
            self.__propDic['Name'] = name
        self.__grid = 1
        self.__visEnts = [LabelVariable(self.__master, var = self.__propDic['Name'], font = self.__font)]
        self.__visEnts[0].grid(row = row, column = 0, sticky = 'ew')

    def addProperty(self, propname, visible = True):
        if propname in self.__props:
            raise KeyError('ListItem instance already has property "' + propname + '".')
        if visible:
            self.__props[propname] = 'v'
            a = tk.StringVar(self.__master)
            self.__propDic[propname] = a
            b = LabelVariable(master = self.__master, var = a, font = self.__font)
            b.grid(row = self.__row, column = self.__grid, sticky = 'ew')
            self.__grid += 1
            self.__visEnts.append(b)
        else:
            self.__props[propname] = 'h'
            self.__propDicInvisible[propname] = tk.StringVar(self.__master)
        self.__override[propname] = None

    def setPropertyValue(self, propname, value):
        if not propname in self.__props:
            raise KeyError(propname)
        if self.__props[propname] == 'v':
            self.__propDic[propname].set(value)
        else:
            self.__propDicInvisible[propname].set(value)

    def getPropertyValue(self, propname):
        if not propname in self.__props:
            raise KeyError(propname)
        if self.__props[propname] == 'v':
            return self.__propDic[propname].get()
        else:
            return self.__propDicInvisible[propname].get()

    def set_font(self, fontname):
        self.__font.configure(family = fontname)

    def setRow(self, row):
        for x in range(len(self.__visEnts)):
            self.__visEnts[x].grid(row = row, column = x, sticky = 'ew')

    def getSort(self, prop):
        if prop in self.__props:
            if self.__override[prop] != None:
                return self.getPropertyValue(self.__override[prop])
            else:
                return self.getPropertyValue(prop)

    def addSortOverride(self, prop, override):
        self.__override[prop] = override



class LabelVariable(tk.Label):
    def __init__(self, master = None, cnf = {}, var = None, value = None, name = None, **kwargs):
        tk.Label.__init__(self, master, cnf, **kwargs)
        if var != None:
            self.__var = var
        else:
            self.__var = tk.StringVar(self, value, name)
        self.configure(textvariable = self.__var)

    def get(self):
        return self.__var.get()

    def set(self, value):
        self.__var.set(value)

    def clear(self):
        self.__value = []



class FileExplorerItem(ListItem):
    def __init__(self, row, master = None, font = None, relativePath = None):
        ListItem.__init__(self, row, master, font, name = relativePath)
        # Add extra properties
        self.addProperty('Type')
        self.addProperty('Size')
        self.addProperty('Modified')
        self.addProperty('RealDate', False)
        # Use unix timestamp to sort by modify time rather than the date string
        self.addSortOverride('Modified', 'RealDate')
        # Set file type
        if path.isFolder(relativePath):
            self.setPropertyValue('Type', 'Folder')
        elif len(relativePath.split('.')) == 1:
            self.setPropertyValue('Type', 'File')
        else:
            self.setPropertyValue('Type', '{} File'.format(relativePath.split('.')[-1]))
        # Set file size
        a = os.stat(relativePath)
        b = a.st_size
        if b < 1024:
            c = str(b) + ' B'
        elif b < 1048576:
            c = str(b / 1024) + ' KB'
        elif b < 1073741824:
            c = str(b / 1048576) + ' MB'
        else:
            c = str(b / 1073741824) + ' GB'
        self.setPropertyValue('Size', c)
        #Get modified date and timestamp
        self.setPropertyValue('RealDate', str(a._integer_mtime))
        self.setPropertyValue('Modified', datetime.datetime.fromtimestamp(a._integer_mtime).__format__('%m/%d/%Y %I:%M:%S %p'))



class FloatVar(tk.Variable):
    def __init__(self, master = None, value = 0.0, name = None):
        tk.Variable.__init__(self, master, value, name)

    def set(self, value):
        value = float(value)
        tk.Variable.set(self, value)



class ListVariable(object):
    def __init__(self):
        object.__init__(self)
        self.__value = []

    def get(self, index = None):
        if index == None:
            return copy.deepcopy(self.__value)
        else:
            return self.__value[index]

    def set(self, index, value = None):
        if value == None:
            self.__value = copy.deepcopy(list(index))
        else:
            self.__value[index] = value

    def append(self, *args, **kwargs):
        self.__value.append(*args)

    def clear(self):
        self.__value = []

    def count(self, *args, **kwargs):
        return self.__value.count(*args)

    def extend(self, *args, **kwargs):
        self.__value.extend(*args, **kwargs)

    def index(self, value, start = 0, stop = 2147483647):
        return self.__value.index(value, start, stop)

    def insert(self, *args, **kwargs):
        self.__value.insert(*args, **kwargs)

    def pop(self, index = -1):
        return self.__value.pop(index)

    def sort(self, *args, **kwargs):
        self.__value.sort(*args, **kwargs)

    def remove(self, value, reverse = False):
        self.__value.pop(self.__value.index(value, reverse))

    def reverse(self):
        self.__value.reverse()

    def __add__(self, *args):
        return self.__value.__add__(*args)

    def __contains__(self, *args):
        return self.__value.__contains__(*args)

    def __delslice__(self, *args):
        self.__value.__delslice__(*args)

    def __delitem__(self, *args):
        self.__value.__delitem__(*args)

    def __eq__(self, *args):
        return self.__value.__eq__(*args)

    def __ge__(self, *args):
        return self.__value.__ge__(*args)

    def __getitem__(self, *args):
        return self.__value.__getitem__(*args)

    def __getslice__(self, *args):
        return self.__value.__getslice__(*args)

    def __gt__(self, *args):
        return self.__value.__gt__(*args)

    def __iadd__(self, *args):
        self.__value.__iadd__(*args)

    def __imul__(self, *args):
        self.__value.__imul__(*args)

    def __iter__(self, *args):
        return self.__value.__iter__(*args)

    def __le__(self, *args):
        return self.__value.__le__(*args)

    def __lt__(self, *args):
        return self.__value.__lt__(*args)

    def __len__(self, *args):
        return self.__value.__len__(*args)

    def __mul__(self, *args):
        return self.__value.__mul__(*args)

    def __ne__(self, *args):
        return self.__value.__ne__(*args)

    def __repr__(self, *args):
        return self.__value.__repr__(*args)

    def __reversed__(self, *args):
        return self.__value.__reversed__(*args)

    def __rmul__(self, *args):
        return self.__value.__rmul__(*args)

    def __setitem__(self, *args):
        self.__value.__setitem__(*args)

    def __setslice__(self, *args):
        self.__value.__setslice__(*args)

    if sys.version_info[0] >= 3:
        def __sizeof__(self, *args):
            return self.__value.__sizeof__(*args)



class SelectableList(tk.Widget, tk.XView, tk.YView):
    """
    Class that works very similarly to the tkinter default Listbox,
    with each item having specific attributes that can be either
    hidden or visible. These can then be used to sort the items.
    """
    def __init__(self, master = None, cnf = {}, listItemClass = ListItem, **kwargs):
        tk.Widget.__init__(self, master, cnf, **kwargs)
        tk.XView.__init__(self, master, cnf, **kwargs)
        tk.YView.__init__(self, master, cnf, **kwargs)
        self.__itemlist = []
        self.__proplist = []
        self.__newItemClass = listItemClass
        self.vsb_x = tk.Scrollbar(self, orient = 'horizontal', command = self.xview)
        self.vsb_y = tk.Scrollbar(self, orient = 'vertical', command = self.yview)
        self.configure(xscrollcommand = self.vsb_x.set)
        self.configure(yscrollcommand = self.vsb_y.set)

    def newItem(self, name, additionalData = {}):
        self.__itemlist.append(self.__newItemClass(self, font, name))



class OverlapGuide(object):
    def __init__(self):
        object.__init__(self)
        self.hasRule = []
        self.rules = {}
        self.combinationTags = {}
        self.wanted = [] # List that contains tag groups for which a combo tag has yet to be specified

    def tagOff(self, comboTag, tag):
        return self.combinationTags[comboTag].tagOff(tag)

    def hasOverlapRule(self, tag):
        """
        Used to check if `tag` has any entries in the guide.
        """
        return tag in self.hasRule

    def haveOverlapRule(self, tags):
        """
        Used to check if there is a rule for the overlap of every tag in `tags`
        """
        if len(tags) == 1:
            return tags[0]
        tags = list(tags)
        tags.sort()
        tags = tuple(tags)
        try:
            return self.rules[tags]
        except KeyError:
            if not tags in self.wanted:
                self.wanted.append(tags)
            return tags

    def addRule(self, tags, overlapTag):
        """
        Adds a rule to replace the overlap of all the tags in `tags` with `overlapTag`
        """
        for x in tags:
            if not x in self.hasRule:
                self.hasRule.append(x)
        tags = list(tags)
        tags.sort()
        tags = tuple(tags)
        self.rules[tags] = overlapTag
        self.combinationTags[overlapTag] = CombinationTag(overlapTag, tags, self)
        if tags in self.wanted:
            self.wanted.remove(tags)
            for x in self.combinationTags:
                self.combinationTags[x].build()

    def resetAll(self):
        self.rules = {}
        self.hasRule = []
        self.combinationTags = {}
        self.wanted = []



class CombinationTag(object):
    def __init__(self, name, tags, overlapGuide):
        object.__init__(self)
        self.__og = overlapGuide
        self.__name = name
        self.__tags = tags
        self.__hasMissingCombos = False
        self.__tagOff = {}
        if len(tags) > 2:
            self.build(True)
        else:
            self.__tagOff[tags[0]] = tags[1]
            self.__tagOff[tags[1]] = tags[0]

    def tagOff(self, tag):
        return self.__tagOff[tag]

    def build(self, force = False):
        if self.__hasMissingCombos or force:
            self.__hasMissingCombos = False
            for x in itertools.combinations(self.__tags, len(self.__tags) - 1):
                for y in self.__tags:
                    if y not in x:
                        self.__tagOff[y] = self.__og.haveOverlapRule(x)
                        if type(self.__tagOff[y]) == tuple:
                            self.__hasMissingCombos = True
                        break

    @property
    def name(self):
        return self.__name

# Module Functions #
def withinSelection(widget, tag):
    a = widget.tag_ranges(tk.SEL)
    if a == ():
        raise Exception('No text has been selected')
    b = widget.tag_ranges(tag)
    if b == ():
        return False
    return rangeWithinRange(a, b)

def rangeWithinRange(a, b):
    """
    Returns true if the range a is within any of the range in b
    """
    if b == ():
        return False
    a = createPositonPairs(a)[0]
    b = createPositonPairs(b)
    for x in b:
        if int(a[0][0]) >= int(x[0][0]):
            if int(a[1][0]) <= int(x[1][0]):
                if int(a[0][1]) >= int(x[0][1]):
                    if int(a[1][1]) <= int(x[1][1]):
                        return True
    return False

def createPositonPairs(table):
    return [(table[2 * x].string.split('.'), table[(2 * x) + 1].string.split('.')) for x in range((len(table)/2))]
