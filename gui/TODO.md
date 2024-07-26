### TODO

#### Server
* Leaderboard - if all albums are selected, have the option for leaderboard in the Past Game Summary area. For simplicity you can do this w a CSV file, otherwise databases
    * As for actually integrating the Leaderboard into the UI, I'm thinking of separating the post-game container into 2 tabs; the past game stats tab and a leaderboard tab. The two tabs should only show after each game is ended, not when there is a game going on. The container should only contain the lyrics and the game interface during a game. In the leaderboard tab, the user should have the option of putting their scores into the leaderboard (database) under the (tentative) conditions that they 1) had all albums enabled, and 2) played at least x rounds (I'm thinking 20?). The leaderboard should be based on points out of total possible. Will have the user's name, date(time), and points of total possible.
    * REMEMBER to have different leaderboards for survival vs casual mode!!!
         * Regarding the above point - it might be better to only have a leaderboard for survival mode. Casual mode is too unrestricted. Would have to have a separate leaderboard for easy, medium, and hard modes. Once the user ends the game and the tab shows up, it should default to the leaderboard specific to the game settings they just played, but there will also be a dropdown so they can view other leaderboards. If in casual mode, make sure there is an info message or something saying leaderboard is only for survival mode, but of course they can view the leaderboards still. 
* Add seed-setting in advanced options so that generated lyrics are the same. Maybe there isn't a huge application but it would be fun if two people (e.g. me and Hannah) wanted to compete against each other
* Check that the Mary's Song and I Can Fix Him issues have been resolved

#### UI
* Might be nice to have the Hint and Give Up buttons disappear after the user gives up or answers correctly. Key word might; play around w it
* Go through all the themes and correct any that may be too harsh on the eye
    * Make SN background color a darker shade of purple
    * Make Red BG darker/duller
    * Make 1989 duller, and change button colors (too much contrast; maybe go for a grey or blue)
    * Make Lover inputs darker; too bright
    * Test black text with folklore
* Figure out how to grey out the buttons when they are disabled - they used to be fine but with the theming it goes away
    * Got the greyed out part (made the buttons transparent) but the text stays the same color. Would be nice to change text to grey
* Make sure the error/success/etc messages show up fine w each theme
* The red IMPORTANT text in the instructions is kind of blinding for certain themes. Same w the green text for total points. See if you can change that based on theme or just use a different color overall that works for all themes
* Possibly consider changing fonts based on theme, but most likely I will just retain the same font for everything
* More detailed instructions; talk abt capitalization and minor spelling errors
* Consider putting the theme settings elsewhere, not in the Instructions expander but not in the form either bc then it won't go through until the button is clicked I believe
* Put Giveup button next to Hint button; not below
* Create long name to short name mapping for albums so the names in the multiselect and in the album stats are simplified
* Add hints used as a general stat

#### Data
* TTPD appears to be non-explicit
* Add non-album singles to the dataset (album = Non-Album Single) and provide the option of filtering them out
* [LOW PRIORITY] Add data-pulling pipeline to a folder, maybe something like .../data. Is still in R, probably won't change that

#### Testing and General
* Make sure the game works fine. Play it a ton and keep track of any possible mistakes 
* Clean up the app file (convert all global vars to all caps); move non-streamlit functions out, maybe do something about the initializing session states (they're piling up), and the CSS can all go somewhere confined as well 
* Casual docstrings for the functions that are specific to the UI, maybe formal ones for externally created functions
* An idea I'm casually putting out - tayLyrics could be the first of many sub-apps contained within one large repository of lyrics games. I have the Python lyrics scraper now as well (though most likely it'll need correcting and to be properly reorganized), so I can essentially create this app for any artist I want. I'm imagining a general website, and then theres a dropdown of artists whose lyrics games are available. Each game should be custom-made and not dull with a default theme and name. Ideally I'd also want some way of letting people suggest what artist should be added next to the repository, via a poll or contact or whatever other way there is. I am not planning on designing the broader repository website as physically as I am doing w the individual apps. I'm thinking of using maybe Quarto? Not sure how it works but I'm willing to check it out. Think it's R tho.