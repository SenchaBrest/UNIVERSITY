#!/bin/sh
cd

# Задание 1

man ls
ls -l /etc
ls -l /bin
ls -l /home/arsbrest

# Задание 2
cd /
ls -l 
cd

# Задание 3

ls -l /etc/shadow
ls -l /etc/passwd
cat /etc/shadow
cat /etc/passwd

# Задание 4

touch 1 2 3 4
ls
chmod 700 1
chmod 647 2
chmod 304 3
chmod 272 4
ls -l


# Задание 5

touch 5 6 7 8
ls
chmod a-rwx 5 ; chmod a-rwx 6 ; chmod a-rwx 7 ; chmod a-rwx 8
chmod u+rwx 5
chmod u+rw,g+r,o+rwx 6
chmod u+wx,o+r 7
chmod u+w,g+rwx,o+w 8
ls -l
total 40

# Задание 6

touch z1 z2 z3
chmod 06 z1
chmod 33 z2
chmod 200 z3
ls -l

# Задание 7

touch www
chmod 222 www
ls -l www

# Задание 8

cp /bin/ls /home/arsbrest/
ls
chmod 666 ls
./ls

# Задание 9

cd /root