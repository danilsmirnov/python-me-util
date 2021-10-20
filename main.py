import time
from tkinter import *
import pandas as pd
from icecream import ic

from utils import browser, PDScrapper, NRScrapper
from config import Config
from prettytable import PrettyTable


def create_window(name: str, height: int, width: int, resizable: bool):
    size = f'{height}x{width}'
    window = Tk()
    window.title(name)
    window.geometry(size)
    window.resizable(width=resizable, height=resizable)
    return window


def launch_pd():
    global pd
    button_pd.config(text='PD launched')
    pd = browser(Config.PD_URL)
    pd.driver.minimize_window()
    time.sleep(1)
    scrape_pd()


def launch_nr():
    global nr
    nr = browser(Config.NR_URL)
    nr.driver.minimize_window()
    button_nr.config(text='NR launched')
    time.sleep(1)
    scrape_nr()


def scrape_pd():
    global frame_right
    pd.refresh()
    time.sleep(10)
    scrapper = PDScrapper(pd)
    frame_right.destroy()
    frame_right = Frame(window, bd=5)
    frame_right.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.95)
    pd_checks_frame = Frame(frame_right)
    title = Label(pd_checks_frame, text=f'Total failed checks at {time.asctime()}')
    title.pack()
    errors = scrapper.get_errors()
    for error in errors:
        #print(error.get_text(), error, type(error), sep='\n')
        table_item = []
        for item in error:
            table_item.append(item.get_text())
        item = {
            'Check': table_item[0],
            'Started': table_item[1],
            'Ended': table_item[2]
        }
        check_color = '#bb0000' if item['Ended'] == 'Ongoing' else None
        text = f'{table_item[0]} from {table_item[1]}, status: {table_item[2]}'
        error_frame = Frame(pd_checks_frame, bd=5)
        check = Label(error_frame, text=table_item[0], font=("Courier", 9))
        started = Label(error_frame, text=table_item[1], font=("Courier", 9))
        ended = Label(error_frame, text=table_item[2], font=("Courier", 9), bg=check_color)
        check.grid(row=0, column=1, sticky='w') # pack(anchor='w')
        started.grid(row=0, column=2, sticky='n') # pack(anchor='center')
        ended.grid(row=0, column=0, sticky='e') # pack(anchor='e')
        error_frame.pack(anchor='w', expand=True, fill=BOTH)
    pd_checks_frame.place(relwidth=1)

    window.after(50000, scrape_pd)


def scrape_nr():
    nr.refresh()
    time.sleep(10)
    scrapper = NRScrapper(nr)
    activity_stream_list = scrapper.get_activity_stream()
    last_activity = activity_stream_list[0]
    last_activity_title = last_activity.find('h1', class_='nr1-BaseActivityListItem-title')
    last_activity_subtitle = last_activity.find('p', class_="nr1-BaseActivityListItem-subtitle").get_text()
    last_activity_message = last_activity.find('div', class_='nr1-BaseActivityListItem-description').get_text()
    nr_checks_frame = Frame(frame_right)
    title = Label(nr_checks_frame, text=f'Last activity at NR')
    title.pack()
    #title_label = Label(nr_checks_frame, text=last_activity_title)
    subtitle_label = Label(nr_checks_frame, text=last_activity_subtitle)
    message_label = Label(nr_checks_frame, text=last_activity_message)
    #title_label.pack()
    subtitle_label.pack()
    message_label.pack()
    nr_checks_frame.pack()
    window.after(50000, scrape_nr)

    # for div_item in activity_stream_list:
    #     item_list = []
    #     for item in div_item:
    #         item_list.append(item)
    #         title = item.find('h1', class_='nr1-BaseActivityListItem-title').get_text()
    #         subtitle = item.find('p', class_="nr1-BaseActivityListItem-subtitle").get_text()
    #         message = item.find('div', class_='nr1-BaseActivityListItem-description').get_text()
    #         print(title, subtitle, message, sep='\n')

if __name__ == '__main__':
    window = create_window('monitoring', 600, 350, False)
    window.attributes('-topmost', True)

    frame_left = Frame(window, bd=5)
    frame_left.place(relx=0.005, rely=0.05, relwidth=0.2, relheight=0.95)
    frame_right = Frame(window, bd=5)
    frame_right.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.95)

    button_pd = Button(frame_left, text='Launch PD', command=launch_pd)
    button_nr = Button(frame_left, text='Launch NR', command=launch_nr)
    button_exit = Button(frame_left, text='Close application', command=lambda: window.destroy())
    button_pd.pack()
    button_nr.pack()
    button_exit.pack(side=BOTTOM)


    info = Label(frame_right, text='Launch PD at first', font=12, justify=CENTER)
    info.pack()
    # button = Button(window, text='some btn')
    # button.grid(column=0, row=0)
    # frame_text = Frame()
    # frame_text.pack()
    # greeting = Label(master=frame_text, text='Hola').pack()
    # frame_buttons = Frame()
    # frame_buttons.pack()
    # btn_1 = Button(master=frame_buttons, text='btn_1', command=lambda: clicked_btn_1('pd')).grid(column=0, row=2)
    # btn_2 = Button(master=frame_buttons, text='btn_2', command=lambda: clicked_btn_1('nr')).grid(column=1, row=2)
    # btn_3 = Button(master=frame_buttons, text='btn_3').grid(column=2, row=2)
    window.mainloop()
