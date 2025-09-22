# Recipe Suggester App

This is a web application that helps users discover recipes based on their preferences. It features a variety of filters for categories, dietary needs, and macronutrient content to help you find the perfect dish.

### Features

- **Dynamic Filtering:** Search and filter recipes by category, diet (vegetarian, non-vegetarian, vegan), gluten content.
- **Macronutrient Filtering:** Find recipes based on macro profiles like high-protein, low-fat, or low-carb.
- **Interactive UI:** The application updates in real-time as you apply filters.
- **Dockerized:** The app runs in a containerized environment, making it easy to set up and run on any machine.

### Technologies Used

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python with Flask (used to serve the JSON data)
* **Data:** A custom JSON dataset of 1000 recipes made from kaggle dataset (linked below)
* **Containerization:** Docker

### How to Run the Application

This application runs on a pre-processed JSON file created from a public Kaggle dataset.

1.  **Get the Data:**
    First, download the raw dataset (`recipes.csv`) from the following Kaggle link:
    [\[https://www.kaggle.com/datasets/iraz/recipes-with-macros-and-diets/data\](https://www.kaggle.com/datasets/iraz/recipes-with-macros-and-diets/data)]

2.  **Process the Data:**
    To generate the `recipes_clean_1000.json` file, you need to run the `cleaning.ipynb` notebook. This notebook will clean the raw data and produce the JSON file that the app uses.

3.  **Run the App with Docker:**
    To run this application, you will need to have **Docker** and **Docker Compose** installed on your machine.
    * Clone the repository to your local machine:
      ```bash
      git clone [https://github.com/Nefeli-Apostolou/Recipe-Suggester.git]
      ```
    * Navigate to the project directory:
      ```bash
      cd Recipe-Suggester
      ```
    * Build and run the Docker containers in detached mode:
      ```bash
      docker-compose up -d
      ```

The application will be available at `http://localhost:5000` in your web browser.

To stop the application, run the following command in the project directory:
```bash
docker-compose down
```

### 📜 License
- This project is for educational and personal use.
- Dataset belongs to the original Kaggle contributors.