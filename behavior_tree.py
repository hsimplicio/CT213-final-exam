from enum import Enum
from constants import *
import random
import math


class ExecutionStatus(Enum):
    """
    Represents the execution status of a behavior tree node.
    """
    SUCCESS = 0
    FAILURE = 1
    RUNNING = 2


class BehaviorTree(object):
    """
    Represents a behavior tree.
    """
    def __init__(self, root=None):
        """
        Creates a behavior tree.

        :param root: the behavior tree's root node.
        :type root: TreeNode
        """
        self.root = root

    def update(self, agent):
        """
        Updates the behavior tree.

        :param agent: the agent this behavior tree is being executed on.
        """
        if self.root is not None:
            self.root.execute(agent)


class TreeNode(object):
    """
    Represents a node of a behavior tree.
    """
    def __init__(self, node_name):
        """
        Creates a node of a behavior tree.

        :param node_name: the name of the node.
        """
        self.node_name = node_name
        self.parent = None

    def enter(self, agent):
        """
        This method is executed when this node is entered.

        :param agent: the agent this node is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the behavior tree node logic.

        :param agent: the agent this node is being executed on.
        :return: node status (success, failure or running)
        :rtype: ExecutionStatus
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class LeafNode(TreeNode):
    """
    Represents a leaf node of a behavior tree.
    """
    def __init__(self, node_name):
        super().__init__(node_name)


class CompositeNode(TreeNode):
    """
    Represents a composite node of a behavior tree.
    """
    def __init__(self, node_name):
        super().__init__(node_name)
        self.children = []

    def add_child(self, child):
        """
        Adds a child to this composite node.

        :param child: child to be added to this node.
        :type child: TreeNode
        """
        child.parent = self
        self.children.append(child)


class SequenceNode(CompositeNode):
    """
    Represents a sequence node of a behavior tree.
    """
    def __init__(self, node_name):
        super().__init__(node_name)
        # We need to keep track of the last running child when resuming the tree execution
        self.running_child = None

    def enter(self, agent):
        # When this node is entered, no child should be running
        self.running_child = None

    def execute(self, agent):
        if self.running_child is None:
            # If a child was not running, then the node puts its first child to run
            self.running_child = self.children[0]
            self.running_child.enter(agent)
        loop = True
        while loop:
            # Execute the running child
            status = self.running_child.execute(agent)
            if status == ExecutionStatus.FAILURE:
                # This is a sequence node, so any failure results in the node failing
                self.running_child = None
                return ExecutionStatus.FAILURE
            elif status == ExecutionStatus.RUNNING:
                # If the child is still running, then this node is also running
                return ExecutionStatus.RUNNING
            elif status == ExecutionStatus.SUCCESS:
                # If the child returned success, then we need to run the next child or declare success
                # if this was the last child
                index = self.children.index(self.running_child)
                if index + 1 < len(self.children):
                    self.running_child = self.children[index + 1]
                    self.running_child.enter(agent)
                else:
                    self.running_child = None
                    return ExecutionStatus.SUCCESS


class SelectorNode(CompositeNode):
    """
    Represents a selector node of a behavior tree.
    """
    def __init__(self, node_name):
        super().__init__(node_name)
        # We need to keep track of the last running child when resuming the tree execution
        self.running_child = None

    def enter(self, agent):
        # When this node is entered, no child should be running
        self.running_child = None

    def execute(self, agent):
        if self.running_child is None:
            # If a child was not running, then the node puts its first child to run
            self.running_child = self.children[0]
            self.running_child.enter(agent)
        loop = True
        while loop:
            # Execute the running child
            status = self.running_child.execute(agent)
            if status == ExecutionStatus.FAILURE:
                # This is a selector node, so if the current node failed, we have to try the next one.
                # If there is no child left, then all children failed and the node must declare failure.
                index = self.children.index(self.running_child)
                if index + 1 < len(self.children):
                    self.running_child = self.children[index + 1]
                    self.running_child.enter(agent)
                else:
                    self.running_child = None
                    return ExecutionStatus.FAILURE
            elif status == ExecutionStatus.RUNNING:
                # If the child is still running, then this node is also running
                return ExecutionStatus.RUNNING
            elif status == ExecutionStatus.SUCCESS:
                # If any child returns success, then this node must also declare success
                self.running_child = None
                return ExecutionStatus.SUCCESS


class RoombaBehaviorTree(BehaviorTree):
    """
    Represents a behavior tree of a roomba cleaning robot.
    """
    def __init__(self,move_foward_time, move_in_spiral_time, go_back_time, spiral_factor, initial_radius_spiral):
        super().__init__()
        # Todo: construct the tree here
        move_forward = MoveForwardNode(move_foward_time)
        move_in_spiral = MoveInSpiralNode(move_in_spiral_time, spiral_factor, initial_radius_spiral)
        go_back = GoBackNode(go_back_time)
        rotate = RotateNode()
        move_sequence = SequenceNode("MoveSequence")
        move_sequence.add_child(move_forward)
        move_sequence.add_child(move_in_spiral)
        back_sequence = SequenceNode("BackSequence")
        back_sequence.add_child(go_back)
        back_sequence.add_child(rotate) 
        sequence = SelectorNode("Sequence")
        sequence.add_child(move_sequence)
        sequence.add_child(back_sequence)
        self.root = sequence
        

class MoveForwardNode(LeafNode):
    def __init__(self, move_foward_time):
        super().__init__("MoveForward")
        # Todo: add initialization code
        self.n = 0
        self.move_forward_time = move_foward_time
        
    def enter(self, agent):
        # Todo: add enter logic
        agent.status = ExecutionStatus.RUNNING
        self.n = 0
        pass

    def execute(self, agent):
        # Todo: add execution logic
        self.n += 1
        t = self.n * SAMPLE_TIME
        if(agent.status == ExecutionStatus.RUNNING):
            agent.set_velocity(FORWARD_SPEED,0)
            if(agent.get_bumper_state()):
                return ExecutionStatus.FAILURE
            elif(t > self.move_forward_time):
                return ExecutionStatus.SUCCESS
            else:
                return ExecutionStatus.RUNNING
        pass


class MoveInSpiralNode(LeafNode):
    def __init__(self,move_in_spiral_time, spiral_factor, initial_radius_spiral):
        super().__init__("MoveInSpiral")
        self.move_in_spiral_time = move_in_spiral_time
        self.spiral_factor = spiral_factor
        self.initial_radius_spiral = initial_radius_spiral
        # Todo: add initialization code
        self.n = 0 #inicializando a variavel
        
    def enter(self, agent):
        # Todo: add enter logic
        agent.status = ExecutionStatus.RUNNING
        self.n = 0 #setando o valor para zero novamente
        pass

    def execute(self, agent):
        # Todo: add execution logic
        self.n += 1
        t = self.n * SAMPLE_TIME
        r = self.initial_radius_spiral + self.spiral_factor * t
        #linear_velocity = ANGULAR_SPEED * r
        angular_velocity = FORWARD_SPEED/r
        agent.set_velocity(FORWARD_SPEED, angular_velocity)
        if(agent.status == ExecutionStatus.RUNNING):
            if(t > self.move_in_spiral_time):
                return ExecutionStatus.SUCCESS
            elif(agent.get_bumper_state()):
                return ExecutionStatus.FAILURE
            else:
                return ExecutionStatus.RUNNING
        pass


class GoBackNode(LeafNode):
    def __init__(self,go_back_time):
        self.go_back_time = go_back_time
        super().__init__("GoBack")
        # Todo: add initialization code
        self.n = 0

    def enter(self, agent):
        # Todo: add enter logic
        agent.status = ExecutionStatus.RUNNING
        self.n = 0

    def execute(self, agent):
        # Todo: add execution logic
        self.n += 1
        t = self.n * SAMPLE_TIME
        if(agent.status == ExecutionStatus.RUNNING):
            agent.set_velocity(BACKWARD_SPEED,0)
            if(t > self.go_back_time ):
                return ExecutionStatus.SUCCESS
            else:
                return ExecutionStatus.RUNNING
        pass


class RotateNode(LeafNode):
    def __init__(self):
        super().__init__("Rotate")
        # Todo: add initialization code
        self.n = 0
        self.random_time = random.uniform(0,3)
        self.signal = random.randrange(-1,2,2)
        
        
    def enter(self, agent):
        # Todo: add enter logic
        self.n = 0
        self.random_time = random.uniform(0,3)
        self.signal = random.randrange(-1,2,2)
        agent.status = ExecutionStatus.RUNNING

    def execute(self, agent):
        # Todo: add execution logic
        self.n += 1
        t = self.n * SAMPLE_TIME
        if(agent.status == ExecutionStatus.RUNNING):
            agent.set_velocity(0,self.signal*ANGULAR_SPEED)
            if(t > self.random_time):
                return ExecutionStatus.SUCCESS
            else:
                return ExecutionStatus.RUNNING
        pass

