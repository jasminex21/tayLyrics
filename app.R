library(shiny)
library(tidyverse)
library(stringr)
library(stringdist)
library(shinyjs)
library(shinyWidgets)
library(emo)

jscode <- '
$(function() {
  var $els = $("[data-proxy-click]");
  $.each(
    $els,
    function(idx, el) {
      var $el = $(el);
      var $proxy = $("#" + $el.data("proxyClick"));
      $el.keydown(function (e) {
        if (e.keyCode == 13) {
          $proxy.click();
        }
      });
    }
  );
});
'

allLyrics = read_csv("allTaylorLyrics.csv")
allLyrics$track_name = str_trim(gsub("\\(.*\\)", "", allLyrics$track_name))

ui = fluidPage(titlePanel(title = div(strong("How well do you know Taylor Swift's lyrics?"), 
                                      style = "color: white;font-weight:800;"), 
                          windowTitle = "tayLyrics"),
               useShinyjs(),
               includeCSS("www/styles.css"), 
               tags$head(tags$script(HTML(jscode))),
               setBackgroundImage(src = "enchanted1dulled.jpg"),
               br(),
               sidebarLayout(
                 sidebarPanel(
                   h3(strong(paste0("Welcome to ", emo::ji("sparkles"), 
                                    "tayLyrics", emo::ji("sparkles")))),
                   p("Lyrics range from debut to ", strong(em("Midnights"))),
                   p("Ignore anything in paretheses, e.g. ", em("don't"), " use (Taylor's Version) or (10 Minute Version) in your answers. Don't worry about capitalization and minor spelling errors!"),
                   # div(p('Click the purple button below to generate a random lyric (or set of lyrics) from Taylor Swift\'s discography, ranging from her self-titled debut album to her tenth studio album, ', strong(em("Midnights")), "."),
                   # p("Capitalisation does not matter, and minor spelling mistakes/punctuation differences are ignored. Do not include anything in parentheses, e.g. (Taylor's Version) or (10 Minute Version)."), style = "font-size: 16px;"),
                   hr(), 
                   h4(strong("Generate your random lyric")),
                   selectInput("mode", 
                               label = "Select game mode", 
                               choices = c("Easy mode (an entire section; # of lines varies)" = 1, 
                                           "Medium mode (2 lines)" = 2, 
                                           "Hard mode (1 line)" = 3), 
                               selected = 1), 
                   actionButton("button", 
                                label = "Generate!"), 
                   hr(), 
                   # h4(strong("Directions:")), 
                   # div(p(strong("Modes:")), 
                   # tags$ol(
                   #   tags$li("Easy mode: generates an entire section of a track, e.g., the bridge, or the chorus"), 
                   #   tags$li("Medium mode: generates two lines from a track, from the same section"), 
                   #   tags$li("Hard mode: generates a single line from a track")
                   # ), 
                   # p(strong("Submitting, Hints and Giving Up:")),
                   # tags$ul(
                   #   tags$li('If you have a guess, press the green ', 
                   #           tags$span(style = "color: green", strong('"Submit"')), 
                   #           "button"),
                   #   tags$li('If the correct guess is at the tip of your tongue and you just need a little nudge, the orange ', tags$span(style = "color: orange", strong('"Hint"')), "button will give you the album the track is from"), 
                   #   tags$li('If you have absolutely no clue what the answer is, press the red ', 
                   #           tags$span(style = "color: red", strong('"Give Up"')), "button to reveal the answer and start a new round")
                   # ),
                   p(strong("Points:")), 
                   tags$ul(
                     tags$li("Correct guess in easy mode = +3 points"), 
                     tags$li("Correct guess in medium mode = +8 points"), 
                     tags$li("Correct guess in hard mode = +10 points"),
                     tags$li("Incorrect guess in any mode = -2 points"),
                     tags$li("Hint = -1 point"), 
                     tags$li("Give up = -3 points")
                   )
                   
                 ), 
                 mainPanel(width = 7, 
                           br(),
                           div(h3(strong("What song is the following (set of) lyrics from?")), 
                               style = "color: white;"),
                           br(),
                           wellPanel(htmlOutput("randGenerated")), 
                           hr(), 
                           # here
                           # textInput("guess",
                           #           label = "Enter your guess",
                           #           placeholder = "e.g. Back to December, or Shake it Off"), 
                           # actionButton("submit",
                           #              label = "Submit"),
                           # actionButton("hintButton",
                           #              label = "Hint"),
                           # actionButton("giveUpButton",
                           #              label = "Give up"),
                           # br(), 
                           # br(),
                           # htmlOutput("guessFeedback"),
                           # htmlOutput("printHint"), 
                           # htmlOutput("printAnswer"), 
                           # hr(),
                           # wellPanel(h4(strong("Your Stats")),
                           #           div(textOutput("totalRounds"),
                           #               textOutput("totalCorrect"),
                           #               textOutput("pointsProp"),
                           #               span(style = "color: #079B7B", textOutput("totalPoints")),
                           #               style = "font-weight: bold"))
                           fluidRow(
                             column(6,
                                    tagAppendAttributes(textInput("guess",
                                              label = div("Enter your guess", 
                                                          style = "color: white;"),
                                              placeholder = "e.g. Back to December, or Shake it Off"), 
                                              `data-proxy-click` = "submit"),
                                    actionButton("submit",
                                                 label = "Submit"),
                                    actionButton("hintButton",
                                                 label = "Hint"),
                                    actionButton("giveUpButton",
                                                 label = "Give up"),
                                    br(),
                                    br(),
                                    htmlOutput("guessFeedback"),
                                    htmlOutput("printHint"),
                                    htmlOutput("printAnswer"),
                                    br(),
                                    br()),
                             column(6,
                                    wellPanel(h4(strong("Your Stats")),
                                              div(textOutput("totalRounds"),
                                              textOutput("totalCorrect"),
                                              textOutput("pointsProp"),
                                              span(style = "color: #079B7B", textOutput("totalPoints")), style = "font-weight: bold"))))
                           ) 

               )
               
)

server = function(input, output, session) {
  rounds = reactiveValues(roundValue = 0)
  
  buttonPressed = eventReactive(input$button, {
    rounds$roundValue = rounds$roundValue + 1
    shinyjs::disable("button")
    shinyjs::enable("hintButton")
    shinyjs::enable("submit")
    shinyjs::enable("giveUpButton")
    randNum = floor(runif(1, min = 1, max = nrow(allLyrics)))
    if (input$mode == 3) {
      allLyrics[randNum,]
    }
    else if (input$mode == 2) {
      randSection = allLyrics$element[randNum]
      if (allLyrics$element[randNum + 1] == randSection) {
        start = randNum
        end = randNum + 1
      }
      else {
        start = randNum - 1
        end = randNum
      }
      allLyrics[start:end,]
    }
    else if (input$mode == 1) {
      randSection = allLyrics$element[randNum]

      end = randNum
      while (allLyrics$element[end + 1] == randSection) {
        end = end + 1
      }
      start = randNum
      while (allLyrics$element[start - 1] == randSection) {
        start = start - 1
      }
      allLyrics[start:end,]
    }
  })
  
  counter = reactiveValues(counterValue = 0)
  corrects = reactiveValues(correctsValue = 0)
  availPoints = reactiveValues(availValue = 0)
  
  output$randGenerated = renderUI({
    HTML(paste(buttonPressed()$lyric, collapse = "<br/>"))
  })
  wantHint = eventReactive(input$hintButton, {
    counter$counterValue = counter$counterValue - 1
    shinyjs::disable("hintButton")
    buttonPressed()$album_name[1]
  })
  secButtonPressed = eventReactive(input$submit, {
    req(input$guess)
    guess = str_trim(input$guess)
    titleLength = nchar(buttonPressed()$track_name[1])
    allowedDiff = ceiling(0.33 * titleLength)
    if (stringdist(str_to_lower(buttonPressed()$track_name[1]), 
                   str_to_lower(guess)) <= allowedDiff) {
      corrects$correctsValue = corrects$correctsValue + 1
      shinyjs::enable("button")
      shinyjs::disable("giveUpButton")
      shinyjs::disable("hintButton")
      shinyjs::reset("guess")
      shinyjs::disable("submit")
      if (input$mode == 1) {
        counter$counterValue = counter$counterValue + 2
        availPoints$availValue = availPoints$availValue + 2
      }
      else if (input$mode == 2) {
        counter$counterValue = counter$counterValue + 6
        availPoints$availValue = availPoints$availValue + 6
      }
      else {
        counter$counterValue = counter$counterValue + 8
        availPoints$availValue = availPoints$availValue + 8
      }
      HTML(paste(tags$span(style = "color:#70FF23;font-size:larger;font-weight:800", 
                            tags$strong("Correct!")),
                  br(),  
                  em(strong(buttonPressed()$track_name[1])),
                     ", ", 
                     strong(em(buttonPressed()$element[1])),
                  ", from the album ", 
                  em(strong(buttonPressed()$album_name[1])), 
                  br(), br(), sep = ""))
    }
    else {
      counter$counterValue = counter$counterValue - 2
      if (input$mode == 1) {
        availPoints$availValue = availPoints$availValue + 2
      }
      else if (input$mode == 2) {
        availPoints$availValue = availPoints$availValue + 6
      }
      else {
        availPoints$availValue = availPoints$availValue + 8
      }
      HTML(paste0(tags$span(style = "color: red;font-size:larger", strong("That is incorrect")), 
                  br(), 
                  div("Try again, you can do it! (or if you can't, you can give up)", 
                      style = "color:white;"), 
                  br()))
    }
  })
  output$guessFeedback = renderUI({
    secButtonPressed()
  })
  output$printHint = renderUI({
    HTML(paste0(tags$span(style = "color:orange;", tags$strong("Hint: ")),
                "these lyrics come from the album ", 
                tags$em(tags$strong(wantHint())), 
                br(), br()))
  })
  wantAnswer = eventReactive(input$giveUpButton, {
    counter$counterValue = counter$counterValue - 3
    shinyjs::disable("submit")
    shinyjs::enable("button")
    shinyjs::disable("giveUpButton")
    shinyjs::disable("hintButton")
    shinyjs::reset("guess")
    buttonPressed()$track_name[1]
  })
  output$printAnswer = renderUI({
    # shinyjs::show("printAnswer")
    HTML(paste0(tags$span(style = "color: red", tags$strong("Answer: ")), 
                "the correct answer was ", 
                tags$em(tags$strong(wantAnswer())), 
                ", ", 
                tags$strong(buttonPressed()$element[1]), 
                br(), br()))
  })
  output$totalRounds = renderText({
    paste0("Current round: ", rounds$roundValue)
  })
  output$totalCorrect = renderText({
    percentage = round((corrects$correctsValue / rounds$roundValue) * 100, digits = 2)
    paste0("Accuracy: ", corrects$correctsValue, "/", rounds$roundValue, 
           " (", percentage, "%)")
  })
  output$totalPoints = renderText({
    paste0("Total points: ", counter$counterValue)
  })
  output$pointsProp = renderText({
    propPerc = round((counter$counterValue / availPoints$availValue) * 100, digits = 2)
    paste0("Points out of total possible: ", counter$counterValue, "/", availPoints$availValue, " (", propPerc, "%)")
  })
  observeEvent(input$submit, {
    shinyjs::show("guessFeedback")
  })
  observeEvent(input$button, {
    shinyjs::hide("guessFeedback")
    shinyjs::hide("printHint")
    shinyjs::hide("printAnswer")
  })
  observeEvent(input$hintButton, {
    shinyjs::show("printHint")
  })
  observeEvent(input$giveUpButton, {
    shinyjs::show("printAnswer")
  })
  # observeEvent(input$guess, {
  #   shinyjs::enable("submit")
  # })
}

shinyApp(ui = ui, server = server)
