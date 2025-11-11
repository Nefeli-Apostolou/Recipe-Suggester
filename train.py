# In train.py
import config
from data_loader import get_tokenized_dataset
from transformers import (
    T5ForConditionalGeneration,
    Trainer,
    TrainingArguments
)

def run_training():
    """
    Loads model, data, and runs the training.
    """
    
    # 1. Load Data and Tokenizer
    print("--- Loading Data ---")
    train_dataset, tokenizer = get_tokenized_dataset()
    
    # 2. Load Pre-trained T5 Model
    print("--- Loading Model ---")
    model = T5ForConditionalGeneration.from_pretrained(config.MODEL_NAME)
    model.to(config.DEVICE) # Move model to GPU if available

    # 3. Define Training Arguments
    # These are all the settings for the training run
    print("--- Setting up Training ---")
    training_args = TrainingArguments(
        output_dir=config.OUTPUT_DIR,
        num_train_epochs=config.NUM_EPOCHS,
        per_device_train_batch_size=config.BATCH_SIZE,
        learning_rate=config.LEARNING_RATE,
        
        # Logging and Saving
        logging_dir=f"{config.OUTPUT_DIR}/logs",
        logging_steps=100,
        save_steps=1000,
        save_total_limit=2,
        
        # Optimization
        # fp16=True makes training *much* faster on NVIDIA GPUs
        fp16=True if config.DEVICE == "cuda" else False, 
        
        # Evaluation (if you had a test set)
        # evaluation_strategy="steps",
        # eval_steps=1000, 
    )

    # 4. Initialize the Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        # You would add an eval_dataset here if you made a test split
        # eval_dataset=tokenized_dataset["test"], 
    )

    # 5. Start Training
    print("--- Starting Training ---")
    trainer.train()

    # 6. Save the Final Model and Tokenizer
    print("--- Training Complete ---")
    print(f"Saving model to {config.OUTPUT_DIR}")
    trainer.save_model()
    tokenizer.save_pretrained(config.OUTPUT_DIR)

if __name__ == "__main__":
    run_training()