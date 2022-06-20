import os, random, time, platform, re, json
import requests
import zipfile
from pynput import keyboard
from pynput.keyboard import Key

#############################################################
#############################################################
difficulty = 4  # 0 is Easy, 1 is Medium, 2 is Hard, 3 is Expert, 4 is XD
key_to_listen_for = Key.home
difficulty_range_enabled = True  # change to True if you want to enable the difficulty range
difficulty_score_max = 45
difficulty_score_min = 0
#############################################################
#############################################################

customs_dir_windows = os.path.expandvars('%USERPROFILE%\\AppData\\LocalLow\\Super Spin Digital\\Spin Rhythm XD\\Custom')
customs_dir_mac = os.path.expanduser('~/Library/Application Support/Super Spin Digital/Spin Rhythm XD/Custom')
customs_dir = ''

difficulty_names = ["Easy", "Medium", "Hard", "Expert", "XD"]


def initialize_cache():
    if not os.path.exists('spinshare-cache.json'):
        print("Caching custom song information from spinsha.re, please wait a moment...")
        payload = '{"searchQuery": ""}'
        spinshare_cache = requests.post("https://spinsha.re/api/searchCharts", data=payload).text
        spinshare_cache = spinshare_cache
        with open('spinshare-cache.json', 'w') as f:  # write api response to cache
            f.write(spinshare_cache)
        return spinshare_cache
    else:  # if cache exists, read it
        if int(time.time()) - int(os.path.getmtime('spinshare-cache.json')) < 60 * 60 * 4:  # if cache is older than 4 hours, refresh it
            print("Using recently cached custom song information from spinsha.re")
            with open('spinshare-cache.json', 'r') as f:
                spinshare_cache = f.read()
            return spinshare_cache
        else:
            print("Removing old cache file")
            os.remove('spinshare-cache.json')
            return initialize_cache()


spinshare_cache = initialize_cache()
id_list = []  # list of custom song ids
newest_song_id = 0
spinshare_cache_json = json.loads(spinshare_cache)
for song in spinshare_cache_json['data']:
    id_list.append(song['id'])
    if song['id'] > newest_song_id:
        newest_song_id = song['id']

print("Loaded information about " + str(newest_song_id) + " custom songs from spinsha.re")
print("Ready! Press " + str(key_to_listen_for) + " to spin!")
random_song_id = 0
random_song_fileReference = ''
song_has_difficulty = False
random_song_difficulty_score = 0
random_song_title = ''
random_song_artist = ''
random_song_charter = ''


def choose_random_song():
    random_song_id = random.choice(id_list)
    for song in spinshare_cache_json['data']:
        if song['id'] == random_song_id:
            random_song_fileReference = song['fileReference']
            random_song_title = song['title']
            random_song_artist = song['artist']
            random_song_charter = song['charter']
            song_has_difficulty = song['has' + difficulty_names[difficulty] + 'Difficulty']
            if difficulty_range_enabled:
                if song_has_difficulty:
                    try:
                        random_song_difficulty_score = int(song[difficulty_names[difficulty] + 'Difficulty'])
                    except TypeError:
                        print("Error: null value for difficulty score for song ID " + str(random_song_id))
                        return choose_random_song()
                    return random_song_id, random_song_fileReference, random_song_title, random_song_artist, random_song_charter, random_song_difficulty_score
                else:
                    return choose_random_song()  # choose a new song if the difficulty is not available
            else:
                return random_song_id, random_song_fileReference, random_song_title, random_song_artist, random_song_charter, 0


# cheers to the spinsha.re devs https://github.com/SpinShare/client/blob/master/src/components/Overlays/PlayOverlay.vue#L80
# shell.openExternal('steam://run/1058830//play "' + this.$props.fileReference + '.srtb" difficulty ' + difficulty);
def get_launch_uri(chart, difficulty):
    return 'steam://run/1058830//play ' + chart + ' difficulty ' + str(difficulty)


def song_exists_locally(random_song_fileReference):  # no need to re-download the song if it already exists
    # file_reference = requests.get("https://spinsha.re/api/song/" + str(song_number)).json()['data']['fileReference']  # https://spinsha.re/api/docs/open/songs#detail
    customs = os.listdir(customs_dir)
    for file in customs:
        if file.startswith(random_song_fileReference):
            return True
    return False


def download_song(download_attempts, random_song_id):
    url = "https://spinsha.re/api/song/" + str(random_song_id) + "/download"
    response = requests.get(url)
    filename = ''
    if response.status_code == 200:
        if "Content-Disposition" in response.headers:  # https://stackoverflow.com/a/53299682 this is a way to get the filename from the download
            filename = re.findall("filename=(.+)", response.headers["Content-Disposition"])[0]
            filename = filename.replace('"', '')
            # = filename.replace('.zip', '')
        else:  # if that doesn't work, we can always query the api and determine the filename from the fileReference string
            filename = random_song_fileReference + ".zip"
        full_path = customs_dir + "\\" + filename
        with open(full_path, "wb") as f:
            f.write(response.content)  # write custom chart .zip bundle to the disk
        print("Downloaded to " + full_path)
        unzip_and_move_files(full_path)
        return True, random_song_id
    else:  # if response code != 200
        download_attempts += 1
        return False, None


def stage_download(download_attempts):  # prepare to download the random song, first determine if it meets our requirements
    random_song_id, random_song_fileReference, random_song_title, random_song_artist, random_song_charter, random_song_difficulty_score = choose_random_song()
    if song_exists_locally(random_song_fileReference):
        print("Song already exists locally, no need to download")
        #  file_reference = requests.get("https://spinsha.re/api/song/" + str(random_song_id)).json()['data']['fileReference']  # we need the fileReference string because that's how the custom charts are named
        return True, random_song_id, random_song_fileReference, random_song_title, random_song_artist, random_song_charter, random_song_difficulty_score
    elif difficulty_range_enabled:
        # api_call = requests.get("https://spinsha.re/api/song/" + str(random_song_id)).json()
        # song_has_requested_difficulty = api_call['data']['has' + difficulty_names[difficulty] + 'Difficulty']
        if song_has_difficulty:
            # difficulty_score = int(api_call['data'][difficulty_names[difficulty] + 'Difficulty'])
            if difficulty_score_min <= random_song_difficulty_score <= difficulty_score_max:
                print("Song has the requested difficulty score (" + str(random_song_difficulty_score) + "), downloading")
                successful, random_song_id = download_song(download_attempts, random_song_id)
                return successful, random_song_id, random_song_fileReference, random_song_title, random_song_artist, random_song_charter, random_song_difficulty_score
            else:
                print("Song difficulty is out of range, skipping")
                return False, None, None, None, None, None, None
        else:
            print("Song does not have the requested difficulty " + difficulty_names[difficulty] + ", skipping")
            return False, None, None, None, None, None, None
    else:  # song doesn't exist locally, and difficulty range is not enabled
        successful, random_song_id =  download_song(download_attempts, random_song_id)
        return successful, random_song_id, random_song_fileReference, random_song_title, random_song_artist, random_song_charter, random_song_difficulty_score


def unzip_and_move_files(full_path):
    with zipfile.ZipFile(full_path, 'r') as zipped_song:
        zipped_song.extractall(customs_dir)
    os.remove(full_path)  # remove the zip file after extracting it


def start_process(download_attempts):  # needed to separate this from on_press(), because we need to track the download attempts, and on_press by default is only able to pass the key as an argument
    print("Downloading a random song from https://spinsha.re")
    download_status, random_song_id, random_song_fileReference, random_song_title, random_song_artist, random_song_charter, random_song_difficulty_score = stage_download(download_attempts)
    if download_status:
        print("Successfully downloaded " + random_song_title + " by " + random_song_artist + ", charted by " + random_song_charter + ", difficulty score" + str(random_song_difficulty_score))
        print("Downloaded from https://spinsha.re/song/" + str(random_song_id))
        print("Launching the game with the downloaded song")

        uri = get_launch_uri(random_song_fileReference, difficulty)
        print(uri)
        if platform.system() == 'Windows':
            os.startfile(uri)
        elif platform.system() == 'Darwin':
            webbrowser.open(uri)
    else:
        print("Failed to download a random song from https://spinsha.re, trying again")
        if download_attempts >= 15:
            print("Failed to download 15 times, check your internet connection or the spinsha.re website")
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

