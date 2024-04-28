import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration, T5Config
import os
import json

class T5SequenceToSequence(torch.nn.Module):
    def __init__(self, pretrained_encoder_model_name):
        super(T5SequenceToSequence, self).__init__()
        
        # Load pretrained T5 encoder
        self.encoder = T5ForConditionalGeneration.from_pretrained(pretrained_encoder_model_name)
        
        # Freeze the encoder parameters
        for param in self.encoder.parameters():
            param.requires_grad = False
        
        # Initialize T5 decoder configuration
        decoder_config = T5Config.from_encoder_decoder_pretrained(pretrained_encoder_model_name, pretrained_encoder_model_name)
        
        # Create T5 decoder
        self.decoder = T5ForConditionalGeneration(decoder_config)

    def forward(self, input_ids, decoder_input_ids):
        # Forward pass through T5 encoder for each paragraph
        encoded_paragraphs = []
        for input_id in input_ids:
            encoder_output = self.encoder(input_ids=input_id.unsqueeze(0))
            encoded_paragraphs.append(encoder_output.last_hidden_state)
        
        # Concatenate encoded representations
        combined_encoding = torch.cat(encoded_paragraphs, dim=1)
        
        # Forward pass through T5 decoder
        decoder_output = self.decoder(input_ids=decoder_input_ids, encoder_outputs=combined_encoding)
        
        return decoder_output

# Usage example
tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5SequenceToSequence("t5-small")

# Iterate over each file
for file_name in file_names:
    # Extract id from the file name
    id = file_name.split("_")[2]
    
    # Read paragraphs from the file
    with open(os.path.join(folder_path, file_name), "r") as file:
        paragraphs = file.readlines()
    
    # Encode each paragraph
    input_ids = []
    for paragraph in paragraphs:
        # Encode the paragraph using T5 tokenizer
        encoded_paragraph = tokenizer.encode(paragraph, return_tensors="pt", padding=True, truncation=True)
        input_ids.append(encoded_paragraph)
    
    # Generate decoder input
    decoder_input = tokenizer.encode("Your decoder input here", return_tensors="pt", padding=True, truncation=True)
    
    # Forward pass through the model
    outputs = model(torch.stack(input_ids), decoder_input)
    
    # Store output in dictionary
    combined_data[id] = outputs

# Write combined data to a single JSON file
with open("combined_adj_graph.json", "w") as output_file:
    json.dump(combined_data, output_file, indent=4)

print("Combined JSON file created successfully.")