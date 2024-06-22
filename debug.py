from models import storage
from models.user import User

# Reload storage to ensure it's populated
storage.reload()

# User ID to check
user_id = '89982d93-dfe1-447f-b2dd-dca03de8871c'

# Fetch user
user = storage.get(User, user_id)

if user:
    print("User found:", user.to_dict())
else:
    print("User not found")

