#!/bin/bash
# Задание 1
echo "hi to file1" > file1
cat file1
echo "hi to file2" >> file2
cat file2
echo "bye to file1" > file1
cat file1
echo "bye to file2" >> file2
cat file2

# Задание 2

cat file2 > file1
cat file1

# Задание 3

echo stderr>&2
cat > myscript.sh <<EOF
#!/bin/bash
echo stdout
echo stderr>&2
exit 0
EOF
chmod +x myscript.sh
sh myscript.sh
sh myscript.sh > file1
echo stderr 2> file3 && echo stderr 2> file2
cat file3
cat file2
sh myscript.sh > file3 2> file3
cat file3
sh myscript.sh > file4 2>> file4
cat file4

# Задание 4

sort -r /etc/group | tail -n 15 | head -n 3 | tail -n 1
sort -r /etc/group | tail -n 15 | head -n 6 | tail -n 1

# Задание 5

ls -l /dev | grep '^b' | wc -l
ls -l /dev | grep '^с' | wc -l

# Задание 6

cat > myscript2.sh << EOF
#!/bin/bash
for i in "\$@"
do
echo "\$i"
done
exit 0
EOF
chmod +x myscript2.sh
./myscript2.sh 1 2 3
sh myscript2.sh 1 2 3