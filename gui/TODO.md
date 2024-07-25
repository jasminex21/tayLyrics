### TODO

#### Mistakes
* TTPD appears to be non-explicit

#### Theming
* Go through all the themes and correct any that may be too harsh on the eye
    * Make SN background color a darker shade of purple
    * Make Red BG darker/duller
    * Make 1989 duller, and change button colors (too much contrast; maybe go for a grey or blue)
    * Make Lover inputs darker; too bright
    * Test black text with folklore
* Figure out how to grey out the buttons when they are disabled - they used to be fine but with the theming it goes away
    * Got the greyed out part (made the buttons transparent) but the text stays the same color. Would be nice to change text to grey
* See if you can change the background color and text color of the message that displays when you hover over buttons
    * I found out that this seems to only be possible by changing what's actually in the config.toml file? If it cannot be changed through CSS, find a good neutral color combo that works for all themes
* Make sure the error/success/etc messages show up fine w each theme
* The red IMPORTANT text in the instructions is kind of blinding for certain themes. Same w the green text for total points. See if you can change that based on theme or just use a different color overall that works for all themes
* Possibly consider changing fonts based on theme, but most likely I will just retain the same font for everything

#### Major
* Leaderboard - if all albums are selected, have the option for leaderboard in the Past Game Summary area. For simplicity you can do this w a CSV file, otherwise databases
* Add non-album singles to the dataset (album = Non-Album Single) and provide the option of filtering them out
* Add seed-setting in advanced options so that generated lyrics are the same. Maybe there isn't a huge application but it would be fun if two people (e.g. me and Hannah) wanted to compete against each other
* Figure out hosting
* Would be fun to have more detailed stats on how well your game went by album - like a counter dict that counts up your accuracy by album

#### Minor

#### Testing and General
* Make sure the game works fine. Play it a ton and keep track of any possible mistakes 
* Clean up the app file (convert all global vars to all caps); move non-streamlit functions out, maybe do something about the initializing session states (they're piling up), and the CSS can all go somewhere confined as well 