# Implementation

- I used next.js for front end and tailwindcss for styling. Front end is alright looking nothing fancy.
- I used axios to fetch data from backend to frontend, along with axios interceptors to get new refresh tokens for JWT.
- I used flask for backend and mongodb for database.
- JWT is used for authentication of routes.
- BCrypt is used to hash the password before storing.
- Google books API is used for fetching the book info.
- I split the backend into two layers, one which recieves the request from front end, the other one that will handle the logic and send it back to the first and then to frontend.
- The error handling kinda sucks, right now. I got inspiration from Golang, how it returns the error if it occurs, which I liked when I spent a really long time of 7 days on learning it.
- I split each functionality into its own seperate api.
- Although the backend is ready for search functionality and followers mechanism, I couldnt implement it in the front end.
- Except the error handling and some front end being left out, I tried my best to complete this main project.
- Thank you
