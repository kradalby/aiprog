#!/bin/bash


for i in 6 7
do
python 2048game.py --trains $i --learningrate 0.001 --sizes 48 1024 4 --types rect soft --notation derp
python 2048game.py --trains $i --learningrate 0.001 --sizes 48 2048 4 --types rect soft --notation derp
#python 2048game.py --trains $i --learningrate 0.001 --sizes 48 4096 4 --types rect soft --notation derp
done
