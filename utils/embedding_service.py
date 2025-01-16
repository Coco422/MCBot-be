from typing import List
import numpy as np
from database.connection import get_db_connection, release_db_connection
import os
import aiohttp
import asyncio

# ----------配置日志-------------
from utils.ray_logger import LoggerHandler
log_file = "main.log"
logger = LoggerHandler(logger_level='DEBUG',file="logs/"+log_file)
# -----------日志配置完成----------
class EmbeddingService:
    def __init__(self, model_name: str = "text-embedding-ada-002"):
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
        service_url = os.getenv("EMBEDDING_SERVICE_URL", "http://172.16.99.32:8989/getBGEencodeByText")
        
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
                            # Parse the response JSON
                            result = await response.json()
                            # Assuming the response contains a field "embedding" with the vector
                            if "embedding" in result:
                                return result["embedding"]
                            else:
                                raise ValueError("Response does not contain 'embedding' field")
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
    
    async def search_similar(self, embedding: List[float], top_k: int = 3) -> List[dict]:
        """Search for similar content in database using embedding vector"""
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Convert embedding to PostgreSQL array format
            embedding_array = "[" + ",".join(map(str, embedding)) + "]"
            
            # Updated query to call the stored procedure
            query = """
            SELECT * FROM "tobacco"."use_vec_get_top_laws"(%s::public.vector)
            LIMIT %s;
            """
            cursor.execute(query, (embedding_array, top_k))
            results = cursor.fetchall()
            
            # Map the results to a list of dictionaries
            return [{
                "law_id": row[0],
                "law_name": row[1],
                "chapter": row[2],
                "article_content": row[3],
                "referenced_article_1": row[4],
                "referenced_article_content_1": row[5],
                "referenced_article_2": row[6],
                "referenced_article_content_2": row[7],
                "similarity": float(row[8])
            } for row in results]
            
        except Exception as e:
            logger.error(f"Database search failed: {e}")
            return []
        finally:
            if conn:
                release_db_connection(conn)

# Singleton instance
embedding_service = EmbeddingService()