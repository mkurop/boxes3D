#!/usr/bin/env python3
import os
import rtree
import math
from portion import closed, closedopen, openclosed
# Notatka, bo nie przyjmuje nie zmienionego kodu
# usuwanie plików z poprzedniego działania programu
try:
    os.remove('3d_index.idx')
    os.remove('3d_index.dat')
except:
    pass


class box3D:
    def __init__(self, interval_x, interval_y, interval_z):
        self.interval_x = interval_x
        self.interval_y = interval_y
        self.interval_z = interval_z

    def get_interval_x(self):
        return self.interval_x

    def get_interval_y(self):
        return self.interval_y

    def get_interval_z(self):
        return self.interval_z

    @staticmethod
    def factory(x1, y1, z1, x2, y2, z2):
        return box3D(closed(x1, x2), closed(y1, y2), closed(z1, z2))


class boxStack:
    def __init__(self):
        self.stack = []

    def get_stack(self):
        return self.stack

    def set_stack(self, new_stack):
        self.stack = new_stack

    def append(self, added):
        self.stack.append(added)

    def extend(self, added):
        self.stack.extend(added)

    def pop(self):
        return self.stack.pop()


class tree:
    def __init__(self):
        # tworzenie drzewa
        self.properties = rtree.index.Property()
        # ustawienia drzewa
        self.properties.dimension = 3
        self.tree = rtree.index.Index('3d_index', properties=self.properties)

    def get_tree(self):
        return self.tree

    def set_tree(self, new_tree):
        self.tree = new_tree


class algorytm:
    def permute(self, sortin, permutation):
        assert len(sortin) == len(permutation)
        return [sortin[i] for i in permutation]

    def my_sort(self, inputlist):
        inputlist = zip(inputlist, range(len(inputlist)))
        aux = sorted(inputlist, key = lambda x : x[0])
        sorted2in = [aux[i][1] for i in range(len(aux))]
        list2 = zip(sorted2in, range(len(sorted2in)))
        aux1 = sorted(list2, key = lambda x : x[0])
        in2sorted = [aux1[i][1] for i in range(len(aux1))]
        sort = [aux[i][0] for i in range(len(aux))]
        return sort, in2sorted, sorted2in

    def divide_in(self, int1, int2):
        return [int1 | int2]

    def divide_half_out(self, int1, int2):
        up, low = (int1.upper, int2.upper), (int1.lower, int2.lower)
        if int2.lower == int1.lower:
            return [closed(min(low), min(up)), openclosed(min(up), max(up))]
        else:
            return [closed(min(low), max(low)), openclosed(max(low), max(up))]

    def divide_out(self, int1, int2):
        inter = int1 & int2
        return [int1 - inter, inter, int2 - inter]

    def divide_equal(self, int1, int2):
        return [closedopen(int1.lower, math.floor(int1.upper/2)), openclosed(math.floor(int2.upper/2), int2.upper)]

    def is_in(self, interval1, interval2):
        union = interval1 & interval2
        return True if ((union == interval1) ^ (union == interval2)) and (interval2.lower != interval1.lower and interval1.upper != interval2.upper)  else False

    def is_equal(self, interval1, interval2):
        return True if interval1 == interval2 else False

    def is_out(self, interval1, interval2):
        return True if (interval1.lower != interval2.lower) and (interval2.upper != interval1.upper) and (interval1 & interval2) else False

    def is_separate(self, int1, int2):
        return False if int1 & int2 else True

    def is_half_out(self, int1, int2):
        return True if ((int1.lower == int2.lower) ^ (int2.upper == int1.upper)) and ((int2 == int2 & int1) ^ (int1 == int1 & int2)) else False

    def rozbij(self, q, i):
        print(q.interval_x, q.interval_y, q.interval_z)
        print(i.interval_x, i.interval_y, i.interval_z,'\n')
        sort, in2sorted, sorted2in = self.my_sort(self.canonical(q.interval_x, q.interval_y, q.interval_z, i.interval_x, i.interval_y, i.interval_z))
        if sort == ['in I II', 'in I II', 'in I II']:
            return [box3D(i.interval_x, i.interval_y, i.interval_z)]
        elif sort == ['in II I', 'in II I', 'in II I']:
            return [box3D(q.interval_x, q.interval_y, q.interval_z)]
        elif sort == ['in I II', 'in I II', 'in II I']:
            return [box3D(q.interval_x, q.interval_y, q.interval_z), box3D(i.interval_x, i.interval_y, closed(i.interval_z.lower, q.interval_z.lower)),
                    box3D(i.interval_x, i.interval_y, closed(q.interval_z.upper, i.interval_z.upper))]

            #1  2  3  3  5  7
            #2  3  2  4  7  7

    def canonical_int(self, int_x, int_x_i, int_y, int_y_i, int_z, int_z_i):
        results = []

        return results

    def canonical_box(self, inter, inter_i):
        if self.is_in(inter, inter_i):
            if inter.upper < inter_i.upper:
                return 'in I II'
            else:
                return 'in II I'
        elif self.is_half_out(inter, inter_i):
            if inter.upper < inter_i.upper:
                return 'h-o I II'
            else:
                return 'h-o II I'
        elif self.is_equal(inter, inter_i):
            return 'e'
        elif self.is_out(inter, inter_i):
            if inter.upper < inter_i.upper:
                return 'o I II'
            else:
                return 'o II I'
        elif self.is_separate(inter, inter_i):
            return 's'

    def canonical(self, inter_x, inter_y, inter_z, inter_x_i, inter_y_i, inter_z_i):
        return self.canonical_box(inter_x, inter_x_i),  self.canonical_box(inter_y, inter_y_i),  self.canonical_box(inter_z, inter_z_i)


    @staticmethod
    # początek funkcji głównej
    def algorytm(Q, tree):
        iD = 0
        alg = algorytm()
        # główna pętla trwająca do skrócenia długości wejściowego zbioru do wartości 0
        while not len(Q.get_stack()) == 0:
            # komenda pop
            q = Q.pop()
            # sprawdzanie czy w drzewie pudełko q się przecina
            if list(tree.tree.intersection(([q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper]), True)):
                # zwrócenie z drzewa pierwszego obiektu, z którym pudełko się przecina
                i = list(tree.tree.intersection((q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper), True))[0]
                inter = [item for item in i.bbox]
                tree.tree.delete(i.id, [i.bounds[0], i.bounds[2], i.bounds[4], i.bounds[1], i.bounds[3], i.bounds[5]])
                i = box3D.factory(inter[0], inter[1], inter[2], inter[3], inter[4], inter[5])
                #print(q.interval_x, q.interval_y, q.interval_z)
                canonical = alg.rozbij(q, i)
                Q.append(canonical[0]) if type(canonical) is not tuple else Q.extend(k for k in canonical)
            else:
                #print(q.interval_x, q.interval_y, q.interval_z)
                # w przeciwnym wypadku dodanie do drzewa nowego pudełka
                tree.tree.insert(iD, [q.interval_x.lower, q.interval_y.lower, q.interval_z.lower, q.interval_x.upper, q.interval_y.upper, q.interval_z.upper])
                # zwiększenie zmiennej iD
                iD += 1
        # wypisanie drzewa
        lista = tree.tree.intersection(tree.tree.get_bounds(), True)
        lista = [(item.bbox)for item in lista]
        print('\n')
        for i in lista:
            print([i[0], i[3]], end = '') if i[0] != i[3] else print([i[0]], end = '')
            print(' x ', end = '')
            print([i[1], i[4]], end = '') if i[1] != i[4] else print([i[1]], end = '')
            print(' x ', end = '')
            print([i[2], i[5]], end = '\n') if i[2] != i[5] else print([i[2]], end = '\n')
        #zwrócenie drzewa
        return tree.tree


Q = boxStack()


pudelka = int(input('Ile pudełek?: '))
for i in range(pudelka):
    # (int(num) for num in input('\nPodaj 6 liczb dla jednego z pudełek oddzielonput()), int(input()), int(input()), ine spacją oraz przecinkiem: '))
    Q.append(box3D.factory(int(input("Podaj po jednej z sześciu współrzędnych pudełka oddzielonych enterem: \n")), int(input()), int(input()), int(input()), int(input()), int(input())))
algorytm.algorytm(Q, tree())


'''TEST FUNKCJI'''
'''
import unittest
class testing(unittest.TestCase):
    def setUp(self):
        self.we1 = [0, 1, 2, 5, 6, 7]
        self.we2 = [10, 20, 30, 44, 22, 31]
        self.we3 = [-2, 10, 3, 11, 13, 5]
        self.q = boxStack()
        self.q.append(box3D.factory(self.we1[0], self.we1[1],self.we1[2],self.we1[3],self.we1[4],self.we1[5]))
        self.i = list(tree().tree.intersection((self.we1[0], self.we1[1],self.we1[2],self.we1[3],self.we1[4],self.we1[5]), objects=True))
        self.tree = tree()
        self.tree.tree.insert(0, self.we1)
    def test_funkcji_algorytm(self):
        self.assertTrue(algorytm().algorytm(self.q,self.tree).get_bounds() == self.tree.tree.get_bounds())
    def test_funkcji_rozbij(self):
        self.q = box3D.factory(self.we1[0], self.we1[1],self.we1[2],self.we1[3],self.we1[4],self.we1[5])
        self.i = box3D(closed(self.we1[0],self.we1[3]), closed(self.we1[1],self.we1[4]), closed(self.we1[2],self.we1[5]))
        self.assertEqual(algorytm().rozbij(self.q, self.i) , (algorytm().rozbijanie(closed(self.we1[0], self.we1[3]), closed(self.we1[0], self.we1[3])),algorytm().rozbijanie(closed(self.we1[1], self.we1[4]), closed(self.we1[1], self.we1[4])),algorytm().rozbijanie(closed(self.we1[2], self.we1[5]), closed(self.we1[2], self.we1[5]))))
    def test_funkcji_rozbijanie(self):
        self.assertEqual(algorytm().rozbijanie(closed(self.we3[1], self.we3[4]),closed(self.we2[0], self.we2[3])), (empty(), closed(10,13), openclosed(13, 44)))



if __name__ == '__main__':
    unittest.main()

'''
