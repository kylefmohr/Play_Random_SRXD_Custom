import os, random, time, platform, re
import requests
import zipfile
import bs4
from pynput import keyboard
from pynput.keyboard import Key

difficulty = 4  # 0 is Easy, 1 is Medium, 2 is Hard, 3 is Expert, 4 is XD
key_to_listen_for = Key.home

customs_dir_windows = os.path.expandvars('%USERPROFILE%\\AppData\\LocalLow\\Super Spin Digital\\Spin Rhythm XD\\Custom')
customs_dir_mac = os.path.expanduser('~/Library/Application Support/Super Spin Digital/Spin Rhythm XD/Custom')
customs_dir = ''

try:
    spinshare_new = requests.get("https://spinsha.re/new")
    spinshare_newest_song_number = bs4.BeautifulSoup(spinshare_new.text, "html.parser").find(class_="song-item").get("href").split("/")[-1]  # that's a hefty one-liner. it parses the html of spinsha.re/new to determine the newest song number, and therefore the highest possible random song number
except:
    print("Failed to get the newest song number from https://spinsha.re, using outdated value instead")
    spinshare_newest_song_number = 6291
#   also:
#   TODO: add difficulty range


def enumerate_customs():  # reads the identifier of every custom song in your library, for later use in launch_game
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


def song_exists_locally(song_number):
    file_reference = requests.get("https://spinsha.re/api/song/" + str(song_number)).json()['data']['fileReference']  # https://spinsha.re/api/docs/open/songs#detail
    customs = os.listdir(customs_dir)
    for file in customs:
        if file.startswith(file_reference):
            return True
    return False


def download_song(download_attempts):
    random_song_number = random.randint(1000, spinshare_newest_song_number)  # according to spinsha.re devs, this should include all songs, but this scheme may change in the future
    if song_exists_locally(random_song_number):
        print("Song already exists locally, no need to download")
        file_reference = requests.get("https://spinsha.re/api/song/" + str(random_song_number)).json()['data']['fileReference']  # we need the fileReference string because that's how the custom charts are named
        return True, file_reference
    else:
        url = "https://spinsha.re/api/song/" + str(random_song_number) + "/download"
        response = requests.get(url)
        filename = ''
        if response.status_code == 200:
            if "Content-Disposition" in response.headers:  # https://stackoverflow.com/a/53299682 this is a way to get the filename from the download
                filename = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]
                filename = filename.replace('"', '')
                file_reference = filename.replace('.zip', '')
            else:  # if that doesn't work, we can always query the api and determine the filename from the fileReference string
                file_reference = requests.get("https://spinsha.re/api/song/" + str(random_song_number)).json()['data']['fileReference']  # https://spinsha.re/api/docs/open/songs#detail
                filename = file_reference + ".zip"
            full_path = customs_dir + "\\" + filename
            with open(full_path, "wb") as f:
                f.write(response.content)  # write new custom song to disk
            print("Downloaded to " + full_path)
            unzip_and_move_files(full_path)
            return True, file_reference
        else:  # if response code != 200
            download_attempts += 1
            return False, None


def unzip_and_move_files(full_path):
    with zipfile.ZipFile(full_path, 'r') as zipped_song:
        zipped_song.extractall(customs_dir)
    os.remove(full_path)


def start_process(download_attempts):  # needed to separate this from on_press(), because we need to track the download attempts, and on_press by default is only able to pass the key as an argument
    print("Downloading a random song from https://spinsha.re")
    download_status, file_reference = download_song(download_attempts)
    if download_status:
        print("Successfully downloaded a random song from https://spinsha.re")
        print("Launching the game with the downloaded song")

        uri = get_launch_uri(file_reference, difficulty)
        print(uri)
        if platform.system() == 'Windows':
            os.startfile(uri)
        elif platform.system() == 'Darwin':
            webbrowser.open(uri)
    else:
        print("Failed to download a random song from https://spinsha.re, trying again")
        if download_attempts >= 5:
            print("Failed to download 5 times, check your internet connection or the spinsha.re website")
            exit()
        else:
            print("Trying again, attempt " + str(download_attempts + 1))
            start_process(download_attempts)  # retry download


def on_press(key):  # callback for when 'any' key gets pressed on your keyboard, regardless of which app has focus
    if key == key_to_listen_for:
        start_process(0)


if __name__ == '__main__':
    if platform.system() == 'Windows':
        customs_dir = customs_dir_windows
    elif platform.system() == 'Darwin':
        import webbrowser
        customs_dir = customs_dir_mac
    else:
        print("Unsupported OS")
        exit()
    listener = keyboard.Listener(on_press=on_press)  # set up the keyboard listener and its callback
    listener.start()
    while True:
        time.sleep(0.05)  # reduce CPU usage
        pass
