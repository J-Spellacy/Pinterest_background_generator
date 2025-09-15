# Pinterest_background_generator
Python code to scrape a user's requested data html file and then generate a background, this will hopefully executable in my sway config file at startup to create a new full resolution background each time.

In order to run this code as a script in your window manager config, you need to grant permission to the file with:

chmod +x /home/user/path_to_file/run_background.sh

Please only do this if you trust the documents and have read through them. (Use at own risk).

I then add the following lines to my sway config:

exec_always /home/user/path_to_file/run_background.sh
output * bg "/home/jude/path_to_file/collage.png" fill

Again please manually check that the script is working from the terminal before running this in the config file, although I have done this and it just does nothing if an error occurs.

For a hyprland config, I did the following:

