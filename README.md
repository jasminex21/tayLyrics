# tayLyrics

#### How well do you know Taylor Swift's lyrics? :D

This is still a work in progress, but for entertainment purposes, [here](https://jasminex21.shinyapps.io/tayLyrics/) is the link to the game. 

***

#### Here is the general layout of the app: 

![image](https://github.com/jasminex21/tayLyrics/assets/109494334/01621c73-7a5e-408a-be70-5b0d38dd8e9d)
![image](https://github.com/jasminex21/tayLyrics/assets/109494334/44d053e0-99c0-445e-9ca7-69aa110b64fd)


Instructions are provided on the left sidebar, as needed. 

***

#### Points breakdown:
*Subject to change*

Additions: 
- Correct guess in easy mode: +1pt
- Correct guess in medium mode: +6pts
- Correct guess in hard mode: +8pts

Deductions: 
- Hint: -1pt per hint
- Incorrect guess in any mode: -2pts
- Giving up: -3pts (change this to -2pts)

***

#### TODO: 
- **To address first**:
  - Get the hints to show up on top of each other instead of Hint 2 obscuring Hint 1
  - When an answer is wrong when a previous round's answer was correct, the output jumps a little? Not sure how to fix it but it would be really nice to
 - Allow users to choose which hint they want - this would also fix the issue where the hints obscure each other; I can pretty easily separate them by doing this
 - Maybe limit the number of guesses per round? Or at least provide the option of doing so?
- Fix the points system - it's a little too arbitrary right now. Penalizes too much as well.
  - Points breakdown in the instructions panel 
- Possibly filter out lyrics that are < 5 words in length for medium and hard mode, and also the lyrics that are simply the same word repeated over and over
  - Instead of filtering out automatically, it could be nice to allow the user to choose a minimum number of words in the generated line(s) - some people may not appreaciate the lyric being "Ooh-ah"
- Add more detailed statistics:
  - Pie charts showing album distribution of correct and incorrect (gave up) responses
- Saving user data (your highest %, longest streak, etc.)
  - Streaks in general would be cool - this should be easy to implement. Use a counter. 
- Possibly add non-album singles e.g. Only the Young, Christmas Tree Farm (but provide users with the option of removing them)
- (SHOULD NOW BE FIXED) I could have seen wrong but there might be an issue with the previous/next lyric hint where the lyric came from an entirely different song? Maybe I imagined this.
- Add option to set seed for the randomizer - but might need to have an info button for it for an explanation of what it does 

