import torch.nn as nn
from transformers import T5ForConditionalGeneration

class DecoderModel(nn.Module):
    def __init__(self, decoder_model_name):
        super(DecoderModel, self).__init__()
        self.decoder = T5ForConditionalGeneration.from_pretrained(decoder_model_name)

    def forward(self, encoder_hidden_states):
        decoder_outputs = self.decoder(encoder_hidden_states)
        return decoder_outputs