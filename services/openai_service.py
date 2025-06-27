import os
import openai
from typing import Tuple
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    """OpenAI APIとの統合を管理するサービスクラス"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        openai.api_key = self.api_key
    
    async def generate_response(self, prompt: str, model: str = "gpt-3.5-turbo") -> Tuple[str, int]:
        """
        OpenAI APIを使用してテキスト応答を生成
        
        Args:
            prompt (str): 入力プロンプト
            model (str): 使用するモデル名
            
        Returns:
            Tuple[str, int]: (生成された応答, 使用トークン数)
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            generated_text = response.choices[0].message.content.strip()
            tokens_used = response.usage.total_tokens
            
            return generated_text, tokens_used
            
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def generate_summary(self, text: str) -> Tuple[str, int]:
        """
        テキストの要約を生成
        
        Args:
            text (str): 要約対象のテキスト
            
        Returns:
            Tuple[str, int]: (要約, 使用トークン数)
        """
        prompt = f"以下のテキストを簡潔に要約してください:\n\n{text}"
        return await self.generate_response(prompt)
    
    async def generate_translation(self, text: str, target_language: str = "Japanese") -> Tuple[str, int]:
        """
        テキストの翻訳を生成
        
        Args:
            text (str): 翻訳対象のテキスト
            target_language (str): 翻訳先の言語
            
        Returns:
            Tuple[str, int]: (翻訳結果, 使用トークン数)
        """
        prompt = f"以下のテキストを{target_language}に翻訳してください:\n\n{text}"
        return await self.generate_response(prompt)

