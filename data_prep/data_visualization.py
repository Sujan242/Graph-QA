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
                    print("answer" + " " + data['answer'])
                    print(f"Question-decomposition {data['question_decomposition']}") # this contains the steps required to arrive at the answer
            num_hops = len(data['question_decomposition'])

            if hops.get(num_hops)==None:
                hops[num_hops] = 0
            hops[num_hops] += 1

    print(hops) # {2: 14376, 3: 4387, 4: 1175}

main()
