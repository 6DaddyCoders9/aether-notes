import os
from supabase import create_client, Client

# Get Supabase credentials from environment variables
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# Create a single, reusable Supabase client instance
supabase_client: Client = create_client(url, key)