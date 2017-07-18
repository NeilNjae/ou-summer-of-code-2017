var fs = require("fs");

const WIDTH = 80;
const HEIGHT = 8;

var initial_grid = new Array(HEIGHT);
for (var i = 0; i < HEIGHT; i++) {
  initial_grid[i] = new Array(WIDTH);
  for (var j = 0; j < WIDTH; j++) {
    initial_grid[i][j] = false;
  }
}

function printGrid(g) {
    return g.map(function (row) {
        return row.map(showCell).join(''); 
    }).join('\n');
}

function showCell(c) {
    if (c) {
        return '*';
    } else {
        return ' ';
    }
}

// toggle the value of a cell
function toggle(c) {
    if (c) {
        return false;
    } else {
        return true;
    }
}

// turn a stirng into a command (a three-element array)
function parseCommand(str) {
    var command = str.split(' ').slice(-3);
    command[1] = Number(command[1]);
    command[2] = Number(command[2]);
    return command;
}

// implement the instructions
function top(from, to, grid) {
    for (var c = from-1; c < to; c++) {
        grid[0][c] = toggle(grid[0][c]);
    };
    return grid;
}

function left(from, to, grid) {
    for (var r = from-1; r < to; r++) {
        grid[r][0] = toggle(grid[r][0]);
    };
    return grid;
}

function rotate_column(col, raw_n, grid) {
    var n = raw_n % HEIGHT;
    var temp_column = new Array(HEIGHT);
    for (var i = 0; i < HEIGHT; i++) {
        temp_column[i] = grid[i][col-1];
    };
    var new_col = temp_column.slice(-n).concat(temp_column.slice(0, -n));
    for (var i = 0; i < HEIGHT; i++) {
        grid[i][col-1] = new_col[i];
    };   
    return grid;
}

function rotate_row(row, raw_n, grid) {
    var n = raw_n % WIDTH;
    var temp_row = new Array(WIDTH);
    for (var i = 0; i < WIDTH; i++) {
        temp_row[i] = grid[row-1][i];
    };
    var new_row = temp_row.slice(-n).concat(temp_row.slice(0, -n));
    for (var i = 0; i < WIDTH; i++) {
        grid[row-1][i] = new_row[i];
    };
    return grid;
}


// Dispatch table for execution
var dispatchTable = {'top': top, 'left': left, 
    'row': rotate_row, 'column': rotate_column};


// Do one command, based on the function stored in the dispatch table
function dispatchCommand(grid, command) {
    return dispatchTable[command[0]](command[1], command[2], grid);
}

// Execute all the commands as a fold on the initial grid
function executeCommands(commands, grid) {
    return commands.reduce(dispatchCommand, grid);
}


// Merge the lines of the grid into one line, then pick out the true values
function count_pixels(grid) {
    return  grid.reduce(
                function (t, l) {return t.concat(l);}
            ).filter(
                function (c) {return c;}
            ).length
}

var instrs = fs.readFileSync('05-pixels.txt').toString().split('\n');
var instructions = instrs.map(parseCommand);

var final_grid = executeCommands(instructions, initial_grid);

console.log(count_pixels(final_grid));
console.log(printGrid(final_grid));
