"""
Redis Keyspace Notifications Listener for Session Expiry Events

SETUP INSTRUCTIONS:
1. Enable Redis notifications in redis-cli:
   - Open redis-cli
   - Run: CONFIG SET notify-keyspace-events "Ex"
   - The "Ex" flags enable expired key events (E) and keyspace notifications (x)

2. Run this listener in a separate terminal:
   - python redis_listener.py

3. Keep this listener running alongside the FastAPI server:
   - In one terminal: python redis_listener.py (listener)
   - In another terminal: uvicorn openai_main:app --reload (FastAPI server)

The listener subscribes to Redis keyspace expiry events and monitors for sessions
(keys starting with '999999:') to automatically log when they expire.
"""

import redis
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RedisKeyspaceListener:
    """Listens to Redis keyspace notifications for expired session keys."""
    
    def __init__(self, host='localhost', port=6379, db=0):
        """
        Initialize the Redis listener.
        
        Args:
            host (str): Redis host address
            port (int): Redis port
            db (int): Redis database number
        """
        self.host = host
        self.port = port
        self.db = db
        self.redis_client = None
        self.pubsub = None
    
    def connect(self):
        """Establish connection to Redis."""
        try:
            self.redis_client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            logger.info(f"✅ Connected to Redis at {self.host}:{self.port}")
        except redis.ConnectionError as e:
            logger.error(f"❌ Failed to connect to Redis: {e}")
            raise
    
    def start_listening(self):
        """Start listening to keyspace expiry events."""
        if not self.redis_client:
            self.connect()
        
        # Subscribe to keyspace notifications for expired keys
        # Format: __keyevent@{db}__:expired
        self.pubsub = self.redis_client.pubsub()
        channel = f'__keyevent@{self.db}__:expired'
        
        self.pubsub.subscribe(channel)
        logger.info(f"👂 Listening to channel: {channel}")
        logger.info("🎧 Waiting for session expiry events...")
        
        try:
            for message in self.pubsub.listen():
                self._handle_message(message)
        except KeyboardInterrupt:
            logger.info("\n⏹️  Listener stopped by user")
        except Exception as e:
            logger.error(f"❌ Error in listener: {e}")
        finally:
            self.cleanup()
    
    def _handle_message(self, message):
        """
        Process incoming keyspace notification messages.
        
        Args:
            message (dict): Redis message object
        """
        if message['type'] == 'message':
            expired_key = message['data']
            
            # Filter for user session keys (starting with '999999:')
            if expired_key.startswith('999999:'):
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(
                    f"🔔 SESSION EXPIRED: {expired_key} | "
                    f"⏰ Time: {timestamp} | "
                    f"💾 Saving in Vector DB, session dying..."
                )
                logger.info(f"Session expired and logged: {expired_key}")
    
    def cleanup(self):
        """Clean up resources."""
        if self.pubsub:
            self.pubsub.close()
        if self.redis_client:
            self.redis_client.close()
        logger.info("🧹 Cleanup complete")


def main():
    """Main entry point for the Redis keyspace listener."""
    try:
        listener = RedisKeyspaceListener(host='localhost', port=6379, db=0)
        listener.start_listening()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1
    return 0


if __name__ == '__main__':
    exit(main())
