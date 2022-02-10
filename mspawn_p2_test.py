"""
Author: Jared Hall, <your_name_here>
Last Modified Date: 01/28/2022
Description: This file contains some useful methods to help you test your code.
             Also contains some starter codes for testing.
"""
from mspawn_p2 import *
import pytest
def heapValidator(heap):
    """
    Description: This method validates the heap.
    Usage:  heapValidator(PQ._heap)
    Returns: tuple. (bool, str)
    Format: (True/False, reason)
    """
    returnValue = (True, "PASSED")
    # Step-01: Varifies that the heap contains tuples of the correct format.
    if(type(heap) != list):
        returnValue = (False, "FAILED: heap must be a list.")
    elif(len(heap) == 0):
        pass
    else:
        start = 1 if(type(heap[0]) != tuple) else 0
        for i in range(start, len(heap), 1):
            if(type(heap[i]) != tuple):
                returnValue = (False, "FAILED: Heap must consist of tuples")
            elif(type(heap[i][0]) != int or heap[i][0] <= 0):
                returnValue = (False, "FAILED: each tuple in the heap must "+\
                "have a positive int as the priority")
            else:
                try:
                    heap[i][1]
                except:
                    returnValue = (False, "FAILED: Incorrectly formatted "+\
                    "tuple. Must have an item to queue")
    # step-02: Validate the heap. (e.g., make sure all nodes obey heap rules)
    if(returnValue[0] and len(heap) != 0):
        start = 1 if(type(heap[0]) != tuple) else 0
        if(len(heap) > start):
            parentIndex = 0
            for i in range(start, len(heap), 1):
                if(i == 0):
                    parentIndex = 0
                else:
                    parentIndex = (i-2)//2 if( i % 2 == 0) else (i - 1)//2
                if(heap[i][0] > heap[parentIndex][0]):
                    returnValue = (False, f"Invalid heap detected: Child-{i}"+\
                    f" {heap[i]} > parent-{parentIndex} {heap[parentIndex]}")
                    break
    return returnValue


class TestMain:
    def test_initValid(self):
        # Hint: test a valid constructor call
        PQ = PriorityQueue(5)
        assert PQ.capacity == 5

    def test_initInvalidNonInt(self):
        # Hint: Test the constructor with something that is not an int
        with pytest.raises(QueueCapacityTypeError):
            PQ = PriorityQueue("non valid int")

    def test_initInvalidNeg(self):
        # Hint: Test the constructor with a negative int
        with pytest.raises(QueueCapacityBoundError):
            PQ = PriorityQueue(-1)

    def test_strValid(self):
        # Hint: Test the string method See format from project document.
        PQ = PriorityQueue(5)

        for i in range(5):
            # I wrote this after my last few test so this is the same test values and the
            # array value should be the same (16, 9, 1, 0, 4) (double checked by hand)
            PQ.insert((i * i, "value"))

        assert PQ.__str__() == "[(16, 'value')(9, 'value')(1, 'value')(0, 'value')(4, 'value')]"

    def test_insertInvalidInput(self):
        # Hint: Test what happens when you try to insert invalid input.
        PQ = PriorityQueue(1)
        assert PQ.insert("bad") == False

    def test_insertFull(self):
        # Hint: Test what happens if you try to insert into a full PQ
        PQ = PriorityQueue(3)
        with pytest.raises(QueueIsFull):
            for i in range(4):
                PQ.insert((4-i, i))

    def test_insertValid(self):
        # Hint: Test what happens when you try to insert valid input.
        #      Dont forget to validate the heap! (^,^)
        PQ = PriorityQueue(3)

        for i in range(3):
            PQ.insert((3-i,i))

        assert heapValidator(PQ.heap) == (True, "PASSED")

    def test_extractMaxEmpty(self):
        # Hint: Test what happens if you try to extract when the PQ is empty
        PQ = PriorityQueue(1)
        with pytest.raises(QueueIsEmpty):
            PQ.extractMax()

    def test_extractMaxNotEmpty(self):
        # Hint: Test what happens if you try to extract when the PQ is not empty
        pass
    def test_peekMaxEmpty(self):
        # Hint: Test what happens if you try to peek when the PQ is empty
        PQ = PriorityQueue(1)
        assert PQ.peekMax() == False

    def test_peekMaxNotEmpty(self):
        # Hint: Test what happens if you try to peek when the PQ is not empty
        PQ = PriorityQueue(3)
        for i in range(3):
            PQ.insert((3-i,i))

        assert PQ.peekMax() == (3,0)

    def test_isEmptyNoItems(self):
        # Hint: Test what happens when isEmpty is called when the PQ is empty.
        PQ = PriorityQueue(1)
        assert PQ.isEmpty() == True

    def test_isEmptyNotEmpty(self):
        # test what happens if isEmpty is called when the queue is not empty.
        pass
    def test_isFullNoItems(self):
        # Hint: Test what happens when isFull is called when the PQ is empty.

        PQ = PriorityQueue(3)
        assert PQ.isFull() == False

    def test_isFullFull(self):
        # test what happens if isFull is called when the queue is full.

        PQ = PriorityQueue(3)
        for i in range(3):
            PQ.insert((3-i,i))

        assert PQ.isFull() == True

    def test_priorityFunction(self):
        """
        This method I wrote because I want something that actually tests the PQ functionality by
        inserting values with varying priorities and then accurately heapifying them
        """
        PQ = PriorityQueue(5)

        for i in range(5):
            # this inserts tuples that start at low priority (so the priority values are in "reverse" order)
            # and then tests that the values are ordered correctly in the array
            # largest p at the top in descending order
            PQ.insert((i * i, "value"))
            compArray = [0] * 5

        for i in range(5):
            value = PQ.heap[i]
            compArray[i] = value[0]

        # I did this by hand and tracked the swaps on paper...old school but it works
        assert compArray == [16,9,1,0,4]



    def testPriorityFunctionExtract(self):
        """
        I wrote this method so that I can test the re-heapifying function of my PQ
        and making sure even when a max is extracted the PQ is still ordered correctly
        """

        PQ = PriorityQueue(5)

        for i in range(5):
            # this inserts tuples that start at low priority (so the priority values are in "reverse" order)
            # and then tests that the values are ordered correctly in the array
            # largest p at the top in descending order
            # THEN it extracts one and checks it's still in max heap order

            PQ.insert((i * i, "value"))
            compArray = [0] * 5

        assert PQ.extractMax()[0] == 16

        for i in range(5):

            if PQ.heap[i] == None:
                compArray[i] = None

            else:
                value = PQ.heap[i]
                compArray[i] = value[0]

        # bonus make sure you get the max priority

        assert compArray == [9,1,0,4,None]
