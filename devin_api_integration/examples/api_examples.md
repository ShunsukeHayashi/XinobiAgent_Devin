# Devin API Examples

## Example 1: Creating a New Devin Session

```python
import requests
import os

# API configuration
api_key = os.environ.get("DEVIN_API_KEY")
base_url = "https://api.devin.ai/v1"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Create a new session
def create_session(prompt, playbook_id=None):
    """
    Create a new Devin session with the given prompt and optional playbook ID.
    
    Args:
        prompt: The task description for Devin
        playbook_id: Optional playbook ID to guide execution
        
    Returns:
        The session ID if successful, None otherwise
    """
    url = f"{base_url}/sessions"
    
    # Prepare request data
    data = {
        "prompt": prompt
    }
    
    # Add playbook ID if provided
    if playbook_id:
        data["playbook_id"] = playbook_id
    
    # Send request
    response = requests.post(url, headers=headers, json=data)
    
    # Check if request was successful
    if response.status_code == 200:
        return response.json().get("session_id")
    else:
        print(f"Error creating session: {response.status_code}")
        print(response.text)
        return None

# Example usage
prompt = "Create a to-do list app using Vue"
playbook_id = "playbook-e40fe364a84a45f78a86d1f60d7ea1fd"
session_id = create_session(prompt, playbook_id)

if session_id:
    print(f"Session created with ID: {session_id}")
else:
    print("Failed to create session")
```

## Example 2: Sending a Message to an Existing Session

```python
import requests
import os

# API configuration
api_key = os.environ.get("DEVIN_API_KEY")
base_url = "https://api.devin.ai/v1"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Send a message to a session
def send_message(session_id, message):
    """
    Send a message to an existing Devin session.
    
    Args:
        session_id: The ID of the session to send the message to
        message: The message to send
        
    Returns:
        True if successful, False otherwise
    """
    url = f"{base_url}/session/{session_id}/message"
    
    # Prepare request data
    data = {
        "message": message
    }
    
    # Send request
    response = requests.post(url, headers=headers, json=data)
    
    # Check if request was successful
    if response.status_code == 200:
        return True
    else:
        print(f"Error sending message: {response.status_code}")
        print(response.text)
        return False

# Example usage
session_id = "session-123456"
message = "Add a pagination feature to the Vue app"
success = send_message(session_id, message)

if success:
    print(f"Message sent to session {session_id}")
else:
    print("Failed to send message")
```

## Example 3: Uploading a File to a Session

```python
import requests
import os

# API configuration
api_key = os.environ.get("DEVIN_API_KEY")
base_url = "https://api.devin.ai/v1"

# Headers for authentication (without Content-Type for multipart/form-data)
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Upload a file
def upload_file(file_path):
    """
    Upload a file to be used in Devin sessions.
    
    Args:
        file_path: Path to the file to upload
        
    Returns:
        The attachment ID if successful, None otherwise
    """
    url = f"{base_url}/attachments"
    
    # Prepare file for upload
    with open(file_path, "rb") as file:
        files = {
            "file": (os.path.basename(file_path), file)
        }
        
        # Send request
        response = requests.post(url, headers=headers, files=files)
    
    # Check if request was successful
    if response.status_code == 200:
        return response.json().get("attachment_id")
    else:
        print(f"Error uploading file: {response.status_code}")
        print(response.text)
        return None

# Example usage
file_path = "requirements.txt"
attachment_id = upload_file(file_path)

if attachment_id:
    print(f"File uploaded with ID: {attachment_id}")
else:
    print("Failed to upload file")
```

## Example 4: Getting Session Details

```python
import requests
import os

# API configuration
api_key = os.environ.get("DEVIN_API_KEY")
base_url = "https://api.devin.ai/v1"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {api_key}"
}

# Get session details
def get_session_details(session_id):
    """
    Get details of a specific Devin session.
    
    Args:
        session_id: The ID of the session to get details for
        
    Returns:
        The session details if successful, None otherwise
    """
    url = f"{base_url}/session/{session_id}"
    
    # Send request
    response = requests.get(url, headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error getting session details: {response.status_code}")
        print(response.text)
        return None

# Example usage
session_id = "session-123456"
session_details = get_session_details(session_id)

if session_details:
    print(f"Session details: {session_details}")
else:
    print("Failed to get session details")
```
