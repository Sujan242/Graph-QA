import torch
from torch.utils.data import DataLoader
from transformers import T5Tokenizer, get_linear_schedule_with_warmup


# train_json_file = "drive/MyDrive/Graph_QA/musique_ans_v1.0_train.jsonl"
# Initialize tokenizer and dataset
tokenizer = AutoTokenizer.from_pretrained("google/t5-efficient-small-el16")
dataset = MusiqueDataSet(json_file_name="drive/MyDrive/Graph_QA/musique_ans_v1.0_train.jsonl", max_length= 256, tokenizer=tokenizer)

# Initialize encoder and decoder models
encoder_model = Encoder(encoder_model_name='google/t5-efficient-small-el16')
decoder_model = DecoderModel(decoder_model_name='google/t5-efficient-small-el16')

# Define batch size, learning rate, and number of epochs
batch_size = 2
learning_rate = 1e-4
num_epochs = 10

# Initialize dataloader with the specified batch size
#TODO update shuffle to True
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False, drop_last=True)

# Define optimizer and loss function
optimizer = torch.optim.Adam(decoder_model.parameters(), lr=learning_rate)
criterion = torch.nn.CrossEntropyLoss()

# Calculate total number of training steps (number of batches * number of epochs)
total_steps = len(dataloader) * num_epochs

# Create linear learning rate scheduler with warmup
scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=1000, num_training_steps=total_steps)

encoder_model.to('cuda')
decoder_model.to('cuda')
# Training loop
for epoch in range(num_epochs):
    batch_num = 0
    for step, batch in enumerate(dataloader):
        batch_num += 1
        # input_embeddings = batch['input']
        # answers = batch['answers']

        question_encodings = batch['question_encodings'].to('cuda')
        paragraph_encodings = batch["paragraph_encodings"].to('cuda')

        optimizer.zero_grad()

        # Move model to GPU if not already done

        # print(question_encodings.shape)
        # print(paragraph_encodings.shape)

        encoder_hidden_states = encoder_model(question_encodings, paragraph_encodings)

        batch['question_encodings'].to('cpu')
        batch["paragraph_encodings"].to('cpu')

        # print(encoder_hidden_states)

        # print(encoder_hidden_states.shape)
        answer_encodings = batch["answers"].to('cuda')

        decoder_outputs = decoder_model(decoder_input_ids = answer_encodings, encoder_hidden_states=encoder_hidden_states)

        # print(decoder_outputs)
        batch["answers"].to('cpu')

        loss = criterion(decoder_outputs.view(-1, decoder_outputs.size(-1)), answer_encodings.view(-1))

        loss.backward()
        optimizer.step()

        scheduler.step()

        print(f"completing a batch{batch_num}")

        

        # break
    torch.save(decoder_model.state_dict(), f'drive/MyDrive/Graph_QA/decoder_model_epoch{epoch}.pth')
    torch.save(encoder_model.state_dict(), f'drive/MyDrive/Graph_QA/encoder_model_epoch{epoch}.pth')
    # break
    print(f'Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}')

# Save trained model
# torch.save(decoder_model.state_dict(), 'drive/MyDrive/Graph_QA/decoder_model.pth')
# torch.save(encoder_model.state_dict(), 'drive/MyDrive/Graph_QA/encoder_model.pth')