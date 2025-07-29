# Country Data Visualization App

This application fetches data about countries using the [REST Countries API](https://restcountries.com/), stores it in a PostgreSQL database using Docker, and displays the data through a web dashboard built with Dash (Plotly).

## Features

- Fetches country data including name, population, region, flag, area
- Saves data to a PostgreSQL database using SQLAlchemy
- Provides a sortable, paginated table with country information
- Displays flags of selected country

---

## How to Run the App

### 1. Clone the Repository

- git clone https://github.com/jevtovicc/ai-digital-task
- cd ai-digital-task

### 2. Create .env file
Create a .env file in the root directory of the project before running docker-compose.

Here is an example of what the .env file should look like:
DB_HOST=<db>
DB_PORT=<port>
DB_NAME=<aidigitaldb>
DB_PASSWORD=<dbpassword>
DB_USER=<dbuser>

### 3. Run Docker Containers
docker-compose up --build

This will:

- Build the image for the app
- Start both the PostgreSQL database and the Dash app
- Automatically fetch country data and populate the database on first run


### 4. Open the Web App
Once everything is running, open your browser and go to: http://localhost:8050 <br> You should see the dashboard with country data and flags.
