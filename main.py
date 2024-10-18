import matplotlib.pyplot as plt
from nguyenpanda.swan import green, yellow

import autograd
from autograd.func import *


@autograd.utils.performance()
def demo1():
    with autograd.utils.PerformanceTimer() as timer:
        x = autograd.symbol('x')
        f = Cos(x) + Sin(x * x / 100) * x / 50

        rand = (-30, 100)
        n_points = 10000

        linspace = [rand[0] + i * (rand[1] - rand[0]) / (n_points - 1) for i in range(n_points)]
        nodes = [f.evaluate_and_derive(x, x=value) for value in linspace]

    val = [v.v for v in nodes]
    der = [v.p for v in nodes]

    plt.scatter(linspace, val, label="Function Values", color="blue", s=1)
    plt.scatter(linspace, der, label="Derivative Values", color="red", s=1)
    plt.legend()
    plt.title("Function and Derivative Values")
    plt.grid(True)
    plt.xlabel("x values (0 to 99)")
    plt.ylabel("f(x) and f'(x)")
    plt.show()

    return timer()


@autograd.utils.performance()
def demo2():
    with autograd.utils.PerformanceTimer() as timer:
        x = autograd.symbol('x')
        f = 'x*x+1/(sin(x)-1.05)'
        f = autograd.parser.parser_expression(f)

        rand = (-5, 5)
        n_points = 10000

        linspace = [rand[0] + i * (rand[1] - rand[0]) / (n_points - 1) for i in range(n_points)]
        nodes = [f.evaluate_and_derive(x, x=value) for value in linspace]

    val = [v.v for v in nodes]
    der = [v.p for v in nodes]

    plt.scatter(linspace, val, label="Function Values", color="blue", s=1)
    plt.scatter(linspace, der, label="Derivative Values", color="red", s=1)
    plt.legend()
    plt.title("Function and Derivative Values")
    plt.grid(True)
    plt.xlabel("x values (0 to 99)")
    plt.ylabel("f(x) and f'(x)")
    plt.show()

    return timer()


@autograd.utils.performance()
def demo3():
    with autograd.utils.PerformanceTimer() as timer:
        x = autograd.symbol('x')

        f = '4*x - x*x + 10*sin(x) + cos(ln(x+10)-x) + 10'
        f = autograd.parser.parser_expression(f)

        xn, threshold, alpha, idx = 0, 1e-10, 0.8, 0
        node = f.evaluate_and_derive(x, x=xn)
        val = node.v
        der = node.p
        while abs(val) > threshold:
            print(f'{idx: >4}. f({xn: 20.15f}) = {val: 20.15f} | df = {der: 20.15f}')
            xn = xn - alpha * val / der  # Newton-Raphson update step
            idx += 1
            node = f.evaluate_and_derive(x, x=xn)
            val = node.v
            der = node.p
        print(yellow(f'{idx: >4}. f({xn: 20.15f}) = {val: 20.15f} | df = {der: 20.15f}'))

        xm, threshold, alpha, idx = 2, 1e-10, 0.8, 0
        node = f.evaluate_and_derive(x, x=xm)
        val = node.v
        der = node.p
        while abs(val) > threshold:
            print(f'{idx: >4}. f({xm: 20.15f}) = {val: 20.15f} | df = {der: 20.15f}')
            xm = xm - alpha * val / der  # Newton-Raphson update step
            idx += 1
            node = f.evaluate_and_derive(x, x=xm)
            val = node.v
            der = node.p

        print(yellow(f'{idx: >4}. f({xm: 20.15f}) = {val: 20.15f} | df = {der: 20.15f}'))

        n, rand = 10000, (-5, 8)
        linspace = [rand[0] + i * (rand[1] - rand[0]) / (n - 1) for i in range(n)]
        nodes = [f.evaluate_and_derive(x, x=value) for value in linspace]

    val, der = [v.v for v in nodes], [v.p for v in nodes]

    plt.figure(figsize=(10, 6))
    plt.scatter(linspace, val, label="Function Values", color="blue", s=1)
    plt.scatter(linspace, der, label="Derivative Values", color="red", s=1)

    plt.scatter([xn], [0], color='green', s=100, zorder=5, label="Root (f(x) = 0)")
    plt.scatter([xm], [0], color='green', s=100, zorder=5, label="Root (f(x) = 0)")
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(xn, color='green', linestyle='--', label=f'Root at x = {xn:.5f}')
    plt.axvline(xm, color='green', linestyle='--', label=f'Root at x = {xm:.5f}')
    plt.axvline(0, color='black', linewidth=1)

    plt.legend()
    plt.title("Function, Derivative Values, and Root")
    plt.grid(True)
    plt.xlabel("x values")
    plt.ylabel("f(x) and f'(x)")
    plt.show()

    return timer()


if __name__ == '__main__':
    total_time, calculate_time = demo1()
    print('`demo1` calculated in', green(calculate_time), 'ms')
    print('`demo1` executed in', green(total_time), 'ms')
    print(yellow('=' * 30))

    total_time, calculate_time = demo2()
    print('`demo2` calculated in', green(calculate_time), 'ms')
    print('`demo2` executed in', green(total_time), 'ms')
    print(yellow('=' * 30))

    total_time, calculate_time = demo3()
    print('`demo3` calculated in', green(calculate_time), 'ms')
    print('`demo3` executed in', green(total_time), 'ms')
    print(yellow('=' * 30))
