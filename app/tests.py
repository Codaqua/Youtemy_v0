from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)

#first Test
def test_get_home_status():
    path = "/"
    # python requests
    # r = requests.get(path)
    response = client.get(path)
    status_code = response.status_code
    content_type = response.headers['content-type']
    assert status_code == 200 # HTTP response
    assert content_type == "application/json"

# Run python -m pip install -r app/requirements.txt
# ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'app/requirements.txt'

# Notice:  A new release of pip is available: 23.0.1 -> 23.1.1
# Notice:  To update, run: pip install --upgrade pip
# Error: Process completed with exit code 1.