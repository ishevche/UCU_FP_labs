"""
File: algorithms.py

Graph processing algorithms
"""

from Graph_case_study.linkedstack import LinkedStack


def topoSort(g, startLabel=None):
    stack = LinkedStack()
    g.clearVertexMarks()
    for v in g.vertices():
        if not v.isMarked():
            dfs(g, v, stack)
    return stack


def dfs(g, v, stack):
    v.setMark()
    for w in g.neighboringVertices(v.getLabel()):
        if not w.isMarked():
            dfs(g, w, stack)
    stack.push(v)


def bfs(g, queue, stack):
    if not queue:
        return
    v = queue.pop(0)
    v.setMark()
    for w in g.neighboringVertices(v.getLabel()):
        if not w.isMarked():
            queue += [w]
    bfs(g, queue, stack)
    stack.push(v)
