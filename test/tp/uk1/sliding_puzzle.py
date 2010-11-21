# -*- coding: cp1250 -*-


# Projekt zespołowy.
# Projekt: Układanka przesuwanka.
# Realizacja: Bartosz Andreatto, Paweł Born : I1-32, grupa A


import math
import copy
import random
from Queue import PriorityQueue


# ---------------------------------------------------------------------TESTY-----------------------------------------------------

class PuzzleState():
    '''Klasa reprezentująca stan planszy.'''
    
    # Prywatny atrybut określający rozmiar planszy.
    __dimension = 3
    
    # Akcesor umożliwiający odczyt rozmiaru planszy.
    @staticmethod
    def get_dimension():
        return PuzzleState.__dimension
    
    # Funkcja wywoływana podczas tworzenia instancji danej klasy.
    def __init__(self, parent, puzzle_board):
        if parent is None:
            self.__puzzle_board = puzzle_board[:]
            
            self.compute_heuristic_grade()
        else:
            self.__parent = parent
            self.__puzzle_board = parent.__puzzle_board[:]
    
    # Prywatny atrybut określający aktualną planszę.
    __puzzle_board = []
    
    # Prywatny atrybut określający "rodzica" danego stanu planszy.
    __parent = None
    
    # Prywatny atrybut określający "dzieci" danego stanu planszy.
    __children = []
    
    # Prywatny atrybut określający faktyczny koszt przejścia od stanu początkowego.
    __g = 0
    
    # Prywatny atrybut określający wartość heurystyki szacującą koszt przejścia do stanu docelowego.
    __h = 0
    
    # Akcesor umożliwiający odczyt aktualnej planszy.
    def get_puzzle_board(self):
        return self.__puzzle_board
    
    # Akcesor umożliwiający zapis aktualnej planszy.
    def set_puzzle_board(self, new_puzzle_board):
        self.__puzzle_board = new_puzzle_board[:]
        
    # Akcesor umożliwiający odczyt "rodzica" aktualnego stanu planszy. 
    def get_parent(self):
        return self.__parent
        
    # Akcesor umożliwiający zapis "rodzica" aktualnego stanu planszy.
    def set_parent(self, new_parent):
        self.__parent = new_parent
        
    # Akcesor umożliwiający odczyt "dzieci" aktualnego stanu planszy.
    def get_children(self):
        return self.__children
        
    # Akcesor umożliwiający zapis "dzieci" aktualnego stanu planszy.
    def set_children(self, new_children):
        self.__children = new_children[:]
        
    # Akcesor umożliwiający odczyt faktycznego kosztu przejścia od stanu początkowego.
    def get_g(self):
        return self.__g
        
    # Akcesor umożliwiający zapis faktycznego kosztu przejścia od stanu początkowego.
    def set_g(self, new_g):
        self.__g = new_g
        
    # Akcesor umożliwiający odczyt wartości heurystyki szacującej koszt przejścia do stanu docelowego.
    def get_h(self):
        return self.__h
        
    # Akcesor umożliwiający zapis wartości heurystyki szacującej koszt przejścia do stanu docelowego.
    def set_h(self, new_h):
        self.__h = new_h
        
    # Metoda wyznaczająca poziom heurystyki danej planszy.
    def compute_heuristic_grade(self):
        heuristic_grade = 0

        for search_row in range(0, PuzzleState.__dimension):
            for search_column in range(0, PuzzleState.__dimension):
                heuristic_grade += math.fabs(search_column - math.fmod(self.__puzzle_board[search_row * PuzzleState.__dimension + search_column] - 1, PuzzleState.__dimension)) + math.fabs(search_row - math.floor((self.__puzzle_board[search_row * PuzzleState.__dimension + search_column] - 1) / PuzzleState.__dimension))
                
        self.__h = int(heuristic_grade / 2)
    
    # Metoda wyznaczająca klucz identyfikujący daną planszę.
    def get_hash_code(self):
        hash_code = ''
        
        for search_row in range(0, PuzzleState.__dimension):
            hash_code += '|'
            
            for search_column in range(0, PuzzleState.__dimension):
                if self.__puzzle_board[search_row * PuzzleState.__dimension + search_column] != PuzzleState.__dimension * PuzzleState.__dimension:
                    hash_code += str(self.__puzzle_board[search_row * PuzzleState.__dimension + search_column])
                else:
                    hash_code += ' '
                
                hash_code += '|'
            
            if search_row < PuzzleState.__dimension - 1:
                hash_code += '\n'
        
        return hash_code
    
    # Metoda uaktualniająca daną komórkę planszy.
    def set_value(self, search_row, search_column, new_value):
        self.__puzzle_board[search_row * PuzzleState.__dimension + search_column] = new_value
        

class PuzzleSolution():
    '''Klasa rozwiązująca układankę.'''
    
    # Prywatny atrybut określający ilość iteracji mieszających planszę.
    __mix_iterator = 100
    
    # Prywatny atrybut określający nazwę pliku zawierającego początkową planszę.
    __file_name = 'my_board.txt'
    
    # Akcesor umożliwiający odczyt ilości iteracji mieszających planszę.
    @staticmethod
    def get_mix_iterator():
        return PuzzleSolution.__mix_iterator
    
    # Akcesor umożliwiający odczyt nazwy pliku zawierającego początkową planszę.
    @staticmethod
    def get_file_name():
        return PuzzleSolution.__file_name
    
    # Funkcja wywoływana podczas tworzenia instancji danej klasy.
    def __init__(self):
        pass
        
    # Prywatny atrybut określający stany zakwalifikowane do analizy.
    __open = PriorityQueue()
    
    # Prywatny atrybut określający stany poddane analizie.
    __closed = {}
    
    # Prywatny atrybut określający stan będący stanem początkowym układanki.
    __initial_state = None
    
    # Prywatny atrybut określający stan będący rozwiązaniem układanki.
    __solution_state = None
    
    # Prywatny atrybut określający początkową planszę.
    __initial_board = []
    
    # Akcesor umożliwiający odczyt stanów poddanych analizie.
    def get_closed(self):
        return self.__closed
        
    # Akcesor umożliwiający odczyt stanu będącego rozwiązaniem układanki.
    def get_solution_state(self):
        return self.__solution_state
        
    # Prywatna metoda wyznaczająca "dzieci" danego stanu planszy.
    def __build_children(self, puzzle_state):
        flag_found = False
        
        for search_row in range(0, PuzzleState.get_dimension()):
            for search_column in range(0, PuzzleState.get_dimension()):
                if puzzle_state.get_puzzle_board()[search_row * PuzzleState.get_dimension() + search_column] == PuzzleState.get_dimension() * PuzzleState.get_dimension():
                    flag_found = True
                    
                    break
            
            if flag_found:
                break
                
        children = []
        
        if search_row != 0:                                     # up
            new_child_up = PuzzleState(puzzle_state, None)
            
            new_child_up.set_value(search_row, search_column, puzzle_state.get_puzzle_board()[(search_row - 1) * PuzzleState.get_dimension() + search_column])
            new_child_up.set_value(search_row - 1, search_column, PuzzleState.get_dimension() * PuzzleState.get_dimension())
            
            new_child_up.compute_heuristic_grade()
            new_child_up.set_g(new_child_up.get_g() + 1)
            
            children.append(new_child_up)
            
        if search_row != PuzzleState.get_dimension() - 1:       # down
            new_child_down = PuzzleState(puzzle_state, None)
            
            new_child_down.set_value(search_row, search_column, puzzle_state.get_puzzle_board()[(search_row + 1) * PuzzleState.get_dimension() + search_column])
            new_child_down.set_value(search_row + 1, search_column, PuzzleState.get_dimension() * PuzzleState.get_dimension())
            
            new_child_down.compute_heuristic_grade()
            new_child_down.set_g(new_child_down.get_g() + 1)

            children.append(new_child_down)
            
        if search_column != 0:                                  # left
            new_child_left = PuzzleState(puzzle_state, None)
            
            new_child_left.set_value(search_row, search_column, puzzle_state.get_puzzle_board()[search_row * PuzzleState.get_dimension() + search_column - 1])
            new_child_left.set_value(search_row, search_column - 1, PuzzleState.get_dimension() * PuzzleState.get_dimension())
            
            new_child_left.compute_heuristic_grade()
            new_child_left.set_g(new_child_left.get_g() + 1)

            children.append(new_child_left)
            
        if search_column != PuzzleState.get_dimension() - 1:    # right
            new_child_right = PuzzleState(puzzle_state, None)    
            
            new_child_right.set_value(search_row, search_column, puzzle_state.get_puzzle_board()[search_row * PuzzleState.get_dimension() + search_column + 1])
            new_child_right.set_value(search_row, search_column + 1, PuzzleState.get_dimension() * PuzzleState.get_dimension())
            
            new_child_right.compute_heuristic_grade()
            new_child_right.set_g(new_child_right.get_g() + 1)
            
            children.append(new_child_right)

        return children
        
    # Prywatna Metoda sprawdzająca czy dany stan układanki jest stanem końcowym.
    def __is_solution(self, puzzle_state):
        if puzzle_state.get_h() == 0:
            return True
        
        return False
        
    # Prywatna metoda wyznaczająca rozwiązanie układanki.
    def __do_search(self):
        current_state = copy.deepcopy(self.__initial_state)
        
        while True:
            if self.__is_solution(current_state):
                self.__solution_state = copy.deepcopy(current_state)
                
                break
            else:
                current_state.set_children(self.__build_children(current_state))
                
                children = current_state.get_children()[:]
                for puzzle_state in children:
                    if puzzle_state.get_hash_code() in self.__closed:
                        continue
                    else:
                        tmp_open = PriorityQueue()
                        
                        found_the_same = False
                        found_the_same_better = False
                        for counter in range(0, self.__open.qsize()):
                            existing_puzzle_state = self.__open.get()
                        
                            if puzzle_state.get_hash_code() == existing_puzzle_state[1].get_hash_code():
                                found_the_same = True
                                
                                if puzzle_state.get_g() < existing_puzzle_state[1].get_g():
                                    found_the_same_better = True
                                    
                                    tmp_open.put((puzzle_state.get_g() + puzzle_state.get_h(), puzzle_state))
                            
                            if not found_the_same_better:
                                tmp_open.put(existing_puzzle_state)
                                
                            found_the_same_better = False
                        
                        if not found_the_same:
                            tmp_open.put((puzzle_state.get_g() + puzzle_state.get_h(), puzzle_state))
                        
                        while not tmp_open.empty():
                            self.__open.put(tmp_open.get())
                        
            self.__closed[current_state.get_hash_code()] = current_state
            
            if self.__open.empty():
                break
            else:
                current_state = self.__open.get()[1]
        
    # Prywatna metoda wyznaczająca w sposób losowy początkową planszę.
    def __rand_values(self):
        
        for search_row in range(0, PuzzleState.get_dimension()):
            for search_column in range(0, PuzzleState.get_dimension()):
                self.__initial_board.append(search_row * PuzzleState.get_dimension() + search_column + 1)
                
        blank_row = PuzzleState.get_dimension() - 1
        blank_column = PuzzleState.get_dimension() - 1
        
        random.seed()
        
        for counter in range(0, PuzzleSolution.__mix_iterator):
            current_direction = random.randint(1, PuzzleState.get_dimension())

            if current_direction == 1:      # up
                if blank_row != 0:
                    self.__initial_board[blank_row * PuzzleState.get_dimension() + blank_column] = self.__initial_board[(blank_row - 1) * PuzzleState.get_dimension() + blank_column]
                    self.__initial_board[(blank_row - 1) * PuzzleState.get_dimension() + blank_column] = PuzzleState.get_dimension() * PuzzleState.get_dimension()
                    
                    blank_row -= 1
                
            elif current_direction == 2:    # down
                if blank_row != PuzzleState.get_dimension() - 1:
                    self.__initial_board[blank_row * PuzzleState.get_dimension() + blank_column] = self.__initial_board[(blank_row + 1) * PuzzleState.get_dimension() + blank_column]
                    self.__initial_board[(blank_row + 1) * PuzzleState.get_dimension() + blank_column] = PuzzleState.get_dimension() * PuzzleState.get_dimension()
                    
                    blank_row += 1
                
            elif current_direction == 3:    # left
                if blank_column != 0:
                    self.__initial_board[blank_row * PuzzleState.get_dimension() + blank_column] = self.__initial_board[blank_row * PuzzleState.get_dimension() + blank_column - 1]
                    self.__initial_board[blank_row * PuzzleState.get_dimension() + blank_column - 1] = PuzzleState.get_dimension() * PuzzleState.get_dimension()
                    
                    blank_column -= 1
                
            else:                           # right
                if blank_column != PuzzleState.get_dimension() - 1:
                    self.__initial_board[blank_row * PuzzleState.get_dimension() + blank_column] = self.__initial_board[blank_row * PuzzleState.get_dimension() + blank_column + 1]
                    self.__initial_board[blank_row * PuzzleState.get_dimension() + blank_column + 1] = PuzzleState.get_dimension() * PuzzleState.get_dimension()
                    
                    blank_column += 1
    
    # Prywatna metoda wypisująca ścieżkę przejść stanów.
    def __print_path_states(self):
        print '------------------------------'
        print 'Ścieżka przejść stanów:'
        print '------------------------------'
        print ''
        
        path_states = []
        current_state = self.__solution_state
        
        path_states.append(current_state)
        while not current_state.get_parent() is None:
            current_state = current_state.get_parent()
        
            path_states.append(current_state)
        
        path_states.reverse()
        
        for puzzle_state in path_states:
            print puzzle_state.get_hash_code()
            print ''
            
    # Prywatna metoda zapisująca daną planszę do pliku tekstowego.
    def __write_board(self):
        file_wr = open(PuzzleSolution.__file_name, 'w')
        
        for counter in range(0, PuzzleState.get_dimension() * PuzzleState.get_dimension()):
            file_wr.write(str(self.__initial_board[counter]))
            
            if math.fmod(counter + 1, PuzzleState.get_dimension()) == 0:
                if counter != PuzzleState.get_dimension() * PuzzleState.get_dimension() - 1:
                    file_wr.write('\n')
            else:
                file_wr.write(' ')
                
        file_wr.flush()
        file_wr.close()
        
    # Główna metoda testująca.
    def run_test(self):
        self.__rand_values()

        self.__write_board()
        
        self.__initial_state = PuzzleState(None, self.__initial_board)
        
        self.__do_search()
        
        print ''
        
        print '------------------------------'
        print 'Początkowy stan planszy:'
        print '------------------------------'
        print ''
        
        print self.__initial_state.get_hash_code()
        print ''
        
        self.__print_path_states()
        
        print '------------------------------'
        print 'Końcowy stan planszy:'
        print '------------------------------'
        print ''
        
        print self.__solution_state.get_hash_code()
        print ''
        
# ---------------------------------------------------------------------TESTY-----------------------------------------------------


class PuzzleSliding():
    '''Klasa reprezentująca stan gry.'''
    
    # Funkcja wywoływana podczas tworzenia instancji danej klasy.
    def __init__(self):
        pass
        
    # Prywatny atrybut określający planszę.
    __puzzle_board = []
    
    # Prywatny atrybut okeślający sąsiadów pustej komórki.
    __neighbours = []
    
    # Prywatny atrybut określający ilość wykonanych ruchów.
    __counter_movements = 0
    
    # Prywatna metoda odczytująca daną planszę z pliku tekstowego.
    def __read_board(self):
        return_flag = True
        
        try:
            file_re = open(PuzzleSolution.get_file_name(), 'r')
        
            lines_file = file_re.readlines()
            if len(lines_file) != PuzzleState.get_dimension():
                return_flag = False
            else:    
                for each_line in lines_file:
                    numbers = each_line.split()
                    
                    if len(numbers) != PuzzleState.get_dimension():
                        return_flag = False
                        
                        break
                    
                    for num in numbers:
                        self.__puzzle_board.append(int(num))
            
            file_re.close()
        except IOError:
            return_flag = False
            
        return return_flag
        
    # Prywatna metoda sprawdzająca poprawność stanu planszy.
    def __check_correctness_board(self):
        for counter_value in range(0, PuzzleState.get_dimension() * PuzzleState.get_dimension() - 1):
            value = self.__puzzle_board[counter_value]
            
            if value < 1 or value > PuzzleState.get_dimension() * PuzzleState.get_dimension():
                return False
            
            for counter_compare_value in range(counter_value + 1, PuzzleState.get_dimension() * PuzzleState.get_dimension()):
                compare_value = self.__puzzle_board[counter_compare_value]
                
                if value == compare_value:
                    return False
        
        return True

    # Prywatna metoda sprawdzająca czy dany stan planszy jest stanem końcowym.
    def __is_finite_state(self):
        flag_return = True
        
        for search_row in range(0, PuzzleState.get_dimension()):
            for search_column in range(0, PuzzleState.get_dimension()):
                if self.__puzzle_board[search_row * PuzzleState.get_dimension() + search_column] != search_row * PuzzleState.get_dimension() + search_column + 1:
                    flag_return = False
                    
                    break
                    
        return flag_return

    # Prywatna metoda wypisująca stan aktualnej planszy.
    def __print_puzzle_board(self):
        printed_board = ''
        
        for search_row in range(0, PuzzleState.get_dimension()):
            printed_board += '|'
            
            for search_column in range(0, PuzzleState.get_dimension()):
                if self.__puzzle_board[search_row * PuzzleState.get_dimension() + search_column] != PuzzleState.get_dimension() * PuzzleState.get_dimension():
                    printed_board += str(self.__puzzle_board[search_row * PuzzleState.get_dimension() + search_column])
                else:
                    printed_board += ' '
                    
                printed_board += '|'
                
            if search_row < PuzzleState.get_dimension() - 1:
                printed_board += '\n'
                
        print printed_board

    # Prywatna metoda wyznaczająca sąsiadów pustej komórki.
    def __find_neighbours(self):
        flag_found = False
        
        for search_row in range(0, PuzzleState.get_dimension()):
            for search_column in range(0, PuzzleState.get_dimension()):
                if self.__puzzle_board[search_row * PuzzleState.get_dimension() + search_column] == PuzzleState.get_dimension() * PuzzleState.get_dimension():
                    flag_found = True
                    
                    break
            
            if flag_found:
                break

        list_neighbours = []
        
        if search_row != 0:                                     # up neighbour
            list_neighbours.append(self.__puzzle_board[(search_row - 1) * PuzzleState.get_dimension() + search_column])
            
        if search_row != PuzzleState.get_dimension() - 1:       # down neighbour
            list_neighbours.append(self.__puzzle_board[(search_row + 1) * PuzzleState.get_dimension() + search_column])
            
        if search_column != 0:                                  # left neighbour
            list_neighbours.append(self.__puzzle_board[search_row * PuzzleState.get_dimension() + search_column - 1])
            
        if search_column != PuzzleState.get_dimension() - 1:    # right neighbour
            list_neighbours.append(self.__puzzle_board[search_row * PuzzleState.get_dimension() + search_column + 1])
            
        self.__neighbours = list_neighbours

    # Prywatna metoda sprawdzająca poprawność wykonanego ruchu.
    def __check_neighbour(self, set_neighbour):
        return_flag = False
        
        for neighbour in self.__neighbours:
            if neighbour == set_neighbour:
                return_flag = True
                
                break
                
        return return_flag

    # Prywatna metoda wykonująca ruch na planszy.
    def __move_nums(self, neighbour):
        flag_found_empty = False
        
        for search_empty_row in range(0, PuzzleState.get_dimension()):
            for search_empty_column in range(0, PuzzleState.get_dimension()):
                if self.__puzzle_board[search_empty_row * PuzzleState.get_dimension() + search_empty_column] == PuzzleState.get_dimension() * PuzzleState.get_dimension():
                    flag_found_empty = True
                    
                    break
                    
            if flag_found_empty:
                break
                
        flag_found_neighbour = False
        
        for search_neighbour_row in range(0, PuzzleState.get_dimension()):
            for search_neighbour_column in range(0, PuzzleState.get_dimension()):
                if self.__puzzle_board[search_neighbour_row * PuzzleState.get_dimension() + search_neighbour_column] == neighbour:
                    flag_found_neighbour = True
                    
                    break
                    
            if flag_found_neighbour:
                break
                
        self.__puzzle_board[search_empty_row * PuzzleState.get_dimension() + search_empty_column] = neighbour
        self.__puzzle_board[search_neighbour_row * PuzzleState.get_dimension() + search_neighbour_column] = PuzzleState.get_dimension() * PuzzleState.get_dimension()
        
    # Główna metoda.
    def run_game(self):
        if self.__read_board():
            if self.__check_correctness_board():
                print 'Rozpoczęcie gry.'
                print '(Wyjście z programu: q)'
                print ''
                
                exit_decision = False
                
                while not self.__is_finite_state():
                    print 'Ilość wykonanych ruchów: ', str(self.__counter_movements)
                    print 'Stan planszy:'
                    self.__print_puzzle_board()
                    print ''
                    
                    self.__find_neighbours()
                    string_decision = 'Twój ruch (' + str(self.__neighbours) + '): '
                    
                    try:
                        decision = raw_input(string_decision)
                        if decision.lower() == 'q':
                            exit_decision = True
                            
                            break
                        else:
                            move_decision = int(decision)
                            print ''
                            
                            if not self.__check_neighbour(move_decision):
                                print 'Uwaga. Wykonano nieprawidłowy ruch.'
                                print ''
                                
                            else:
                                self.__move_nums(move_decision)
                                
                                self.__counter_movements += 1
                    except:
                        print ''
                        print 'Uwaga. Nieprawidłowy format danych.'
                        print ''
                
                if not exit_decision:
                    print 'Ilość wykonanych ruchów: ', str(self.__counter_movements)
                    print 'Stan planszy:'
                    self.__print_puzzle_board()
                    print ''

                print ''
                print 'Zakończenie gry.'
            else:
                print 'Uwaga. Plansza początkowa została zainicjowana błędnymi liczbami.'
        else:
            print 'Uwaga. Wskazany plik nie istnieje lub został błędnie wypełniony liczbami.'
        

# Główna funkcja programu.
def main():
    test = PuzzleSolution()
    test.run_test()
    
    #game = PuzzleSliding()
    #game.run_game()
    
if __name__ == '__main__':
    main()
    