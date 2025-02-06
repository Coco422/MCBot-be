from typing import List, Dict
from tools.openai_chat import get_chat_response

async def generate_title(messages: List[dict]) -> str:
    """
    Generate chat title
    """
    messages_payload = [{
        "role": "user",
        "content": f"""
Create a concise, 3-5 word title with an emoji as a title for the prompt in the given language. Suitable Emojis for the summary can be used to enhance understanding but avoid quotation marks or special formatting. RESPOND ONLY WITH THE TITLE TEXT.

Examples of titles:
📉 Stock Market Trends
🍪 Perfect Chocolate Chip Recipe
Evolution of Music Streaming
Remote Work Productivity Tips
Artificial Intelligence in Healthcare
🎮 Video Game Development Insights

Prompt: {messages}
        """
    }]
    return await get_chat_response(messages_payload)