import sys


program = '>' + '+' * 61 + '>' + '+' * 33 + '>' + '+' * 24
program += """


read character into cell 9
>>>>>>,



while cell 9 != 0 # have an input
[
  set cell 10 to 1
  >[-]+

  # clear cells 4 and 0
  <<<<<<[-]<<<<[-]>
  # copy cell 1 to cell 0 using cell 4
  [-<+>>>>+<<<]
  >>>[-<<<+>>>]
  <<<<
  
  subtract cell 0 from cell 9 
  [->>>>>>>>>-<<<<<<<<<]
  >>>>>>>>>
  
  while cell 9 != 0 # we're not at an exit
  [
    set cell 10 to 0
    >[-]
    
    copy cell 2 to cell 0 using cell 4
    <<<<<<<<[-<<+>>>>+<<]
    >>[-<<+>>]
    <<<<
    
    subtract cell 0 from cell 9
    [->>>>>>>>>-<<<<<<<<<]
    >>>>>

    set cell 5 to 1
    [-]+
    >>>>

    
    while cell 9 != 0 # we're going down
    [
      clear cell 5
      <<<<[-]
      copy cell 7 to cell 11 using cell 12
      >>[->>>>+>+<<<<<]
      >>>>>[-<<<<<+>>>>>]
      
      cell 12 is zero
      
      while cell 11 != 0 # above ground
      <
      [
        set cell 12 to 1
        >[-]+
        
        clear cell 11
        <[-]
      end
      ] 11
      
      while cell 12 != 0
      >
      [
        decrement cell 7
        <<<<<-
        
        set cell 12 to zero
        >>>>>[-]
      end
      ] 12
        
      <<<<<<
      decrement cell 6
      -
      
      have now dealt with the input so clear cell 9
      >>>[-]
    end
    ] 9
    
    
    while cell 5 != 0 # we're going up
    <<<<
    [
      clear cell 5
      [-]


      # set cell 12 to 0
      >>>>>>>[-]

      ### if 6 == 0 or 7 != 0
      ###   set cell 12 to 1

      # copy cell 6 to cell 11 using cell 12
      <<<<<<[->>>>>+>+<<<<<<]
      >>>>>>[-<<<<<<+>>>>>>]
  
      set cell 12 to 1
      [-]+

      while cell 11 != 0
      <
      [
        clear cell 12
        >[-]

        set cell 11 to 0
        <[-]
      end 11
      ] 11



      # copy cell 7 to cell 11 using cell 13
      <<<<[->>>>+>>+<<<<<<]
      >>>>>>[-<<<<<<+>>>>>>]

      # while cell 11 != 0
      <<
      [
        set cell 12 to 1
        >[-]+

        set cell 11 to 0
        <[-]
      
      # end 11
      ] 11
      # add cell 12 to cell 7
      >[-<<<<<+>>>>>]

      # increment cell 6
      <<<<<<+
      <
    end
    ] 5
    
  have now dealt with the non exit node
  clear cell 9
  >>>>  
  [-]
  end
  ] 9
  
  while cell 10 != 0 # at an exit
  >
  [
    copy cell 7 to cell 12 using cell 13 (highest)
    <<<[->>>>>+>+<<<<<<]
    >>>>>>[-<<<<<<+>>>>>>]
    
    while cell 12 != 0 (above ground level)
    <
    [
      copy cell 8 to cell 11 using cell 13 (highest)
      <<<<[->>>+>>+<<<<<]
      >>>>>[-<<<<<+>>>>>]
      
      cell 13 is zero
      
      ### subtract 11 from 12 ensuring 12 gte 0
      ### add 12 to 8
      
      while cell 11 != 0
      <<
      [
        copy cell 12 to cell 14 using cell 15
        >[->>+>+<<<]
        >>>[-<<<+>>>]
        
        while cell 14 != 0
        <
        [
          set cell 13 to 1
          <[-]+
          decrement cell 14
          >-
        end
        ] 14
        while cell 13 != 0
        <
        [
          decrement cell 12
          <-
          decrement cell 13
          >-
        end
        ] 13
        
        decrement cell 11
        <<-
      end
      ] 11
      
      >[-<<<<+>>>>]
      add cell 12 to cell 8
    ] 12
    <<
    clear 10
    [-]
  ] 10
  
  
  
  read character into cell 9
  <,
end 
] 9

output cell 8
<.

"""


def execute(filename):
    f = open(filename, "r")
    evaluate(f.read())
    f.close()


def evaluate(code, inp=None, debug=False, execution_limit=0):
    code     = cleanup(list(code))
    bracemap = buildbracemap(code)

    cells, codeptr, cellptr = [0], 0, 0
    inputptr = 0
    execution_count = 0
    outputs = []

    try:
        while codeptr < len(code):
            command = code[codeptr]
            
            if debug:
                print(command, codeptr, cellptr, cells)

            if command == ">":
                cellptr += 1
                if cellptr == len(cells): cells.append(0)

            if command == "<":
                cellptr = 0 if cellptr <= 0 else cellptr - 1

            if command == "+":
                cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

            if command == "-":
                cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

            if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
            if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
            if command == ".": 
                print(cells[cellptr]) # sys.stdout.write(chr(cells[cellptr]))
                outputs += [cells[cellptr]]
            if command == ",": 
                if inputptr >= len(inp):
                        # raise EOFError
                        cells[cellptr] = 0
                else:
                    cells[cellptr] = ord(inp[inputptr])
                    inputptr += 1

            codeptr += 1
            execution_count += 1
            if execution_limit != 0 and execution_count > execution_limit:
                break
    except EOFError:
        pass
    print(execution_count)
    return cells, codeptr, cellptr, outputs


def cleanup(code):
    return list(filter(lambda x: x in '.,[]<>+-', code))


def buildbracemap(code):
    temp_bracestack, bracemap = [], {}

    for position, command in enumerate(code):
        if command == "[": temp_bracestack.append(position)
        if command == "]":
            start = temp_bracestack.pop()
            bracemap[start] = position
            bracemap[position] = start
    return bracemap

def main():

  open('part2.bf', 'w').write(program + '\n')
  inpt = '^=vvv=^^^=^=vv'
  inpt = 'v^^^^^v=v='
  inpt = open('02-lifts.txt').read().strip()
  # cells, codeptr, cellptr, outputs = evaluate(program, inp=inpt, execution_limit=200000, debug=True)
  # cells, codeptr, cellptr, outputs = evaluate(program, inp=inpt, debug=True)
  cells, codeptr, cellptr, outputs = evaluate(program, inp=inpt)
  print(cells, codeptr, cellptr, outputs)

if __name__ == "__main__": main()
    