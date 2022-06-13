## Spin Rhythm lets you play a random song from the main soundtrack. Why can't we do the same for custom charts? 
This project aims to change that. This will let you press a hotkey of your choice to start playing a new, random custom chart. It works equally as well regardless of if the game is open or not! 

## Variables you may want to change:

[`difficulty`: default is 4, which is XD](https://github.com/kylefmohr/Play_Random_SRXD_Custom/blob/18715cecb7fcff52af6da8deee4a5e7282130408/main.py#L5)

If you want expert, change it to 3

Hard, change to 2, etc. etc

[`key_to_listen_for`: by default, **it is listening for the "Home" key** on the keyboard to be pressed](https://github.com/kylefmohr/Play_Random_SRXD_Custom/blob/18715cecb7fcff52af6da8deee4a5e7282130408/main.py#L5)

You can change it to any of these:

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

* Open a command prompt and cd to this directory


* run `pip3 install -r requirements.txt`

* then run `python3 main.py`

You can then simply leave that command prompt running in the background. It should work now, test it out!

If you run into issues or just want some help, feel free to DM me on Discord forsalebypwner#2310

If you find a bug or have anything you think should be change, opening issues and pull requests is always welcome!

### On MacOS only:

Upon first launch of the script, you'll get a pop-up prompting you to allow input monitoring for this program, you must do so for it to work. Additionally, every time you start the program, it will print out a message that says "This process is not trusted! Input event monitoring will not be possible until it is added to accessibility clients." **regardless of whether you've given it input monitoring permissions or not**
