import torch.nn as nn
from transformers import T5ForConditionalGeneration

class DecoderModel(nn.Module):
    def __init__(self, decoder_model_name):
        super(DecoderModel, self).__init__()
        self.model = T5ForConditionalGeneration.from_pretrained(decoder_model_name)

    def forward(self, decoder_input_ids, encoder_hidden_states):
        decoder_input_ids = self.model._shift_right(decoder_input_ids)
        decoder_outputs = self.model.decoder(input_ids= decoder_input_ids, encoder_hidden_states=encoder_hidden_states).last_hidden_state
        decoder_outputs = decoder_outputs * (768 ** -0.5)
        return self.model.lm_head(decoder_outputs)