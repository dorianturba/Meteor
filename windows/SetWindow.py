#
#     Meteor
#     Copyright (C) 2018 Dorian Turba
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
from functools import partial
from tkinter import Menu, Label, Frame, StringVar, Entry, Button, EW

from menus import EditMenu
from words_sets import WordsSet
from windows.Window import Window
from words_sets.Word import Word


class SetWindow(Window):
    menu: Menu
    edit_menu: EditMenu
    words_set: WordsSet

    def __init__(self, edit_menu: EditMenu, words_set: WordsSet,
                 parent=None, ):
        Window.__init__(self, parent)
        self.window = parent
        self.edit_menu = edit_menu
        self.words_set = words_set
        edit_menu.edit_set_menu.entryconfig(words_set.get_name(),
                                            state='disabled')
        self.menu = edit_menu.edit_set_menu
        self.master.title(words_set.get_name())

        self.words_entries = dict()

        first_lang_lbl = Label(self, text=words_set.first_language)
        sec_lang_lbl = Label(self, text=words_set.second_language)
        weight_lang_lbl = Label(self, text='Weight')
        first_lang_lbl.grid(row=0, column=0)
        sec_lang_lbl.grid(row=0, column=1)
        weight_lang_lbl.grid(row=0, column=2)
        for word in words_set.words:
            if str(word) in self.words_entries:
                continue
            frame = Frame(self)
            frame.grid(column=0, columnspan=4)
            first_txt_var = StringVar()
            sec_txt_var = StringVar()
            weight_txt_var = StringVar()
            word_entry_left = Entry(frame, textvariable=first_txt_var)
            word_entry_left.grid(row=0, column=0)
            word_entry_right = Entry(frame, textvariable=sec_txt_var)
            word_entry_right.grid(row=0, column=1)
            word_entry_weight = Entry(frame, textvariable=weight_txt_var)
            word_entry_weight.grid(row=0, column=2)
            word_entry_left.insert(0, word.first)
            word_entry_right.insert(0, word.second)
            word_entry_weight.insert(0, word.weight)
            del_btn = Button(frame, text='delete', command=partial(self.delete,
                                                                   str(word)))
            del_btn.grid(row=0, column=3)

            self.words_entries[str(word)] = {
                'word_entry_left': word_entry_left,
                'word_entry_right': word_entry_right,
                'word_entry_weight': word_entry_weight,
                'word_del': del_btn,
                'word_value': word,
            }

        save_btn = Button(self, text='Save', command=self.save)
        save_btn.grid(column=0, columnspan=4, sticky=EW)
        save_btn.config(state='normal')

    def save(self):
        tmp = list()
        for entry in self.words_entries.values():
            tmp.append(Word(first=entry['word_entry_left'].get(),
                            second=entry['word_entry_right'].get(),
                            weight=entry['word_entry_weight'].get()))
        self.words_set.words = tmp
        self.edit_menu.window.save()

    def delete(self, name):
        word = self.words_entries[name]['word_value']
        entries = self.words_entries[name]
        entries['word_entry_left'].destroy()
        entries['word_entry_right'].destroy()
        entries['word_entry_weight'].destroy()
        entries['word_del'].destroy()
        del self.words_entries[name]
        try:
            self.words_set.words.remove(word)
        except ValueError:
            print(f'word {word} not found, maybe already deleted')

    def destroy(self):
        self.menu.entryconfig(self.words_set.get_name(),
                              state='normal')
        Window.destroy(self)
