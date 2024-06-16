### IR:
    > Make routine an official class, instead of an abstract `collections.abc.Sequence`. It will make typing easier, and modifications more consistent.

    > Add a possibility to save/load IR directly to/from a file without compiling to BF.

    > Add a de-compiler functionality from BF to IR (needed for `ASSIGN` instruction, since I am too lazy to manually rewrite 255 algorithms)

### Memoptix:
    > Make exceptions more detailed and persistent

    > Make scope detection more intuitive. Make sure `Free` is applied when owner's value is zero, if there's a chance it's no -> warn or raise an exception. Automatically add `Free` if it's known for a fact that value is zero (for example after a loop). Add an intuitive constraint `GlobalUnit` to make globally scoped units explicit, and raise an error if a unit is not global and is not freed. 

    > Abstract the resolver away from owners/metainfo context. 

    > Add an exception when second freeing

    > Add an exception when freeing the unknown owner

### XBF:
    > Optimize instructions. To ease the task add `multidispatch`

    > Make freeing and allocating buffer units easier.

    > Try to reduce code repetition.

    > Add a way to save or load commands from a text file with custom syntax.

    > Instructions to implement:
        > ✅ INPUT
        > INPUT_INT 
        > ✅ DISPLAY 
        > DISPLAY_INT
        > ✅ INIT_UNIT
        > ✅ INIT_ARRAY
        > ✅ ASSIGN
        > ARRAY_READ
        > ARRAY_WRITE
        > ARRAY_MAP
        > ✅ CLEAR
        > ✅ COPY
        > ✅ ADD
        > ✅ SUB
        > ✅ MUL
        > ✅ DIVMOD
        > ✅ DIV
        > ✅ MOD
        > ✅ CALLZ
        > CALLGE
        > CALLGT
        > CALLLE
        > CALLLT
        > ✅ NOT
        > XOR
        > AND
        > OR
        > ✅ LSHIFT
        > ✅ RSHIFT
        > ✅ MIGRATE
        > ADDC
        > SUBC
        > MULC
        > DIVC
