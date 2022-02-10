"""
Program Project 1:
Author: Madeline Spawn
Date: 01/21/2022

Description: Three classes: Node, Queue, Stack.
-Node contains data and it's next node
-Queue (comprised of nodes) functions using FIFO principle as well as full/empty methods
-Stack (comprised of nodes) functions using LIFO with full/empty methods

"""


# ====================Exceptions FOR QUEUE===============


class QueueCapacityTypeError(Exception):
    """
    if Queue capacity is the wrong type (not int) raise this exception!
    """
    pass


class QueueCapacityBoundError(Exception):
    """
    if queue capacity is negative or zero
    """
    pass


class QueueIsFull(Exception):
    """
    Raise this is exception if Queue is full when trying to add (for enqueue)
    """


class QueueIsEmpty(Exception):
    """
    raise this exception if the Queue is empty (for dequeue)
    """


# =============================================

# =====================Class==================

class Node:
    """
    This class holds data that is stored in Queue and Stack...Queue and Stacks are comprised of Nodes
    """

    def __init__(self, data=None):
        self.data = data
        self.next = None

    def setNext(self, next):
        """
        I wrote this method so I could just pass in an argument and have the next be set to that...
        it makes the code cleaner and feels simpler to read + understand
        """
        self.next = next


class Queue:
    """
    This class is comprised of Nodes (see above). It functions on the FIFO principle (First in first out)
    so it will have methods the will add to the tail end  and take from the head of the queue. It also has
    methods that check for capacity.
    """

    def __init__(self, capacity):

        # error handling for type error and bound error
        if (type(capacity) != int):
            raise QueueCapacityTypeError("ERROR: capacity is not an int")
        if (capacity <= 0):
            raise QueueCapacityBoundError("ERROR: Your capacity is equal to or less than zero")

        # set head and tail to none for empty and currentSize to 0 for empty
        self.head = self.tail = None
        self.capacity = capacity
        self.currentSize = 0

    def enqueue(self, item):
        """
        This method takes an item and adds it to the tail of the queue which maintains the LIFO
        principle. If list is empty tail and head are the same else ypu append to the tail
        by setting tail next to new item and of course increment
        """

        if self.isFull():
            raise QueueIsFull("ERROR: The Queue is full!")


        else:
            add = Node(item)

            if self.isEmpty():
                self.head = self.tail = add


            else:
                self.tail.setNext(add)
                self.tail = add

        self.currentSize += 1
        return True

    def dequeue(self):
        """
        This method removes an item from the head of the queue (as per LIFO) and then decrements the size.
        """

        # error handling if queue is empty
        if self.isEmpty():
            raise QueueIsEmpty("ERROR: Queue is empty")

        else:
            deq = self.head
            deq.next = None
            self.head = deq.next

        self.currentSize -= 1
        return deq.data

    def front(self):
        """
        This method returns the front value (head) of the queue without de-queue-ing it
        """

        if self.isEmpty():
            raise QueueIsEmpty("ERROR: No value to return because Queue is empty")

        else:
            return self.head.data

    def isEmpty(self):
        """
        This method checks if the queue is empty by checking id size is still or has
        been decremented to 0
        """
        if self.currentSize == 0:
            return True
        else:
            return False

    def isFull(self):
        """
        This method checks if the queue is full by comparing currentSize and capacity
        """
        if self.currentSize >= self.capacity:
            return True
        else:
            return False


# ====================Exceptions FOR STACK===============


class StackCapacityTypeError(Exception):
    """
    Raise this error is stack is the wrong type (not int)
    """
    pass


class StackCapacityBoundError(Exception):
    """
    Raise this error if the stack capacity is negative or 0
    """
    pass


class StackIsFull(Exception):
    """
    Raise this error is stack is greater than capacity
    """
    pass


class StackIsEmpty(Exception):
    """
    Raise this error if the stack is empty
    """
    pass


# =======================================================

# =====================Class==================


class Stack:
    """
    This class is comprised of Nodes (see above). It functions on the LIFO principle (Last in first out)
    so it will have methods the will push Nodes on the top of stack and then pop from the top of the Stack.
    It also has methods that check for capacity.
    """

    def __init__(self, capacity):

        # this is the error handling section for bound and type error
        if type(capacity) != int:
            raise StackCapacityTypeError("ERROR: capacity is not an int")
        if capacity <= 0:
            raise StackCapacityBoundError("ERROR: Your capacity is equal to or less than zero")

        # initializes head to none (empty) and current size to 0 (empty)
        self.head = None
        self.capacity = capacity
        self.currentSize = 0

    def push(self, item):
        """
        This method pushes a new item on top of the stack (FIFO). It does this by setting the head
        to the new item if empty or by storing push at the heads next pointer and setting head
        to the pushed item then incrementing the size of the stack
        """

        # error handling
        if self.isFull():
            raise StackIsFull("ERROR: cannot push this item on the stack because it is full")

        else:
            push = Node(item)
            if self.isEmpty():
                self.head = push
                self.currentSize += 1
                return True

            else:
                push.setNext(self.head)
                self.head = push
                self.currentSize += 1
                return True

    def pop(self):
        """
        Pop takes the top item of the stack and gets rid of it by setting the next item in the stack
        to the head and decrementing the size of the stack
        """

        # error handling
        if self.isEmpty():
            raise StackIsEmpty("ERROR: cannot pop because the stack is empty")

        else:
            pop = self.head
            self.head = pop.next
            pop.next = None
            self.currentSize -= 1
            return pop.data

    def isEmpty(self):
        """
        This method checks if the queue is empty by checking if current size is still in or has been set to
         it's "empty" state via decrementing in pop or initializing init
        """
        if self.currentSize == 0:
            return True
        else:
            return False

    def peek(self):
        if self.isEmpty():
            return False
        return self.head.data

    def isFull(self):
        """
        This method checks if the queue is full by checking is currentSize as set by incrementing in push
        is equal (or greater than)the capacity.
        """
        if self.currentSize >= self.capacity:
            return True
        else:
            return False

# ------------------------ Priority Queue Class --------------

class PriorityQueue:
    def __init__(self, capacity):
        if (type(capacity) != int):
            raise QueueCapacityTypeError("ERROR: capacity is not an int")
        if (capacity <= 0):
            raise QueueCapacityBoundError("ERROR: Your capacity is equal to or less than zero")

        self.capacity = capacity
        self.heap = [None] * capacity
        self.currentSize = 0

    def __str__(self):
        """
        this method returns a string representation of the priority queue (i.e (pq, value)
        """
        if self.isEmpty():
            return "[]"
        else:
            buffer = "["
            for i in range(self.currentSize):
                buffer += str(self.heap[i])
            buffer += "]"

        return buffer

    def insert(self, item):
        """
        this method inserts a tuple (item) that has a piece of data and it's required priority in the pQ
        """
        if self.isFull():
            raise QueueIsFull("This priority queue is full")
        if type(item) != tuple:
            return False


        self.heap[self.currentSize] = item
        self.currentSize += 1
        self.makeHeap()

        return True

    def extractMax(self):
        """
        remove value in PQ that has highest priority and then re-heaps the PQ
        """

        if self.isEmpty():
            raise QueueIsEmpty("Tried to extract from an empty queue")

        extracted = self.heap[0]
        self.currentSize -= 1

        for i in range(self.currentSize):
            self.heap[i] = self.heap[i + 1]

            # this corrects so that there's not the original i+1 that never gets overwritten
            if (i == self.currentSize-1):
                print("reached")
                self.heap[i+1] = None


        self.maxHeapify(self.currentSize, 0)

        return extracted

    def peekMax(self):
        """
        looks at the value in the highest priority but leaves it alone
        """
        if self.isEmpty():
            return False

        elif self.isFull():
            return self.heap[0]

    def isEmpty(self):
        """
        This method checks if the Priority queue is empty by checking if current size is still in or has been set to
         it's "empty" state via decrementing in pop or initializing init
        """
        if self.currentSize == 0:
            return True
        else:
            return False

    def isFull(self):
        """
        This method checks if the priority queue is full by checking is currentSize as set by incrementing in push
        is equal (or greater than)the capacity.
        """
        if self.currentSize >= self.capacity:
            return True
        else:
            return False

    def maxHeapify(self, currentSize, maxIndex=0):
        """
        called in extract max to reorder the heap after a value has been removed we do this by using an algorithm that compares
        and it's children and makes sure that the priority of the children is less than the priority of the parent

        """
        leftChildIndex = 2 * maxIndex + 1  # this formula gives us the index of the tuple 1 after the parent (left)
        rightChildIndex = 2 * maxIndex + 2  # this formula gives us the index of the tuple 2 after the parent (right)

        max = self.heap[maxIndex]

        if leftChildIndex < currentSize and self.heap[leftChildIndex][0] > max[0]:
            # this checks if left child exists (index is below current size) and if the priority is higher than
            # the parent

            max = self.heap[leftChildIndex]
            newMaxIndex = leftChildIndex

        if rightChildIndex < currentSize and self.heap[rightChildIndex][0] > max[0]:
            # this checks if right child exists (index is below current size) and if the priority is higher than the
            # parent and note we don't need to compare children because if right is greater than left it will become
            # new max

            max = self.heap[rightChildIndex]
            newMaxIndex = rightChildIndex

        if max != self.heap[maxIndex]:
            # if our max is not at the top of our heap than we need to swap and made it our new max

            self.swap(maxIndex, newMaxIndex)

            # now call heapify down the line of the array since we messed everything up
            # by swapping and need to fix it

            self.maxHeapify(currentSize, newMaxIndex)


    def swap(self, currentMaxIndex, newMaxIndex):
        """
        called to swap the child and parent tuples. I understand the way a child and parent relationship
        works in a tree however for my own conceptualization I call them current and new max rather than
        parent (current max) and child (new max).
        """
        self.heap[currentMaxIndex], self.heap[newMaxIndex] = self.heap[newMaxIndex], self.heap[currentMaxIndex]

    def makeHeap(self):
        # I wrote this method because after looking at heapify I realized if the top
        # tree is sorted it thinks it's good so I need a ground up-top down heaping method
        # basically something that top down sorts the sub trees from bottom tree to top tree

        for i in range(self.getParent(self.currentSize), -1, -1):
            # minus one is so that we check for heap[0]
            # and "increment" minus one...I love the chaos of python loops

            self.maxHeapify(self.currentSize, i)

    def getParent(self, currentSize):
        # takes the left node and gets it's parent
        # I see why this is important now!

        parent = currentSize//2 - 1 # inverse func of (2 * size + 1)
        return parent
