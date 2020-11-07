# fish-i

An Python 3 interpreter for the [><>](https://esolangs.org/wiki/Fish) programming language.

The interpreter differs from the reference implementation on the following points:

 - Division

   If both operands are integer and the result is exact, the result will be integer, [Fraction](https://docs.python.org/3/library/fractions.html) otherwise. Fractions will be displayed as floats. This allows for arbitrary precision arithmetic without removing floating point division.

 - Stack Operations

   Stack operations have been written to not error whenever possible

   - `$` with zero or one items on the stack will have no effect
   - `:` with zero items on the stack will have no effect
   - `@`

     with zero or one items on the stack will have no effect

     with two items on the stack will act as `$`

   - `[`

     with zero items on the stack will error

     with less than `n` items on the stack will pull the entire stack

   - `]` no change

   - `l` no change

   - `r` no change

   - `{`

     with zero or one items on the stack will have no effect

     with two items on the stack will act as `$`

     with three items on the stack will act as `@@`

   - `}`

     with zero or one items on the stack will have no effect

     with two items on the stack with act as `$`

     with three items on the stack will act as `@`

   - `~` with zero items on the stack will have no effect
