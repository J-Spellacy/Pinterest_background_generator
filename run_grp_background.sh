#!/bin/bash
# activates venv (replace with path to venv mine is here obviously)
source /home/jude/pint_venv/bin/activate


# replace with path to your image cluster pickle files and python script (mine are in the same folder by default cause I am lazy this will change later)
for f in /home/jude/Documents/python_stuff/images_cluster_*.pkl; do
    python /home/jude/Documents/python_stuff/grp_background_gen.py "$f"
done