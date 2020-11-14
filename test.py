from elliptic_curve_cryptosystem import *

# Y^2 = X^3 + 2X + 9 (mod 23)

if __name__ == '__main__':
    a = 2
    b = 9
    p = 23
    # get all the point on 'curve'
    res = []
    for i in range(p):
        try:
            temp = computing_square_roots(a, b, p, i)
            if temp:
                res.extend([(i, j) for j in temp])
        except AssertionError:
            continue
    print('\n----compute the order of all points-----\n')
    # figure out all points's order
    for point in res:
        order = order_of_given_point(a, b, p, point)
        print(f"Order of the point ({point[0]:<2}, {point[1]:2}) is {order}.")
    