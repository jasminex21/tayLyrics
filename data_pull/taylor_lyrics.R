library(spotifyr)
library(tidyverse)
library(taylor)

# Setting up Spotify client ID and client secret
# Sys.setenv(SPOTIFY_CLIENT_ID = '7...')
# Sys.setenv(SPOTIFY_CLIENT_SECRET = '9...')
access_token <- get_spotify_access_token()

# Creating a tibble/df containing Taylor's Spotify data
taylor = get_artist_audio_features('taylor swift') %>% 
  as_tibble()

# Selecting relevant information from tibble
taylor$album_release_date = ymd(taylor$album_release_date)
taylor = taylor %>%
  select(track_name, 
         danceability, 
         energy, 
         loudness, 
         speechiness, 
         acousticness, 
         instrumentalness, 
         liveness, 
         valence, 
         tempo, 
         time_signature, 
         duration_ms, 
         explicit, 
         key_name, 
         mode_name, 
         key_mode, 
         album_name, 
         album_release_date, 
         track_id, 
         album_id) %>%
  arrange(album_release_date) %>%
  filter(album_name %in% c("Midnights (3am Edition)",
                           "Taylor Swift", 
                           "Fearless (Taylor's Version)",
                           "Speak Now (Taylor's Version)",
                           "Red (Taylor's Version)", 
                           "folklore (deluxe version)", 
                           "evermore (deluxe version)",
                           "reputation", 
                           "Lover", 
                           "1989 (Taylor's Version)", 
                           "THE TORTURED POETS DEPARTMENT: THE ANTHOLOGY")) %>%
  filter(!duplicated(track_name))

# Changing the deluxe edition titles to the original title (aesthetic purposes)
taylor$album_name[taylor$album_name == "Midnights (3am Edition)"] = "Midnights"
taylor$album_name[taylor$album_name == "folklore (deluxe version)"] = "folklore"
taylor$album_name[taylor$album_name == "evermore (deluxe version)"] = "evermore"
taylor$album_name[taylor$album_name == "THE TORTURED POETS DEPARTMENT: THE ANTHOLOGY"] = "THE TORTURED POETS DEPARTMENT" 

# Removing remixes and demos
taylor = taylor %>% filter(!str_detect(taylor$track_name, "Acoustic"), 
                           !str_detect(taylor$track_name, "Voice Memo"), 
                           !str_detect(taylor$track_name, "Demo"), 
                           !str_detect(taylor$track_name, "Piano"),
                           !str_detect(taylor$track_name, "POP"), 
                           !str_detect(taylor$track_name, "Pop"))

taylor$track_name[taylor$track_name == "Teardrops On My Guitar - Radio Single Remix"] = "Teardrops On My Guitar"

# Making changes to track names in both dataframes such that the track names match perfectly
taylor_all_songs$track_name = gsub("\\[", "(", taylor_all_songs$track_name)
taylor_all_songs$track_name = gsub("\\]", ")", taylor_all_songs$track_name)
taylor$track_name = gsub("<U\\+2019>", "'", taylor$track_name)
taylor$track_name = gsub("<U\\+2018>", "'", taylor$track_name)
taylor$track_name = gsub('\"', '', taylor$track_name)
taylor_all_songs$track_name = gsub('\"', '', taylor_all_songs$track_name)
taylor$track_name = gsub("’", "'", taylor$track_name)
taylor$track_name = gsub("‘", "'", taylor$track_name)
taylor$track_name = str_trim(gsub("\\s\\(feat[^()]*\\)", "", taylor$track_name))
taylor$track_name = str_trim(gsub("- bonus track", "", taylor$track_name))

taylor$track_name[taylor$track_name == "A Place in this World"] = "A Place In This World" 
taylor$track_name[taylor$track_name == "Tied Together with a Smile"] = "Tied Together With A Smile"
taylor$track_name[taylor$track_name == "I Knew You Were Trouble."] = "I Knew You Were Trouble"
taylor$track_name[taylor$track_name == "Superstar (Taylor's Version)"] = "SuperStar (Taylor's Version)" 
taylor$track_name[taylor$track_name == "When Emma Falls in Love (Taylor's Version) (From The Vault)"] = "When Emma Falls In Love (Taylor's Version) (From The Vault)"
taylor$track_name[taylor$track_name == "I Look in People's Windows"] = "I Look In People's Windows"
taylor$track_name[taylor$track_name == "Chloe or Sam or Sophia or Marcus"] = "Chloe Or Sam Or Sophia Or Marcus"
taylor$track_name[taylor$track_name == "I Can Do It With a Broken Heart"] = "I Can Do It With A Broken Heart"
taylor$track_name[taylor$track_name == "Who's Afraid of Little Old Me?"] = "Who's Afraid Of Little Old Me?"

taylor_all_songs$album_name[taylor_all_songs$track_name == "I'm Only Me When I'm With You"] = "Taylor Swift"

# Filtering out songs from taylor_all_songs that are *not* included in taylor
taylor_all_songs = taylor_all_songs %>% 
  filter(taylor_all_songs$track_name %in% taylor$track_name)

# Unnesting taylor_all_songs to create a "tall" dataframe where
# each line from a song corresponds to a row in the dataframe
allLyrics = taylor_all_songs %>% 
  select("lyrics", 
         "track_name", 
         "album_name") %>%
  unnest(lyrics) %>%
  select(-(element_artist))

write.csv(allLyrics, "TAYLOR_LYRICS_JUN2024.csv")