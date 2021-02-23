#!/bin/sh

./manage.py migrate
./manage.py runserver 0.0.0.0:8181

# while :
# do
#     sleep 5
#     echo "Ok"
# done