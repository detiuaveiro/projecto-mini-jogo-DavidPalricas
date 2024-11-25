class State:
    """The State class is responsible for managing the states of the entity
    
       The class has the following attributes:
            - name: The name of the state
    """

    def __init__(self, name) -> None:
        """
            Initializes a new instance of the State class
        """
        self.name = name

    def enter(self):
        """The enter method is responsible for entering the state"""
        print(f"Entering {self.name}")

    def update(self, object):
        """The update method is responsible for updating the state of the entity

            Args:
                - object (Entity): The entity that the state belongs to
        """
        pass

    def exit(self):
     """The exit method is responsible for exiting the state"""
     pass

class Transition:
    """The Transition class is responsible for managing the transitions between the entity's states
    
       The class has the following attributes:
            - _from: The state from which the transition occurs
            - _to: The state to which the transition occurs
    """

    def __init__(self, _from, _to) -> None:
        """
           Initializes a new instance of the Transition class
        """
        self._from = _from
        self._to = _to

class Idle(State):
    """The Idle class is responsible for managing the idle state of the entity
    """

    def __init__(self) -> None:
        """
            Initializes a new instance of the Idle class, and calls the constructor of the State class (the parent class)
        """

        super().__init__(self.__class__.__name__)

    def update(self, object):
        """The update method is responsible for updating the idle state of the entity

            Args:
                - object (Entity): The entity that the state belongs to

            Returns:
                - bool: A flag indicating to update the entity state
        """

        print("waiting for your command...")
        return super().update(object)

class Walk(State):
    """The Walk class is responsible for managing the walk state of the entity
    """

    def __init__(self) -> None:
        """ 
            Initializes a new instance of the Walk class, and calls the constructor of the State class (the parent class)
        """

        super().__init__(self.__class__.__name__)

    def update(self, object):
        """The update method is responsible for updating the walk state of the entity

            Args:
                - object (Entity): The entity that the state belongs to

            Returns:
                - bool: A flag indicating to update the entity state
        """

        print("Moving")
        return super().update(object)
    
class Jump(State):
    """The Jump class is responsible for managing the jump state of the entity
    """

    def __init__(self) -> None:
        """ 
            Initializes a new instance of the Jump class, and calls the constructor of the State class (the parent class)
        """

        super().__init__(self.__class__.__name__)

    def update(self, object):
        """The update method is responsible for updating the jump state of the entity

            Args:
                - object (Entity): The entity that the state belongs to

            Returns:
                - bool: A flag indicating to update the entity state
        """

        print("Jumping")
        return super().update(object)
    

class FSM:
    def __init__(self, states, transitions):
        """
        Initializes the FSM with states and transitions.
        
        :param states: A dictionary of states.
        :param transitions: A dictionary of transitions.
        """
        self._states = states
        self._transitions = transitions
        self.current = list(states.values())[0]  # Set the initial state to the first state in the dictionary

    def update(self):
        """
        Updates the current state.
        """
        self.current()

    def transition(self, transition_name):
        """
        Transitions to a new state based on the transition name.
        
        :param transition_name: The name of the transition.
        """
        if transition_name in self._transitions:
            from_state, to_state = self._transitions[transition_name]
            if self.current == self._states[from_state]:
                self.current = self._states[to_state]
    