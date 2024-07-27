### TODO

#### Server
* Add seed-setting in advanced options so that generated lyrics are the same. Maybe there isn't a huge application but it would be fun if two people (e.g. me and Hannah) wanted to compete against each other

#### UI
* Go through all the themes and correct any that may be too harsh on the eye
    * Make SN background color a darker shade of purple
    * Make Red BG darker/duller
    * Make 1989 duller, and change button colors (too much contrast; maybe go for a grey or blue)
    * Make Lover inputs darker; too bright
    * Test black text with folklore
* Figure out how to grey out the buttons when they are disabled - they used to be fine but with the theming it goes away
    * Got the greyed out part (made the buttons transparent) but the text stays the same color. Would be nice to change text to grey
* The red IMPORTANT text in the instructions is kind of blinding for certain themes. Same w the green text for total points. See if you can change that based on theme or just use a different color overall that works for all themes
* Possibly consider changing fonts based on theme, but most likely I will just retain the same font for everything
* The success and error message backgrounds are kind of hard to see for some themes. See if you can either adjust the themes, or make changes to the success/error message background colors
* Possibly change the color of the dataframe, but not needed; looks fine as is
* Add a "Created w/ love by jasminex21" thingie somewhere (probably bottom of sidebar) and link to GitHub repo

#### Data
* TTPD appears to be non-explicit
* Add non-album singles to the dataset (album = Non-Album Single) and provide the option of filtering them out
    * This would require restructuring and probably re-writing most of the data-pulling pipeline (it is quite messy now since it's old)
* [LOW PRIORITY] Add data-pulling pipeline to a folder, maybe something like .../data. Is still in R, probably won't change that

#### Testing and General
* Make sure the game works fine. Play it a ton and keep track of any possible mistakes 
* Clean up the app file (convert all global vars to all caps); move non-streamlit functions out, maybe do something about the initializing session states (they're piling up), and the CSS can all go somewhere confined as well 
* Casual docstrings for the functions that are specific to the UI, maybe formal ones for externally created functions
* An idea I'm casually putting out - tayLyrics could be the first of many sub-apps contained within one large repository of lyrics games. I have the Python lyrics scraper now as well (though most likely it'll need correcting and to be properly reorganized), so I can essentially create this app for any artist I want. I'm imagining a general website, and then theres a dropdown of artists whose lyrics games are available. Each game should be custom-made and not dull with a default theme and name. Ideally I'd also want some way of letting people suggest what artist should be added next to the repository, via a poll or contact or whatever other way there is. I am not planning on designing the broader repository website as physically as I am doing w the individual apps. I'm thinking of using maybe Quarto? Not sure how it works but I'm willing to check it out. Think it's R tho.