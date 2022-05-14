"""
Stack to queue converter.
"""

from arraystack import ArrayStack
from arrayqueue import ArrayQueue


def stack_to_queue(stack: ArrayStack) -> ArrayQueue:
    """
    Stack to queue converter.
    """
    reversed_stack = ArrayStack(stack)
    answer_queue = ArrayQueue()
    while not reversed_stack.isEmpty():
        answer_queue.add(reversed_stack.pop())
    return answer_queue
