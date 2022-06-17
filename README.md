## Spin Rhythm lets you play a random song from the main soundtrack. Why can't we do the same for custom charts? 
This project aims to change that. It's compatible with both the PC and Mac! It will let you press a hotkey of your choice to start playing a new, random custom chart. It works equally as well regardless of if the game is open or not! 

### Additionally, you can choose to download and play a random song from [spinsha.re](https://spinsha.re/)!
## Variables you may want to change:

I'm hoping this is self-explanatory enough, but feel free to ask if you have questions! Discord is forsalebypwner#2310
Look for this section near the beginning of the program:

```
#############################################################
#############################################################
difficulty = 4  # 0 is Easy, 1 is Medium, 2 is Hard, 3 is Expert, 4 is XD
key_to_listen_for = Key.home
difficulty_range_enabled = False  # change to True if you want to enable the difficulty range
difficulty_score_max = 45  # a narrow range may cause the search to take longer or even fail
difficulty_score_min = 0
#############################################################
#############################################################
```

You can change key_to_listen_for to any of these:

<details>
    <summary>List of valid hotkeys</summary>
  
  * Key.alt

  * Key.alt_l

  * Key.alt_r

  * Key.alt_gr

  * Key.backspace

  * Key.caps_lock

  * Key.cmd

  * Key.cmd_l

  * Key.cmd_r

  * Key.ctrl

  * Key.ctrl_l

  * Key.ctrl_r

  * Key.delete

  * Key.down

  * Key.end

  * Key.enter

  * Key.esc

  * Key.f1

  * Key.f2

  * Key.f3

  * Key.f4

  * Key.f5

  * Key.f6

  * Key.f7

  * Key.f8

  * Key.f9

  * Key.f10

  * Key.f11

  * Key.f12

  * Key.f13

  * Key.f14

  * Key.f15

  * Key.f16

  * Key.f17

  * Key.f18

  * Key.f19

  * Key.f20

  * Key.home

  * Key.left

  * Key.page_down

  * Key.page_up

  * Key.right

  * Key.shift

  * Key.shift_l

  * Key.shift_r

  * Key.space

  * Key.tab

  * Key.up

  * Key.media_play_pause

  * Key.media_volume_mute

  * Key.media_volume_down

  * Key.media_volume_up

  * Key.media_previous

  * Key.media_next

  * Key.insert

  * Key.menu

  * Key.num_lock

  * Key.pause

  * Key.print_screen

  * Key.scroll_lock
</details>

## How to install and run

* Install Python 3 if you don't already have it https://python.org

* Download this repository as a zip file or clone

* Open a command prompt and navigate to the folder where you downloaded the repository

* run `pip3 install -r requirements.txt`

* **if you'd like to play one of your already downloaded charts**, run `python3 play-random-song-local.py`

* **if you'd like to download and play a random chart from [spinsha.re](https://spinsha.re)**, run `python3 download-and-play-from-spinsha.re.py`

You can then simply leave that command prompt running in the background. It's now waiting for you to press the hotkey, test it out!

If you choose to download and run from [spinsha.re](https://spinsha.re), you **must** follow their [usage policy](https://spinsha.re/api/docs/usage-policy)! Also, please be respectful and don't waste their bandwidth by spamming the hotkey, shit's expensive yo. I'm not affiliated with them, but here are a few ways you can support them! https://spinsha.re/support

If you run into issues or just want some help, feel free to DM me on Discord forsalebypwner#2310

If you find a bug or have anything you think should be change, opening issues and pull requests is always welcome!

### Known issues:

If you're already in-game and press the button to download a new random custom song, you will get an error if you're still in the custom song selection screen. You can workaroud this simply by going back to the SRXD main menu before pressing the button. 

### On MacOS only:

Upon first launch of the script, you'll get a pop-up prompting you to allow input monitoring for this program, you must do so for it to work. Additionally, every time you start the program, it will print out a message that says "This process is not trusted! Input event monitoring will not be possible until it is added to accessibility clients." **regardless of whether you've given it input monitoring permissions or not**. This can be safely ignored. 
