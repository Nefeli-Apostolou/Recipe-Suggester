from datasets import load_dataset
from transformers import T5Tokenizer
import config

def get_tokenized_dataset():
    """
    Loads and tokenizes the dataset.
    Returns the dataset and the tokenizer.
    """
    
    # 1. Load the tokenizer for the T5 model
    print(f"Loading tokenizer for '{config.MODEL_NAME}'...")
    tokenizer = T5Tokenizer.from_pretrained(config.MODEL_NAME)
    
    # 2. Load the .jsonl file
    print(f"Loading dataset from '{config.TRAINING_FILE}'...")
    raw_dataset = load_dataset('json', data_files=config.TRAINING_FILE)
    raw_dataset['train'] = raw_dataset['train'].select(range(10000))

    # 3. Define the preprocessing (tokenization) function
    def preprocess_function(examples):
        # The 'input' and 'target' keys match our .jsonl file
        inputs = examples['input']
        targets = examples['target']
        
        # Tokenize inputs
        model_inputs = tokenizer(
            inputs, 
            max_length=config.MAX_INPUT_LENGTH, 
            padding="max_length", 
            truncation=True
        )
        
        # Tokenize targets
        # We use 'with tokenizer.as_target_tokenizer():' for targets
        with tokenizer.as_target_tokenizer():
            labels = tokenizer(
                targets, 
                max_length=config.MAX_TARGET_LENGTH, 
                padding="max_length", 
                truncation=True
            )
        
        # Set the 'labels' for the model
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    # 4. Apply the tokenization to the entire dataset
    # We use .map() for efficiency. batched=True processes multiple items at once.
    print("Tokenizing dataset...")
    tokenized_dataset = raw_dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=['input', 'target'] # We don't need the old text columns
    )
    
    # 'train' split is created by default when loading a single file
    return tokenized_dataset['train'], tokenizer


