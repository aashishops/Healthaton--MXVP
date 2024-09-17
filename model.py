from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "ruslanmv/Medical-Llama3-8B"
device = 'cpu'

print("Starting script...")

try:
    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, use_cache=False)
    print("Model loaded.")
    
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    print("Tokenizer loaded.")
    
    print("Saving model and tokenizer...")
    model.save_pretrained('./saved_model')
    tokenizer.save_pretrained('./saved_model')
    print("Model and tokenizer saved.")

except Exception as e:
    print("Error during model/tokenizer loading or saving:", e)
