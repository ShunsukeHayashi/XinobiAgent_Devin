# Devin API Structure Research
## API Endpoints
Based on the repository analysis, the Devin API has the following endpoints:
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/sessions` | POST | Create a new Devin session |
| `/sessions` | GET | List all Devin sessions |
| `/session/{session_id}` | GET | Get details of a specific session |
| `/session/{session_id}/message` | POST | Send a message to a session |
| `/secrets` | GET | List all secrets |
| `/secrets/{secret_id}` | DELETE | Delete a secret |
| `/attachments` | POST | Upload a file |
