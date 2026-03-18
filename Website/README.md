# Not Fable — Book Discovery & Personal Library Web App (Next.js + Flask + MongoDB)

Not Fable is a full‑stack book discovery and personal library application. The frontend is built with Next.js (App Router) and styled using Tailwind CSS, while the backend is implemented in Flask with MongoDB as the database. The app integrates with the Google Books API to fetch book information, and supports JWT-based authentication (access + refresh tokens). On the client side, API calls are handled through a centralized Axios setup with interceptors that automatically attach the access token and transparently refresh it when it expires—redirecting users to login when refresh fails.

On the backend, the project is organized into separate modules for routes, models, a database access layer (dbAPI), and an external integration layer (googleAPI), keeping request handling and business logic separated. Passwords are stored securely using hashing (BCrypt mentioned in the project documentation). The codebase is also structured to support additional features like search and a followers mechanism, even if parts of those flows were not completed in the UI.

** Tech stack: Next.js 15, React 19, Tailwind CSS, Flask, MongoDB, JWT auth, Google Books API. **
