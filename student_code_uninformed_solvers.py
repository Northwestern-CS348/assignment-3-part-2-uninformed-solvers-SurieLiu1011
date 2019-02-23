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
        print("Current state:", str(Current_Gamestate.state))
        if Current_Gamestate.state == self.victoryCondition:
            return True
        movables = self.gm.getMovables()

        if len(movables) != 0:
            moveTonext = movables[Current_Gamestate.nextChildToVisit]
            self.gm.makeMove(moveTonext)
            if GameState(self.gm.getGameState(), 0, None) not in self.visited:
                Current_Gamestate.nextChildToVisit += 1
            else:
                while self.visited.__contains__(GameState(self.gm.getGameState(), 0, None)):
                    self.gm.reverseMove(moveTonext)
                    Current_Gamestate.nextChildToVisit += 1
                    if Current_Gamestate.nextChildToVisit < len(movables):
                        moveTonext = movables[Current_Gamestate.nextChildToVisit]
                        self.gm.makeMove(moveTonext)
                    else:
                        self.gm.reverseMove(Current_Gamestate.requiredMovable)
                        return False
            new_gamestate = GameState(self.gm.getGameState(), Current_Gamestate.depth + 1, moveTonext)
            Current_Gamestate.children.append(new_gamestate)
            new_gamestate.parent = Current_Gamestate
            self.visited[new_gamestate] = False
            self.currentState = new_gamestate

        else:
            print("No children!")
            if Current_Gamestate.requiredMovable != None:
                self.gm.reverseMove(Current_Gamestate.requiredMovable)
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.queue1 = Queue()
        self.queue2 = Queue()
        self.queue1.put(self.currentState)
        self.queue2.put([])
        self.solveOneStep()

    def to_origin(self, curr_state):

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
        if self.queue1 and self.queue2:
            curr_state = self.queue1.get()
            require_move = self.queue2.get()
            self.visited[curr_state] = True
            self.to_origin(self.currentState)
            print("Current state:", str(curr_state.state))
            #("curr_state:", curr_state.state)
            # update game master:
            for item in require_move:
                self.gm.makeMove(item)
            print("Current game master:", str(self.gm.getGameState()))
            if curr_state.state == self.victoryCondition:
                return True
            movebales = self.gm.getMovables()

            if len(movebales) != 0:
                for move in movebales:
                    self.gm.makeMove(move)
                    new_state = GameState(self.gm.getGameState(), curr_state.depth+1, move)

                    if new_state not in self.visited:
                        new_require = []
                        for re in require_move:
                            new_require.append(re)
                        #print("old_require:" , new_require)
                        new_require.append(move)
                        #print("new_require: ", new_require)
                        curr_state.children.append(new_state)
                        new_state.parent = curr_state
                        self.visited[new_state] = False
                        self.queue1.put(new_state)
                        self.queue2.put(new_require)
                        self.gm.reverseMove(move)
                    else:
                        print("Children", str(new_state.state), "has been visited")
                        self.gm.reverseMove(move)
                #print("curr state", self.currentState.state)
                self.currentState = curr_state
                #print("new curr state", self.currentState.state)
            else:
                print("No children!")
                return False
        return False

