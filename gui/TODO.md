### TODO

#### Server
* Add seed-setting in advanced options so that generated lyrics are the same. Maybe there isn't a huge application but it would be fun if two people (e.g. me and Hannah) wanted to compete against each other

#### UI
* The success and error message backgrounds are kind of hard to see for some themes. See if you can either adjust the themes, or make changes to the success/error message background colors

#### Data
* TTPD appears to be non-explicit
* Add non-album singles to the dataset (album = Non-Album Single) and provide the option of filtering them out
    * This would require restructuring and probably re-writing most of the data-pulling pipeline (it is quite messy now since it's old)

#### Testing and General
* Make sure the game works fine. Play it a ton and keep track of any possible mistakes 
* Clean up the app file (convert all global vars to all caps); move non-streamlit functions out, maybe do something about the initializing session states (they're piling up), and the CSS can all go somewhere confined as well 
* An idea I'm casually putting out - tayLyrics could be the first of many sub-apps contained within one large repository of lyrics games. I have the Python lyrics scraper now as well (though most likely it'll need correcting and to be properly reorganized), so I can essentially create this app for any artist I want. I'm imagining a general website, and then theres a dropdown of artists whose lyrics games are available. Each game should be custom-made and not dull with a default theme and name. Ideally I'd also want some way of letting people suggest what artist should be added next to the repository, via a poll or contact or whatever other way there is. I am not planning on designing the broader repository website as physically as I am doing w the individual apps. I'm thinking of using maybe Quarto? Not sure how it works but I'm willing to check it out. Think it's R tho.