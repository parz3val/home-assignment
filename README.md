# Home Assignment

## How to run

1. `clone $repo`
2. `cd $repo`
3. `pytest`

## Improvements

1. Due to amount of time and limited knowledge about requirements, I implemented a generic generator for to complete the requirements. But, having more info about requirements and coding guidelines would improve the code quality further.

2. I've captured requirements into simple unit tests. They are enough for now, but doing something like hypothesis testing would provide better confidence over the solution.

3. To avoid anything other than standard library, I opted to use generators, but using asyncio would be much better if it this was in a real project.

4. I've used structs to model the data but used a makeshift orm to map the commands to statements, could be done with structs if used with pydantic, and code would've been much readable as well.

5. Comments. I would've written more comments if I had more time to spare and work on this.
