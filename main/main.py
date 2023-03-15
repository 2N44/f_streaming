import os
import platform
import gui
import util


def main():

    #locate file

    software_path = util.file_path()

    #load saved parameters

    saved_par = util.read_param(os.path.join(software_path, 'parameters.json'))

    #default downloads path

    if saved_par['path'] == '':

        saved_par['path'] = os.path.join(software_path,'Music')
        util.save_param(saved_par, os.path.join(util.file_path(), 'parameters.json'))

    #check platfrom

    current_platform = platform.system()

    if saved_par['platform'] != current_platform:

        saved_par['platform'] = current_platform

    #update font to fit the platform

    if saved_par['platform'] == 'Linux':

        saved_par['font'] == 'Liberation Sans'

    if saved_par['platform'] == 'Windows':

        saved_par['font'] == 'Arial'

    #open GUI

    main_window = gui.main_win()
    main_window.__init_main__(saved_par, software_path)
    main_window.open_main()



if __name__ == '__main__':

    main()