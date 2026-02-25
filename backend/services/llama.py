import os
from llama_cpp import Llama, LlamaGrammar
import json

class Translator:
    def __init__(self, model_path:str, grammar_path = "") -> None:
        self.llm = Llama(model_path=model_path, n_gpu_layers=0)
        self.grammar_path = grammar_path

    def build_promptv2(self, input_content: str, sentence_context: str,  from_lang: str, to_lang:str) -> str:
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
    
    def _get_grammar(self, grammar_path:str) -> LlamaGrammar:
        with open(grammar_path, 'r') as gf:
            content = gf.read()

            return LlamaGrammar.from_string(content)
        
    def generate_response(self, prompt:str):

        if not self.grammar_path == "":

            try:
                grammar = self._get_grammar(self.grammar_path)
                model_output = self.llm(prompt=prompt, max_tokens=200, grammar=grammar, temperature=0.05, repeat_penalty=1.15)

                return json.loads(model_output["choices"][0]["text"])
            except:
                return {}

        else:
            model_output = self.llm(prompt=prompt, max_tokens=200, temperature=0.05, repeat_penalty=1.15)
            try:
                return json.loads(model_output["choices"][0]["text"])
            except:
                return {}