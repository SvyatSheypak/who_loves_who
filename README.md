# About
A Python script to solve a 'Who loves who' task - it obtains information from sentences like `Jim likes Larry and Jean, but hates Kim.` and then tells who loves/likes/who. It uses graph with names as verices and directed edges of three labels: `loves`, `likes` and `hates`. In order to be able to answer to questions like "Who likes Jim" in constant time a reverse graph is also maintained. It is allowed to person to feel several feelings to a single person, but it is not allowed to delete edges from graphs and forget peoples' attitudes.

# Requirements
Scripts requires only Python3, as it imports only standart modules such as `argparse` and `sys`.

# Run
Basic run
```
python3 wlw.py
```

# Options
`-f, --file` 
        Read info from file, for example from [input.txt](https://github.com/SvyatSheypak/who_loves_who/blob/master/input.txt)

`-l, --line`
        Read info from promted sentence

`-d, --description`
        Get list of all people program knows something about

`-q, --question`
        Ask a program about a certain person in form `Who likes X`, `Whom loves X`, `X hates` or simply `X` 

`-h, --help`
        Display this help and exit

`-e, --exit`
        Exit program
        
# Usage examples
```
python3 wlw.py -f input.txt
-d
All Subjects: Jim, Bob, Jean, Kim, Larry
All Objects: Larry, Jean, Kim, Bob, Jim, Martin, Karl
-q Kim hates
Kim hates Jim
-q Who likes Kim
Kim is liked by Bob
-q Whom Bob likes
Bob likes Larry and Kim
-q Larry
Larry loves Martin and hates Karl and Jean. Larry is liked by Jim, Bob and Kim.
-l Alice loves Sean
-q Sean
Sean is loved by Alice.
-q Mr.Bean
No info on Mr.Bean.
```
