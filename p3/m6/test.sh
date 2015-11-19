#!/bin/bash


run1="--trains 5 --learningrate 0.001 --sizes 16 8 8 8 4 --types rect rect rect soft --notation original"
run2="--trains 10 --learningrate 0.001 --sizes 16 8 8 8 4 --types rect rect rect soft --notation original"
run3="--trains 15 --learningrate 0.001 --sizes 16 8 8 8 4 --types rect rect rect soft --notation original"
run4="--trains 20 --learningrate 0.001 --sizes 16 8 8 8 4 --types rect rect rect soft --notation original"
run5="--trains 30 --learningrate 0.001 --sizes 16 8 8 8 4 --types rect rect rect soft --notation original"

for i in 1 1 1 1 1
do
    python 2048game.py $run1
done

for i in 1 1 1 1 1
do
    python 2048game.py $run2
done

for i in 1 1 1 1 1
do
    python 2048game.py $run3
done

for i in 1 1 1 1 1
do
    python 2048game.py $run4
done

for i in 1 1 1 1 1
do
    python 2048game.py $run5
done
