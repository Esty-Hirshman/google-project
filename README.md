# google-project
### Automatic sentence completion

In order to make the user experience of the Google search engine better,
the development team decided to allow completion
Of sentences from articles, documentation and information files on various technological topics

The purpose of the completion action is to make it easier for the user to find the most appropriate sentence.

All information is stored in the suffix tree in order to retrieve it when searching in the fastest time.

In the case of several matches to the typed text, we will set a score (score) for each match:
1. The base score is double the number of characters typed and a match was found for them.
2. Replacement of a lowering character according to the following details: first character 5 points, second character 4, third character 3, fourth character 2, fifth character
And onwards 1.
3. Deleting a character or adding a character receives a reduction of 2 points except for the first 4 characters (first character 10 points, character
Monday 8, third note 6, fourth note 4

The program works in two stages:
1. First stage (offline) is a stage in which the system reads the text files (from a predetermined place)
And prepares them for the service phase (serving)
2. Second stage (online) is a stage where the system waits for input.
* As soon as the user types characters and presses Enter the system displays the five
The best completions (in case of a tie on the system sorts the strings with the same score by alphabet).
* After viewing the completions, the system allows the user to continue typing from where he left off.
* If the user types "#" it means that the user has finished typing for this sentence and returns to the initial state
If no results are found a "not found" message will be displayed

### run the program 
download theproject and in terminal type:
```
main.py
```

### Watch the program run
https://youtu.be/uQibOftVv5k
