import pytest 
import json

def test_productionplan(client):
  with open('example_payloads/payload1.json', 'r') as payload_file:
    response = client.post("/productionplan", json=json.load(payload_file))
    print(response.data)
    assert b'powerplants' in response.data
    
