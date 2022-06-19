import os, random, time, platform
from pynput import keyboard
from pynput.keyboard import Key

difficulty = 4  # 0 is Easy, 1 is Medium, 2 is Hard, 3 is Expert, 4 is XD
key_to_listen_for = Key.home
customs_dir_windows = os.path.expandvars('%USERPROFILE%\\AppData\\LocalLow\\Super Spin Digital\\Spin Rhythm XD\\Custom')
customs_dir_mac = os.path.expanduser('~/Library/Application Support/Super Spin Digital/Spin Rhythm XD/Custom')
customs_dir = ''


def enumerate_customs(): # reads the identifier of every custom song in your library, for later use in launch_game
    os.chdir(customs_dir)
    customs = os.listdir()
    custom_charts = []
    for file in customs:
        if file.endswith(".srtb"):
            custom_charts.append(file)

    return custom_charts


# cheers to the spinsha.re devs https://github.com/SpinShare/client/blob/master/src/components/Overlays/PlayOverlay.vue#L80
# shell.openExternal('steam://run/1058830//play "' + this.$props.fileReference + '.srtb" difficulty ' + difficulty);
def get_launch_uri(chart, difficulty):
    return 'steam://run/1058830//play ' + chart + ' difficulty ' + str(difficulty)


def on_press(key): # callback for when 'any' key gets pressed on your keyboard, regardless of which app has focus
    if key == key_to_listen_for:
        print("Starting new random song")
        custom_charts = enumerate_customs()
        random_song = random.choice(custom_charts)
        uri = get_launch_uri(random_song, difficulty)
        if platform.system() == 'Windows':
            os.startfile(uri)
        elif platform.system() == 'Darwin':  # why os.startfile not exist on Mac? 🤷
            webbrowser.open(uri)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        customs_dir = customs_dir_windows
    elif platform.system() == 'Darwin':
        import webbrowser
        customs_dir = customs_dir_mac
    else:
        print("Unsupported OS")
        exit()
    listener = keyboard.Listener(on_press=on_press) # set up the keyboard listener and its callback
    listener.start()
    while True:
        time.sleep(0.05)  # reduce CPU usage
        pass

