from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        CurrentState = []
        # calculate the number of disks in KB:
        #NumberOfDisk = 0
        #for facts in self.kb.facts:
        #    if facts.statement.terms[1] == "disk":
        #        NumberOfDisk += 1
        #if NumberOfDisk > 5:
        #    print("Please use less than 5 disks.")
        # find the matched facts:
        '''
        for facts in self.kb.facts:
            if (facts.statement.predicate == "on") and (facts.statement.terms[1] == Constant("peg1")):
                if facts.statement.terms[0] == Constant("disk1"):
                    CurrentState[0].append(1)
                elif facts.statement.terms[0] == Constant("disk2"):
                    CurrentState[0].append(2)
                elif facts.statement.terms[0] == Constant("disk3"):
                    CurrentState[0].append(3)
                elif facts.statement.terms[0] == Constant("disk4"):
                    CurrentState[0].append(4)
                else:
                    CurrentState[0].append(5)


            elif facts.statement.predicate == "on" and facts.statement.terms[1] == Constant("peg2"):
                if facts.statement.terms[0] == Constant("disk1"):
                    CurrentState[1].append(1)
                elif facts.statement.terms[0] == Constant("disk2"):
                    CurrentState[1].append(2)
                elif facts.statement.terms[0] == Constant("disk3"):
                    CurrentState[1].append(3)
                elif facts.statement.terms[0] == Constant("disk4"):
                    CurrentState[1].append(4)
                else:
                    CurrentState[1].append(5)

            elif facts.statement.predicate == "on" and facts.statement.terms[1] == Constant("peg3"):
                if facts.statement.terms[0] == Constant("disk1"):
                    CurrentState[2].append(1)
                elif facts.statement.terms[0] == Constant("disk2"):
                    CurrentState[2].append(2)
                elif facts.statement.terms[0] == Constant("disk3"):
                    CurrentState[2].append(3)
                elif facts.statement.terms[0] == Constant("disk4"):
                    CurrentState[2].append(4)
                else:
                    CurrentState[2].append(5)

        #print(CurrentState)
        # ascending order:
        for i in range(0, len(CurrentState)):
            CurrentState[i].sort()

        # transfer to ():
        for i in range(0, len(CurrentState)):
            CurrentState[i] = tuple(CurrentState[i])
        GetState = tuple(CurrentState)

        return GetState

        #pass
        '''
        ask1 = parse_input("fact: (on ?x peg1")
        ask2 = parse_input("fact: (on ?x peg2")
        ask3 = parse_input("fact: (on ?x peg3")
        answer1 = self.kb.kb_ask(ask1)
        answer2 = self.kb.kb_ask(ask2)
        answer3 = self.kb.kb_ask(ask3)
        answers = [answer1, answer2, answer3]

        for item in answers:
            peg = []
            if item:
                for an in item:
                    disk = int(str(an).split(":")[1][-1])
                    peg.append(disk)
                peg.sort()
                CurrentState.append(peg)
            else:
                CurrentState.append([])

        for i in range(0, len(CurrentState)):
            CurrentState[i] = tuple(CurrentState[i])
        GetState = tuple(CurrentState)

        return GetState
    def findTargetPeg(self, term):
        if term == Constant("peg1"):
            return 1
        elif term == Constant("peg2"):
            return 2
        else:
            return 3
    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        #pass

        #print("movable_statement:", movable_statement)
        Current_state = self.getGameState()
        tar_peg = self.findTargetPeg(movable_statement.terms[2])
        length = len(Current_state[tar_peg-1])
        if length == 0:
            # target is empty:
            #new_s1 = Statement(["top", movable_statement.terms[0], movable_statement.terms[2]])
            #new_fac1 = Fact(new_s1, [])
            new_s2 = Statement(["on", movable_statement.terms[0], movable_statement.terms[2]])
            new_fac2 = Fact(new_s2, [])
            #self.kb.kb_add(new_fac1)
            self.kb.kb_add(new_fac2)
            old_s1 = Statement(["top", movable_statement.terms[0], movable_statement.terms[1]])
            old_s2 = Statement(["on", movable_statement.terms[0], movable_statement.terms[1]])
            old_s3 = Statement(["empty", movable_statement.terms[2]])
            self.kb.kb_retract(Fact(old_s1))
            self.kb.kb_retract(Fact(old_s2))
            self.kb.kb_retract(Fact(old_s3))
        else:
            # target is not empty:
            #new_s1 = Statement(["top", movable_statement.terms[0], movable_statement.terms[2]])
            #new_fac1 = Fact(new_s1, [])
            new_s2 = Statement(["on", movable_statement.terms[0], movable_statement.terms[2]])
            new_fac2 = Fact(new_s2, [])
            #self.kb.kb_add(new_fac1)
            self.kb.kb_add(new_fac2)
            old_s1 = Statement(["top", movable_statement.terms[0], movable_statement.terms[1]])
            old_s2 = Statement(["on", movable_statement.terms[0], movable_statement.terms[1]])
            old_s3 = Statement(["top", "disk"+str(Current_state[tar_peg-1][0]), movable_statement.terms[2]])
            self.kb.kb_retract(Fact(old_s1))
            self.kb.kb_retract(Fact(old_s2))
            self.kb.kb_retract(Fact(old_s3))
        # add initial peg information:(empty & top)
        Current_state = self.getGameState()
        for i in range(0, len(Current_state)):

            if len(Current_state[i]) == 0:
                new_emp_s = Statement(["empty", "peg"+str(i+1)])
                new_emp = Fact(new_emp_s, [])
                self.kb.kb_add(new_emp)
            else:
                new_top_s = Statement(["top", "disk"+str(Current_state[i][0]), "peg"+str(i+1)])
                new_top = Fact(new_top_s, [])
                self.kb.kb_add(new_top)





        '''
        for facts in self.kb.facts:

            if match(movable_statement, facts.statement):
                # delete pre state:

                for facts in self.kb.facts:
                    if facts.statement.predicate == "on" and facts.statement.terms[0] == movable_statement.terms[0] and facts.statement.terms[1] == movable_statement.terms[1]:
                        facts = self.kb._get_fact(facts)
                        self.kb.kb_retract(facts)
                    if facts.statement.predicate == "top" and facts.statement.terms[0] == movable_statement.terms[0] and facts.statement.terms[1] == movable_statement.terms[1]:
                        facts = self.kb._get_fact(facts)
                        self.kb.kb_retract(facts)

                # move:
                new_statement = Statement(["on", movable_statement.terms[0], movable_statement.terms[2]])
                new_fact = Fact(new_statement, [])
                if new_fact in self.kb.facts:
                    print("Error, please make a movement")
                    return
                else:
                    self.kb.kb_assert(new_fact)
                # find top:
                new_state = self.getGameState()
                s = False

                if movable_statement.terms[1] == Constant("peg1"):
                    if new_state[0] != ():
                        index = new_state[0][0]
                        s = self.findtop(index, "peg1")

                elif movable_statement.terms[1] == Constant("peg2"):
                    if new_state[1] != ():
                        index = new_state[1][0]
                        s = self.findtop(index, "peg2")
                elif movable_statement.terms[1] == Constant("peg3"):
                    if new_state[2] != ():
                        index = new_state[2][0]
                        s = self.findtop(index, "peg3")
                else:
                    print("error: only have 3 pegs")
                    return
                if s:
                    new_top1 = Fact(s, [])
                    if new_top1 not in self.kb.facts:
                        self.kb.kb_assert(new_top1)

                ss = Statement(["top", movable_statement.terms[0], movable_statement.terms[2]])
                new_top2 = Fact(ss, [])
                if new_top2 not in self.kb.facts:
                    self.kb.kb_assert(new_top2)

                #find empty:
                # remove pre
                if movable_statement.terms[2] == Constant("peg1"):
                    pre_empty = Statement(["empty", "peg1"])
                elif movable_statement.terms[2] == Constant("peg2"):
                    pre_empty = Statement(["empty", "peg2"])
                else:
                    pre_empty = Statement(["empty", "peg3"])

                for facts in self.kb.facts:
                    if facts.statement == pre_empty:
                        facts = self.kb._get_fact(facts)
                        self.kb.kb_retract(facts)
                # add new
                for i in range(0, len(new_state)):
                    if len(new_state[i]) == 0:
                        sss = Statement(["empty", self.findempty(i+1)])
                        new_empty = Fact(sss, [])
                        if new_empty not in self.kb.facts:
                            self.kb.kb_assert(new_empty)



        #print(self.getGameState())
        '''



    '''
        
    def findtop(self, index, peg):

        if index == 1:
            new_statement = Statement(["top", "disk1", peg])
        elif index == 2:
            new_statement = Statement(["top", "disk2", peg])
        elif index == 3:
            new_statement = Statement(["top", "disk3", peg])
        elif index == 4:
            new_statement = Statement(["top", "disk4", peg])
        elif index == 5:
            new_statement = Statement(["top", "disk5", peg])
        else:
            print("error: only have 5 disks")
            return
        return new_statement

    def findempty(self, index):
        if index == 1:
            return "peg1"
        elif index == 2:
            return "peg2"
        elif index == 3:
            return "peg3"
        else:
            print("error: only have 3 pegs")
            return

        '''









    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getTileNumber(self, tile):
        if tile == Constant("tile1"):
            return 1
        elif tile == Constant("tile2"):
            return 2
        elif tile == Constant("tile3"):
            return 3
        elif tile == Constant("tile4"):
            return 4
        elif tile == Constant("tile5"):
            return 5
        elif tile == Constant("tile6"):
            return 6
        elif tile == Constant("tile7"):
            return 7
        elif tile == Constant("tile8"):
            return 8
        elif tile == Constant("empty"):
            return -1
        else:
            print("Only have 9 tiles")
            return

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        #pass


        CurrentState = []
        row1 = []
        row2 = []
        row3 = []
        for facts in self.kb.facts:
            if facts.statement.predicate == "position" and facts.statement.terms[2] == Constant("pos1"):
                row1.append(facts.statement.terms[1].term.element)
            elif facts.statement.predicate == "position" and facts.statement.terms[2] == Constant("pos2"):
                row2.append(facts.statement.terms[1].term.element)
            elif facts.statement.predicate == "position" and facts.statement.terms[2] == Constant("pos3"):
                row3.append(facts.statement.terms[1].term.element)
        # ascending order:
        row1.sort()
        row2.sort()
        row3.sort()
        CurrentState.append(row1)
        CurrentState.append(row2)
        CurrentState.append(row3)
        for facts in self.kb.facts:
            if facts.statement.predicate == "position":
                if facts.statement.terms[2] == Constant("pos1"):
                    for i in range(0, len(row1)):

                        if row1[i] == facts.statement.terms[1].term.element:
                            tilenumber = self.getTileNumber(facts.statement.terms[0])
                            CurrentState[0][i] = tilenumber
                elif facts.statement.terms[2] == Constant("pos2"):
                    for i in range(0, len(row2)):

                        if row2[i] == facts.statement.terms[1].term.element:
                            tilenumber = self.getTileNumber(facts.statement.terms[0])
                            CurrentState[1][i] = tilenumber
                elif facts.statement.terms[2] == Constant("pos3"):
                    for i in range(0, len(row3)):

                        if row3[i] == facts.statement.terms[1].term.element:
                            tilenumber = self.getTileNumber(facts.statement.terms[0])
                            CurrentState[2][i] = tilenumber
                '''
        
                for tiles in row1:
                    if facts.statement.terms[2] == Constant("pos1"):

                        if tiles == facts.statement.terms[1].term.element:
                            tilenumber = self.getTileNumber(facts.statement.terms[0])
                            CurrentState[0][0] = tilenumber
                for tiles in row2:
                    if facts.statement.terms[2] == Constant("pos2"):

                        if tiles == facts.statement.terms[1].term.element:
                            tilenumber = self.getTileNumber(facts.statement.terms[0])
                            CurrentState[1].append(tilenumber)
                for tiles in row3:
                    if facts.statement.terms[2] == Constant("pos3"):

                        if tiles == facts.statement.terms[1].term.element:
                            tilenumber = self.getTileNumber(facts.statement.terms[0])
                            CurrentState[2].append(tilenumber)
                '''
        # transfer to ():
        for i in range(0, len(CurrentState)):
            CurrentState[i] = tuple(CurrentState[i])
        GetState = tuple(CurrentState)

        return GetState

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        #pass
        #print("movable_statement:", movable_statement)
        Current_state = self.getGameState()



        # target is empty:
        new_s1 = Statement(["position", movable_statement.terms[0], movable_statement.terms[3], movable_statement.terms[4]])
        new_fac1 = Fact(new_s1, [])
        new_s2 = Statement(["position", "empty", movable_statement.terms[1], movable_statement.terms[2]])
        new_fac2 = Fact(new_s2, [])
        self.kb.kb_add(new_fac1)
        self.kb.kb_add(new_fac2)
        old_s1 = Statement(["position", movable_statement.terms[0], movable_statement.terms[1], movable_statement.terms[2]])
        old_s2 = Statement(["position", "empty", movable_statement.terms[3], movable_statement.terms[4]])
        #old_s3 = Statement(["empty", movable_statement.terms[2]])
        self.kb.kb_retract(Fact(old_s1))
        self.kb.kb_retract(Fact(old_s2))
        #self.kb.kb_retract(Fact(old_s3))


        '''
        for fact_move in self.kb.facts:

            if match(movable_statement, fact_move.statement):
                # delete pre state:

                for facts in self.kb.facts:
                    if facts.statement.predicate == "position" and facts.statement.terms[0] == movable_statement.terms[0] and facts.statement.terms[1] == movable_statement.terms[1] and facts.statement.terms[2] == movable_statement.terms[2]:
                        facts = self.kb._get_fact(facts)
                        self.kb.kb_retract(facts)
                for facts in self.kb.facts:
                    if facts.statement.predicate == "position" and facts.statement.terms[0] == Constant("empty") and facts.statement.terms[1] == movable_statement.terms[3] and facts.statement.terms[2] == movable_statement.terms[4]:
                        facts = self.kb._get_fact(facts)
                        self.kb.kb_retract(facts)
                print("state after delete:", self.kb)
                # move:
                new_statement = Statement(["position", movable_statement.terms[0], movable_statement.terms[3], movable_statement.terms[4]])
                new_fact = Fact(new_statement, [])
                if new_fact in self.kb.facts:
                    print("Error, please make a movement")
                    return
                else:
                    self.kb.kb_assert(new_fact)

                new_emptys = Statement(["position", "empty", movable_statement.terms[1], movable_statement.terms[2]])
                new_empty = Fact(new_emptys, [])
                if new_empty in self.kb.facts:
                    print("Error, please make a movement")
                    return
                else:
                    self.kb.kb_assert(new_empty)
                print("state after move:", self.kb)

        return
'''

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
