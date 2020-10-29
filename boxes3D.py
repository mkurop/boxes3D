import rtree

class boxStack:
    '''
    Klasa przechowująca dane\n
    stosu pudełek z wejścia programu
    '''

    def __init__(self):
        '''Stos pudełek'''
        self.stack = []

    def get_stack(self):
        '''
        Funkcja get stosu\n
        :return: Obecny stos\n
        :rtype: boxStack
        '''
        return self.stack

    def set_stack(self, new_stack):
        '''
        Funkcja set stosu \n
        :param new_stack: aktualizowanie stanu stosu
        '''
        self.stack = new_stack

    def append(self, added):
        '''
        Funkcja append stosu\n
        :param added: element do dodania do stosu
        '''
        self.stack.append(added)

    def extend(self, added):
        '''
        Funkcje extend stosu\n
        :param added: element, który posłuży do rozszerzenia stosu
        '''
        self.stack.extend(added)

    def pop(self):
        '''
        Funkcje pop stosu\n
        :return: stos pomniejszony o ostatni element\n
        :rtype: boxStack
        '''
        return self.stack.pop()

class tree:
    '''Klasa przechowująca instrukcje drzewa'''

    def __init__(self):
        '''Tworzenie drzewa'''
        self.properties = rtree.index.Property()
        self.properties.dimension = 3
        self.tree = rtree.index.Index('3d_index', properties=self.properties)

    def get_tree(self):
        '''
        Funkcje get drzewa\n
        :return: drzewo rtree na którym algorytm główny zamieszcza pudełka\n
        :rtype: rtree
        '''
        return self.tree

    def set_tree(self, new_tree):
        '''
        Funkcje set drzewa\n
        :param new_tree: nowe drzewo
        '''
        self.tree = new_tree
