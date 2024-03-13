#!/bin/bash

# Define variables
input_directory='/Volumes/G_MLS_RB_UHOME$/qfavey/01_Experiments/06_Muscle_inhibition/Cc2d2a_morphometry_2/2dpf/Images'
output_directory='/Volumes/G_MLS_RB_UHOME$/qfavey/01_Experiments/06_Muscle_inhibition/Cc2d2a_morphometry_2/2dpf/Analysis'
csv_filename='RESULTS.csv'
json_filename='inf.json'
image_extension='.png'

# Run the Python command with variables
python inference.py -i $input_directory -o $output_directory -fc $csv_filename -fj $json_filename -t $image_extension