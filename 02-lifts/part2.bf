>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>+++++++++++++++++++++++++++++++++>++++++++++++++++++++++++


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


