from pathlib import Path
from transformers import AutoTokenizer

MODEL_DIR = Path(r".\indictrans2_onnx\int8")

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    str(MODEL_DIR),
    trust_remote_code=True
)

text = "eng_Latn kan_Knda Hello, how are you?"

tokens = tokenizer(
    text,
    return_tensors="np"
)

print("Tokenizer loaded successfully!")
print("Input IDs shape:", tokens["input_ids"].shape)
print("Attention mask shape:", tokens["attention_mask"].shape)
print("Input IDs:", tokens["input_ids"])