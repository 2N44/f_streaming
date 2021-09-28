import gui
import command as cmd
import os


def main():
    #locate file

    software_path = cmd.file_path()

    #load saved parameters

    saved_par = cmd.read_param(os.path.join(software_path, 'parameters.json'))

    if saved_par['path'] == '':

        saved_par['path'] == software_path
        cmd.save_param(saved_par, os.path.join(cmd.file_path(), 'parameters.json'))

    #open GUI

    main_window = gui.main_win()
    main_window.__init_main__(saved_par,software_path)
    main_window.open_main()



if __name__ == '__main__':

    main()