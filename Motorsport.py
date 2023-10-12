import curses
import time
import os
import pyautogui
import random
import subprocess

def get_duration(stdscr):
    curses.echo()
    stdscr.addstr(10, 0, "How much time (minutes): ")
    stdscr.refresh()
    dm = stdscr.getstr(10, 31, 5)
    curses.noecho()
    return int(dm)

def execute_option3(stdscr):
    global altf4
    global input_delay
    stdscr.clear()
    stdscr.refresh()
    altf4 = False
    input_delay_in = get_input(stdscr, "Input delay: ", 10)
    close = get_input(stdscr, "Close game after finishing race: ", 11)
    input_delay = int(input_delay_in)
    closing = int(close)
    if closing == 0:
        pass
    if closing == 1:
        altf4 = True
    curses.noecho()
    return altf4, input_delay

def get_input(stdscr, prompt, line_number):
    curses.echo()
    stdscr.addstr(line_number, 0, " " * curses.COLS)
    stdscr.addstr(line_number, 0, prompt)
    stdscr.refresh()
    user_input = stdscr.getstr(line_number, len(prompt))
    curses.noecho()
    return user_input

def execute_option1(stdscr):
    stdscr.clear()
    stdscr.refresh()
    dm = get_duration(stdscr)
    stdscr.clear()
    stdscr.refresh()
    enter(dm, stdscr, altf4, input_delay)

def execute_option2(stdscr):
    stdscr.clear()
    stdscr.refresh()

    lap_time_input = get_input(stdscr, "Enter lap time (e.g., 1:30,500): ", 10)
    num_laps_input = get_input(stdscr, "Enter number of laps: ", 11)

    lap_time = lap_time_input.decode('utf-8')
    num_laps = int(num_laps_input)

    try:
        minutes, seconds_milliseconds = lap_time.split(":")
        seconds, milliseconds = seconds_milliseconds.split(",")
        minutes = int(minutes)
        seconds = int(seconds)
        milliseconds = int(milliseconds)

        lap_time_in_seconds = (minutes * 60) + seconds + (milliseconds / 1000)
        total_time_in_seconds = lap_time_in_seconds * num_laps
        total_time_in_minutes = total_time_in_seconds / 60

        stdscr.addstr(13, 0, " " * curses.COLS)
        stdscr.addstr(13, 0, f"Total time needed: {total_time_in_minutes:.2f} minutes")
    except ValueError:
        stdscr.addstr(13, 0, " " * curses.COLS)
        stdscr.addstr(13, 0, "Invalid input. Please use the format 'minutes:seconds,milliseconds'")

    stdscr.refresh()
    time.sleep(4)

def enter(dm, stdscr, close, delay):
    global times
    times = 0
    end_time = time.time() + dm * 60
    list1 = ['s', 'w', 'a', 'd']
    try:
        while True:
            if time.time() < end_time:
                key = random.choice(list1)
                pyautogui.press(key)
                info_text = f'Pressed [{times}] times'
                ending = f'Ending at {time.strftime("%H:%M:%S", time.localtime(end_time))}'
                stdscr.addstr(12, 0, info_text)
                stdscr.addstr(13, 0, ending)
                stdscr.refresh()
                times += 1
                time.sleep(delay)
            if close == True:
                if time.time() > end_time:
                    stdscr.refresh()
                    info_text = f'Closing game and exiting'
                    ending = f'Thanks for using my toll :)'
                    stdscr.addstr(12, 0, info_text)
                    stdscr.addstr(13, 0, ending)
                    stdscr.refresh()
                    time.sleep(3)
                    subprocess.call(["taskkill", "/F", "/IM", "forza_gaming.desktop.x64_release_final.exe"])
                    time.sleep(2)
                    exit(69)
            if time.time() > end_time:
                stdscr.refresh()
                ending = f'Thanks for using my toll :)'
                stdscr.addstr(12, 0, ending)
                stdscr.refresh()
                time.sleep(3)
                curses.noecho()
            else:
                pass
    except KeyboardInterrupt:
        pass

def main(stdscr):
    try:
        curses.curs_set(0)
        stdscr.nodelay(1)
        stdscr.clear()

        options = ["[1]     Anti AFK", "   [2]  Calculate Time", "[3]     Setup  ", '[4]     Github ',"[q]     Exit   "]
        current_option = 0
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        box = curses.newwin(14, curses.COLS, (height - 14) // 2, 0)

        while True:
            stdscr.clear()
            time.sleep(0.1)
            box.box()
            title = "Forza Motorsport Auto Farm v1.0"
            subtitle = "Made by Buck3ts41"
            box.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD)
            box.addstr(2, (curses.COLS - len(subtitle)) // 2, subtitle)

            for i, option in enumerate(options):
                x = (curses.COLS - len(option)) // 2
                y = 4 + i
                if i == current_option:
                    box.attron(curses.A_REVERSE)
                    box.addstr(y, x, option, curses.A_BOLD)
                    box.attroff(curses.A_REVERSE)
                else:
                    box.addstr(y, x, option)
            key = stdscr.getch()
            box.refresh()

            if key == ord("1"):
                execute_option1(stdscr)
            elif key == ord("2"):
                execute_option2(stdscr)
            elif key == ord("4"):
                os.system('start www.github.com/Buck3ts41')
            elif key == ord("3"):
                execute_option3(stdscr)
            elif key == ord("q") or key == ord("Q"):
                break
    except Exception as e:
        stdscr.addstr(15, 0, f"Error: {str(e)}")
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)
