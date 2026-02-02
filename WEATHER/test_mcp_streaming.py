#!/usr/bin/env python3
"""
Test MCP Server with proper HTTP Streaming support
"""
import json
import requests  # Better for SSE streaming than httpx

BASE_URL = "http://localhost:8080"

def test_mcp_with_session():
    """Test MCP with proper session handling"""
    print("🔌 Testing MCP with session...")
    
    # Start a session
    with requests.Session() as session:
        # Initialize
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
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"
        }
        
        print("  📤 Sending initialize...")
        response = session.post(
            f"{BASE_URL}/mcp",
            json=init_request,
            headers=headers,
            timeout=10.0,
            stream=True
        )
        
        print(f"  Status: {response.status_code}")
        print(f"  Content-Type: {response.headers.get('Content-Type', 'unknown')}")
        
        # Try to read SSE stream
        if "text/event-stream" in response.headers.get("Content-Type", ""):
            print("  📡 Reading SSE stream...")
            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data:"):
                        data = decoded[5:].strip()
                        if data:
                            try:
                                parsed = json.loads(data)
                                print(f"  ✅ Received: {json.dumps(parsed, indent=2)}")
                            except json.JSONDecodeError:
                                print(f"  Raw: {data}")
        else:
            # Regular JSON response
            try:
                data = response.json()
                print(f"  Response: {json.dumps(data, indent=2)}")
            except:
                print(f"  Response: {response.text}")
        
        print("\n  📤 Listing tools...")
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response2 = session.post(
            f"{BASE_URL}/mcp",
            json=list_request,
            headers=headers,
            timeout=10.0,
            stream=True
        )
        
        print(f"  Status: {response2.status_code}")
        
        # Try to read SSE stream
        if "text/event-stream" in response2.headers.get("Content-Type", ""):
            print("  📡 Reading SSE stream...")
            for line in response2.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith("data:"):
                        data = decoded[5:].strip()
                        if data and data != "[DONE]":
                            try:
                                parsed = json.loads(data)
                                if "result" in parsed and "tools" in parsed["result"]:
                                    tools = parsed["result"]["tools"]
                                    print(f"  ✅ Available tools: {len(tools)}")
                                    for tool in tools:
                                        print(f"    - {tool.get('name', 'unknown')}: {tool.get('description', '')[:60]}...")
                                else:
                                    print(f"  Received: {json.dumps(parsed, indent=2)}")
                            except json.JSONDecodeError:
                                print(f"  Raw: {data}")
        else:
            try:
                data = response2.json()
                print(f"  Response: {json.dumps(data, indent=2)}")
            except:
                print(f"  Response: {response2.text}")

if __name__ == "__main__":
    print("=" * 70)
    print("MCP HTTP Streaming Test")
    print("=" * 70 + "\n")
    
    # Check health first
    print("🏥 Health check...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5.0)
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}\n")
    except Exception as e:
        print(f"  Error: {e}\n")
        exit(1)
    
    test_mcp_with_session()
    
    print("\n" + "=" * 70)
    print("Testing complete!")
    print("=" * 70)
