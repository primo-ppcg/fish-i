# fish-i

A Python 3 interpreter for the [><>](https://esolangs.org/wiki/Fish) programming language.

The interpreter differs from the reference implementation on the following points:

 - Division

   If both operands are integer and the result is exact, the result will be integer, [Fraction](https://docs.python.org/3/library/fractions.html) otherwise. Fractions will be displayed as floats. This allows for arbitrary precision arithmetic without removing floating point division.

 - Stack Operations

   - `{` and `}`

     With zero items on the stack these will have no effect, rather than crashing.
