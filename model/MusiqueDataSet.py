import json
from torch.utils.data import Dataset, DataLoader

class MusiqueDataSet(Dataset):
    def __init__(self, json_file_name, max_length, tokenizer):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.set_input_output_data(json_file_name)
    
    def __len__(self):
        return len(self.input_data)
    
    def __getitem__(self, idx):
        question_text = self.questions_data[idx]
        paragraphs_list = self.paragraphs_data[idx]
        output_text = self.output_data[idx]
        
        # Tokenize input and output texts
        # using encode_plus because each string literal may contain multiple sequences
        question_tokenized = self.tokenizer.encode_plus(question_text, max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt")

        paragraphs_tokenized = [self.tokenizer.encode_plus(paragraph_text, max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt")
        for paragraph_text in paragraphs_list]

        output_tokenized = self.tokenizer.encode_plus(output_text, max_length=self.max_length, padding="max_length", truncation=True, return_tensors="pt")
        
        return input_tokenized, output_tokenized

    def set_input_output_data(self, json_file_name):
 
        # Opening JSON file
        f = open(json_file_name)
        
        self.questions_data = []
        self.output_data = []
        self.paragraphs_data = []
        # returns JSON object as 
        # a dictionary
        with open(json_file_name, "r") as file:

            for line in file:

                row = json.loads(line)
                question_data_point = self.get_question_data_point(row["question"])
                paragraph_data_point = self.get_paragraph_data_point(row["paragraphs"])
                output_data_point = self.get_output_data_point(row["answer"], row["question_decomposition"], row["paragraphs"])

                self.questions_data.append(question_data_point)
                self.paragraphs_data.append(paragraph_data_point)
                self.output_data.append(output_data_point)

    def get_question_data_point(self, question):
        s = ""
        s += "Question: "

        # add the question here 
        s += question
        return s

    def get_paragraph_data_point(self, paragraphs):
        paragraph_rep = []
        for paragraph in paragraphs:
            s = ""
            s += "Title: " + paragraph["title"] + " "

            s += "Context: "

            fact_num=0

            for fact in paragraph["paragraph_text"].split('.'):
                if fact == "" or fact == " ":
                    continue
                fact_num += 1 
                s += f"[f{fact_num}]: {fact}. "

            paragraph_rep.append(s)

        return paragraph_rep

    def get_output_data_point(self, answer, question_decomposition, paragraphs):

        s = ""
        hop_num = 0
        for hop in question_decomposition:
            paragraph_idx = hop["paragraph_support_idx"]
            hop_num += 1
            for paragraph in paragraphs:
                if paragraph_idx == paragraph["idx"]:
                    title = paragraph["title"]
                    s += f"[title-{hop_num}] {title} "
                    break

        s += f"[answer] {answer}"

        return s

def main():
    dataset = MusiqueDataSet("../musique_data_v1.0/data/musique_ans_v1.0_train.jsonl", 256, "test")

if __name__ == '__main__':
    main()