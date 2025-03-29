from redis_connection import redis_client
import time

class RateLimiter:
    """
    This class implements a simple rate limiting mechanism using a Redis based approach
    """
    def __init__(self, limit_per_second):
        self.limit_per_second = limit_per_second

    def is_allowed(self, user_id):
        """
        This method checks if the user is allowed to make a request based on the rate limit. 
        
        Logic:
            1. Get the current timestamp and round it to the nearest second.
            2. Construct a redis key using the user ID and the current timestamp.
            3. Increment the request count for that key in Redis. (This will create the key if that doesn't exist)
            4. If this is the first request, set an expiration time of 1 second for that key.
            5. If the request count is greater than the limit, return False, i.e The user has exceeded the rate limit.
            6. Otherwise, return True, i.e The user is allowed to make the request.
        
        Args:
            user_id (str): The ID of the user making the request.
            
        Returns:
            bool: True if the request is allowed, False if the rate limit is exceeded.
        """
        current_time = int(time.time())
        key = f"limiting:{user_id}:{current_time}"

        num_requests = redis_client.incr(key)

        if num_requests == 1:
            redis_client.expire(key, 1)

        return num_requests <= self.limit_per_second