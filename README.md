# Klarity - CS50x Version - a fitness planning app
#### Video Demo: https://youtu.be/OH7pMVVFAUU
#### Description:
Klarity v1.0 is a fitness planning app that can help you unlock your full potential by helping you stay on track with personalized workouts, smart planning tools, and goal-focused guidance whether you are just starting out or leveling up your fitness journey. Klarity is a Python-based application and uses Flask, HTML, Javascript, CSS and SQL to make the perfect fitness app for you.

You can create a profile to help keep track of your weight and current fitness level. Klarity also helps you narrow down a focus for a workout and gives you the right exercises to help you get that pump in for any muscle of your choosing. In the Plan tab, you can see a calendar of the current month. Clicking on a day can show your workout history, current weight and current fitness level for that day which can help guide you towards a journey towards self-improvement. ​

For the login, logout and register pages, I took inspiration from the said functions from cs50 finance. For registration, I created a user schema: CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL); I included check_password_hash, generate_password_hash for password security. And helpers.py contains an apology function for errors through apology.html (again sampled from cs50 finance.)

In the register page, the user registers with a username, password, and confirmation password. For the html pages, I used layout.html (sampled from cs50 finance) to create foundations for the following html files in the template folder: apology.html, focus.html, home.html, layout.html, login.html, muscles.html, plan.html, profile.html, register.html, videos.html.
In home page (home.html), there’s an elevator pitch for visitors to get the gist of the site. In home.html, there’s a quote from a fitness or sports legend to inspire visitors. In the home page, the user only sees the menu bar which includes homepage, pitch and quote if registered and logged in - these pages and the shortcuts on the top menu bar aren’t viewed by visitors without accounts.

For the profile page, I created a schema to keep track of profile accounts: CREATE TABLE profiles (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, name TEXT NOT NULL, fitnesslvl TEXT NOT NULL, age INTEGER NOT NULL, weight INTEGER NOT NULL, bmi INTEGER, FOREIGN KEY (id) REFERENCES users(id)); There, the user can create, edit and change the required fields: username, fitness experience level, weight and age and not required field: bmi. These fields are used to track the user's progression over time.

In the focus page, the user can choose workout location - home or in-gym. They can choose the focus type - warm up, strength building, fat loss, cardio, flexibility, muscle gain, resistance training, health & wellbeing and recovery. Then, the user is brought to muscles.html where they can click on a muscle image to access exercises specifically for that chosen muscle based on their profile personalization. The muscles they can choose are in a table and include general, abductors, abs, adductors, biceps, calves, chest, forearms, glutes, hamstrings, hip flexors, IT Band, lats, lower back, upper back, neck, obliques, palmar fascia, quads, shoulders, traps and triceps. The images for these muscles are taken from bodybuilding.com, specifically the link - https://www.muscleandstrength.com/exercises.

This info and the info passed into both the focus and the profile page are then stored in a workout schema - CREATE TABLE workouts (id INTEGER NOT NULL, fitnesslvl TEXT NOT NULL, weight INTEGER NOT NULL, location TEXT NOT NULL, focus TEXT NOT NULL, muscle TEXT NOT NULL DEFAULT 'general', day INT NOT NULL, month INT NOT NULL, year INT NOT NULL); to keep track of workout specifics and personalize workouts.

In muscles.html, I used queries to keep track of workout specifics and personalize workouts. These fields are passed into the exercises route and its function. The exercises function acts as an intermediary function. It gets these fields (and the fields fitnesslvl and weight), updates the workouts table and passes them into videos.html, to select the right videos based on the muscle, location, focus and fitnesslvl fields. The videos are mostly in iframe elements with sources taken from YouTube, specifically the channel Muscle & Strength, using the No Cookie mode to embed videos without storing cookies on users' devices, enhancing privacy.

In the plan function, I used the datetime module for the date and try and except loop to get the correct amount of days in a month (i.e. 28 days for February, etc.) In the planner page, there is an accurate calendar table for the current month, made through calendar.js in the static folder where each day is correctly placed on the right day of the week. Additionally, if the user worked out on a day, then it has an anchor element with some query parameters pertaining to that date of the workout day. The date info query parameters are then used to get all the workouts that day and place them in a paragraph above the table.

The app is also named after the album, Clarity by the band Jimmy Eat World :)

UPDATE 9/22/25:
I added a try and except block in the focus function to make sure a profile is created prior to setting up focus

UPDATE 9/27/25:
Instead of pasting the workout object in plan.html without styling, I used Flexbox to make the calendar and the workout object for the selected day to be side by side. And for every workout object, I used a table just like the calendar to display workout objects better. And passed in the user's username into the plan html file which takes the place for the id field in a workout object so that the user doesn't just see the number id but something better, their username.

UPDATE 9/28/25:
Fix error in muscles.html where, to /exercises in app.py, some muscles had the query parameter name "exercise" instead of the correct parameter name used in app.py, "muscle" which meant some muscles couldn't be chosen for a workout thus passing in None instead of the right muscle.
Instead of a million iframe elements in muscle.html for the videos for a given muscle, i used youtube api to search and find shorts pertaining to the muscle, fitness level, and focus - ex. "beginner abs warm-up." And used a list for video ids. Thus, streamlining the video process of the application and keeping videos.html short and sweet. I also made a flex-container for the the youtube shorts videos to make them appear side by side. And I made sure a new workout isn't added everytime the user refreshes the page in the case the videos don't work etc.

UPDATE 10/1/25:
For the videos, I used youtube-nocookie.com/embed/... because the videos refused to connect. I used it to embed the videos to place the content directly onto the page instead of the user having to be directed to the content externally. Additionally, it load the videos without cookies and tracking. Essentially, it allows my little private project to use youtube videos and displays them with privacy. However, I still kept having the error "error 153 Video player configuration error" or just the error, "video unavailable." I believe it had to do with embedding being disabled on the videos themselves. So, I decided to forgo with the videos that I assume have embedding disabled. Using YouTube IFrame Player API, my script checkvideo.js (thats with a query passed in containing an array of the video ids) handles that with event listeners to respond to specific player events like when the videos are loaded so, unavailable videos (which are off the bat loaded with a state of unstarted) are removed.

Future Plans:
-a Level for every workout; level crown
-a calorie tracker
-Gamify the app, include youtube shorts for every exercise, using side scrolling method to go from short to short
-Maybe use multiple profiles for a username (say for a family - ex. Smith family, Jim, John)
