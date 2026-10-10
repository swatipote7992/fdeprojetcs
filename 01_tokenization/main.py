import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")
text = "Hello, world! This is a test string to demonstrate tokenization."
tokens = encoder.encode(text)

print("Original text:", text)
print("Tokenized output:", tokens)

decoded = encoder.decode(tokens)
print("Decoded text:", decoded) 
