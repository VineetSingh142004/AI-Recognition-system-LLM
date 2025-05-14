@echo off
set CUDA_VISIBLE_DEVICES=0
set OMP_NUM_THREADS=4
set MKL_NUM_THREADS=4
python src/main.py