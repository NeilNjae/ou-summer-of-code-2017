| Instruction | Description |
|:------------|:------------|
| `inc r`     | increment contents of register `r` |
| `dec r`     | decrement contents of register `r` |
| `set r i`   | set contents of register `r` to literal value `i` |
| `cpy r s`   | set contents of register `r` into register `s` | 
| `sto r m`   | store contents of register `r` into memory location `m` |
| `ld r m`    | load contents of memory location `m` into register `r` |
| `jmp i`     | jump to instruction `i` places forward |
| `jpz r i`   | jump to instruction `i` places forward if<br>register `r` contains zero, otherwise continue to next instruction |

