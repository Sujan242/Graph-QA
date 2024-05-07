import torch.nn as nn
from transformers import T5ForConditionalGeneration, T5EncoderModel

class Encoder(nn.Module):
    def __init__(self, encoder_model_name):
        super(Encoder, self).__init__()
        self.encoder = T5EncoderModel.from_pretrained(encoder_model_name)
        self.encoder.eval()  # Freeze the encoder during training
        for param in self.encoder.parameters():
            param.requires_grad = False

    def forward(self, question_encodings, paragraph_encodings):

        outputs = []

        # Encode question

        question_outputs = self.encoder(input_ids=question_encodings).last_hidden_state
        outputs.append(question_outputs)
        # # Encode each paragraph independently

        for i in range(50):
            paragraph_output = self.encoder(input_ids=torch.squeeze(paragraph_encodings[:,i,:], dim=1)).last_hidden_state
            outputs.append(paragraph_output)

        # Concatenate paragraph encodings
        concatenated_encodings = torch.cat(outputs, dim=1)


        return concatenated_encodings