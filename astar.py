import queue as Q

#define state representation
class State:
	g_val = int()
	h_val = int()
	loc = None
	dirt = set()
	path = ''
	def __lt__(self, other):
		return self.h_val < other.h_val

#initialize world
init_location = ()
init_dirt = set()
obstacles = set()

#read world metadata
cols = int(input())
rows = int(input())

#find nearest dirt square to given point
def h(loc, dirt):
	dists = Q.PriorityQueue()
	for d in dirt:
		dy = loc[0] - d[0]
		dx = loc[1] - d[1]
		dists.put((dy ** 2 + dx ** 2) ** 0.5)
	if(dists.empty()):
		return 0
	return dists.get()

#generate children of a given node
def expand(node, open, closed):
	closed.add(node)

	if node.loc[0] - 1 >= 0:
		upper_loc = (node.loc[0] - 1, node.loc[1])
		if upper_loc not in obstacles:
			u_state = State()
			u_state.g_val = node.g_val + 1
			u_state.loc = (node.loc[0] - 1, node.loc[1])
			u_state.dirt = set(node.dirt)
			u_state.path = node.path + 'N'
			u_state.h_val = u_state.g_val + h(u_state.loc, u_state.dirt)
			if u_state not in closed:
				open.put(u_state)

	if node.loc[0] + 1 < rows:
		lower_loc = (node.loc[0] + 1, node.loc[1])
		if lower_loc not in obstacles:
			d_state = State()
			d_state.g_val = node.g_val + 1
			d_state.loc = (node.loc[0] + 1, node.loc[1])
			d_state.dirt = set(node.dirt)
			d_state.path = node.path + 'S'
			d_state.h_val = d_state.g_val + h(d_state.loc, d_state.dirt)
			if d_state not in closed:
				open.put(d_state)

	if node.loc[1] - 1 >= 0:
		left_loc = (node.loc[0], node.loc[1] - 1)
		if left_loc not in obstacles:
			l_state = State()
			l_state.g_val = node.g_val + 1
			l_state.loc = (node.loc[0], node.loc[1] - 1)
			l_state.dirt = set(node.dirt)
			l_state.path = node.path + 'W'
			l_state.h_val = l_state.g_val + h(l_state.loc, l_state.dirt)
			if l_state not in closed:
				open.put(l_state)

	if node.loc[1] + 1 < cols:
		right_loc = (node.loc[0], node.loc[1] + 1)
		if right_loc not in obstacles:
			r_state = State()
			r_state.g_val = node.g_val + 1
			r_state.loc = (node.loc[0], node.loc[1] + 1)
			r_state.dirt = set(node.dirt)
			r_state.path = node.path + 'E'
			r_state.h_val = r_state.g_val + h(r_state.loc, r_state.dirt)
			if r_state not in closed:
				open.put(r_state)

	if node.loc in node.dirt:
		v_state = State()
		v_state.g_val = node.g_val
		v_state.loc = (node.loc[0], node.loc[1])
		v_state.dirt = set(node.dirt)
		v_state.dirt.remove(node.loc)
		v_state.path = node.path + 'V'
		v_state.h_val = v_state.g_val + h(v_state.loc, v_state.dirt)
		if v_state not in closed:
			open.put(v_state)

	return

#a* algorithm on given State
def a_star(root):
	open = Q.PriorityQueue()
	closed = set()
	open.put(root)

	while not open.empty():
		node = open.get()
		if len(node.dirt) == 0:
			for s in node.path:
				print(s)
			return
		expand(node, open, closed)

	print('no path exists.')
	return

#main function body

#read world
for i in range(rows):
	line = input()
	#iterate over line
	for j in range(cols):
		#if occupied space, add to appropriate var
		if line[j] == '@':
			init_location = (i, j)
		elif line[j] == '*':
			init_dirt.add((i, j))
		elif line[j] == '#':
			obstacles.add((i, j))

#create initial state
init_state = State()
init_state.loc = init_location
init_state.dirt = init_dirt
a_star(init_state)