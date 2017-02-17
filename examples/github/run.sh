#!/bin/bash

# Get the GitHub Logo
wget https://assets-cdn.github.com/images/modules/logos_page/GitHub-Mark.png

python svg.py -i GitHub-Mark.png -o GitHub-Mark.svg