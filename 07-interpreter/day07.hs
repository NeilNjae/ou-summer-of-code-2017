module Main(main) where

import Text.Parsec hiding (State)
import Text.ParserCombinators.Parsec.Number
import Control.Monad.State.Lazy
-- import Debug.Trace

type Register = Char 
type Location = Int 

data Instruction =   Inc Register
                   | Dec Register
                   | Set Register Int
                   | Cpy Register Register
                   | Jmp Int
                   | Jpz Register Int
                   deriving (Show, Eq)

data Machine = Machine { a :: Int
                       , b :: Int
                       , c :: Int
                       , d :: Int
                       , pc :: Int
                       , instructions :: [Instruction]} 
               deriving (Show, Eq)

-- testInstructions = "set c 0\n\
-- \sto a 1"

testInstructions = "set c 0\n\
\cpy a d\n\
\jpz b 8\n\
\dec b\n\
\cpy d a\n\
\jpz a 4\n\
\inc c\n\
\dec a\n\
\jmp -3\n\
\jmp -7\n\
\cpy a d"

emptyMachine :: Machine
emptyMachine = Machine {a=0, b=0, c=0, d=0, pc=0, instructions=[]} 

main :: IO ()
main = do 
    text <- readFile "07-program.txt" 
    let instructions = successfulParse $ parseIfile text
    part1 instructions
    part2 instructions
    -- let text = testInstructions
    -- let instrs = successfulParse $ parseIfile text
    -- let m0 = emptyMachine {instructions=instrs, a = 7, b = 3}
    -- let mf = snd $ runState runMachine m0
    -- print mf

part1 :: [Instruction] -> IO ()
part1 instrs = 
    do  let m0 = emptyMachine {instructions=instrs, a = 7}
        let mf = snd $ runState runMachine m0
        print (a mf)

part2 :: [Instruction] -> IO ()
part2 instrs = 
    do  let m0 = emptyMachine {instructions=instrs, a = 937}
        let mf = snd $ runState runMachine m0
        print (a mf)


runMachine :: State Machine ()
runMachine = 
    do  m <- get
        if (pc m) >= (length $ instructions m)
            then return ()
            else do executeStep
                    runMachine

executeStep :: State Machine ()
executeStep = 
    do  m <- get
        let i = (instructions m)!!(pc m)
        put (executeInstruction i m)


executeInstruction :: Instruction -> Machine -> Machine
-- executeInstruction i m | trace (show i ++ " " ++ show m) False = undefined
executeInstruction (Inc r) m = m' {pc=pc1}
    where pc1 = (pc m) + 1
          v = readRegister m r
          m' = writeRegister m r (v+1)
executeInstruction (Dec r) m = m' {pc=pc1}
    where pc1 = (pc m) + 1
          v = readRegister m r
          m' = writeRegister m r (v-1)
executeInstruction (Set r v) m = m' {pc=pc1}
    where pc1 = (pc m) + 1
          m' = writeRegister m r v
executeInstruction (Cpy s d) m = m' {pc=pc1}
    where pc1 = (pc m) + 1
          v = readRegister m s
          m' = writeRegister m d v
executeInstruction (Jmp d) m = m {pc=pcj}
    where pcj = (pc m) + d
executeInstruction (Jpz r d) m 
    | v == 0 = m {pc=pcj}
    | otherwise = m {pc=pc1}
    where pc1 = (pc m) + 1
          pcj = (pc m) + d
          v = readRegister m r



readRegister :: Machine -> Register -> Int
readRegister m r = 
     case r of
        'a' -> (a m)
        'b' -> (b m)
        'c' -> (c m)
        'd' -> (d m)

writeRegister :: Machine -> Register -> Int -> Machine
writeRegister m r v =
    case r of 
        'a' -> m {a=v}
        'b' -> m {b=v}
        'c' -> m {c=v}
        'd' -> m {d=v}


instructionFile = instructionLine `sepEndBy` newline 
instructionLine = incL <|> decL <|> setL <|> cpyL <|> jmpL <|> jpzL

incL = Inc <$> (try (string "inc") *> spaces *> register)
decL = Dec <$> (try (string "dec") *> spaces *> register)
setL = Set <$> (try (string "set") *> spaces *> register) <*> (spaces *> location)
cpyL = Cpy <$> (try (string "cpy") *> spaces *> register) <*> (spaces *> register)
jmpL = Jmp <$> (try (string "jmp") *> spaces *> location)
jpzL = Jpz <$> (try (string "jpz") *> spaces *> register) <*> (spaces *> location)

location = int
register = oneOf "abcd"

parseIfile :: String -> Either ParseError [Instruction]
parseIfile input = parse instructionFile "(unknown)" input

parseIline :: String -> Either ParseError Instruction
parseIline input = parse instructionLine "(unknown)" input

successfulParse :: Either ParseError [a] -> [a]
successfulParse (Left _) = []
successfulParse (Right a) = a
