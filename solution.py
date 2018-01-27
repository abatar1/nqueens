#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script uses nqueens.py module for solving 8-queens problem by using 
a genetic algorithm
"""
import sys
import nqueens as nq


if __name__ == '__main__':
    print('Python version:', sys.version)
    solver = nq.Solver_8_queens()
    best_fit, epoch_num, visualization = solver.solve(1.0, 1000)
    print("Best solution:")
    print("Fitness:", best_fit)
    print("Iterations:", epoch_num)
    print(visualization)
