### TODO

#### Mistakes
* Next round button disappears when theme is changed mid-round
    * Presumably the solution would be to use a session state 
* Takes away lives even for hints somehow only after you've answered incorrectly before
* TTPD appears to be non-explicit

#### Theming
* Go through all the themes and correct any that may be too harsh on the eye
* Figure out how to grey out the buttons when they are disabled - they used to be fine but with the theming it goes away
* See if you can change the background color and text color of the message that displays when you hover over buttons
* Make sure the error/success/etc messages show up fine w each theme
* The red IMPORTANT text in the instructions is kind of blinding for certain themes. Same w the green text for total points. See if you can change that based on theme or just use a different color overall that works for all themes
* Possibly consider changing fonts based on theme, but most likely I will just retain the same font for everything

#### Major
* Leaderboard - if all albums are selected, have the option for leaderboard in the Past Game Summary area. For simplicity you can do this w a CSV file, otherwise databases
* Add non-album singles to the dataset (album = Non-Album Single) and provide the option of filtering them out
* Figure out hosting

#### Minor
* Hover message for End Current Game button
* Fearless theme is very ugly

#### Testing and General
* Make sure the game works fine. Play it a ton and keep track of any possible mistakes 
* Clean up the app file; move non-streamlit functions out, maybe do something about the initializing session states (they're piling up), and the CSS can all go somewhere confined as well