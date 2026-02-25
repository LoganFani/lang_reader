from llama_cpp import Llama, LlamaGrammar
import json

MODEL_PATH = "llama/models/mistral-7b-instruct-v0.2.Q4_0.gguf"

def build_prompt(input_content: str, from_lang: str, to_lang:str) -> str:
    return f"""
You are a specialized language tutor.

Return ONLY valid JSON matching this schema:
{{
  "original_content": string,
  "translation": string,
  "example_sentence": string
}}

Rules:
- example_sentence MUST be in {from_lang}
- Do NOT include extra keys
- Do NOT include explanations
- Do NOT include markdown
- Do NOT repeat fields

Original Language: {from_lang}
Target Language: {to_lang}
Original Content: {input_content}

Rules:
- Match the tone/register of the original content (casual vs formal vs slang).
- example_sentence MUST be written in {from_lang}
- If unsure, write a simple, natural {from_lang} sentence using the same structure
- Never omit any field
"""

def build_promptv2(input_content: str, sentence_context: str,  from_lang: str, to_lang:str) -> str:
    return f"""
You are a specialized language tutor.

Return ONLY valid JSON matching this schema:
{{
  "original_content": string,
  "translation": string,
}}

Rules:
- Translate the input content based on the sentence context.
- DO NOT translate the original_content field.
- Do NOT include extra keys
- Do NOT include explanations
- Do NOT include markdown
- Do NOT repeat fields
- Match the tone/register of the sentence context (casual vs formal vs slang).
- Never omit any field

Original Language: {from_lang}
Target Language: {to_lang}
Original Content: {input_content}
Sentence Context: {sentence_context}
"""

def get_grammar(grammar_path:str) -> LlamaGrammar:
    with open(grammar_path, 'r') as gf:
        content = gf.read()

        return LlamaGrammar.from_string(content)

llm = Llama(model_path=MODEL_PATH, n_gpu_layers=0)

prompt = build_promptv2("un podcast para practicar español de forma muy práctica.","¿cómo están? Yo estoy muy feliz. Bienvenidos a Un cafecito en español, un podcast para practicar español de forma muy práctica.", "Spanish", "English")
json_grammar = get_grammar("llama/grammar/json.gbnf")

model_output = llm(prompt=prompt, max_tokens=200, grammar=json_grammar, temperature=0.05, repeat_penalty=1.15)

print(json.loads(model_output["choices"][0]["text"]))