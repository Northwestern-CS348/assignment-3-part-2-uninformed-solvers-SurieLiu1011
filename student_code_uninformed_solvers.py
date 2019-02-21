from queue import Queue
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)


    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        Current_Gamestate = self.currentState
        self.visited[Current_Gamestate] = True
        if Current_Gamestate.state == self.victoryCondition:
            return True
        movables = self.gm.getMovables()
        if len(movables) == 0:
            if Current_Gamestate.requiredMovable != None:
                self.gm.reverseMove(Current_Gamestate.requiredMovable)

        elif Current_Gamestate.nextChildToVisit >= len(movables):
            if Current_Gamestate.requiredMovable != None:
                self.gm.reverseMove(Current_Gamestate.requiredMovable)

        else:

            moveTonext = movables[Current_Gamestate.nextChildToVisit]
            Current_Gamestate.nextChildToVisit += 1
            self.gm.makeMove(moveTonext)
            while ((Current_Gamestate.parent is not None) and (Current_Gamestate.parent.state == self.gm.getGameState())) or (GameState(self.gm.getGameState(), 0, None) in self.visited):
                self.gm.reverseMove(moveTonext)

                if Current_Gamestate.nextChildToVisit >= len(movables):

                    self.gm.reverseMove(Current_Gamestate.requiredMovable)
                    return False
                else:
                    moveTonext = movables[Current_Gamestate.nextChildToVisit]
                    Current_Gamestate.nextChildToVisit += 1
                    self.gm.makeMove(moveTonext)

            new_gamestate = GameState(self.gm.getGameState(), Current_Gamestate.depth+1, moveTonext)
            Current_Gamestate.children = new_gamestate
            new_gamestate.parent = Current_Gamestate
            #self.visited[new_gamestate] = True
            self.currentState = new_gamestate
        return False



'''
        ### Student code goes here
        #current_gamemaster = self.gm
        current_gamestate = self.currentState
        current_kb = current_gamestate.state
        #print("current_kb:", current_kb)
        self.visited[current_gamestate] = True
        if self.currentState.state == self.victoryCondition:
            return True
        # get children:
        movables = self.gm.getMovables()

        # if no children or children all visited, go back:
        if len(movables) == 0:
            print("no children")
            current_gamestate = current_gamestate.parent
            if current_gamestate.requiredMovable is not None:
                self.gm.reverseMove(current_gamestate.requiredMovable)
        elif current_gamestate.nextChildToVisit >= len(movables):
            current_gamestate = current_gamestate.parent
            print("all children have been visited")
            if current_gamestate.requiredMovable is not None:
                self.gm.reverseMove(current_gamestate.requiredMovable)
        # expand if have unvisited children:
        else:
            print("expand")
            move = movables[current_gamestate.nextChildToVisit]
            self.gm.makeMove(move)
            current_gamestate.nextChildToVisit += 1

            # if child is the same as parent or child is visited, go back:
            while ((current_gamestate.parent is not None) and (current_gamestate.parent.state == self.gm.getGameState())) or self.visited.__contains__(GameState(self.gm.getGameState(), 0, None)):
                self.gm.reverseMove(move)
                print("this child is the same as parent or visited")
                if current_gamestate.nextChildToVisit >= len(movables):
                    # self.currentState = current_gamestate.parent
                    # all children have been visited and go back to parent node:
                    self.gm.reverseMove(current_gamestate.requiredMovable)
                    return False
                else:
                    move = movables[current_gamestate.nextChildToVisit]
                    self.gm.makeMove(move)
                    current_gamestate.nextChildToVisit += 1

            new_state = self.gm.getGameState()
            # print("new state:", new_state)
            # print("movable:", self.gm.getMovables())

            new_gamestate = GameState(new_state, current_gamestate.depth + 1, move)
            current_gamestate.children.append(new_gamestate)
            new_gamestate.parent = current_gamestate
            self.currentState = new_gamestate

        return False
'''




class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue = Queue()
        self.queue.put([self.currentState, []])
        self.solveOneStep()

    def to_origin(self):
        curr_state = self.currentState
        while curr_state.parent is not None:
            self.gm.reverseMove(curr_state.requiredMovable)
            curr_state = curr_state.parent

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        ### Student code goes here
        if self.queue:
            node = self.queue.get()
            curr_state = node[0]
            require_move = node[1]
            self.visited[curr_state] = True
            self.to_origin()

            #("curr_state:", curr_state.state)
            # to record in visit_list:
            for item in require_move:
                self.gm.makeMove(item)
            if curr_state.state == self.victoryCondition:
                return True
            movebales = self.gm.getMovables()
            if len(movebales) != 0:
                for move in movebales:
                    self.gm.makeMove(move)
                    if ((curr_state.parent is not None) and (curr_state.parent.state == self.gm.getGameState())) or (self.visited.__contains__(GameState(self.gm.getGameState(), 0, None))):
                        self.gm.reverseMove(move)
                        continue
                    new_state = GameState(self.gm.getGameState(), curr_state.depth+1, move)
                    new_require = [re for re in require_move]
                    #print("old_require:" , new_require)
                    new_require.append(move)
                    #print("new_require: ", new_require)
                    curr_state.children.append(new_state)
                    new_state.parent = curr_state
                    self.visited[new_state] = True
                    self.queue.put([new_state, new_require])
                    self.gm.reverseMove(move)
                #print("curr state", self.currentState.state)
                self.currentState = curr_state
                #print("new curr state", self.currentState.state)

        return False

