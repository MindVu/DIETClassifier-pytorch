import json
import re

def process_jsonl_file(file_path):
    intents_examples = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            intent = data['intent']
            sentence_annotation = data['sentence_annotation']
            transformed_annotation = transform_sentence_annotation(sentence_annotation)
            examples = intents_examples.get(intent, [])
            examples.append(transformed_annotation)
            intents_examples[intent] = examples

    return intents_examples

def transform_sentence_annotation(sentence_annotation):
    entities = re.findall(r'\[([^:]+) : ([^\]]+)\]', sentence_annotation)
    for entity, value in entities:
        sentence_annotation = sentence_annotation.replace(f'[{entity} : {value}]', f'[{value}]({entity})')
    return sentence_annotation

def write_to_txt(intents_examples, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("nlu:\n")
        for intent, examples in intents_examples.items():
            output_file.write(f"- intent: {intent}\n")
            output_file.write("  examples: |\n")
            for example in examples:
                output_file.write(f"    - {example}\n")

if __name__ == "__main__":
    jsonl_file_path = "private_test.jsonl"  # Replace with the actual path to your JSONL file
    output_file_path = "output_file.txt"  # Replace with the desired output file path
    intents_examples = process_jsonl_file(jsonl_file_path)
    write_to_txt(intents_examples, output_file_path)
