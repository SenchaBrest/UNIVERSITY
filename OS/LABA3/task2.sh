#!/bin/bash
while [ true ]
do
    echo "Enter a number:"
    echo "1. Search for a file."
    echo "2. Kill all bash processes of active person."
    echo "3. Exit."
    read number

    if [ $number -eq 1 ]
    then
        echo "Enter a folder name:"
        read folder
        echo "Enter a file name:"
        read file
        if [ -f $folder/$file ]
        then
            echo "File exists.\n"
        else
            echo "File does not exist.\n"
        fi
    elif [ $number -eq 2 ]
    then
        user=$(whoami)
        ps -u $user | grep bash | awk '{print $1}' | xargs kill -9

    elif [ $number -eq 3 ]
    then
        break
    else
        echo "You entered a wrong number."
    fi
done