# Laser display boards

You're off on your first sightseening trip of your holiday and you need to catch the right llama-rickshaw to get there. You arrive all keen at the llama-rickshaw station, only to find a scene of chaos. The bad news is that there are lots of llama-rickshaws heading to different places. The good news is that above each bay is a display board that shows where that llama-rickshaw is heading. The bad news is that all the display boards have gone down. The good news is that the station staff are handing out the machine-code instructions to generate the messages on the board. 

Given your l33t haxor skilz, it will be no problem to recreate the messages on the display boards.

The board is grid, 80 pixels wide and 8 pixels tall, with row 1 being the top row and column 1 being the left column. The pixels are changed with these commands:

* `top A B` switches the state of the pixels in the topmost row from columns A to B inclusive. If a pixel was lit, it becomes dark; if it was dark, it becomes lit.
* `left A B` is similar, but works on the left edge, toggling the state of pixels in the leftmost column in rows A to B inclusive. 
* `rotate column A B` rotates column A by B spaces down. Pixels that are moved beyond the bottom edge "wrap around" to the top edge.
* `rotate row A B` rotates row A by B spaces to the right. Pixels that are moved beyond the right edge "wrap around" to the left edge.

You can assume all numbers are integers, the row and column values are always valid, and `A` $\le$ `B` in the `left` and `top` commands.

For instance, with a smaller grid that is 10 pixels wide and 4 tall, this is what a sample sequence of instructions would do.

* `top 1 6` turns on the first six pixels on the top row.
```
******....
..........
..........
..........
```

* `rotate column 2 3` moves the lit pixel on the second column to the bottom row.
```
*.****....
..........
..........
.*........
```

* `top 3 10` turns off the pixels in columns 4, 5, and 6, and turns on the pixels in columns 7 to 10.

```
*.....****
..........
..........
.*........
```

* `rotate column 8 5` moves the one lit pixel in column 8 down five rows, wrapping it all the way around the display and leaving the board with one lit pixel in that column one row lower.
```
*.....*.**
.......*..
..........
.*........
```

* `rotate row 2 6` moves that pixel off the right edge of the display, to it wraps around to appear in column 4.
```
*.....*.**
...*......
..........
.*........
```

* `left 1 3` toggles the pixels in rows 1, 2, and 3 of the first column. The top left pixel (previously on) turns off, while the pixels in rows 2 and 3 come on.
```
......*.**
*..*......
*.........
.*........
```

