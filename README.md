# Pinterest_background_generator
Python code to scrape a user's requested data html file and then generate a set of backgrounds grouped by colour using k-means clustering, this is executable in a window manager config file at startup to create a new full resolution background each time or in your waybar config as a sequence of changeable backgrounds.

Before editing and using the bash scripts and config files please run pint_scraper.py and png_conv_res_label.py with the following edits:

In pint_scraper.py:
```
HTML_FILE = "/home/user/path_to_file/pinterest.html"
OUTPUT_DIR = "/home/user/path_to_file/pint_pins"
```
In png_conv_res_label.py:
```
FOLDER = "/home/user/path_to_file/pint_pins"
```
Once both have run, please ensure that all images are png and have the format "pin_0000_0000_0000.png".

There may be a large number of unrecognised pins at the end of the folder, in a file manager look for the last recognisable pin and delete all pins with numbers greater, these are adverts and I haven't edited the code to not include those (lazy). It is a very quick fix.

In order to run this code as a script in your window manager config or as I would suggest in your waybar config, you need to generate the executables with:

```
chmod +x /home/user/path_to_file/run_grp_background.sh
chmod +x /home/user/path_to_file/background_seq.sh
```

Please only do this if you trust the documents and have read through them. (Use at own risk). When doing so please replace user and path_to_file with your own user and the path you placed the file on.

You will have to edit the shell script with your own python virtual environment with all dependencies installed already through pip, I recommend creating a new one. 
Inside run_grp_background.sh:

```
source /home/user/path_to_file/your_venv/bin/activate
```
This will be replaced with whatever path and virtual environment name you have made.

To test the shell script run the following line in a fresh terminal:

```
/home/user/path_to_file/run_grp_background.sh
```
If you wish to use one of the generated cluster backgrounds only then do the following:

For a hyprland config, I did the following:

Adding the appropriate file paths to hyprpaper (the wallpaper env I use, instructions would be different for others):

```
preload = /home/user/path_to_file/collage_0.png
wallpaper = /home/user/path_to_file/collage_0.png
```
Replacing the 0 with the cluster number of your choice.

Instruct hyprland to run the script before loading hyprpaper so that the background is new each time:

```
exec-once = /home/user/path_to_file/run_grp_background.sh
exec-once = hyprpaper
```
Again please manually check that the script is working from the terminal before running this in the config file, although I have done this and it just does nothing if an error occurs.

Here is an example of a background generated with the code and my pinterest, all credit for images to the respective owners on pinterest, link to my pinterest: https://uk.pinterest.com/judespell/_pins/.


<img width="1367" height="769" alt="20250927_120004" src="https://github.com/user-attachments/assets/8879db03-f998-48dc-8c94-1d4f0201a1ad" />

<img width="960" height="540" alt="collage_1k" src="https://github.com/user-attachments/assets/249153fe-1c19-42d6-98ab-8b4e74bcb5e4" />

For use in a waybar config with background_seq.sh, you must do the following:

Open background_seq.sh in a text editor or with code -oss and edit the following lines:

```
wallpapers=(
    "/home/user/path_to_file/collage_0.png"
    "/home/user/path_to_file/collage_1.png"
    "/home/user/path_to_file/collage_2.png"
    "/home/user/path_to_file/collage_3.png"
    "/home/user/path_to_file/collage_4.png"
    "/home/user/path_to_file/collage_5.png"
)

```
Please ensure these are also preloaded in the hyprpaper.conf file as such:

```
preload = /home/user/path_to_file/collage_0.png
preload = /home/user/path_to_file/collage_1.png
preload = /home/user/path_to_file/collage_2.png
preload = /home/user/path_to_file/collage_3.png
preload = /home/user/path_to_file/collage_4.png
preload = /home/user/path_to_file/collage_5.png

```

In the waybar config file which is usually in /home/user/.config/waybar you can make the following addition:

Firstly when listing modules in each third you should add this line to whichever third you would like the button to be:

```
...
"modules-left": [
    "custom/wallpaper",
    "your other modules here"
],
...
```

I have placed it on the left third but you can change this, you should already have the modules-left in your config and if not you should read through the waybar wiki as it is really helpful.
Then when listing modules you should add this code block, editing the format with a different icon of your choosing:

```
"custom/wallpaper": {
    "format": "   ",
    "on-click": "/home/jude/Documents/python_stuff/background_seq.sh",
    "tooltip": true,
    "tooltip-format": "cycle wallpaper",
    "interval": 0 
},
```

Rebooting your computer or reloading hyprland and killing waybar and restarting it, you should then be able to click through the backgrounds in a set sequence.

