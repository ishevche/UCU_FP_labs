"""
Queue to stack converter.
"""

from arraystack import ArrayStack
from arrayqueue import ArrayQueue


def queue_to_stack(queue: ArrayQueue) -> ArrayStack:
    """
    Queue to stack converter.
    """
    reversed_stack = ArrayStack(queue)
    answer_stack = ArrayStack()
    while not reversed_stack.isEmpty():
        answer_stack.push(reversed_stack.pop())
    return answer_stack
