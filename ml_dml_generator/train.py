
import os
from transformers import T5Tokenizer, T5ForConditionalGeneration, Trainer, TrainingArguments, TextDataset, DataCollatorForSeq2Seq

def create_dataset(input_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for file in os.listdir(input_dir + '/docs'):
            if file.endswith('.docx'):
                doc_path = os.path.join(input_dir, 'docs', file)
                sql_path = os.path.join(input_dir, 'sqls', file.replace('.docx', '.sql'))
                if os.path.exists(sql_path):
                    from docx import Document
                    doc = Document(doc_path)
                    text = "\n".join(p.text for p in doc.paragraphs)
                    with open(sql_path, 'r', encoding='utf-8') as f_sql:
                        sql = f_sql.read()
                    f_out.write(f"Generate SQL: {text}\t{sql}\n")

create_dataset("training_data", "train.txt")

tokenizer = T5Tokenizer.from_pretrained("t5-small")
model = T5ForConditionalGeneration.from_pretrained("t5-small")

def load_dataset(file_path, tokenizer):
    return TextDataset(tokenizer=tokenizer, file_path=file_path, block_size=512)

train_dataset = load_dataset("train.txt", tokenizer)
data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

training_args = TrainingArguments(
    output_dir="./model",
    per_device_train_batch_size=2,
    num_train_epochs=2,
    logging_dir="./logs",
    save_total_limit=1
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    data_collator=data_collator,
)

trainer.train()
trainer.save_model("./model")
tokenizer.save_pretrained("./model")
print("Training complete. Model saved to ./model")
