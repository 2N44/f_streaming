import os
import sys
import util
import tagger
import info_query as info
import dler as dl
from pathlib import Path
from copy import deepcopy
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, ttk, Toplevel, font, filedialog
from PIL import Image
from PIL import ImageTk as itk

def toggle_state(toggle_bool):

    if toggle_bool:

        return 'toggle_on'

    else:

        return 'toggle_off'

def loading_img_path(path, index, total):

    percent=100*index/total

    if percent%2 > 1:

        number = str(int(percent-percent%2 +2))

    else:

        number = str(int(percent-percent%2))

    return os.path.join(path, 'loading_'+number+'.png')



class dl_win():

    '''
        Download and tagging window, and toplevel windows (Lyrics, search, cancel).
    '''

    def __init_win__(
            self, index_link, total_link, total_modified, total_cancel,
            total_dl, song_tag, saved_param, software_path, url, art_path=None):

        self.index_link = index_link
        self.total_link = total_link
        self.total_canceled = total_cancel
        self.total_modified = total_modified
        self.total_dl = total_dl
        self.song_tag = song_tag
        self.cancel = False
        self.cancelall = False
        self.from_time = '00:00:00'
        self.to_time = song_tag['length']
        self.saved_par = saved_param
        self.software_path = software_path
        self.url = url
        self.art_path = art_path

    def _covert_art(self):

        if self.art_path is None:

            return util.img_from_url(self.song_tag['art url'])

        else:

            return self.art_path

    def cmd_save_com(self):

        self.song_tag['desc'] = self.com_entry_1.get('1.0', 'end-1c')
        self.song_tag['text writer'] = self.com_entry_2.get()
        self.com_window.destroy()

    def cmd_savelyrics(self):

        self.song_tag['lyrics']=self.lyrics_entry_1.get('1.0', 'end-1c')
        self.lyrics_window.destroy()

    def cmd_cancel_btn(self):

        if self.total_link == 1:

            self.dl_window.destroy()

        else:

            self.cancel_win()

    def cmd_cancelone(self):

        self.cancel_window.destroy()
        self.dl_window.destroy()
        self.cancel = True

    def cmd_cancelall(self):

        self.cancel_window.destroy()
        self.dl_window.destroy()
        self.cancelall = True

    def cmd_search(self):

        search_string = self.search_entry_1.get()

        if 'genius.com' in search_string:

            search_string = search_string.split('/')[-1].replace('lyrics', '').replace('-', ' ')

        self.song_tag = info.info_query_title(
            search_string,
            self.song_tag['length'])

        self.dl_entry_2.delete(0, 'end')
        self.dl_entry_3.delete(0, 'end')
        self.dl_entry_4.delete(0, 'end')
        self.dl_entry_5.delete(0, 'end')
        self.dl_entry_6.delete(0, 'end')
        self.dl_entry_7.delete(0, 'end')
        self.dl_entry_8.delete(0, 'end')
        self.dl_entry_9.delete(0, 'end')
        self.dl_entry_10.delete(0 ,'end')
        
        self.dl_button_fg_7 = Image.open(self._covert_art()).resize((180, 180))
        self.dl_button_bg_7.paste(self.dl_button_fg_7, (8, 8))
        self.dl_button_img_7 = itk.PhotoImage(self.dl_button_bg_7)
        self.dl_button_7.configure(image=self.dl_button_img_7)

        if not self.saved_par['monoartist']:

            self.dl_entry_1.delete(0, 'end')
            self.dl_entry_10.insert(0, self.song_tag['title'])
            self.dl_entry_9.insert(0, self.song_tag['artist'])
            self.dl_entry_8.insert(0, self.song_tag['album'])
            self.dl_entry_7.insert(0, self.song_tag['album artist'])
            self.dl_entry_6.insert(0, self.song_tag['track'])
            self.dl_entry_5.insert(0, self.song_tag['total track'])
            self.dl_entry_4.insert(0, self.song_tag['composer'])
            self.dl_entry_3.insert(0, self.song_tag['publisher'])
            self.dl_entry_2.insert(0, self.song_tag['genre'])
            self.dl_entry_1.insert(0, self.song_tag['date'])

        else:

            self.dl_entry_10.insert(0, self.song_tag['title'])
            self.dl_entry_9.insert(0, self.song_tag['artist'])
            self.dl_entry_8.insert(0, self.song_tag['album'])
            self.dl_entry_7.insert(0, self.song_tag['track'])
            self.dl_entry_6.insert(0, self.song_tag['total track'])
            self.dl_entry_5.insert(0, self.song_tag['composer'])
            self.dl_entry_4.insert(0, self.song_tag['publisher'])
            self.dl_entry_3.insert(0, self.song_tag['genre'])
            self.dl_entry_2.insert(0, self.song_tag['date'])

        self.search_window.destroy()

    def cmd_savemp3(self):

        # #initialize loading screen
        # loading_dl = loading_window()
        # loading_dl.__init__loading(self.dl_window, 5, 'Loading metadata ...')
        # loading_dl.open_loading()

        #save

        self.from_time = util.sub_time(self.dl_entry_11.get(), '00:00;15')
        self.to_time = util.add_time(
            util.sub_time(self.dl_entry_12.get(), self.from_time),
            '00:00:15'
        )
        self.song_tag['artist'] = self.dl_entry_9.get()
        self.song_tag['album'] = self.dl_entry_8.get()
        self.song_tag['album_path'] = util.check_dirname(
            self.song_tag['album'])
        
        

        if self.saved_par['monoartist']:

            self.song_tag['title ft'] = self.dl_entry_10.get()
            self.song_tag['composer'] = self.dl_entry_5.get()
            self.song_tag['publisher'] = self.dl_entry_4.get()
            self.song_tag['genre'] = self.dl_entry_3.get()
            self.song_tag['date'] = self.dl_entry_2.get()

            if self.dl_entry_7.get() != '':

                self.song_tag['track'] = int(self.dl_entry_7.get())

            else:

                self.song_tag['track'] = None

            if self.dl_entry_8.get() != '':

                self.song_tag['total track'] = int(self.dl_entry_8.get())

            else:

                self.song_tag['total track'] = None

        else:

            self.song_tag['title'] = self.dl_entry_10.get()
            self.song_tag['album artist'] = self.dl_entry_7.get()
            self.song_tag['composer'] = self.dl_entry_4.get()
            self.song_tag['publisher'] = self.dl_entry_3.get()
            self.song_tag['genre'] = self.dl_entry_2.get()
            self.song_tag['date'] = self.dl_entry_1.get()

            if self.dl_entry_6.get() != '':

                self.song_tag['track'] = int(self.dl_entry_6.get())

            else:

                self.song_tag['track'] = None

            if self.dl_entry_5.get() != '':

                self.song_tag['total track'] = int(self.dl_entry_5.get())

            else:

                self.song_tag['total track'] = None

        path =  os.path.join(
            self.saved_par['path'],
            self.song_tag['album_path']
        )

        # loading_dl.progress_label = 'Creating directory ...'
        # loading_dl.progress()

        #make directory

        util.mkdir_album(path)

        # loading_dl.progress_label = 'Downloading cover art ...'
        # loading_dl.progress()

        #download art
        if self.saved_par['cover_art_dl']:

            dl.dl_art(path, self.song_tag)
            self.art_path = util.pic_path(path, self.song_tag)

        # loading_dl.progress_label = 'Downloading audio file ...'
        # loading_dl.progress()

        #download mp3      
       
        if not util.check_audiofile(self.saved_par, self.song_tag):

            dl.dl_from_to(
                self.url,
                self.from_time,
                self.to_time,
                os.path.join(
                    path,
                    util.check_filename(self.song_tag['title'])),
                self.saved_par['format'],
                self.saved_par['bitrate']
            )

        else:

            print('Already downloaded')

        # loading_dl.progress_label = 'Tagging audio file ...'
        # loading_dl.progress()

        #tag
        audio_path = os.path.join(
            path,
            util.check_filename(self.song_tag['title'])+'.mp3'
        )
        audio_tags = tagger.Tagger(self.saved_par, audio_path, self.art_path)
        audio_tags.tag(self.song_tag)
        
        self.dl_window.destroy()

    def cmd_retry(self):

        search_title = (str(self.dl_entry_10.get())
            +' - '
            +str(self.dl_entry_9.get())
        )

        self.song_tag = info.info_query_title(
            search_title,
            self.song_tag['length']
        )

        self.dl_entry_2.delete(0, 'end')
        self.dl_entry_3.delete(0, 'end')
        self.dl_entry_4.delete(0, 'end')
        self.dl_entry_5.delete(0, 'end')
        self.dl_entry_6.delete(0, 'end')
        self.dl_entry_7.delete(0, 'end')
        self.dl_entry_8.delete(0, 'end')
        self.dl_entry_9.delete(0, 'end')
        self.dl_entry_10.delete(0 ,'end')

        self.dl_button_fg_7 = Image.open(self._covert_art()).resize((180, 180))
        self.dl_button_bg_7.paste(self.dl_button_fg_7, (8, 8))
        self.dl_button_img_7 = itk.PhotoImage(self.dl_button_bg_7)
        self.dl_button_7.configure(image=self.dl_button_img_7)   

        if not self.saved_par['monoartist']:

            self.dl_entry_1.delete(0, 'end')
            self.dl_entry_10.insert(0, self.song_tag['title'])
            self.dl_entry_9.insert(0, self.song_tag['artist'])
            self.dl_entry_8.insert(0, self.song_tag['album'])
            self.dl_entry_7.insert(0, self.song_tag['album artist'])
            self.dl_entry_6.insert(0, self.song_tag['track'])
            self.dl_entry_5.insert(0, self.song_tag['total track'])
            self.dl_entry_4.insert(0, self.song_tag['composer'])
            self.dl_entry_3.insert(0, self.song_tag['publisher'])
            self.dl_entry_2.insert(0, self.song_tag['genre'])
            self.dl_entry_1.insert(0, self.song_tag['date'])

        else:

            self.dl_entry_10.insert(0, self.song_tag['title'])
            self.dl_entry_9.insert(0, self.song_tag['artist'])
            self.dl_entry_8.insert(0, self.song_tag['album'])
            self.dl_entry_7.insert(0, self.song_tag['track'])
            self.dl_entry_6.insert(0, self.song_tag['total track'])
            self.dl_entry_5.insert(0, self.song_tag['composer'])
            self.dl_entry_4.insert(0, self.song_tag['publisher'])
            self.dl_entry_3.insert(0, self.song_tag['genre'])
            self.dl_entry_2.insert(0, self.song_tag['date'])

    def cmd_cover_art(self):

        cover_art_path = filedialog.askopenfilename()
        
        if type(cover_art_path) is str and len(cover_art_path) > 0:

            self.art_path = cover_art_path

            if self.saved_par['screen_size_index'] == 1:

                self.dl_button_fg_7 = Image.open(self._covert_art()).resize((180, 180))
                self.dl_button_bg_7.paste(self.dl_button_fg_7, (8, 8))
                self.dl_button_img_7 = itk.PhotoImage(self.dl_button_bg_7)

            else:

                self.dl_button_fg_7 = Image.open(self._covert_art()).resize((135, 135))
                self.dl_button_bg_7.paste(self.dl_button_fg_7, (6, 6))
                self.dl_button_img_7 = itk.PhotoImage(self.dl_button_bg_7)

            self.dl_button_7.configure(image=self.dl_button_img_7)

#        covert_art = filedialog.askopenfile(
#            mode='r',
#            filetypes=[
#                ('image files', '.jpg; .png; .bmp'),
#                ('all files', '.'),
#            ]
#        )

    def cmd_key_return(self):

        self.dl_button_3.invoke()

    def cmd_key_escape(self):

        self.dl_button_2.invoke()

    def cmd_key_escape_lyrics(self):

        self.lyrics_button_1.invoke()

    def cmd_key_return_com(self):

        self.com_button_2.invoke()

    def cmd_key_return_search(self):

        self.search_button_1.invoke()

    def comment_win(self):

        self.com_path = os.path.join(self.software_path, 'assets', 'comment')
        self.com_window = Toplevel(self.dl_window)
        self.com_window.title('Comment')
        self.com_window.geometry('600x512')
        self.com_window.configure(bg = '#333333')

        self.com_canvas = Canvas(
            self.com_window,
            bg = '#333333',
            height = 512,
            width = 600,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )

        self.com_canvas.place(x = 0, y = 0)

        #BUTTONS
        self.com_button_img_1 = PhotoImage(
            file=os.path.join(self.com_path, 'button_1.png'))
        self.com_button_1 = Button(
            master=self.com_window,
            image=self.com_button_img_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.com_window.destroy,
            relief='flat'
        )
        self.com_button_1.place(
            x=322.0,
            y=440.0,
            width=60.0,
            height=40.0
        )

        self.com_button_img_2 = PhotoImage(
            file=os.path.join(self.com_path, 'button_2.png'))
        self.com_button_2 = Button(
            master=self.com_window,
            image=self.com_button_img_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.cmd_save_com,
            relief='flat'
        )
        self.com_button_2.place(
            x=218.0,
            y=440.0,
            width=60.0,
            height=40.0
        )

        #TEXTAREA
        self.com_entry_img_1 = PhotoImage(
            file=os.path.join(self.com_path, 'entry_1.png'))
        self.com_entry_bg_1 = self.com_canvas.create_image(
            300.0,
            282.0,
            image=self.com_entry_img_1
        )
        self.com_entry_1 = Text(
            master=self.com_window,
            bd=0,
            bg='#333333',
            fg='#B3B3B3',            
            font=(self.saved_par['font'], 14 * -1),
            highlightthickness=0
        )
        self.com_entry_1.place(
            x=50.0,
            y=160.0,
            width=500.0,
            height=246.0
        )

        self.com_entry_1.insert('1.0', self.song_tag['desc'])

        #ENTRY
        self.com_entry_img_2 = PhotoImage(
            file=os.path.join(self.com_path, 'entry_2.png'))
        self.com_entry_bg_2 = self.com_canvas.create_image(
            172.0,
            86.0,
            image=self.com_entry_img_2
        )
        self.com_entry_2 = Entry(
            master=self.com_window,
            bd=0,
            bg='#FFFFFF',
            fg='#000716',
            font=(self.saved_par['font'], 14 * -1),
            highlightthickness=0
        )
        self.com_entry_2.place(
            x=48.0,
            y=72.0,
            width=248.0,
            height=26.0
        )
        self.com_entry_2.insert(0, self.song_tag['text writer'])

        #TEXT
        self.com_canvas.create_text(
            42.64013671875,
            40.0,
            anchor='nw',
            text='Text writer(s):',
            fill='#B3B3B3',
            font=(self.saved_par['font'], 20 * -1)
        )

        self.com_canvas.create_text(
            42.64013671875,
            124.0,
            anchor='nw',
            text='Comment:',
            fill='#B3B3B3',
            font=(self.saved_par['font'], 20 * -1)
        )

        #BIND KEY
        self.com_window.bind(
            '<Escape>',
            lambda event : self.com_button_1.invoke()
        )

        self.com_window.resizable(False, False)
        self.com_window.mainloop()

    def lyrics_win(self):

        self.lyrics_path = os.path.join(self.software_path, 'assets', 'lyrics')
        self.lyrics_window = Toplevel(self.dl_window)
        self.lyrics_window.title('Lyrics of '+str(self.song_tag['title']))
        self.lyrics_window.geometry('500x800')
        self.lyrics_window.configure(bg = '#333333')

        self.lyrics_canvas = Canvas(
            self.lyrics_window,
            bg = '#333333',
            height = 800,
            width = 500,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )

        self.lyrics_canvas.place(x = 0, y = 0)

        #BUTTONS
        self.lyrics_button_img_1 = PhotoImage(
            file=os.path.join(self.lyrics_path, 'button_1.png'))
        self.lyrics_button_1 = Button(
            master=self.lyrics_window,
            image=self.lyrics_button_img_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.lyrics_window.destroy,
            relief='flat'
        )
        self.lyrics_button_1.place(
            x=272.0,
            y=728.0,
            width=60.0,
            height=40.0
        )

        self.lyrics_button_img_2 = PhotoImage(
            file=os.path.join(self.lyrics_path, 'button_2.png'))
        self.lyrics_button_2 = Button(
            master=self.lyrics_window,
            image=self.lyrics_button_img_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.cmd_savelyrics,
            relief='flat'
        )
        self.lyrics_button_2.place(
            x=168.0,
            y=728.0,
            width=60.0,
            height=40.0
        )

        #TEXTAREA
        self.lyrics_entry_img_1 = PhotoImage(
            file=os.path.join(self.lyrics_path, 'entry_1.png'))
        self.lyrics_entry_bg_1 = self.lyrics_canvas.create_image(
            250.0,
            368.0,
            image=self.lyrics_entry_img_1
        )
        self.lyrics_entry_1 = Text(
            master=self.lyrics_window,
            bd=0,
            bg='#333333',
            fg='#B3B3B3',
            font=(self.saved_par['font'], 14 * -1),
            highlightthickness=0
        )
        self.lyrics_entry_1.place(
            x=50.0,
            y=44.0,
            width=400.0,
            height=650.0
        )
        self.lyrics_entry_1.insert('1.0', self.song_tag['lyrics'])

        #BIND KEY
        self.lyrics_window.bind(
            '<Escape>',
            lambda event : self.cmd_key_escape_lyrics()
        )

        self.lyrics_window.resizable(False, False)
        self.lyrics_window.mainloop()

    def cancel_win(self):

        self.cancel_path = os.path.join(self.software_path, 'assets', 'cancel')
        self.cancel_window = Toplevel(self.dl_window)
        self.cancel_window.title('Warning')
        self.cancel_window.geometry('660x152')
        self.cancel_window.configure(bg = '#333333')

        #CANVAS
        self.cancel_canvas = Canvas(
            self.cancel_window,
            bg = '#333333',
            height = 152,
            width = 660,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )

        self.cancel_canvas.place(x = 0, y = 0)

        #BUTTONS
        self.cancel_button_img_1 = PhotoImage(
            file=os.path.join(self.cancel_path, 'button_1.png'))
        self.cancel_button_1 = Button(
            master=self.cancel_window,
            image=self.cancel_button_img_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.cmd_cancelall,
            relief='flat'
        )
        self.cancel_button_1.place(
            x=349.0,
            y=84.0,
            width=120.0,
            height=44.0
        )

        self.cancel_button_img_2 = PhotoImage(
            file=os.path.join(self.cancel_path, 'button_2.png'))
        self.cancel_button_2 = Button(
            master=self.cancel_window,
            image=self.cancel_button_img_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.cmd_cancelone,
            relief='flat'
        )
        self.cancel_button_2.place(
            x=151.0,
            y=84.0,
            width=158.0,
            height=44.0
        )

        #TEXT
        self.cancel_canvas.create_text(
            40.0,
            32.0,
            anchor='nw',
            text='Do you want to cancel this download or all of them ?',
            fill='#B3B3B3',
            font=('Ubuntu Medium', 24 * -1)
        )

        self.cancel_window.resizable(False, False)
        self.cancel_window.mainloop()

    def search_win(self):

        self.search_path = os.path.join(self.software_path, 'assets', 'search')
        self.search_window = Toplevel(self.dl_window)
        self.search_window.title('Search')
        self.search_window.geometry('660x100')
        self.search_window.configure(bg = '#333333')


        self.search_canvas = Canvas(
            self.search_window,
            bg = '#333333',
            height = 100,
            width = 660,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )

        #BUTTON
        self.search_canvas.place(x = 0, y = 0)
        self.search_button_img_1 = PhotoImage(
            file=os.path.join(self.search_path, 'button_1.png'))
        self.search_button_1 = Button(
            master=self.search_window,
            image=self.search_button_img_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.cmd_search,
            relief='flat'
        )
        self.search_button_1.place(
            x=596.0,
            y=36.0,
            width=28.0,
            height=28.0
        )

        #ENTRY
        self.search_entry_img_1 = PhotoImage(
            file=os.path.join(self.search_path, 'entry_1.png'))
        self.search_entry_bg_1 = self.search_canvas.create_image(
            316.0,
            50.0,
            image=self.search_entry_img_1
        )
        self.search_entry_1 = Entry(
            master=self.search_window,
            bd=0,
            bg='#FFFFFF',
            fg='#000716',
            font=(self.saved_par['font'], 14 * -1),
            highlightthickness=0
        )
        self.search_entry_1.place(
            x=40.0,
            y=38.0,
            width=550.0,
            height=24.0
        )
        self.search_entry_1.insert(0, 'Genius link or Search terms')

        #BIND KEY
        self.search_window.bind(
            '<Return>',
            lambda event : self.cmd_key_return_search())
        self.search_window.bind(
            '<Escape>',
            lambda event : self.search_window.destroy())

        self.search_window.resizable(False, False)
        self.search_window.mainloop()

    def open_dl(self):

        self.dl_window = Tk()
        self.dl_window.title(self.song_tag['title ft'])
        self.dl_window.configure(bg = '#333333')

        #ICON
        self.dl_window.iconphoto(
            True,
            PhotoImage(file=os.path.join('assets', 'fstreaming_icon.png'))
        )

        if self.saved_par['screen_size_index'] == 1:

            self.dl_window.geometry('760x928')
            self.dl_path = os.path.join(self.software_path, 'assets', 'download_win')

            self.dl_canvas = Canvas(
                self.dl_window,
                bg = '#333333',
                height = 928,
                width = 760,
                bd = 0,
                highlightthickness = 0,
                relief = 'ridge'
            )

            self.dl_canvas.place(x = 0, y = 0)

            #BUTTONS
            self.dl_button_img_1 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_1.png'))
            self.dl_button_1 = Button(
                image=self.dl_button_img_1,
                borderwidth=0,
                highlightthickness=0,
                command=self.search_win,
                relief='flat'
            )
            self.dl_button_1.place(
                x=488.0,
                y=848.0,
                width=72.0,
                height=48.0
            )

            self.dl_button_img_2 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_2.png'))
            self.dl_button_2 = Button(
                image=self.dl_button_img_2,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_cancel_btn,
                relief='flat'
            )
            self.dl_button_2.place(
                x=392.0,
                y=848.0,
                width=72.0,
                height=48.0
            )

            self.dl_button_img_3 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_3.png'))
            self.dl_button_3 = Button(
                image=self.dl_button_img_3,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_savemp3,
                relief='flat'
            )
            self.dl_button_3.place(
                x=296.0,
                y=848.0,
                width=72.0,
                height=48.0
            )

            self.dl_button_img_4 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_4.png'))
            self.dl_button_4 = Button(
                image=self.dl_button_img_4,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_retry,
                relief='flat'
            )
            self.dl_button_4.place(
                x=200.0,
                y=848.0,
                width=72.0,
                height=48.0
            )
            
            self.dl_button_img_5 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_5.png'))
            self.dl_button_5 = Button(
                image=self.dl_button_img_5,
                borderwidth=0,
                highlightthickness=0,
                command=self.lyrics_win,
                relief='flat'
            )
            self.dl_button_5.place(
                x=392.0,
                y=744.0,
                width=72.0,
                height=44.0
            )

            self.dl_button_img_6 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_6.png'))
            self.dl_button_6 = Button(
                image=self.dl_button_img_6,
                borderwidth=0,
                highlightthickness=0,
                command=self.comment_win,
                relief='flat'
            )
            self.dl_button_6.place(
                x=296.0,
                y=744.0,
                width=72.0,
                height=44.0
            )

            #ENTRIES
            self.entries_bg_img = PhotoImage(
                file=os.path.join(self.dl_path, 'entries_bg.png'))
            self.entries_bg = self.dl_canvas.create_image(
                380.0,
                558.0,
                image=self.entries_bg_img
            )

            self.dl_entry_img_2 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_2.png'))
            self.dl_entry_bg_2 = self.dl_canvas.create_image(
                208.0,
                710.0,
                image=self.dl_entry_img_2
            )
            self.dl_entry_2 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_2.place(
                x=84.0,
                y=696.0,
                width=248.0,
                height=26.0
            )

            self.dl_entry_img_3 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_3.png'))
            self.dl_entry_bg_3 = self.dl_canvas.create_image(
                552.0,
                626.0,
                image=self.dl_entry_img_3
            )
            self.dl_entry_3 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_3.place(
                x=428.0,
                y=612.0,
                width=248.0,
                height=26.0
            )

            self.dl_entry_img_4 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_4.png'))
            self.dl_entry_bg_4 = self.dl_canvas.create_image(
                208.0,
                626.0,
                image=self.dl_entry_img_4
            )
            self.dl_entry_4 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_4.place(
                x=84.0,
                y=612.0,
                width=248.0,
                height=26.0
            )

            self.dl_entry_img_5 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_5.png'))
            self.dl_entry_bg_5 = self.dl_canvas.create_image(
                552.0,
                542.0,
                image=self.dl_entry_img_5
            )
            self.dl_entry_5 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_5.place(
                x=428.0,
                y=528.0,
                width=248.0,
                height=26.0
            )

            self.dl_entry_img_6 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_6.png'))
            self.dl_entry_bg_6 = self.dl_canvas.create_image(
                208.0,
                542.0,
                image=self.dl_entry_img_6
            )
            self.dl_entry_6 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_6.place(
                x=84.0,
                y=528.0,
                width=248.0,
                height=26.0
            )

            self.dl_entry_img_7 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_7.png'))
            self.dl_entry_bg_7 = self.dl_canvas.create_image(
                552.0,
                458.0,
                image=self.dl_entry_img_7
            )
            self.dl_entry_7 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_7.place(
                x=428.0,
                y=444.0,
                width=248.0,
                height=26.0
            )

            self.dl_entry_img_8 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_8.png'))
            self.dl_entry_bg_8 = self.dl_canvas.create_image(
                208.0,
                458.0,
                image=self.dl_entry_img_8
            )
            self.dl_entry_8 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_8.place(
                x=84.0,
                y=444.0,
                width=248.0,
                height=26.0
            )

            self.dl_entry_img_9 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_9.png'))
            self.dl_entry_bg_9 = self.dl_canvas.create_image(
                552.0,
                374.0,
                image=self.dl_entry_img_9
            )
            self.dl_entry_9 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_9.place(
                x=428.0,
                y=360.0,
                width=248.0,
                height=26.0
            )

            self.dl_entry_img_10 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_10.png'))
            self.dl_entry_bg_10 = self.dl_canvas.create_image(
                208.0,
                374.0,
                image=self.dl_entry_img_10
            )
            self.dl_entry_10 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 14 * -1),
                highlightthickness=0
            )
            self.dl_entry_10.place(
                x=84.0,
                y=360.0,
                width=248.0,
                height=26.0
            )

            if not self.saved_par['monoartist']:

                self.dl_entry_img_1 = PhotoImage(
                    file=os.path.join(self.dl_path, 'entry_1.png'))
                self.dl_entry_bg_1 = self.dl_canvas.create_image(
                    552.0,
                    710.0,
                    image=self.dl_entry_img_1
                )
                self.dl_entry_1 = Entry(
                    bd=0,
                    bg='#FFFFFF',
                    fg='#000716',
                    font=(self.saved_par['font'], 14 * -1),
                    highlightthickness=0
                )
                self.dl_entry_1.place(
                    x=428.0,
                    y=696.0,
                    width=248.0,
                    height=26.0
                )

                #Fill fields
                self.dl_entry_1.insert(0, self.song_tag['date'])
                self.dl_entry_2.insert(0, self.song_tag['genre'])
                self.dl_entry_3.insert(0, self.song_tag['publisher'])
                self.dl_entry_4.insert(0, self.song_tag['composer'])
                self.dl_entry_5.insert(0, self.song_tag['total track'])
                self.dl_entry_6.insert(0, self.song_tag['track'])
                self.dl_entry_7.insert(0, self.song_tag['album artist'])
                self.dl_entry_8.insert(0, self.song_tag['album'])
                self.dl_entry_9.insert(0, self.song_tag['artist'])
                self.dl_entry_10.insert(0, self.song_tag['title'])

                #TEXT
                self.dl_canvas.create_text(
                    422.6400146484375,
                    664.0,
                    anchor='nw',
                    text='Date:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    78.6400146484375,
                    664.0,
                    anchor='nw',
                    text='Genre:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    422.6400146484375,
                    580.0,
                    anchor='nw',
                    text='Publisher:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )        

                self.dl_canvas.create_text(
                    78.6400146484375,
                    580.0,
                    anchor='nw',
                    text='Composer:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    422.6400146484375,
                    496.0,
                    anchor='nw',
                    text='Total track:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    78.6400146484375,
                    496.0,
                    anchor='nw',
                    text='Track n°:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    422.6400146484375,
                    412.0,
                    anchor='nw',
                    text='Album artist:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    78.6400146484375,
                    412.0,
                    anchor='nw',
                    text='Album:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    422.6400146484375,
                    328.0,
                    anchor='nw',
                    text='Artist(s):',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )        

                self.dl_canvas.create_text(
                    78.6400146484375,
                    328.0,
                    anchor='nw',
                    text='Title:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

            else:

                #Fill fields
                self.dl_entry_2.insert(0, self.song_tag['date'])
                self.dl_entry_3.insert(0, self.song_tag['genre'])
                self.dl_entry_4.insert(0, self.song_tag['publisher'])
                self.dl_entry_5.insert(0, self.song_tag['composer'])
                self.dl_entry_6.insert(0, self.song_tag['total track'])
                self.dl_entry_7.insert(0, self.song_tag['track'])
                self.dl_entry_8.insert(0, self.song_tag['album'])
                self.dl_entry_9.insert(0, self.song_tag['artist'])
                self.dl_entry_10.insert(0, self.song_tag['title'])

                #TEXT
                self.dl_canvas.create_text(
                    78.6400146484375,
                    664.0,
                    anchor='nw',
                    text='Date:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    422.6400146484375,
                    580.0,
                    anchor='nw',
                    text='Genre:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    78.6400146484375,
                    580.0,
                    anchor='nw',
                    text='Publisher:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )        

                self.dl_canvas.create_text(
                    422.6400146484375,
                    496.0,
                    anchor='nw',
                    text='Composer:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    78.6400146484375,
                    496.0,
                    anchor='nw',
                    text='Total track:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    422.6400146484375,
                    412.0,
                    anchor='nw',
                    text='Track n°:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    78.6400146484375,
                    412.0,
                    anchor='nw',
                    text='Album:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    422.6400146484375,
                    328.0,
                    anchor='nw',
                    text='Artist:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

                self.dl_canvas.create_text(
                    78.6400146484375,
                    328.0,
                    anchor='nw',
                    text='Title:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 20 * -1)
                )

            #IMAGES
            self.dl_image_img_1 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_1.png'))
            self.dl_image_1 = self.dl_canvas.create_image(
                640.0,
                240.0,
                image=self.dl_image_img_1
            )        

            self.dl_image_img_2 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_2.png'))
            self.dl_image_2 = self.dl_canvas.create_image(
                522.0,
                240.0,
                image=self.dl_image_img_2
            )

            self.dl_image_img_3 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_3.png'))
            self.dl_image_3 = self.dl_canvas.create_image(
                417.0,
                240.0,
                image=self.dl_image_img_3
            )

            self.dl_loading_img = PhotoImage(
                file=loading_img_path(os.path.join(self.dl_path, 'loading'), self.index_link+1, self.total_link))
            self.dl_loading = self.dl_canvas.create_image(
                688.0,
                122.0,
                image=self.dl_loading_img
            )

            #TEXT
            self.dl_canvas.create_text(
                578.0,
                229.0,
                anchor='nw',
                text=str(self.total_dl),
                fill='#808080',
                font=(self.saved_par['font'], 24 * -1)
            )        

            self.dl_canvas.create_text(
                463.0,
                228.0,
                anchor='nw',
                text=str(self.total_modified),
                fill='#808080',
                font=(self.saved_par['font'], 24 * -1)
            )

            self.dl_canvas.create_text(
                360.0,
                228.0,
                anchor='nw',
                text=str(self.total_canceled),
                fill='#808080',
                font=(self.saved_par['font'], 24 * -1)
            )

            self.dl_canvas.create_text(
                568.0,
                107.0,
                anchor='nw',
                text=str(self.index_link+1)+'/'+str(self.total_link),
                fill='#808080',
                font=(self.saved_par['font'], 24 * -1)
            )

            #TIME STAMPS
            self.dl_entry_img_11 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_11.png'))
            self.dl_entry_bg_11 = self.dl_canvas.create_image(
                380.0,
                90.0,
                image=self.dl_entry_img_11
            )
            self.dl_entry_11 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 22 * -1),
                highlightthickness=0
            )
            self.dl_entry_11.place(
                x=336.0,
                y=76.0,
                width=88.0,
                height=26.0
            )
            self.dl_entry_11.insert(0, self.from_time)

            self.dl_image_img_5 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_5.png'))
            self.dl_image_5 = self.dl_canvas.create_image(
                295.0,
                147.0,
                image=self.dl_image_img_5
            )

            self.dl_entry_img_12 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_12.png'))
            self.dl_entry_bg_12 = self.dl_canvas.create_image(
                380.0,
                148.0,
                image=self.dl_entry_img_12
            )
            self.dl_entry_12 = Entry(
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                font=(self.saved_par['font'], 22 * -1),
                highlightthickness=0
            )
            self.dl_entry_12.place(
                x=336.0,
                y=134.0,
                width=88.0,
                height=26.0
            )
            self.dl_entry_12.insert(0, self.to_time)

            self.dl_image_img_6 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_6.png'))
            self.dl_image_6 = self.dl_canvas.create_image(
                295.0,
                89.0,
                image=self.dl_image_img_6
            )

            #COVERART SELECTOR
            self.dl_button_bg_7 = Image.open(
                os.path.join(self.dl_path, 'button_7.png'))
            self.dl_button_fg_7 = Image.open(self._covert_art()).resize((180, 180))
            self.dl_button_bg_7.paste(self.dl_button_fg_7, (8, 8))
            self.dl_button_img_7 = itk.PhotoImage(self.dl_button_bg_7)
            self.dl_button_7 = Button(
                image=self.dl_button_img_7,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_cover_art,
                relief='flat'
            )
            self.dl_button_7.place(
                x=60.0,
                y=60.0,
                width=196.0,
                height=196.0
            )

        else:

            self.dl_window.geometry('573x700')
            self.dl_path = os.path.join(self.software_path, 'assets', 'tiny_download_win')

            self.dl_canvas = Canvas(
                self.dl_window,
                bg = '#333333',
                height = 700,
                width = 573,
                bd = 0,
                highlightthickness = 0,
                relief = 'ridge'
            )

            self.dl_canvas.place(x = 0, y = 0)

            #BUTTONS
            self.dl_button_img_1 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_1.png'))
            self.dl_button_1 = Button(
                master=self.dl_window,
                image=self.dl_button_img_1,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_search,
                relief='flat'
            )
            self.dl_button_1.place(
                x=368.10345458984375,
                y=639.6551513671875,
                width=54.310333251953125,
                height=36.2069091796875
            )

            self.dl_button_img_2 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_2.png'))
            self.dl_button_2 = Button(
                master=self.dl_window,
                image=self.dl_button_img_2,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_cancel_btn,
                relief='flat'
            )
            self.dl_button_2.place(
                x=295.6896667480469,
                y=639.6551513671875,
                width=54.310333251953125,
                height=36.2069091796875
            )

            self.dl_button_img_3 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_3.png'))
            self.dl_button_3 = Button(
                master=self.dl_window,
                image=self.dl_button_img_3,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_savemp3,
                relief='flat'
            )
            self.dl_button_3.place(
                x=223.27586364746094,
                y=639.6551513671875,
                width=54.31034851074219,
                height=36.2069091796875
            )

            self.dl_button_img_4 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_4.png'))
            self.dl_button_4 = Button(
                master=self.dl_window,
                image=self.dl_button_img_4,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_retry,
                relief='flat'
            )
            self.dl_button_4.place(
                x=150.86207580566406,
                y=639.6551513671875,
                width=54.31034851074219,
                height=36.2069091796875
            )

            self.dl_button_img_5 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_5.png'))
            self.dl_button_5 = Button(
                master=self.dl_window,
                image=self.dl_button_img_5,
                borderwidth=0,
                highlightthickness=0,
                command=self.lyrics_win,
                relief='flat'
            )
            self.dl_button_5.place(
                x=295.6896667480469,
                y=561.2069091796875,
                width=54.310333251953125,
                height=33.18963623046875
            )

            self.dl_button_img_6 = PhotoImage(
                file=os.path.join(self.dl_path, 'button_6.png'))
            self.dl_button_6 = Button(
                master=self.dl_window,
                image=self.dl_button_img_6,
                borderwidth=0,
                highlightthickness=0,
                command=self.comment_win,
                relief='flat'
            )
            self.dl_button_6.place(
                x=223.27586364746094,
                y=561.2069091796875,
                width=54.31034851074219,
                height=33.18963623046875
            )

            #ENTRIES
            self.dl_entries_bg_img = PhotoImage(
                file=os.path.join(self.dl_path, 'image_1.png'))
            self.dl_entries_bg = self.dl_canvas.create_image(
                286.17241287231445,
                420.29310607910156,
                image=self.dl_entries_bg_img
            )

            self.dl_entry_img_2 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_2.png'))
            self.dl_entry_bg_2 = self.dl_canvas.create_image(
                156.89654922485352,
                535.5603332519531,
                image=self.dl_entry_img_2
            )
            self.dl_entry_2 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_2.place(
                x=65.32758712768555,
                y=525.0,
                width=183.13792419433594,
                height=19.12066650390625
            )

            self.dl_entry_img_3 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_3.png'))
            self.dl_entry_bg_3 = self.dl_canvas.create_image(
                416.37933349609375,
                472.1982879638672,
                image=self.dl_entry_img_3
            )
            self.dl_entry_3 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_3.place(
                x=324.81036376953125,
                y=461.637939453125,
                width=183.137939453125,
                height=19.120697021484375
            )

            self.dl_entry_img_4 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_4.png'))
            self.dl_entry_bg_4 = self.dl_canvas.create_image(
                156.89654922485352,
                472.1982879638672,
                image=self.dl_entry_img_4
            )
            self.dl_entry_4 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_4.place(
                x=65.32758712768555,
                y=461.637939453125,
                width=183.13792419433594,
                height=19.120697021484375
            )

            self.dl_entry_img_5 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_5.png'))
            self.dl_entry_bg_5 = self.dl_canvas.create_image(
                416.37933349609375,
                408.8362274169922,
                image=self.dl_entry_img_5
            )
            self.dl_entry_5 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_5.place(
                x=324.81036376953125,
                y=398.27587890625,
                width=183.137939453125,
                height=19.120697021484375
            )

            self.dl_entry_img_6 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_6.png'))
            self.dl_entry_bg_6 = self.dl_canvas.create_image(
                156.89654922485352,
                408.8362274169922,
                image=self.dl_entry_img_6
            )
            self.dl_entry_6 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_6.place(
                x=65.32758712768555,
                y=398.27587890625,
                width=183.13792419433594,
                height=19.120697021484375
            )

            self.dl_entry_img_7 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_7.png'))
            self.dl_entry_bg_7 = self.dl_canvas.create_image(
                416.37933349609375,
                345.4741668701172,
                image=self.dl_entry_img_7
            )
            self.dl_entry_7 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_7.place(
                x=324.81036376953125,
                y=334.913818359375,
                width=183.137939453125,
                height=19.120697021484375
            )

            self.dl_entry_img_8 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_8.png'))
            self.dl_entry_bg_8 = self.dl_canvas.create_image(
                156.89654922485352,
                345.4741668701172,
                image=self.dl_entry_img_8
            )
            self.dl_entry_8 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_8.place(
                x=65.32758712768555,
                y=334.913818359375,
                width=183.13792419433594,
                height=19.120697021484375
            )

            self.dl_entry_img_9 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_9.png'))
            self.dl_entry_bg_9 = self.dl_canvas.create_image(
                416.37933349609375,
                282.11207580566406,
                image=self.dl_entry_img_9
            )
            self.dl_entry_9 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_9.place(
                x=324.81036376953125,
                y=271.5517272949219,
                width=183.137939453125,
                height=19.120697021484375
            )

            self.dl_entry_img_10 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_10.png'))
            self.dl_entry_bg_10 = self.dl_canvas.create_image(
                156.89654922485352,
                282.11207580566406,
                image=self.dl_entry_img_10
            )
            self.dl_entry_10 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_10.place(
                x=65.32758712768555,
                y=271.5517272949219,
                width=183.13792419433594,
                height=19.120697021484375
            )

            if not self.saved_par['monoartist']:

                self.dl_entry_img_1 = PhotoImage(
                    file=os.path.join(self.dl_path, 'entry_1.png'))
                self.dl_entry_bg_1 = self.dl_canvas.create_image(
                    416.37933349609375,
                    535.5603332519531,
                    image=self.dl_entry_img_1
                )
                self.dl_entry_1 = Entry(
                    master=self.dl_window,
                    bd=0,
                    bg='#FFFFFF',
                    fg='#000716',
                    highlightthickness=0
                )
                self.dl_entry_1.place(
                    x=324.81036376953125,
                    y=525.0,
                    width=183.137939453125,
                    height=19.12066650390625
                )

                #Fill fields
                self.dl_entry_1.insert(0, self.song_tag['date'])
                self.dl_entry_2.insert(0, self.song_tag['genre'])
                self.dl_entry_3.insert(0, self.song_tag['publisher'])
                self.dl_entry_4.insert(0, self.song_tag['composer'])
                self.dl_entry_5.insert(0, self.song_tag['total track'])
                self.dl_entry_6.insert(0, self.song_tag['track'])
                self.dl_entry_7.insert(0, self.song_tag['album artist'])
                self.dl_entry_8.insert(0, self.song_tag['album'])
                self.dl_entry_9.insert(0, self.song_tag['artist'])
                self.dl_entry_10.insert(0, self.song_tag['title'])

                #TEXT
                self.dl_canvas.create_text(
                    318.8017578125,
                    500.862060546875,
                    anchor='nw',
                    text='Date:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    500.862060546875,
                    anchor='nw',
                    text='Genre:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    318.8017578125,
                    437.5,
                    anchor='nw',
                    text='Publisher:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    437.5,
                    anchor='nw',
                    text='Composer:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    318.8017578125,
                    374.137939453125,
                    anchor='nw',
                    text='Total track:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    374.137939453125,
                    anchor='nw',
                    text='Track n°:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    318.8017578125,
                    310.77587890625,
                    anchor='nw',
                    text='Album artist:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    310.77587890625,
                    anchor='nw',
                    text='Album:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    318.8017578125,
                    247.41378784179688,
                    anchor='nw',
                    text='Artist(s):',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    247.41378784179688,
                    anchor='nw',
                    text='Title:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

            else:

                #Fill fields
                self.dl_entry_2.insert(0, self.song_tag['date'])
                self.dl_entry_3.insert(0, self.song_tag['genre'])
                self.dl_entry_4.insert(0, self.song_tag['publisher'])
                self.dl_entry_5.insert(0, self.song_tag['composer'])
                self.dl_entry_6.insert(0, self.song_tag['total track'])
                self.dl_entry_7.insert(0, self.song_tag['track'])
                self.dl_entry_8.insert(0, self.song_tag['album'])
                self.dl_entry_9.insert(0, self.song_tag['artist'])
                self.dl_entry_10.insert(0, self.song_tag['title'])

                #TEXT
                self.dl_canvas.create_text(
                    59.31897735595703,
                    500.862060546875,
                    anchor='nw',
                    text='Date:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    318.8017578125,
                    437.5,
                    anchor='nw',
                    text='Genre:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    437.5,
                    anchor='nw',
                    text='Publisher:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    318.8017578125,
                    374.137939453125,
                    anchor='nw',
                    text='Composer:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    374.137939453125,
                    anchor='nw',
                    text='Total track:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    318.8017578125,
                    310.77587890625,
                    anchor='nw',
                    text='Track n°:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    310.77587890625,
                    anchor='nw',
                    text='Album:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    318.8017578125,
                    247.41378784179688,
                    anchor='nw',
                    text='Artist:',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

                self.dl_canvas.create_text(
                    59.31897735595703,
                    247.41378784179688,
                    anchor='nw',
                    text='Title (ft.):',
                    fill='#B3B3B3',
                    font=(self.saved_par['font'], 16 * -1)
                )

            #IMAGES
            self.dl_image_img_2 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_2.png'))
            self.dl_image_2 = self.dl_canvas.create_image(
                482.67242431640625,
                180.94827270507812,
                image=self.dl_image_img_2
            )

            self.dl_canvas.create_text(
                435.99139404296875,
                172.737060546875,
                anchor='nw',
                text='50',
                fill='#808080',
                font=(self.saved_par['font'], 20 * -1)
            )

            self.dl_image_img_3 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_3.png'))
            self.dl_image_3 = self.dl_canvas.create_image(
                393.663818359375,
                180.94827270507812,
                image=self.dl_image_img_3
            )

            self.dl_canvas.create_text(
                349.2456970214844,
                171.98275756835938,
                anchor='nw',
                text='50',
                fill='#808080',
                font=(self.saved_par['font'], 20 * -1)
            )

            self.dl_image_img_4 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_4.png'))
            self.dl_image_4 = self.dl_canvas.create_image(
                313.9181213378906,
                180.40518188476562,
                image=self.dl_image_img_4
            )

            self.dl_canvas.create_text(
                271.5517272949219,
                171.98275756835938,
                anchor='nw',
                text='50',
                fill='#808080',
                font=(self.saved_par['font'], 20 * -1)
            )

            self.dl_image_img_5 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_5.png'))
            self.dl_image_5 = self.dl_canvas.create_image(
                518.8448486328125,
                91.9051742553711,
                image=self.dl_image_img_5
            )

            self.dl_canvas.create_text(
                428.4482727050781,
                80.71121215820312,
                anchor='nw',
                text='50/50',
                fill='#808080',
                font=(self.saved_par['font'], 20 * -1)
            )

            self.dl_image_img_6 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_6.png'))
            self.dl_image_6 = self.dl_canvas.create_image(
                222.20689392089844,
                110.81465148925781,
                image=self.dl_image_img_6
            )

            self.dl_image_img_7 = PhotoImage(
                file=os.path.join(self.dl_path, 'image_7.png'))
            self.dl_image_7 = self.dl_canvas.create_image(
                222.20689392089844,
                67.06465530395508,
                image=self.dl_image_img_7
            )

            #TIME STAMPS
            self.dl_entry_img_11 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_11.png'))
            self.dl_entry_bg_11 = self.dl_canvas.create_image(
                286.63792419433594,
                67.88792991638184,
                image=self.dl_entry_img_11
            )
            self.dl_entry_11 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_11.place(
                x=255.41378784179688,
                y=57.32758712768555,
                width=62.448272705078125,
                height=19.120685577392578
            )
            self.dl_entry_11.insert(0, self.from_time)

            self.dl_entry_img_12 = PhotoImage(
                file=os.path.join(self.dl_path, 'entry_12.png'))
            self.dl_entry_bg_12 = self.dl_canvas.create_image(
                286.63792419433594,
                111.63793563842773,
                image=self.dl_entry_img_12
            )
            self.dl_entry_12 = Entry(
                master=self.dl_window,
                bd=0,
                bg='#FFFFFF',
                fg='#000716',
                highlightthickness=0
            )
            self.dl_entry_12.place(
                x=255.41378784179688,
                y=101.07759094238281,
                width=62.448272705078125,
                height=19.120689392089844
            )
            self.dl_entry_12.insert(0, self.to_time)

            #cover art selector
            self.dl_button_bg_7 = Image.open(
                os.path.join(self.dl_path, 'button_7.png'))
            self.dl_button_fg_7 = Image.open(self._covert_art()).resize((136, 136))
            self.dl_button_bg_7.paste(self.dl_button_fg_7, (6, 6))
            self.dl_button_img_7 = itk.PhotoImage(self.dl_button_bg_7)
            self.dl_button_7 = Button(
                master=self.dl_window,
                image=self.dl_button_img_7,
                borderwidth=0,
                highlightthickness=0,
                command=self.cmd_cover_art,
                relief='flat'
            )
            self.dl_button_7.place(
                x=45.25862121582031,
                y=45.25862121582031,
                width=147.84483337402344,
                height=147.84483337402344
            )

        #BIND KEY
        self.dl_window.bind(
            '<Return>',
            lambda event : self.cmd_key_return())
        self.dl_window.bind(
            '<Escape>',
            lambda event : self.cmd_key_escape())

        self.dl_window.resizable(False, False)
        self.dl_window.mainloop()



class main_win():

    def __init_main__(self, saved_par, software_path):

        self.saved_par = saved_par
        self.software_path = software_path

    def open_main(self):

        self.main_path = os.path.join(self.software_path, 'assets', 'main')
        self.main_window = Tk()
        self.main_window.title('F_streaming')
        self.main_window.geometry('760x300')
        self.main_window.configure(bg = '#333333')

        #check screen size
        if self.main_window.winfo_screenheight() < 928:

            self.saved_par['screen_size_index'] = 0

        #ICON
        self.main_window.iconphoto(
            True,
            PhotoImage(file=os.path.join('assets', 'fstreaming_icon.png'))
        )

        #CANVAS
        self.main_canvas = Canvas(
            self.main_window,
            bg = '#333333',
            height = 300,
            width = 760,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )

        self.main_canvas.place(x = 0, y = 0)

        #BUTTONS
        self.main_button_img_1 = PhotoImage(
            file=os.path.join(self.main_path, 'button_1.png'))
        self.main_button_1 = Button(
            image=self.main_button_img_1,
            borderwidth=0,
            highlightthickness=0,
            command= self.cmd_download,
            relief='flat'
        )
        self.main_button_1.place(
            x=656.0,
            y=212.0,
            width=72.0,
            height=44.0
        )

        self.main_button_img_2 = PhotoImage(
            file=os.path.join(self.main_path, 'button_2.png'))
        self.main_button_2 = Button(
            image=self.main_button_img_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.set_win,
            relief='flat'
        )
        self.main_button_2.place(
            x=692.0,
            y=24.0,
            width=44.0,
            height=44.0
        )

        #IMAGES
        self.main_img_1 = PhotoImage(
            file=os.path.join(self.main_path, 'image_1.png'))
        self.logo = self.main_canvas.create_image(
            42.00000000000003,
            234.0,
            image=self.main_img_1
        )

        self.main_img_logo = PhotoImage(
            file=os.path.join(self.main_path, 'image_2.png'))
        self.img_logo = self.main_canvas.create_image(
            375.0,
            122.0,
            image=self.main_img_logo
        )

        #ENTRY
        self.main_entry_img_1 = PhotoImage(
            file=os.path.join(self.main_path, 'entry_1.png'))
        self.main_entry_bg_1 = self.main_canvas.create_image(
            357.0,
            234.0,
            image=self.main_entry_img_1
        )
        self.main_entry_1 = Entry(
            bd=0,
            bg='#FFFFFF',
            fg='#000716',
            font=(self.saved_par['font'], 14 * -1),
            highlightthickness=0
        )
        self.main_entry_1.place(
            x=87.00000000000003,
            y=218.0,
            width=540.0,
            height=30.0
        )
        self.main_entry_1.insert(0,'Video URL')

        #BIND KEY        
        self.main_window.bind(
            '<Return>',
            lambda event : self.cmd_key_return())

        self.main_window.resizable(False, False)
        self.main_window.mainloop()

    def set_win(self):

        self.set_path = os.path.join(self.software_path, 'assets', 'settings')
        #WINDOW
        self.set_window = Toplevel(self.main_window)
        self.set_window.title('Settings')
        self.set_window.geometry('760x644')
        self.set_window.configure(bg = '#333333')

        #CANVAS
        self.set_canvas = Canvas(
            master=self.set_window,
            bg = '#333333',
            height = 644,
            width = 760,
            bd = 0,
            highlightthickness = 0,
            relief = 'ridge'
        )
        self.set_canvas.place(x = 0, y = 0)

        #BUTTONS
        self.set_button_img_1 = PhotoImage(
            file=os.path.join(self.set_path, 'button_1.png'))
        self.set_button_1 = Button(
            master=self.set_window,
            image=self.set_button_img_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.cmd_save_par,
            relief='flat'
        )
        self.set_button_1.place(
            x=298.0,
            y=572.0,
            width=60.0,
            height=40.0
        )

        self.set_button_img_2 = PhotoImage(
            file=os.path.join(self.set_path, 'button_2.png'))
        self.set_button_2 = Button(
            master=self.set_window,
            image=self.set_button_img_2,
            borderwidth=0,
            highlightthickness=0,
            command=self.set_window.destroy,
            relief='flat'
        )
        self.set_button_2.place(
            x=402.0,
            y=572.0,
            width=60.0,
            height=40.0
        )

        #monoartist
        self.set_canvas.create_text(
            138.0,
            109.0,
            anchor='nw',
            text='Monoartist',
            fill='#B3B3B3',
            font=(self.saved_par['font'], 24 * -1)
        )

        self.set_toggle_mono_img = PhotoImage(
            file=os.path.join(self.set_path, toggle_state(self.saved_par['monoartist'])+'.png'))
        self.set_toggle_mono_button = Button(
            master=self.set_window,
            image=self.set_toggle_mono_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.cmd_toggle_monoartist,
            relief='flat'
        )
        self.set_toggle_mono_button.place(
            x=60.0,
            y=108.0,
            width=58.0,
            height=30.0
        )

        #cover art download
        self.set_canvas.create_text(
            390.0,
            109.0,
            anchor='nw',
            text='Download cover art',
            fill='#B3B3B3',
            font=(self.saved_par['font'], 24 * -1)
        )

        self.set_toggle_cover_img = PhotoImage(
            file=os.path.join(self.set_path, toggle_state(self.saved_par['cover_art_dl'])+'.png'))
        self.set_toggle_cover_button = Button(
            master=self.set_window,
            image=self.set_toggle_cover_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.cmd_toggle_cover,
            relief='flat'
        )
        self.set_toggle_cover_button.place(
            x=312.0,
            y=108.0,
            width=58.0,
            height=30.0
        )

        #COMBOBOXES
        self.set_cbx_1 = ttk.Combobox(
            master=self.set_window,
            values=['Tiny', 'Regular'],
            state='readonly',
            justify='center',
            font=(self.saved_par['font'], 14 * -1)
        )
        self.set_cbx_1.current(self.saved_par['screen_size_index'])
        self.set_cbx_1.place(
            x=564.0,
            y=502.0,
            width=136.0,
            height=28.0
        )

        self.set_canvas.create_text(
            564.0,
            464.0,
            anchor='nw',
            text='Size:',
            fill='#B3B3B3',
            font=(self.saved_par['font'], 24 * -1)
        )

        self.set_cbx_2 = ttk.Combobox(
            master=self.set_window,
            values=['128 kBps', '256 kBps', '320 kBps'],
            state='readonly',
            justify='center',
            font=(self.saved_par['font'], 14 * -1)
        )
        self.set_cbx_2.current(self.saved_par['bitrate_index'])
        self.set_cbx_2.place(
            x=312.0,
            y=502.0,
            width=136.0,
            height=28.0
        )

        self.set_canvas.create_text(
            312.0,
            464.0,
            anchor='nw',
            text='Bitrate:',
            fill='#B3B3B3',
            font=(self.saved_par['font'], 24 * -1)
        )

        self.set_cbx_3 = ttk.Combobox(
            master=self.set_window,
            values=['MP3','AAC','OGG (original codec)'],
            state='readonly',
            justify='center',
            font=(self.saved_par['font'], 14 * -1)
        )
        self.set_cbx_3.current(self.saved_par['format_index'])
        self.set_cbx_3.place(
            x=60.0,
            y=502.0,
            width=136.0,
            height=28.0
        )

        self.set_canvas.create_text(
            60.0,
            464.0,
            anchor='nw',
            text='Format:',
            fill='#B3B3B3',
            font=(self.saved_par['font'], 24 * -1)
        )

        #ENTRIES
        self.set_entry_img_1 = PhotoImage(
            file=os.path.join(self.set_path, 'entry_1.png'))
        self.set_entry_bg_1 = self.set_canvas.create_image(
            544.0,
            414.0,
            image=self.set_entry_img_1
        )
        self.set_entry_1 = Entry(
            master=self.set_window,
            bd=0,
            bg='#FFFFFF',
            fg='#000716',
            highlightthickness=0
        )
        self.set_entry_1.place(
            x=398.0,
            y=402.0,
            width=292.0,
            height=26.0
        )
        self.set_entry_1.insert(0,self.saved_par['spotify client secret'])

        self.set_image_img_1 = PhotoImage(
            file=os.path.join(self.set_path, 'image_1.png'))
        self.set_image_1 = self.set_canvas.create_image(
            398.0,
            382.0,
            image=self.set_image_img_1
        )

        self.set_entry_img_2 = PhotoImage(
            file=os.path.join(self.set_path, 'entry_2.png'))
        self.set_entry_bg_2 = self.set_canvas.create_image(
            216.0,
            414.0,
            image=self.set_entry_img_2
        )
        self.set_entry_2 = Entry(
            master=self.set_window,
            bd=0,
            bg='#FFFFFF',
            fg='#000716',
            highlightthickness=0
        )
        self.set_entry_2.place(
            x=70.0,
            y=402.0,
            width=292.0,
            height=26.0
        )
        self.set_entry_2.insert(0, self.saved_par['spotify client id'])

        self.set_image_img_2 = PhotoImage(
            file=os.path.join(self.set_path, 'image_2.png'))
        self.set_image_2 = self.set_canvas.create_image(
            70.0,
            382.0,
            image=self.set_image_img_2
        )

        self.set_image_img_3 = PhotoImage(
            file=os.path.join(self.set_path, 'image_3.png'))
        self.set_image_3 = self.set_canvas.create_image(
            380.0,
            344.0,
            image=self.set_image_img_3
        )

        self.set_entry_img_3 = PhotoImage(
            file=os.path.join(self.set_path, 'entry_3.png'))
        self.set_entry_bg_3 = self.set_canvas.create_image(
            410.0,
            270.0,
            image=self.set_entry_img_3
        )
        self.set_entry_3 = Entry(
            master=self.set_window,
            bd=0,
            bg='#FFFFFF',
            fg='#000716',
            highlightthickness=0
        )
        self.set_entry_3.place(
            x=130.0,
            y=257.0,
            width=560.0,
            height=26.0
        )
        self.set_entry_3.insert(0, self.saved_par['token genius'])

        self.set_image_img_4 = PhotoImage(
            file=os.path.join(self.set_path, 'image_4.png'))
        self.set_image_4 = self.set_canvas.create_image(
            80.0,
            270.0,
            image=self.set_image_img_4
        )

        self.set_entry_img_4 = PhotoImage(
            file=os.path.join(self.set_path, 'entry_4.png'))
        self.set_entry_bg_4 = self.set_canvas.create_image(
            410.0,
            194.0,
            image=self.set_entry_img_4
        )
        self.set_entry_4 = Entry(
            master=self.set_window,
            bd=0,
            bg='#FFFFFF',
            fg='#000716',
            highlightthickness=0
        )
        self.set_entry_4.place(
            x=130.0,
            y=181.0,
            width=560.0,
            height=26.0
        )
        self.set_entry_4.insert(0, self.saved_par['path'])

        self.set_image_img_5 = PhotoImage(
            file=os.path.join(self.set_path, 'image_5.png'))
        self.set_image_5 = self.set_canvas.create_image(
            80.0,
            194.0,
            image=self.set_image_img_5
        )

        #TEXT
        self.set_canvas.create_text(
            303.0,
            24.0,
            anchor='nw',
            text='SETTINGS',
            fill='#B3B3B3',
            font=('Ubuntu Bold', 32 * -1)
        )

        #BIND KEY
        self.set_window.bind(
            '<Return>',
            lambda event : self.cmd_key_return_par())
        self.set_window.bind(
            '<Escape>',
            lambda event : self.cmd_key_escape_par())

        self.set_window.resizable(False, False)
        self.set_window.mainloop()

    def cmd_key_return(self):

        # return key activate the dl button

        self.main_button_1.invoke()

    def cmd_key_return_par(self):

        self.set_button_1.invoke()

    def cmd_key_escape_par(self):

        self.set_button_2.invoke()

    def cmd_save_par(self):

        str_path = self.set_entry_4.get()
        str_genius = self.set_entry_3.get()
        str_spotify_id = self.set_entry_2.get()
        str_spotify_sc =self.set_entry_1.get()
        str_format = self.set_cbx_3.get().lower()

        if 'ogg' in str_format:

            str_format = None

        format_index = self.set_cbx_3.current()
        int_br = int(self.set_cbx_2.get()[:3])*1000
        br_index = self.set_cbx_2.current()
        screen_size_index = self.set_cbx_1.current()
        params = {
            'font': self.saved_par['font'],
            'platform': self.saved_par['platform'],
            'screen_size_index': screen_size_index,
            'cover_art_dl': self.saved_par['cover_art_dl'],
            'monoartist': self.saved_par['monoartist'],
            'path' : str_path,
            'token genius' : str_genius,
            'spotify client id' : str_spotify_id,
            'spotify client secret' : str_spotify_sc,
            'format' : str_format,
            'format_index' : format_index,
            'bitrate' : int_br,
            'bitrate_index' : br_index
        }
        self.saved_par = params

        util.save_param(
            self.saved_par,
            os.path.join(util.file_path(), 'parameters.json'))

        self.set_window.destroy()

    def cmd_toggle_monoartist(self):

        if self.saved_par['monoartist']:

            self.set_toggle_mono_img.configure(file=os.path.join(self.set_path, 'toggle_off.png'))
            self.saved_par['monoartist'] = False

        else:

            self.set_toggle_mono_img.configure(file=os.path.join(self.set_path, 'toggle_on.png'))
            self.saved_par['monoartist'] = True

    def cmd_toggle_cover(self):

        if self.saved_par['cover_art_dl']:

            self.set_toggle_cover_img.configure(file=os.path.join(self.set_path, 'toggle_off.png'))
            self.saved_par['cover_art_dl'] = False

        else:

            self.set_toggle_cover_img.configure(file=os.path.join(self.set_path, 'toggle_on.png'))
            self.saved_par['cover_art_dl'] = True

    def cmd_download(self):

        url = self.main_entry_1.get()
        url_list = info.info_playlist(url)
        total_link = len(url_list)
        info_tags=[]

        #intialize loading screen

        # loading_metadata = loading_window()
        # loading_metadata._init_loading(self.main_window, total_link,'Downloading metadata 1/'+str(total_link))
        # loading_metadata.open_loading()

        #save songs data

        for i in range(total_link):

            info_tags.append(info.info_query_url(url_list[i]))
        #     loading_metadata.progress_label = 'Downloading metadata '+str(i-1)+'/'+str(total_link)
        #     loading_metadata.progress()
        #
        # loading_metadata.stop()

        #initialize data

        info_init = deepcopy(info_tags)
        total_modified = 0
        total_cancel = 0
        index_link = 0
        total_dl = 0
        cancel = False
        modified = False
        lst_key = [
            'title',
            'title ft',
            'album',
            'artist',
            'album artist',
            'track',
            'total track',
            'date',
            'publisher',
            'lyrics',
            'genre',
            'language',
            'composer',
            'text writer',
            'desc',
            'year',
            'art url']
        
        self.main_window.destroy()

        for index_link in range(total_link):

            info_tag = info_tags[index_link]
            dl_window = dl_win()
            dl_window.__init_win__(
                index_link,
                total_link,
                total_modified,
                total_cancel,
                total_dl,
                info_tag,
                self.saved_par,
                self.software_path,
                url_list[index_link]
            )
            dl_window.open_dl()

            if dl_window.cancelall == True:

                break

            elif dl_window.cancel == False:

                if dl_window.song_tag != info_init[index_link]:

                    total_modified += 1

                total_dl += 1

            elif dl_window.cancel == True:

                total_cancel += 1

        main_window = main_win()

        #load saved parameters

        saved_par = util.read_param(
            os.path.join(self.software_path, 'parameters.json'))
        main_window.__init_main__(saved_par, self.software_path)
        main_window.open_main()