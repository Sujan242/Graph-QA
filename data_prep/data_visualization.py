import json
import matplotlib
def main():
    file_path = "../musique_data_v1.0/data/musique_ans_v1.0_train.jsonl"

    should_print = True
    # print an example from the dataset 
    hops = {}
    with open(file_path, "r") as file:
    # Iterate over each line in the file
        for line in file:
        # Parse the JSON string into a Python dictionary
            data = json.loads(line)
        # Process the data as needed
            if(should_print):
                    should_print = False
                    print(data.keys())  # Example: Print each line of JSONL data

                    print(data["paragraphs"][0])
                    print("question" + " " + data["question"])
                    # "{'idx': 0, 'title': 'Pakistan Super League', 'paragraph_text': 'Pakistan Super League (Urdu: پاکستان سپر لیگ \u202c \u200e; PSL) is a Twenty20 cricket league, founded in Lahore on 9 September 2015 with five teams and now comprises six teams. Instead of operating as an association of independently owned teams, the league is a single entity in which each franchise is owned and controlled by investors.', 'is_supporting': False}"
                    print("answer" + " " + data['answer'])
                    print(f"Question-decomposition {data['question_decomposition']}") # this contains the steps required to arrive at the answer
            num_hops = len(data['question_decomposition'])

            if hops.get(num_hops)==None:
                hops[num_hops] = 0
            hops[num_hops] += 1

    print(hops) # {2: 14376, 3: 4387, 4: 1175}

main()
