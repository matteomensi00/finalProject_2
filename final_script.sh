#!/usr/bin/bash
#pip install pandas
#pip install h3
train=$(wget https://www.dropbox.com/s/2p9f2g3l8y4oizn/train.csv > train.csv)
#scaricare script python
sampling_py=$(curl -l https://raw.githubusercontent.com/matteomensi00/finalProject_2/main/sampling.py > sampling.py)
FinalProjectDE_py=$(curl -l https://raw.githubusercontent.com/matteomensi00/finalProject_2/main/Final_project_DE.py > Final_project_DE.py)
#eseguire script python
python1=$(python3 sampling.py)
python2=$(python3 Final_project_DE.py)
