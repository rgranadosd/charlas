#!/usr/bin/env python3
"""
Test script to verify MCP endpoint is working correctly
"""
import json
import httpx

BASE_URL = "http://localhost:8080"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing /health endpoint...")
    response = httpx.get(f"{BASE_URL}/health")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}\n")

def test_mcp_initialization():
    """Test MCP initialization"""
    print("🔌 Testing MCP initialization...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    try:
        response = httpx.post(
            f"{BASE_URL}/mcp",
            json=init_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=10.0
        )
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {json.dumps(response.json(), indent=2)}\n")
        else:
            print(f"  Error: {response.text}\n")
    except Exception as e:
        print(f"  Error: {e}\n")

def test_list_tools():
    """Test listing available tools"""
    print("🔧 Testing tools/list...")
    
    # First initialize
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    }
    
    try:
        httpx.post(
            f"{BASE_URL}/mcp", 
            json=init_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=5.0
        )
        
        # List tools
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = httpx.post(
            f"{BASE_URL}/mcp",
            json=list_request,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=10.0
        )
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if "result" in data and "tools" in data["result"]:
                print(f"  Available tools: {len(data['result']['tools'])}")
                for tool in data['result']['tools']:
                    print(f"    - {tool.get('name', 'unknown')}")
            else:
                print(f"  Response: {json.dumps(data, indent=2)}")
        else:
            print(f"  Error: {response.text}\n")
    except Exception as e:
        print(f"  Error: {e}\n")

if __name__ == "__main__":
    print("=" * 60)
    print("MCP Endpoint Testing")
    print("=" * 60 + "\n")
    
    test_health()
    test_mcp_initialization()
    test_list_tools()
    
    print("=" * 60)
    print("Testing complete!")
    print("=" * 60)
