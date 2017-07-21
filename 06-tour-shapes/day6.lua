sample_tours = {'FFLRLLFLRL', 'FLLFFLFFFLFFLFLLRRFR', 'FFRLLFRLLFFFRFLLRLLRRLLRLL'}

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

function turn_left(direction)
  return(direction - 1) % 4
end

function turn_right(direction)
  return(direction + 1) % 4
end

function advance(pos, d)
  if d == UP then
    return {x = pos.x, y = pos.y + 1, direction = d}
  elseif d == DOWN then
    return {x = pos.x, y = pos.y - 1, direction = d}
  elseif d == LEFT then
    return {x = pos.x - 1, y = pos.y, direction = d}
  elseif d == RIGHT then
    return {x = pos.x + 1, y = pos.y, direction = d}
  else
    return pos
  end
end

function step(s, current)
  -- print(s, current.x, current.y, current.direction)
  if s == 'F' then
    return advance(current, current.direction)
  elseif s == 'L' then
    return advance(current, turn_left(current.direction))
  elseif s == 'R' then
    return advance(current, turn_right(current.direction))
  else
    error("Invalid instruction")
  end
end

function trace_tour(tour, startx, starty, startdir)
  startx = startx or 0
  starty = starty or 0
  startdir = startdir or RIGHT

  local current = {x = startx, y = starty, direction = startdir}
  local trace = {current}
  for c in tour:gmatch"." do
    current = step(c, current)
    table.insert(trace, current)
  end

  return trace
end


function positions(trace)
  local psns = {}
  for _, p in ipairs(trace) do
    psns[p.x .. ':' .. p.y] = true
  end
  return psns
end


function valid(trace)
  local psns = 1
  for _, _ in pairs(positions(trace)) do
    psns = psns + 1
  end
  return trace[#trace].x == 0 and trace[#trace].y == 0 and psns == #trace
end


function read_tours()
  local tours = {}
  for tour in io.lines('06-tours.txt') do
    table.insert(tours, tour)
  end
  return tours
end


function valid_tours(tours)
  local valids = {}
  for _, t in ipairs(tours) do
    if valid(trace_tour(t)) then
      table.insert(valids, t)
    end
  end
  return valids
end


function steps_total(tours)
  local steps = 0
  for _, t in ipairs(tours) do
    steps = steps + #t
  end
  return steps
end


function trace_distances(tours)
  local tds = {}
  for _, tour in ipairs(tours) do
    local t = trace_tour(tour)
    local l1 = math.abs(t[#t].x) + math.abs(t[#t].y)
    local l1s = tds[l1] or {}
    table.insert(l1s, tour)
    tds[l1] = l1s
  end
  return tds
end


function merge_tours(tour_distances)
  local goods = {}
  for d1, t1s in pairs(tour_distances) do
    for d2, t2s in pairs(tour_distances) do
      if d1 ~= 0 and d2 ~= 0 and math.abs(d1 - d2) <= 1 then
        for _, t1 in ipairs(t1s) do
          for _, t2 in ipairs(t2s) do
            if t1 ~= t2 then
              local t12 = t1 .. t2
              if valid(trace_tour(t12)) then
                table.insert(goods, t12)
              end
            end
          end
        end
      end
    end
  end
  return goods
end

function show_step(step)
  -- sstr = ""
  -- for k, v in pairs(step) do
  --   sstr = sstr .. ', ' .. k .. ': ' .. v
  -- end
  -- return sstr
  return '(' .. step.x .. ', ' .. step.y .. ', ' .. step.direction .. ')'
end

function show_trace(trace)
  local stour = ''
  for _, s in ipairs(trace) do
    stour = stour .. '; ' .. show_step(s)
  end
  return stour
end

trs = read_tours()
tdists = trace_distances(trs)
tpairs = merge_tours(tdists)
-- print(#trs, #valid_tours(trs), steps_total(valid_tours(trs)))
print(steps_total(valid_tours(trs)), 
  steps_total(valid_tours(trs)) + steps_total(tpairs))
