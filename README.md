# AI Recipe Generator

This web application uses a fine-tuned T5 transformer model to generate new, unique recipes based on a list of ingredients provided by the user.

This project is a complete pivot from its original version, which was a static recipe-filtering app. It now uses a powerful AI model trained on over 200,000 recipes to create content on the fly.

## 🚀 Features

* **AI-Powered Generation:** Leverages a T5-small model fine-tuned on the Food.com dataset to create plausible-sounding recipes.
* **Simple UI:** A clean, single-page application to enter ingredients and receive a generated recipe.
* **Flask Backend:** The AI model is served via a lightweight Python Flask API.
* **Full Training Pipeline:** Includes all scripts necessary to preprocess data and train your own model from scratch.

## 🤖 The Model

* **Architecture:** T5-small (a Text-to-Text Transfer Transformer model).
* **Dataset:** Fine-tuned on the [Food.com Recipes and Reviews](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) dataset from Kaggle.
* **Training:** The model was trained on **200,000 recipes** for 3 epochs on a remote GPU (Kaggle Notebook).

## 🛠️ Technologies Used

* **AI / Backend:** Python, Flask, PyTorch, Hugging Face `transformers`
* **Frontend:** HTML, Tailwind CSS, JavaScript

---

## 🏃 How to Run the Application

There are two parts to this project: **1. Running the App** (using the pre-trained model) and **2. Training the Model** (creating your own).

### 1. Running the App (Locally)

This guide assumes you have already downloaded the trained model folder.

> **Note:** The `t5-recipe-generator` model folder is **not** included in this repository (it is too large for Git). You must download it separately after training your own model (see below).

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Nefeli-Apostolou/Recipe-Suggester.git](https://github.com/Nefeli-Apostolou/Recipe-Suggester.git)
    cd Recipe-Suggester
    ```

2.  **Place the Model:**
    Download your trained `t5-recipe-generator` folder and place it in the root of this project directory. The folder structure should look like this:
    ```
    /Recipe-Suggester/
    |-- /t5-recipe-generator/  <-- Your downloaded model
    |-- app.py
    |-- index_ai.html
    |-- requirements.txt
    |-- ... (other files)
    ```

3.  **Create a Virtual Environment:**
    ```bash
    python -m venv .venv
    # On Windows
    .\.venv\Scripts\activate
    # On Mac/Linux
    source .venv/bin/activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the Flask Server:**
    This will load the model into memory and start the API.
    ```bash
    python app.py
    ```
    Wait for the terminal to show `Model loaded successfully`.

6.  **Open the App:**
    In your web browser, open the `index_ai.html` file. You can now enter ingredients and generate recipes!

### 2. Training Your Own Model

If you want to train your own model from scratch:

1.  **Get the Data:** Download the `recipes.csv` file from the [Kaggle dataset](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews) and place it in the root of this project.

2.  **Run the Build Script:** This script cleans the raw data and creates the training file.
    ```bash
    # This will create recipes_training.jsonl
    python build_dataset.py
    ```

3.  **Train the Model (on a GPU):**
    This step is **not** recommended for your local computer. It will take days. You should run this on a service with a free GPU, like **Google Colab** or **Kaggle Notebooks**.

    * Upload all your `.py` files and the `recipes_training.jsonl` file.
    * Install the `requirements.txt`.
    * Run the training script:
    ```bash
    python train.py
    ```
    This will create the `t5-recipe-generator` folder, which you can then download and use.

---

## 📜 License

This project is for educational and personal use.
Dataset belongs to the original Kaggle contributors.
