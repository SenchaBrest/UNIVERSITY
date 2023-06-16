#!/bin/bash
mkdir Kirilovich
mkdir Kirilovich/1
mkdir Kirilovich/1/2 Kirilovich/1/3
mkdir Kirilovich/4
ls -R
cp /etc/group /home/arsbrest/Code/UNIVERSITY/OC/LABA1/Kirilovich/1
ls Kirilovich/1/
cp /etc/group Kirilovich/1/2/
ls Kirilovich/1/2/
cp /etc/group Kirilovich/1/3/
ls Kirilovich/1/3/
cp /etc/group ~/Code/UNIVERSITY/OC/LABA1/Kirilovich/4
rm Kirilovich/4/group
ls
rm -r Kirilovich/1 Kirilovich/4
ls Kirilovich/
head -n 13 /etc/group