#!/bin/bash
#SBATCH -N1
#SBATCH -c4
#SBATCH --mem=10gb
#SBATCH --time=24:00:00
 
# uruchom program 
source /home/rammarad/.bashrc
conda activate spacy
python 3-split_words.py Google-Playstore_descriptions_0.csv

