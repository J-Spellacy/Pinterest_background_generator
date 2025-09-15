# Pinterest_background_generator
Python code to scrape a user's requested data html file and then generate a background, this will hopefully executable in my sway config file at startup to create a new full resolution background each time.

In order to run this code as a script in your window manager config, you need to grant permission to the file with:

```
chmod +x /home/user/path_to_file/run_background.sh
```

Please only do this if you trust the documents and have read through them. (Use at own risk).

You will have to edit the shell script with your own virtual environment with all dependencies installed already through pip, I recommend creating a new one.

I then add the following lines to my sway config:

```
exec_always /home/user/path_to_file/run_background.sh
output * bg "/home/jude/path_to_file/collage.png" fill
```

Again please manually check that the script is working from the terminal before running this in the config file, although I have done this and it just does nothing if an error occurs.

To test the shell script run the following line in a fresh terminal:

```
/home/user/path_to_file/run_background.sh
```

For a hyprland config, I did the following:


Here is an example of a background generated with the code and my pinterest, all credit for images to the respective owners on pinterest, link to my pinterest: https://uk.pinterest.com/judespell/_pins/.

<img width="960" height="540" alt="collage_1k" src="https://github.com/user-attachments/assets/249153fe-1c19-42d6-98ab-8b4e74bcb5e4" />
