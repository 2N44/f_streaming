##
#
# functions and class for the GUI
#
##

import sys, json, os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from copy import deepcopy
import dler as dl
import info_query as info
import command as cmd
import tag



class dl_win():

    def __init_win__(self, index_link, total_link, total_modified, total_cancel, total_dl, song_tag, saved_param,url):

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
        self.index_tab = 1
        self.saved_par = saved_param
        self.url = url

    def cmd_savelyrics(self):

        self.song_tag['lyrics']=self.txt_lyrics.get("1.0", 'end-1c')
        self.lyrics_window.destroy()

    def cmd_cancellyrics(self):

        self.lyrics_window.destroy()

    def cmd_cancelone(self):

        self.cancel_window.destroy()
        self.dl_window.destroy()
        self.cancel = True

    def cmd_cancelall(self):

        self.cancel_window.destroy()
        self.dl_window.destroy()
        self.cancelall = True

    def tab_selected(self, event):

        selected_tab = event.widget.select()
        tab_text = event.widget.tab(selected_tab, "text")
        if tab_text == 'Monoartist':
            self.index_tab = 1
        else:
            self.index_tab = 2


    def cmd_savemp3(self):

        # #initialize loading screen
        # loading_dl = loading_window()
        # loading_dl.__init__loading(self.dl_window, 5, 'Loading metadata ...')
        # loading_dl.open_loading()

        #save

        self.from_time = cmd.sub_time(self.ent_init.get(), '00:00;15')
        self.to_time = cmd.add_time(cmd.sub_time(self.ent_final.get(), self.from_time),'00:00:15')

        if self.index_tab == 1:

            self.song_tag['title ft'] = self.ent_ent1_v1.get()
            self.song_tag['album artist'] = self.ent_ent2_v1.get()
            self.song_tag['album'] = self.ent_ent3_v1.get()
            self.song_tag['composer'] = self.ent_ent6_v1.get()
            self.song_tag['publisher'] = self.ent_ent7_v1.get()
            self.song_tag['genre'] = self.ent_ent8_v1.get()
            self.song_tag['date'] = self.ent_ent9_v1.get()
            self.song_tag['album_path'] = cmd.check_filename(self.song_tag['album'])

            if self.ent_ent4_v1.get() != '':

                self.song_tag['track'] = int(self.ent_ent4_v1.get())

            else:

                self.song_tag['track'] = None

            if self.ent_ent5_v1.get() != '':

                self.song_tag['total track'] = int(self.ent_ent5_v1.get())

            else:

                self.song_tag['total track'] = None

            path =  os.path.join(self.saved_par['path'], self.song_tag['album_path'])

            # loading_dl.progress_label = 'Creating directory ...'
            # loading_dl.progress()

            #make directory

            cmd.mkdir_album(path)

            # loading_dl.progress_label = 'Downloading cover art ...'
            # loading_dl.progress()

            #download art

            dl.dl_art(path, self.song_tag)

            # loading_dl.progress_label = 'Downloading audio file ...'
            # loading_dl.progress()

            #download mp3      
           
            if not cmd.check_audiofile(self.saved_par, self.song_tag):

                dl.dl_from_to(self.url, self.from_time, self.to_time, os.path.join(path, cmd.check_filename(self.song_tag['title'])), self.saved_par['format'], self.saved_par['bitrate'])

            else:

                print('Already downloaded')

            # loading_dl.progress_label = 'Tagging audio file ...'
            # loading_dl.progress()

            #tag mp3

            if self.saved_par['format'] == 'mp3':

                path = os.path.join(path, cmd.check_filename(self.song_tag['title'])+'.mp3')
                tag.tag_v1(path, self.song_tag)

            # loading_dl.progress_label = 'Done'
            # loading_dl.stop()

        else :

            self.song_tag['title'] = self.ent_ent1_v2.get()
            self.song_tag['artist'] = self.ent_ent2_v2.get()
            self.song_tag['album'] = self.ent_ent3_v2.get()
            self.song_tag['album artist'] = self.ent_ent4_v2.get()
            self.song_tag['track'] = int(self.ent_ent5_v2.get())
            self.song_tag['total track'] = int(self.ent_ent6_v2.get())
            self.song_tag['composer'] = self.ent_ent7_v2.get()
            self.song_tag['publisher'] = self.ent_ent8_v2.get()
            self.song_tag['genre'] = self.ent_ent9_v2.get()
            self.song_tag['date'] = self.ent_ent10_v2.get()
            self.from_time = self.ent_init.get()
            self.to_time = self.ent_final.get()
            self.song_tag['album_path'] = cmd.check_filename(self.song_tag['album'])

            path =  os.path.join(self.saved_par['path'], self.song_tag['album_path'])

            # loading_dl.progress_label = 'Creating directory ...'
            # loading_dl.progress()

            #make album directory

            cmd.mkdir_album(path)

            # loading_dl.progress_label = 'Downloading cover art ...'
            # loading_dl.progress()

            #download art

            dl.dl_art(path, self.song_tag)

            # loading_dl.progress_label = 'Downloading audio file ...'
            # loading_dl.progress()

            #download mp3

            if not cmd.check_audiofile(self.saved_par, self.song_tag):

                dl.dl_from_to(self.url, self.from_time, self.to_time, os.path.join(path, cmd.check_filename(self.song_tag['title'])), self.saved_par['format'], self.saved_par['bitrate'])

            else:

                print('Already downloaded')

            # loading_dl.progress_label = 'Tagging audio file ...'
            # loading_dl.progress()

            #tag mp3

            if self.saved_par['format'] == 'mp3':

                path = os.path.join(path, cmd.check_filename(self.song_tag['title']) + '.mp3')
                tag.tag_v2(path, self.song_tag)

            # loading_dl.progress_label = 'Done'
            # loading_dl.stop()

        self.dl_window.destroy()



    def cmd_retry(self):

        if self.index_tab:

            search_title = str(self.ent_ent1_v1.get())+' - '+str(self.ent_ent2_v1.get())

        else:

            search_title = str(self.ent_ent1_v2.get())+' - '+str(self.ent_ent2_v2.get())

        self.song_tag = info.info_query_title(search_title, self.song_tag['length'])
        self.ent_ent1_v1.delete(0, "end")
        self.ent_ent2_v1.delete(0, "end")
        self.ent_ent3_v1.delete(0, "end")
        self.ent_ent4_v1.delete(0, "end")
        self.ent_ent5_v1.delete(0, "end")
        self.ent_ent6_v1.delete(0, "end")
        self.ent_ent7_v1.delete(0, "end")
        self.ent_ent8_v1.delete(0, "end")
        self.ent_ent1_v1.insert(0, self.song_tag['title'])
        self.ent_ent2_v1.insert(0, self.song_tag['album artist'])
        self.ent_ent3_v1.insert(0, self.song_tag['album'])
        self.ent_ent4_v1.insert(0, self.song_tag['track'])
        self.ent_ent5_v1.insert(0, self.song_tag['total track'])
        self.ent_ent6_v1.insert(0, self.song_tag['composer'])
        self.ent_ent7_v1.insert(0, self.song_tag['publisher'])
        self.ent_ent8_v1.insert(0, self.song_tag['genre'])

        self.ent_ent1_v2.delete(0, "end")
        self.ent_ent2_v2.delete(0, "end")
        self.ent_ent3_v2.delete(0, "end")
        self.ent_ent4_v2.delete(0, "end")
        self.ent_ent5_v2.delete(0, "end")
        self.ent_ent6_v2.delete(0, "end")
        self.ent_ent7_v2.delete(0, "end")
        self.ent_ent8_v2.delete(0, "end")
        self.ent_ent9_v2.delete(0, "end")
        self.ent_ent10_v2.delete(0, "end")
        self.ent_ent1_v2.insert(0, self.song_tag['title'])
        self.ent_ent2_v2.insert(0, self.song_tag['artist'])
        self.ent_ent3_v2.insert(0, self.song_tag['album'])
        self.ent_ent4_v2.insert(0, self.song_tag['album artist'])
        self.ent_ent5_v2.insert(0, self.song_tag['track'])
        self.ent_ent6_v2.insert(0, self.song_tag['total track'])
        self.ent_ent7_v2.insert(0, self.song_tag['composer'])
        self.ent_ent8_v2.insert(0, self.song_tag['publisher'])
        self.ent_ent9_v2.insert(0, self.song_tag['genre'])
        self.ent_ent10_v2.insert(0, self.song_tag['date'])



    def cmd_key_return(self):

        self.btn_save.invoke()



    def cmd_key_escape(self):

        self.btn_cancel.invoke()



    def lyrics_win(self):

        #open window

        self.lyrics_window = tk.Toplevel(self.dl_window)
        self.lyrics_window.title('Lyrics of '+str(self.song_tag['title']))

        #grid

        self.lyrics_window.columnconfigure(0, minsize=500,weight=1)

        #frames

        frm_text = tk.Frame(master=self.lyrics_window)
        frm_btns =tk.Frame(master=self.lyrics_window)

        #label

        lbl_title = tk.Label(master=frm_text, text = str(self.song_tag['title'])+' :')

        #text_box

        self.txt_lyrics = tk.Text(master=frm_text)
        self.txt_lyrics.insert('1.0', self.song_tag['lyrics'])

        #buttons

        btn_save = tk.Button(
        master=frm_btns,
        text='Save',
        command=self.cmd_savelyrics
        )
        btn_cancel = tk.Button(
        master=frm_btns,
        text='Cancel',
        command=self.cmd_cancellyrics
        )

        #display

        btn_save.grid(row=0, column=0, sticky='ns',padx=5, pady=5)
        btn_cancel.grid(row=0, column=1, sticky='ns',padx=5, pady=5)
        lbl_title.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.txt_lyrics.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)

        frm_text.grid(row=0, column=0, sticky='nsew')
        frm_btns.grid(row=1, column=0, sticky='ew')



    def cancel_win(self):

        #open window

        self.cancel_window = tk.Toplevel(self.dl_window)
        self.cancel_window.title('Warning')

        #grid

        self.cancel_window.columnconfigure(0, minsize=500,weight=1)

        #frames

        frm_msg = tk.Frame(master=self.cancel_window)
        frm_btns =tk.Frame(master=self.cancel_window)

        #label

        lbl_msg = tk.Label(master=frm_msg, text='Do you want to cancel this download or all of them ?')

        #button

        btn_one = tk.Button(
        master=frm_btns,
        text='Cancel this one',
        command=self.cmd_cancelone
        )
        btn_all = tk.Button(
        master=frm_btns,
        text='Cancel all',
        command=self.cmd_cancelall
        )

        #display

        btn_one.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        btn_all.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
        lbl_msg.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        frm_msg.grid(row=0, column=0, sticky='nsew')
        frm_btns.grid(row=0, column=1, sticky='ns')



    def open_dl(self):

        self.dl_window = tk.Tk()
        self.dl_window.title(self.song_tag['title']+'.mp3')        
        self.dl_window.iconphoto(True, tk.PhotoImage(file='fstreaming_icon.png'))

        # create a notebook

        self.notebook = ttk.Notebook(self.dl_window)
        self.notebook.grid(row=1, column=0, sticky ='ew', padx=5, pady=5)

        # create frames

        frame1 = ttk.Frame(master=self.notebook)
        frame2 = ttk.Frame(master=self.notebook)
        frm_head = tk.Frame(master=self.dl_window)
        frm_time = tk.Frame(master=frm_head)
        frm_ent_s = tk.Frame(master=frm_time)
        frm_ent_f = tk.Frame(master=frm_time)
        frm_count = tk.Frame(master=frm_head)
        frm_btns = tk.Frame(master=self.dl_window)
        frm_lyrics = tk.Frame(master=self.dl_window)

        frm_head.grid(row=0, column=0, sticky='nsew')
        frame1.grid(row=0, column=0, sticky='nsew')
        frame2.grid(row=0, column=1, sticky='nsew')
        frm_lyrics.grid(row=2, column=0)
        frm_btns.grid(row=3, column=0, sticky='ns')
        frm_time.grid(row=0, column=0, sticky='ns')
        frm_count.grid(row=0, column=1, sticky='ns')
        frm_ent_s.grid(row=0, column=0, sticky='ew')
        frm_ent_f.grid(row=1, column=0, sticky='ew')

        frm_ent1_v1 = ttk.Frame(master=frame1)
        frm_ent2_v1 = ttk.Frame(master=frame1)
        frm_ent3_v1 = ttk.Frame(master=frame1)
        frm_ent4_v1 = ttk.Frame(master=frame1)
        frm_ent5_v1 = ttk.Frame(master=frame1)
        frm_ent6_v1 = ttk.Frame(master=frame1)
        frm_ent7_v1 = ttk.Frame(master=frame1)
        frm_ent8_v1 = ttk.Frame(master=frame1)
        frm_ent9_v1 = ttk.Frame(master=frame1)
        frm_ent1_v2 = ttk.Frame(master=frame2)
        frm_ent2_v2 = ttk.Frame(master=frame2)
        frm_ent3_v2 = ttk.Frame(master=frame2)
        frm_ent4_v2 = ttk.Frame(master=frame2)
        frm_ent5_v2 = ttk.Frame(master=frame2)
        frm_ent6_v2 = ttk.Frame(master=frame2)
        frm_ent7_v2 = ttk.Frame(master=frame2)
        frm_ent8_v2 = ttk.Frame(master=frame2)
        frm_ent9_v2 = ttk.Frame(master=frame2)
        frm_ent10_v2 = ttk.Frame(master=frame2)

        lbl_ent1_v1 = ttk.Label(master=frm_ent1_v1, text='Title (ft.) :')
        lbl_ent2_v1 = ttk.Label(master=frm_ent2_v1, text='Artist :')
        lbl_ent3_v1 = ttk.Label(master=frm_ent3_v1, text='Album :')
        lbl_ent4_v1 = ttk.Label(master=frm_ent4_v1, text='Track n° :')
        lbl_ent5_v1 = ttk.Label(master=frm_ent5_v1, text='Total track :')
        lbl_ent6_v1 = ttk.Label(master=frm_ent6_v1, text='Composer :')
        lbl_ent7_v1 = ttk.Label(master=frm_ent7_v1, text='Publisher :')
        lbl_ent8_v1 = ttk.Label(master=frm_ent8_v1, text='Genre :')
        lbl_ent9_v1 = ttk.Label(master=frm_ent9_v1, text='Date :')
        lbl_ent1_v2 = ttk.Label(master=frm_ent1_v2, text='Title :')
        lbl_ent2_v2 = ttk.Label(master=frm_ent2_v2, text='Artists :')
        lbl_ent3_v2 = ttk.Label(master=frm_ent3_v2, text='Album :')
        lbl_ent4_v2 = ttk.Label(master=frm_ent4_v2, text='Album artist :')
        lbl_ent5_v2 = ttk.Label(master=frm_ent5_v2, text='Track n°  :')
        lbl_ent6_v2 = ttk.Label(master=frm_ent6_v2, text='Total track :')
        lbl_ent7_v2 = ttk.Label(master=frm_ent7_v2, text='Composer :')
        lbl_ent8_v2 = ttk.Label(master=frm_ent8_v2, text='Publisher :')
        lbl_ent9_v2 = ttk.Label(master=frm_ent9_v2, text='Genre :')
        lbl_ent10_v2 = ttk.Label(master=frm_ent10_v2, text='Date :')
        lbl_count1 = tk.Label(master=frm_count, text=str(self.index_link+1)+'/'+str(self.total_link))
        lbl_count2 = tk.Label(master=frm_count, text=str(self.total_canceled)+' canceled')
        lbl_count3 = tk.Label(master=frm_count, text=str(self.total_modified)+' modified')
        lbl_count4 = tk.Label(master=frm_count, text=str(self.total_dl)+' downloaded')
        lbl_init = tk.Label(master=frm_ent_s, text='Starting time :')
        lbl_final = tk.Label(master=frm_ent_f, text='Ending time :')


        self.ent_ent1_v1 = ttk.Entry(master=frm_ent1_v1)
        self.ent_ent2_v1 = ttk.Entry(master=frm_ent2_v1)
        self.ent_ent3_v1 = ttk.Entry(master=frm_ent3_v1)
        self.ent_ent4_v1 = ttk.Entry(master=frm_ent4_v1)
        self.ent_ent5_v1 = ttk.Entry(master=frm_ent5_v1)
        self.ent_ent6_v1 = ttk.Entry(master=frm_ent6_v1)
        self.ent_ent7_v1 = ttk.Entry(master=frm_ent7_v1)
        self.ent_ent8_v1 = ttk.Entry(master=frm_ent8_v1)
        self.ent_ent9_v1 = ttk.Entry(master=frm_ent9_v1)
        self.ent_ent1_v2 = ttk.Entry(master=frm_ent1_v2)
        self.ent_ent2_v2 = ttk.Entry(master=frm_ent2_v2)
        self.ent_ent3_v2 = ttk.Entry(master=frm_ent3_v2)
        self.ent_ent4_v2 = ttk.Entry(master=frm_ent4_v2)
        self.ent_ent5_v2 = ttk.Entry(master=frm_ent5_v2)
        self.ent_ent6_v2 = ttk.Entry(master=frm_ent6_v2)
        self.ent_ent7_v2 = ttk.Entry(master=frm_ent7_v2)
        self.ent_ent8_v2 = ttk.Entry(master=frm_ent8_v2)
        self.ent_ent9_v2 = ttk.Entry(master=frm_ent9_v2)
        self.ent_ent10_v2 = ttk.Entry(master=frm_ent10_v2)
        self.ent_init = ttk.Entry(master=frm_ent_s)
        self.ent_final = ttk.Entry(master=frm_ent_f)
        self.ent_ent1_v1.insert(0, self.song_tag['title ft'])
        self.ent_ent2_v1.insert(0, self.song_tag['album artist'])
        self.ent_ent3_v1.insert(0, self.song_tag['album'])
        self.ent_ent4_v1.insert(0, self.song_tag['track'])
        self.ent_ent5_v1.insert(0, self.song_tag['total track'])
        self.ent_ent6_v1.insert(0, self.song_tag['composer'])
        self.ent_ent7_v1.insert(0, self.song_tag['publisher'])
        self.ent_ent8_v1.insert(0, self.song_tag['genre'])
        self.ent_ent9_v1.insert(0, self.song_tag['date'])
        self.ent_ent1_v2.insert(0, self.song_tag['title'])
        self.ent_ent2_v2.insert(0, self.song_tag['artist'])
        self.ent_ent3_v2.insert(0, self.song_tag['album'])
        self.ent_ent4_v2.insert(0, self.song_tag['album artist'])
        self.ent_ent5_v2.insert(0, self.song_tag['track'])
        self.ent_ent6_v2.insert(0, self.song_tag['total track'])
        self.ent_ent7_v2.insert(0, self.song_tag['composer'])
        self.ent_ent8_v2.insert(0, self.song_tag['publisher'])
        self.ent_ent9_v2.insert(0, self.song_tag['genre'])
        self.ent_ent10_v2.insert(0, self.song_tag['date'])
        self.ent_init.insert(0, self.from_time)
        self.ent_final.insert(0, self.to_time)

        #button

        btn_lyrics= tk.Button(
        master=frm_lyrics,
        command=self.lyrics_win,
        text='Lyrics',
        )
        btn_retry = tk.Button(
        master=frm_btns,
        command = self.cmd_retry,
        text='Retry',
        )
        self.btn_save = tk.Button(
        master=frm_btns,
        command = self.cmd_savemp3,
        text='Save',
        )
        self.btn_cancel = tk.Button(
        master=frm_btns,
        command = self.cancel_win,
        text='Cancel',
        )


        lbl_ent1_v1.grid(row=0, column=0, sticky='w')
        lbl_ent2_v1.grid(row=0, column=0, sticky='w')
        lbl_ent3_v1.grid(row=0, column=0, sticky='w')
        lbl_ent4_v1.grid(row=0, column=0, sticky='w')
        lbl_ent5_v1.grid(row=0, column=0, sticky='w')
        lbl_ent6_v1.grid(row=0, column=0, sticky='w')
        lbl_ent7_v1.grid(row=0, column=0, sticky='w')
        lbl_ent8_v1.grid(row=0, column=0, sticky='w')
        lbl_ent9_v1.grid(row=0, column=0, sticky='w')
        lbl_ent1_v2.grid(row=0, column=0, sticky='w')
        lbl_ent2_v2.grid(row=0, column=0, sticky='w')
        lbl_ent3_v2.grid(row=0, column=0, sticky='w')
        lbl_ent4_v2.grid(row=0, column=0, sticky='w')
        lbl_ent5_v2.grid(row=0, column=0, sticky='w')
        lbl_ent6_v2.grid(row=0, column=0, sticky='w')
        lbl_ent7_v2.grid(row=0, column=0, sticky='w')
        lbl_ent8_v2.grid(row=0, column=0, sticky='w')
        lbl_ent9_v2.grid(row=0, column=0, sticky='w')
        lbl_ent10_v2.grid(row=0, column=0, sticky='w')
        lbl_count1.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        lbl_count2.grid(row=1, column=0, sticky='ns', padx=5, pady=5)
        lbl_count3.grid(row=2, column=0, sticky='ns', padx=5, pady=5)
        lbl_count4.grid(row=3, column=0, sticky='ns', padx=5, pady=5)
        lbl_init.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        lbl_final.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.ent_ent1_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent2_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent3_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent4_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent5_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent6_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent7_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent8_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent9_v1.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent1_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent2_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent3_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent4_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent5_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent6_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent7_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent8_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent9_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_ent10_v2.grid(row=1, column=0, sticky='w' ,padx=5, pady=5, ipadx=100)
        self.ent_init.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        self.ent_final.grid(row=1, column=0, sticky='ew', padx=5, pady=5)

        btn_lyrics.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        btn_retry.grid(row=0, column=0, sticky='ns', padx=5, pady=5)
        self.btn_save.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
        self.btn_cancel.grid(row=0, column=2, sticky='ns', padx=5, pady=5)

        frm_ent1_v1.grid(row=0, column=0 , sticky='ew')
        frm_ent2_v1.grid(row=0, column=1 , sticky='ew')
        frm_ent3_v1.grid(row=1, column=0 , sticky='ew')
        frm_ent4_v1.grid(row=1, column=1 , sticky='ew')
        frm_ent5_v1.grid(row=2, column=0 , sticky='ew')
        frm_ent6_v1.grid(row=2, column=1 , sticky='ew')
        frm_ent7_v1.grid(row=3, column=0 , sticky='ew')
        frm_ent8_v1.grid(row=3, column=1 , sticky='ew')
        frm_ent9_v1.grid(row=4, column=0 , sticky='ew')
        frm_ent1_v2.grid(row=0, column=0 , sticky='ew')
        frm_ent2_v2.grid(row=0, column=1 , sticky='ew')
        frm_ent3_v2.grid(row=1, column=0 , sticky='ew')
        frm_ent4_v2.grid(row=1, column=1 , sticky='ew')
        frm_ent5_v2.grid(row=2, column=0 , sticky='ew')
        frm_ent6_v2.grid(row=2, column=1 , sticky='ew')
        frm_ent7_v2.grid(row=3, column=0 , sticky='ew')
        frm_ent8_v2.grid(row=3, column=1 , sticky='ew')
        frm_ent9_v2.grid(row=4, column=0 , sticky='ew')
        frm_ent10_v2.grid(row=4, column=1 , sticky='ew')

        # add frames to notebook

        self.notebook.bind("<<NotebookTabChanged>>", self.tab_selected)
        self.notebook.add(frame1, text='Monoartist')
        self.notebook.add(frame2, text='Multiple artists')

        #bind keys

        self.dl_window.bind('<Return>', lambda event : self.cmd_key_return())
        self.dl_window.bind('<Escape>', lambda event : self.cmd_key_escape())

        self.dl_window.mainloop()



class main_win():

    def __init_main__(self, saved_par, software_path):

        self.saved_par = saved_par
        self.software_path = software_path
        

    def open_main(self):

        #open window

        self.main_window = tk.Tk()
        self.main_window.title('F_streaming')
        self.main_window.iconphoto(True, tk.PhotoImage(file='fstreaming_icon.png'))

        #grid

        self.main_window.columnconfigure(0, minsize=200, weight=1)
        self.main_window.rowconfigure(1, minsize=50, weight=1)

        #frames

        frm_title = tk.Frame(master=self.main_window)
        frm_dl = tk.Frame(master=self.main_window)

        #lbl_title = tk.Label(master=frm_title,text="F_streaming",bg='red',fg='white',width=15,height=3)
        self.logo = ImageTk.PhotoImage(Image.open('logo_resize.png'))
        lbl_title = tk.Label(master=frm_title, image=self.logo)

        self.ent_url = tk.Entry(master=frm_dl,width=50)
        self.ent_url.insert(0,'Video URL')

        #buttons

        btn_par = tk.Button(
            master=frm_dl,
            text="Parameters",
            width=8,
            height=3,
            command = self.par_win,
        )
        self.btn_dl = tk.Button(
            master=frm_dl,
            text="Download",
            width=8,
            height=3,
            command = self.cmd_opendl
        )

        #display

        lbl_title.grid(row=0, column=0, sticky='nsew')
        self.ent_url.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.btn_dl.grid(row=0, column=1, sticky='ew', padx=0, pady=5)
        btn_par.grid(row=0, column=2, sticky='ew', padx=5, pady=5)

        frm_title.grid(row=0, column=0, sticky='ns')
        frm_dl.grid(row=1, column=0, sticky='nsew')

        #bind keypress event

        self.main_window.bind('<Return>', lambda event : self.cmd_key_return())

        self.main_window.mainloop()



    def par_win(self):#finir affichage des datas

        #open window

        self.par_window = tk.Toplevel(self.main_window)
        self.par_window.title('Parameters')

        #grid

        self.par_window.columnconfigure(0, minsize=500,weight=1)

        #frames

        frm_token = tk.Frame(master=self.par_window)
        frm_par = tk.Frame(master=self.par_window)
        frm_name = tk.Frame(master=frm_par)
        frm_str = tk.Frame(master=frm_par)
        frm_fmt = tk.Frame(master=frm_par)
        frm_btns = tk.Frame(master=self.par_window)

        #label

        lbl_path = tk.Label(master=frm_name, text='Directory path :')
        lbl_genius = tk.Label(master=frm_name, text='Token Genius :')
        lbl_sp_id = tk.Label(master=frm_name, text='Spotify client ID :')
        lbl_sp_sc = tk.Label(master=frm_name, text='Spotify client secret :')
        lbl_format = tk.Label(master=frm_fmt, text='Format :')
        lbl_br = tk.Label(master=frm_fmt, text='Bitrates :')

        #entry

        self.ent_path = tk.Entry(master=frm_str)
        self.ent_genius = tk.Entry(master=frm_str)
        self.ent_sp_id = tk.Entry(master=frm_str)
        self.ent_sp_sc = tk.Entry(master=frm_str)
        self.ent_path.insert(0,self.saved_par['path'])
        self.ent_genius.insert(0,self.saved_par['token genius'])
        self.ent_sp_id.insert(0,self.saved_par['spotify client id'])
        self.ent_sp_sc.insert(0,self.saved_par['spotify client secret'])

        #button

        self.btn_save = tk.Button(
        master=frm_btns,
        command=self.cmd_save_par,
        text='Save',
        )
        self.btn_cancel = tk.Button(
        master=frm_btns,
        command=self.par_window.destroy,
        text='Cancel',
        )

        #combobox

        self.cbb_fmt = ttk.Combobox(
        master=frm_fmt,
        values=['MP3','AAC','OGG (original codec)']
        )
        self.cbb_fmt.current(self.saved_par['format_index'])
        self.cbb_br = ttk.Combobox(
        master=frm_fmt,
        values=['128 kBps','256 kBps','320 kBps']
        )
        self.cbb_br.current(self.saved_par['bitrate_index'])


        #display

        self.btn_save.grid(row=0, column=0, sticky='e', pady=5)
        self.btn_cancel.grid(row=0, column=1, sticky='e',padx=5, pady=5)
        self.cbb_fmt.grid(row=0, column=1, padx=5, pady=5)
        self.cbb_br.grid(row=0, column=3, padx=5, pady=5)
        lbl_format.grid(row=0, column=0, padx=5, pady=5)
        lbl_br.grid(row=0, column=2, padx=5, pady=5)
        lbl_path.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        lbl_genius.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        lbl_sp_id.grid(row=2, column=0, sticky='e', padx=5, pady=5)
        lbl_sp_sc.grid(row=3, column=0, sticky='e',padx=5, pady=5)
        self.ent_path.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        self.ent_genius.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        self.ent_sp_id.grid(row=2, column=0, sticky='ew', padx=5, pady=5, ipadx=200)
        self.ent_sp_sc.grid(row=3, column=0, sticky='ew', padx=5, pady=5, ipadx=200)

        frm_name.grid(row=0, column=0, sticky='ew')
        frm_str.grid(row=0, column=1, sticky='ew')
        frm_par.grid(row=0, column=0, sticky='nsew',padx=5, pady=8)
        frm_fmt.grid(row=1, column=0, sticky='ew')
        frm_btns.grid(row=2, column=0, sticky='ns')

        #bind keys to the window

        self.par_window.bind('<Return>', lambda event : self.cmd_key_return_par())
        self.par_window.bind('<Escape>', lambda event : self.cmd_key_escape_par())



    def cmd_opendl(self): #rajouter un chargement lors du lecture des infos

        url = self.ent_url.get()
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
        lst_key = ['title', 'title ft', 'album', 'artist', 'album artist', 'track', 'total track', 'date', 'publisher', 'lyrics', 'genre', 'language', 'composer', 'text writer', 'year', 'art url']
        
        self.main_window.destroy()

        for index_link in range(total_link):

            info_tag = info_tags[index_link]
            dl_window = dl_win()
            dl_window.__init_win__(index_link, total_link, total_modified, total_cancel, total_dl, info_tag, self.saved_par, url_list[index_link])
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

        saved_par = cmd.read_param(os.path.join(self.software_path, 'parameters.json'))
        main_window.__init_main__(saved_par, self.software_path)
        main_window.open_main()



    def cmd_key_return(self):

        # return key activate the dl button

        self.btn_dl.invoke()



    def cmd_key_return_par(self):

        self.btn_save.invoke()



    def cmd_key_escape_par(self):

        self.btn_cancel.invoke()



    def cmd_save_par(self):

        str_path = self.ent_path.get()
        str_genius = self.ent_genius.get()
        str_spotify_id = self.ent_sp_id.get()
        str_spotify_sc =self.ent_sp_sc.get()
        str_format = self.cbb_fmt.get().lower()

        if 'ogg' in str_format:

            str_format = None

        format_index = self.cbb_fmt.current()
        int_br = int(self.cbb_br.get()[:3])*1000
        br_index = self.cbb_br.current()
        params = {
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

        cmd.save_param(self.saved_par, os.path.join(cmd.file_path(), 'parameters.json'))

        self.par_window.destroy()


#not used yet (need multithreading)
class loading_window():

    def _init_loading(self, root_window, total_queue, label):

        self.root_window = root_window
        self.inter_queue = 100/total_queue
        self.progress_label = label

    def update_progress_label(self):

        return self.progress_label


    def progress(self):

        if self.pb['value'] < 100:

            self.pb['value'] += self.inter_queue
            self.lbl_msg['text'] = self.update_progress_label()

        else:

            showinfo(message='Done')


    def stop(self):

        self.pb.stop()
        self.progress_label = 'Done'
        self.load_window.destroy()

    def open_loading(self):

        self.load_window = tk.Toplevel(self.root_window)
        self.load_window.title('Loading ...')

        # label
        self.lbl_msg = ttk.Label(master=self.load_window, text=self.progress_label)

        # progressbar
        self.pb = ttk.Progressbar(
        master=self.load_window,
        orient='horizontal',
        mode='determinate',
        length=280
        )

        self.lbl_msg.grid(row=1, column=0, columnspan=2)
        self.pb.grid(row=0, column=0, columnspan=2, padx=10, pady=20)
