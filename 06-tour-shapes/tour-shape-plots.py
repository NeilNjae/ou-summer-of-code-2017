
# coding: utf-8

# Given a sequence of {F|L|R}, each of which is "move forward one step", "turn left, then move forward one step", "turn right, then move forward one step":
# 1. which tours are closed?
# 2. what is the area enclosed by the tour?

# In[1]:

import collections
import enum
import random
import os

import matplotlib.pyplot as plt

# Use PIL to save some image metadata
from PIL import Image
from PIL import PngImagePlugin

# In[2]:

class Direction(enum.Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    
turn_lefts = {Direction.UP: Direction.LEFT, Direction.LEFT: Direction.DOWN,
              Direction.DOWN: Direction.RIGHT, Direction.RIGHT: Direction.UP}

turn_rights = {Direction.UP: Direction.RIGHT, Direction.RIGHT: Direction.DOWN,
               Direction.DOWN: Direction.LEFT, Direction.LEFT: Direction.UP}

def turn_left(d):
    return turn_lefts[d]

def turn_right(d):
    return turn_rights[d]


# In[3]:

Step = collections.namedtuple('Step', ['x', 'y', 'dir'])
Mistake = collections.namedtuple('Mistake', ['i', 'step'])


# In[4]:

def advance(step, d):
    if d == Direction.UP:
        return Step(step.x, step.y+1, d)
    elif d == Direction.DOWN:
        return Step(step.x, step.y-1, d)
    elif d == Direction.LEFT:
        return Step(step.x-1, step.y, d)
    elif d == Direction.RIGHT:
        return Step(step.x+1, step.y, d)


# In[5]:

def trace_tour(tour, startx=0, starty=0, startdir=Direction.RIGHT):
    current = Step(startx, starty, startdir)
    trace = [current]
    for s in tour:
        if s == 'F':
            current = advance(current, current.dir)
        elif s == 'L':
            current = advance(current, turn_left(current.dir))
        elif s == 'R':
            current = advance(current, turn_right(current.dir))
        trace += [current]
    return trace    


# In[6]:

def positions(trace):
    return [(s.x, s.y) for s in trace]


# In[7]:

def valid(trace):
    return (trace[-1].x == 0 
            and trace[-1].y == 0 
            and len(set(positions(trace))) + 1 == len(trace))


# In[8]:

def chunks(items, n=2):
    return [items[i:i+n] for i in range(len(items) - n + 1)]


# Using the [Shoelace formula](https://en.wikipedia.org/wiki/Shoelace_formula)

# In[9]:

def shoelace(trace):
    return abs(sum(s.x * t.y - t.x * s.y for s, t in chunks(trace, 2))) // 2


# In[10]:

def step(s, current):
    if s == 'F':
        return advance(current, current.dir)
    elif s == 'L':
        return advance(current, turn_left(current.dir))
    elif s == 'R':
        return advance(current, turn_right(current.dir))
    else:
        raise ValueError


# In[11]:

def valid_prefix(tour):
    current = Step(0, 0, Direction.RIGHT)
    prefix = []
    posns = []
    for s in tour:
        current = step(s, current)
        prefix += [s]
        if (current.x, current.y) in posns:
            return ''
        elif current.x == 0 and current.y == 0: 
            return ''.join(prefix)
        posns += [(current.x, current.y)]
    if current.x == 0 and current.y == 0:
        return ''.join(prefix)
    else:
        return ''


# In[12]:

def mistake_positions(trace, debug=False):
    mistakes = []
    current = trace[0]
    posns = [(0, 0)]
    for i, current in enumerate(trace[1:]):
        if (current.x, current.y) in posns:
            if debug: print(i, current)
            mistakes += [Mistake(i+1, current)]
        posns += [(current.x, current.y)]
    if (current.x, current.y) == (0, 0):
        return mistakes[:-1]
    else:
        return mistakes + [Mistake(len(trace)+1, current)]


# In[13]:

def returns_to_origin(mistake_positions):
    return [i for i, m in mistake_positions
           if (m.x, m.y) == (0, 0)]


# In[14]:

def random_walk(steps=1000):
    return ''.join(random.choice('FFLR') for _ in range(steps))


# In[15]:

def bounds(trace):
    return (max(s.x for s in trace),
            max(s.y for s in trace),
            min(s.x for s in trace),
            min(s.y for s in trace))


# In[16]:


plot_wh = {Direction.UP: (0, 1), Direction.LEFT: (-1, 0),
           Direction.DOWN: (0, -1), Direction.RIGHT: (1, 0)}

def plot_trace(trace, colour='k', xybounds=None, fig=None, subplot_details=None, filename=None):
    # plt.axis('on')
    plt.axis('off')
    plt.axes().set_aspect('equal')
    for s, t in chunks(trace, 2):
        w, h = plot_wh[t.dir]
        plt.arrow(s.x, s.y, w, h, head_width=0.1, head_length=0.1, fc=colour, ec=colour, length_includes_head=True)
    xh, yh, xl, yl = bounds(trace)
    if xybounds is not None:    
        bxh, byh, bxl, byl = xybounds
        plt.xlim([min(xl, bxl)-1, max(xh, bxh)+1])
        plt.ylim([min(yl, byl)-1, max(yh, byh)+1])
    else:
        plt.xlim([xl-1, xh+1])
        plt.ylim([yl-1, yh+1])
    if filename:
        plt.savefig(filename)
    plt.close()


# In[17]:

def trim_loop(tour):
    trace = trace_tour(tour)
    mistakes = mistake_positions(trace)
    end_mistake_index = 0
#     print('end_mistake_index {} pointing to trace position {}; {} mistakes and {} in trace; {}'.format(end_mistake_index, mistakes[end_mistake_index].i, len(mistakes), len(trace), mistakes))
    # while this mistake extends to the next step in the trace...
    while (mistakes[end_mistake_index].i + 1 < len(trace) and 
           end_mistake_index + 1 < len(mistakes) and
           mistakes[end_mistake_index].i + 1 == 
           mistakes[end_mistake_index + 1].i):
#         print('end_mistake_index {} pointing to trace position {}; {} mistakes and {} in trace'.format(end_mistake_index, mistakes[end_mistake_index].i, len(mistakes), len(trace), mistakes))
        # push this mistake finish point later
        end_mistake_index += 1
    mistake = mistakes[end_mistake_index]
    
    # find the first location that mentions where this mistake ends (which the point where the loop starts)
    mistake_loop_start = max(i for i, loc in enumerate(trace[:mistake.i])
                             if (loc.x, loc.y) == (mistake.step.x, mistake.step.y))
#     print('Dealing with mistake from', mistake_loop_start, 'to', mistake.i, ', trace has len', len(trace))
    
    # direction before entering the loop
    direction_before = trace[mistake_loop_start].dir
    
    # find the new instruction to turn from heading before the loop to heading after the loop
    new_instruction = 'F'
    if (mistake.i + 1) < len(trace):
        if turn_left(direction_before) == trace[mistake.i + 1].dir:
            new_instruction = 'L'
        if turn_right(direction_before) == trace[mistake.i + 1].dir:
            new_instruction = 'R'
#     if (mistake.i + 1) < len(trace):
#         print('turning from', direction_before, 'to', trace[mistake.i + 1].dir, 'with', new_instruction )
#     else:
#         print('turning from', direction_before, 'to BEYOND END', 'with', new_instruction )
    return tour[:mistake_loop_start] + new_instruction + tour[mistake.i+1:]
#     return mistake, mistake_loop_start, trace[mistake_loop_start-2:mistake_loop_start+8]


# In[18]:

def trim_all_loops(tour, mistake_reduction_attempt_limit=10):
    trace = trace_tour(tour)
    mistake_limit = 1
    if trace[-1].x == 0 and trace[-1].y == 0:
        mistake_limit = 0
    mistakes = mistake_positions(trace)
    
    old_mistake_count = len(mistakes)
    mistake_reduction_tries = 0
    
    while len(mistakes) > mistake_limit and mistake_reduction_tries < mistake_reduction_attempt_limit:
        tour = trim_loop(tour)
        trace = trace_tour(tour)
        mistakes = mistake_positions(trace)
        if len(mistakes) < old_mistake_count:
            old_mistake_count = len(mistakes)
            mistake_reduction_tries = 0
        else:
            mistake_reduction_tries += 1
    if mistake_reduction_tries >= mistake_reduction_attempt_limit:
        return ''
    else:
        return tour


# In[19]:

def reverse_tour(tour):
    def swap(tour_step):
        if tour_step == 'R':
            return 'L'
        elif tour_step == 'L':
            return 'R'
        else:
            return tour_step
        
    return ''.join(swap(s) for s in reversed(tour))


# In[20]:

def wander_near(locus, current, limit=10):
    valid_proposal = False
    while not valid_proposal:
        s = random.choice('FFFRL')
        if s == 'F':
            proposed = advance(current, current.dir)
        elif s == 'L':
            proposed = advance(current, turn_left(current.dir))
        elif s == 'R':
            proposed = advance(current, turn_right(current.dir))
        if abs(proposed.x - locus.x) < limit and abs(proposed.y - locus.y) < limit:
            valid_proposal = True
#     print('At {} going to {} by step {} to {}'.format(current, locus, s, proposed))
    return s, proposed


# In[21]:

def seek(goal, current):
    dx = current.x - goal.x
    dy = current.y - goal.y

    if dx < 0 and abs(dx) > abs(dy): # to the left
        side = 'left'
        if current.dir == Direction.RIGHT:
            s = 'F'
        elif current.dir == Direction.UP:
            s = 'R'
        else:
            s = 'L'
    elif dx > 0 and abs(dx) > abs(dy): # to the right
        side = 'right'
        if current.dir == Direction.LEFT:
            s = 'F'
        elif current.dir == Direction.UP:
            s = 'L'
        else:
            s = 'R'
    elif dy > 0 and abs(dx) <= abs(dy): # above
        side = 'above'
        if current.dir == Direction.DOWN:
            s = 'F'
        elif current.dir == Direction.RIGHT:
            s = 'R'
        else:
            s = 'L'
    else: # below
        side = 'below'
        if current.dir == Direction.UP:
            s = 'F'
        elif current.dir == Direction.LEFT:
            s = 'R'
        else:
            s = 'L'
    if s == 'F':
        proposed = advance(current, current.dir)
    elif s == 'L':
        proposed = advance(current, turn_left(current.dir))
    elif s == 'R':
        proposed = advance(current, turn_right(current.dir))
        
#     print('At {} going to {}, currently {},  by step {} to {}'.format(current, goal, side, s, proposed))

    return s, proposed


# In[22]:

def guided_walk(loci, locus_limit=5, wander_limit=10, seek_step_limit=20):
    trail = ''
    current = Step(0, 0, Direction.RIGHT)    
    l = 0
    finished = False
    while not finished:
        if abs(current.x - loci[l].x) < locus_limit and abs(current.y - loci[l].y) < locus_limit:
            l += 1
            if l == len(loci) - 1:
                finished = True
        s, proposed = wander_near(loci[l], current, limit=wander_limit)
        trail += s
        current = proposed
#     print('!! Finished loci')
    seek_steps = 0
    while not (current.x == loci[l].x and current.y == loci[l].y) and seek_steps < seek_step_limit:
#         error = max(abs(current.x - loci[l].x), abs(current.y - loci[l].y))
#         s, proposed = wander_near(loci[l], current, limit=error+1)
        s, proposed = seek(loci[l], current)
        trail += s
        current = proposed
        seek_steps += 1
    if seek_steps >= seek_step_limit:
        return ''
    else:
        return trail


# In[24]:

def square_tour(a=80):
    "a is width of square"
    return ('F' * a + 'L') * 4


# In[25]:

def cross_tour(a=50, b=40):
    "a is width of cross arm, b is length of cross arm"
    return ('F' *  a + 'L' + 'F' * b + 'R' + 'F' * b + 'L') * 4


# In[26]:

def quincunx_tour(a=60, b=30, c=50):
    "a is length of indent, b is indent/outdent distance, c is outdent outer length"
    return ('F' * a + 'R' + 'F' * b + 'L' + 'F' * c + 'L' + 'F' * c + 'L' + 'F' * b + 'R') * 4


# In[27]:

heart_points = [Step(60, 50, Direction.UP), Step(50, 90, Direction.UP),
                Step(20, 70, Direction.UP), 
                Step(-40, 90, Direction.UP), Step(-60, 80, Direction.UP), 
                Step(0, 0, Direction.RIGHT)]

heart_tour = ''
current = Step(0, 0, Direction.RIGHT)

for hp in heart_points:
    while not (current.x == hp.x and current.y == hp.y):
        s, proposed = seek(hp, current)
        heart_tour += s
        current = proposed

def heart_tour_func(): return heart_tour


# In[28]:

# success_count = 0
# while success_count <= 20:
#     lc = trace_tour(square_tour(a=10))
#     rw = guided_walk(lc, wander_limit=4, locus_limit=2)
#     if rw:
#         rw_trimmed = trim_all_loops(rw)
#         if len(rw_trimmed) > 10:
#             with open('small-squares.txt', 'a') as f:
#                 f.write(rw_trimmed + '\n')
#                 success_count += 1


# In[29]:

# success_count = 0
# while success_count <= 20:
#     lc = trace_tour(square_tour())
#     rw = guided_walk(lc)
#     if rw:
#         rw_trimmed = trim_all_loops(rw)
#         if len(rw_trimmed) > 10:
#             with open('large-squares.txt', 'a') as f:
#                 f.write(rw_trimmed + '\n')
#                 success_count += 1


# In[30]:

# success_count = 0
# while success_count <= 20:
#     lc = trace_tour(cross_tour())
#     rw = guided_walk(lc)
#     if rw:
#         rw_trimmed = trim_all_loops(rw)
#         if len(rw_trimmed) > 10:
#             with open('cross.txt', 'a') as f:
#                 f.write(rw_trimmed + '\n')
#                 success_count += 1


# In[31]:

# success_count = 0
# while success_count <= 20:
#     lc = trace_tour(quincunx_tour())
#     rw = guided_walk(lc)
#     if rw:
#         rw_trimmed = trim_all_loops(rw)
#         if len(rw_trimmed) > 10:
#             with open('quincunx.txt', 'a') as f:
#                 f.write(rw_trimmed + '\n')
#                 success_count += 1


# In[32]:

# with open('tours.txt') as f:
#     for i, tour_s in enumerate(f.readlines()):
#         tour = tour_s.strip()
#         filename = 'tour-{:03}-s{:04}-m{:03}.png'.format(i, len(tour), len(mistake_positions(trace_tour(tour))))
#         plot_trace(trace_tour(tour), filename=filename)
#         im = Image.open(filename)
#         meta = PngImagePlugin.PngInfo()
#         meta.add_text('Description', tour)
#         im.save(filename, 'PNG', pnginfo=meta)

# with open('tours-with-mistakes.txt') as f:
#     for i, tour_s in enumerate(f.readlines()):
#         tour = tour_s.strip()
#         filename = 'tour-{:03}-s{:04}-m{:03}.png'.format(i, len(tour), len(mistake_positions(trace_tour(tour))))
#         plot_trace(trace_tour(tour), filename=filename)
#         im = Image.open(filename)
#         meta = PngImagePlugin.PngInfo()
#         meta.add_text('Description', tour)
#         im.save(filename, 'PNG', pnginfo=meta)

# with open('tours-open.txt') as f:
#     for i, tour_s in enumerate(f.readlines()):
#         tour = tour_s.strip()
#         filename = 'tour-{:03}-s{:04}-m{:03}-open.png'.format(i, len(tour), len(mistake_positions(trace_tour(tour))))
#         plot_trace(trace_tour(tour), filename=filename)
#         im = Image.open(filename)
#         meta = PngImagePlugin.PngInfo()
#         meta.add_text('Description', tour)
#         im.save(filename, 'PNG', pnginfo=meta)

with open('tours-random-walk.txt') as f:
    for i, tour_s in enumerate(f.readlines()):
        tour = tour_s.strip()
        filename = 'tour-{:03}-s{:04}-m{:03}-walk.png'.format(i, len(tour), len(mistake_positions(trace_tour(tour))))
        plot_trace(trace_tour(tour), filename=filename)
        im = Image.open(filename)
        meta = PngImagePlugin.PngInfo()
        meta.add_text('Description', tour)
        im.save(filename, 'PNG', pnginfo=meta)