import os, random, time
from pynput import keyboard
from pynput.keyboard import Key

difficulty = 4  # 0 is Easy, 1 is Medium, 2 is Hard, 3 is Expert, 4 is XD
key_to_listen_for = Key.home


def enumerate_customs(): # reads the identifier of every custom song in your library, for later use in launch_game
    os.chdir(os.path.expandvars('%USERPROFILE%\\AppData\\LocalLow\\Super Spin Digital\\Spin Rhythm XD\\Custom'))
    customs = os.listdir()
    charts = []
    for chart in customs:
        if chart.endswith(".srtb"):
            charts.append(chart)

    return charts


# cheers to the spinshare devs https://github.com/SpinShare/client/blob/master/src/components/Overlays/PlayOverlay.vue#L80
# shell.openExternal('steam://run/1058830//play "' + this.$props.fileReference + '.srtb" difficulty ' + difficulty);
def launch_game(chart, difficulty):
    os.startfile('steam://run/1058830//play ' + chart + ' difficulty ' + str(difficulty))


def on_press(key): # callback for when 'any' key gets pressed on your keyboard, regardless of which app has focus
    if key == key_to_listen_for:
        print("Starting new random song")
        charts = enumerate_customs()
        song = random.choice(charts)
        launch_game(song, difficulty)


if __name__ == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    while True:
        pass
