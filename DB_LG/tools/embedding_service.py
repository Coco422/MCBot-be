from typing import List
from database.connection import get_db_connection, release_db_connection
import os
import aiohttp
import asyncio

# ----------配置日志-------------
from tools.ray_logger import LoggerHandler
log_file = "main.log"
logger = LoggerHandler(logger_level='DEBUG',file="logs/"+log_file)
# -----------日志配置完成----------
class EmbeddingService:
    def __init__(self, model_name: str = "bge-m3"):
        self.model_name = model_name
        
    async def get_embedding(self, text: str, max_retries: int = 3) -> List[float]:
        """
        Get embedding vector for input text by calling a remote embedding service.
        
        Args:
            text: The input text to get embedding for.
            max_retries: Maximum number of retries if the request fails.
        
        Returns:
            A list of floats representing the embedding vector, or None if the request fails.
        
        Raises:
            Exception: If the request fails after retries.
        """
        # Get the service URL from environment variables
        service_url = os.getenv("MCBot_api_embed_url")
        
        # Prepare the request payload
        payload = {
            "msg": text
        }
        
        retries = 0
        while retries < max_retries:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(service_url, json=payload) as response:
                        # Check if the request was successful
                        if response.status == 200:
                            result = await response.json()
                            return result
                        else:
                            # Handle non-200 status codes
                            raise Exception(f"Embedding service returned status code {response.status}")
            except Exception as e:
                # Log the error and retry
                retries += 1
                logger.error(f"Attempt {retries} failed: {e}")
                if retries < max_retries:
                    await asyncio.sleep(1)  # Wait for 1 second before retrying
                else:
                    # If all retries fail, raise an exception
                    raise Exception(f"Failed to get embedding after {max_retries} retries: {e}")
        
        # If all retries fail, return None
        return None
    

    async def lg_search_kb_by_chat(self, embedding: List[float]) -> List[dict]:
        """
        Search for similar content in LG knowledge base using embedding vector

        Args:
            embedding (List[float]): Vector embedding to search with

        Returns:
            List[dict]: List of matching documents with title, content and similarity score
        """
        conn = None
        try:
            # Validate embedding input
            if not embedding or not isinstance(embedding, list):
                logger.error("Invalid embedding input")
                return []
                
            conn = get_db_connection(db_type="lg")
            cursor = conn.cursor()
            
            # 直接传递 embedding 列表给 PostgreSQL
            query = """
                SELECT * FROM csm.use_vec_get_top_kgcont(%s::public.vector);
            """
            cursor.execute(query, (embedding,))
            results = cursor.fetchall()
            
            return [{
                "title": row[0],
                "content": row[1], 
                "similarity": float(row[2])
            } for row in results] if results else []
            
        except Exception as e:
            logger.error(f"LG Knowledge base search failed: {e}")
            return []
        finally:
            if conn:
                release_db_connection(conn,db_type="lg")


# Singleton instance
embedding_service = EmbeddingService()