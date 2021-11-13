#############################
## Author: Vignesh Kothapalli
## NetID: vk2115
## ID: N12417420
#############################
"""
The following module implements the search algorithms to
find a path from start node to goal in a graph.
"""

from collections import deque
import heapq
import logging

from common import euclidean_distance

def bfs(graph, start, goal):
  """Search for a path from start to goal using
  the breadth first search algorithm.

  Args:
    graph: An instance of `common.Graph` class
    start: Name of the starting node
    goal: Name of the destination node
  """
  visited = {name: False for name in graph.get_node_names()}
  queue = deque([])
  queue.append(start)
  found = False

  while queue:
    current_path = queue.popleft()
    node_name = current_path.split(",")[-1]
    if node_name == goal:
      found = True
      break
    if not visited[node_name]:
      logging.debug(f"Expanding: {node_name}")
      visited[node_name] = True
    neighbours = graph.g[node_name]
    for neighbour in neighbours:
      if not visited[neighbour]:
        queue.append(f'{current_path},{neighbour}')

  if found:
    return f'Solution: {current_path.replace(",", "->")}'
  return "Solution: Not found"

def ids(graph, start, goal, depth):
  """Search for a path from start to goal using
  the iterative deepening algorithm.

  Args:
    graph: An instance of `common.Graph` class
    start: Name of the starting node
    goal: Name of the destination node
    depth: depth for terminating the depth search

  NOTE: The `termination_depth` value used here is the maximum
    incremental `depth` value.
  """
  termination_depth = len(graph.nodes)
  found = False
  path = deque([])
  while not found and depth < termination_depth:
    logging.debug(f"Iterative deepening with max depth: {depth}")
    visited = {name: False for name in graph.get_node_names()}
    found, path = _ids_recursor(
      graph=graph,
      start=start,
      goal=goal,
      depth=depth,
      orig_depth=depth,
      visited=visited
    )
    depth += 1

  if found:
    return f'Solution: {"->".join(path)}'
  return "Solution: Not found"

def _ids_recursor(graph, start, goal, depth, orig_depth, visited):
  if start == goal:
    return True, deque([start])
  if depth <= 0:
    logging.debug(f"hit depth={orig_depth}: {start}")
    visited[start] = True
    return False, deque([])

  logging.debug(f"Expanding: {start}")
  visited[start] = True
  neighbours = graph.g[start]
  for neighbour in neighbours:
    if not visited[neighbour]:
      found, path = _ids_recursor(
        graph=graph,
        start=neighbour,
        goal=goal,
        depth=depth-1,
        orig_depth=orig_depth,
        visited=visited
      )
      if found:
        path.appendleft(start)
        return True, path
  return False, deque([])


def astar(graph, start, goal):
  """Search for a path from start to goal using
  the iterative deepening algorithm.

  Args:
    graph: An instance of `common.Graph` class
    start: Name of the starting node
    goal: Name of the destination node
    depth: Initial depth for terminating the depth search
  """
  p_queue = []
  # Each element represents the (g+h, g, h, path) tuple
  heapq.heappush(p_queue, (0, 0, 0, start))
  found = False

  while p_queue:
    cost, g, _, current_path = heapq.heappop(p_queue)
    logging.debug(f'Adding {current_path.replace(",","->")}')
    current_node_name = current_path.split(",")[-1]
    if current_node_name == goal:
      found = True
      break

    neighbours = graph.g[current_node_name]
    for neighbour in neighbours:
      # Skip the neighbour which is already in the current path
      if neighbour in current_path:
        continue
      path = "{},{}".format(current_path, neighbour)
      current_node = graph.nodes[current_node_name]
      neighbour_node = graph.nodes[neighbour]
      goal_node = graph.nodes[goal]
      traversal_cost = round(g + euclidean_distance(current_node, neighbour_node), 2)
      heuristic_cost = euclidean_distance(neighbour_node, goal_node)
      total_cost = round(traversal_cost + heuristic_cost, 2)
      logging.debug(
        f'{path.replace(",","->")} ; g={traversal_cost} h={heuristic_cost} total={total_cost}'
      )
      heapq.heappush(p_queue, (total_cost, traversal_cost, heuristic_cost, path))

  if found:
    return f'Solution: {current_path.replace(",", "->")}'
  return "Solution: Not found"