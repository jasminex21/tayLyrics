### TODO

#### Server
* [PRIORITY] Add a button/option somewhere (less obvious) to download the leaderboard DATABASE - I don't quite know how else I can access the DB that the deployed app is using, and if I update the app, it'll erase the leaderboard unless I have it locally and push it to the repo also. 
* Add seed-setting in advanced options so that generated lyrics are the same. Maybe there isn't a huge application but it would be fun if two people (e.g. me and Hannah) wanted to compete against each other
* One consideration - currently the Leaderboards rank players by the number of rounds they play first, and then by the % of points they got out of the points possible. Both of these should maybe be closer to equally-weighted in the ranking consideration. Maybe combine them in some way. Keep as is for now for simplcity tho.

#### UI


#### Data
* TTPD appears to be non-explicit
* Add non-album singles to the dataset (album = Non-Album Single) and provide the option of filtering them out
    * This would require restructuring and probably re-writing most of the data-pulling pipeline (it is quite messy now since it's old)

#### Testing and General
* An idea I'm casually putting out - tayLyrics could be the first of many sub-apps contained within one large repository of lyrics games. I have the Python lyrics scraper now as well (though most likely it'll need correcting and to be properly reorganized), so I can essentially create this app for any artist I want. I'm imagining a general website, and then theres a dropdown of artists whose lyrics games are available. Each game should be custom-made and not dull with a default theme and name. Ideally I'd also want some way of letting people suggest what artist should be added next to the repository, via a poll or contact or whatever other way there is. I am not planning on designing the broader repository website as physically as I am doing w the individual apps. I'm thinking of using maybe Quarto? Not sure how it works but I'm willing to check it out. Think it's R tho.
* I can implement a bot (my naive bayes model) and see what happens? Like here's how you match up with a bot. Just an idea tho, maybe more so something I do for fun rather than something I actually implement into the app.