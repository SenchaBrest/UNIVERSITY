#!/bin/sh
# Задание 1

ls
ln 1 ~/Code/UNIVERSITY/OS/links
cat ~/Code/UNIVERSITY/OS/links/1
rm 1
ls
cat 1
cat ~/Code/UNIVERSITY/OS/links/1
ln folder1 ~/Code/UNIVERSITY/OS/links

# Задание 2
ls
ln -s /home/arsbrest/Code/UNIVERSITY/OS/LABA2/2 /home/arsbrest/Code/UNIVERSITY/OS/links 
cat /home/arsbrest/Code/UNIVERSITY/OS/links/2 
rm 2
ls
cat /home/arsbrest/Code/UNIVERSITY/OS/links/2 
ln -s /home/arsbrest/Code/UNIVERSITY/OS/LABA2/folder2 /home/arsbrest/Code/UNIVERSITY/OS/links 
ls /home/arsbrest/Code/UNIVERSITY/OS/links/ 

# Задание 3

ln 3 ~/Code/UNIVERSITY/OS/links/3_hard
ln -s /home/arsbrest/Code/UNIVERSITY/OS/LABA2/3 /home/arsbrest/Code/UNIVERSITY/OS/links/3_symbol
ls /home/arsbrest/Code/UNIVERSITY/OS/links/ 
ls -i 3
ls -i /home/arsbrest/Code/UNIVERSITY/OS/links/3_hard
ls -i /home/arsbrest/Code/UNIVERSITY/OS/links/3_symbol