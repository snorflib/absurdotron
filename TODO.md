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

    > Rename migrate to move

    > Make addition and other similar instructions accept a list of arguments instead of a list

    > Make display accept plenty of literal or byte arguments and print them efficiently

    > Make input accept multiple bytes to store data to.

    > Instructions to implement:
        > ✅ INPUT   # INP
        > ✅ DISPLAY # DSP
        > ✅ CLEAR # CLR
        > INC
        > DEC
        > ETL
        > EXL
        > COMPI
        > CODEI
        > COMMI

        > ✅ INIT_UNIT
        > ✅ INIT_ARRAY
        > ARRAY_READ
        > ARRAY_WRITE
        > ✅ COPY
        > ✅ ADD
        > ✅ SUB
        > ✅ MUL
        > ✅ DIVMOD
        > ✅ CALLZ
        > ✅ NOT
        > ✅ ASSIGN
        > XOR
        > AND
        > OR
        > ✅ MIGRATE
