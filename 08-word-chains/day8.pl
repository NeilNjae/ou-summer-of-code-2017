#!/usr/bin/env swipl

:- initialization(main).
:- dynamic neighbours/2.

build_rooms:-
    get_rooms(Rooms),
    build_neighbours(Rooms).

get_rooms(Rooms):-
    setup_call_cleanup(
        open('08-rooms.txt', read, In),
        read_data(In, Rooms),
        close(In)
    ).


read_data(In, L):-
    read_line_to_codes(In, H),
    (   H == end_of_file
    ->  L = []
    ;   L = [H|T],
        read_data(In,T)
    ).


alphabet_codes(A):-
    string_codes('abcdefghijklmnopqrstuvwxyz', A).
    
adjacent(Word, Adjacents):-
    length(Word, N),
    adjacent(N, Word, Adjacents).

adjacent(N, Word, SAdjacents):-
    (N = 0 -> Adjacents = []
    ;
    swap_char(N, Word, NWords),
    N1 is N - 1,
    adjacent(N1, Word, RAdjacents),
    append(NWords, RAdjacents, Adjacents)),
    list_to_ord_set(Adjacents, SAdjacents).

swap_char(N, Word, Swapped):-
    alphabet_codes(As),
    setof(W, 
        A^(member(A, As),
            nth1(N, Word, L, Rest),
            L \= A,
            nth1(N, W, A, Rest)), 
        Swapped).

build_neighbours(Words):-
    build_neighbours(Words, Words).

build_neighbours([], _).
build_neighbours([Word|Words], Dictionary):-
    adjacent(Word, Adjacents),
    intersection(Adjacents, Dictionary, Neighbours),
    string_codes(SWord, Word),
    maplist(string_codes, SNeighbours, Neighbours),
    assertz((neighbours(SWord, SNeighbours):-!)), % Need the cut to keep lookup deterministic in this dynamic predicate
    build_neighbours(Words, Dictionary).




extend([W|Chain], Closed, Extended):-
    neighbours(W, Ns),
    ord_subtract(Ns, Closed, Successors),
    extend_chain(Successors, [W|Chain], Extended).

extend_chain([], _, []).
extend_chain([N|Ns], Chain, [[N|Chain]|Extended]):-
    extend_chain(Ns, Chain, Extended).


distance([], _, 0).
distance([C|Cs], [O|Os], N):-
    (   C == O
    ->  distance(Cs, Os, N)
    ;   distance(Cs, Os, N1),
        N is N1 + 1).

estimated_costed([W|C], Goal, N-[W|C]):-
    length([W|C], N1),
    string_codes(W, Cs),
    distance(Cs, Goal, N2),
    N is N1 + N2.

estimated_costed_all([], _, []).
estimated_costed_all([C|Cs], Goal, [A|As]):-
    estimated_costed(C, Goal, A),
    estimated_costed_all(Cs, Goal, As).


astar(Start, SGoal, Path):-
    string_codes(SGoal, Goal),
    estimated_costed([Start], Goal, Costed),
    astar([Costed], SGoal, Goal, [], Path).

astar([], _, _, []).
astar([_-Current|Agenda0], SGoal, Goal, Closed0, FoundPath):-
    %% write_ln([N-Current, SGoal, Goal]),
    (   Current = [W|_],
        W == SGoal
    ->  FoundPath = Current
    ;   [Word|_] = Current,
        ord_add_element(Closed0, Word, Closed),
        extend(Current, Closed, Extended),
        estimated_costed_all(Extended, Goal, ExtraAgenda),
        append(ExtraAgenda, Agenda0, Agenda1),
        keysort(Agenda1, Agenda),
        astar(Agenda, SGoal, Goal, Closed, FoundPath)
    ).


reachable(Word, Steps, N):-
    reachable(Steps, [Word], [Word], Reachable),
    length(Reachable, ReachableN),
    N is ReachableN - 1.


reachable(N, Found0, Boundary0, Reachable):-
    (   N == 0
    ->  Reachable = Found0
    ;   maplist(neighbours, Boundary0, FoundL),
        flatten(FoundL, Found1),
        list_to_ord_set(Found1, Boundary1),
        ord_subtract(Boundary1, Found0, Boundary),
        ord_union(Found0, Boundary, Found),
        N1 is N - 1,
        reachable(N1, Found, Boundary, Reachable)
    ).  

main(_Argv):- 
    time(build_rooms),
    time(astar("coax", "stay", P)),
    length(P, Part1),
    time(reachable("coax", 10, Part2)),

    writef('Part 1: %w steps from coax to stay\n', [Part1]),
    writef('Part 2: %w rooms reacable in 10 steps from coax\n', [Part2]).
