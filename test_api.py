#!/usr/bin/env python3
"""
Script untuk test API Image Processing
"""

import requests
import json
import sys
import os

def test_health_endpoint():
    """Test health endpoint"""
    try:
        response = requests.get('http://100.124.58.32:5001/api/health', timeout=5)
        print(f"Health Check Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error connecting to health endpoint: {e}")
        return False

def test_process_image_endpoint():
    """Test process image endpoint dengan gambar dummy"""
    try:
        # Buat gambar dummy sederhana
        from PIL import Image
        import io
        
        # Buat gambar RGB sederhana 200x200
        img = Image.new('RGB', (200, 200), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
        data = {
            'header_text': 'Test Header',
            'font_color': 'blue'
        }
        
        response = requests.post('http://100.124.58.32:5001/api/process_image', 
                               files=files, data=data, timeout=30)
        
        print(f"Process Image Status: {response.status_code}")
        if response.status_code == 200:
            print("Image processing successful!")
            print(f"Content-Type: {response.headers.get('content-type')}")
            print(f"Content-Length: {len(response.content)} bytes")
            
            # Simpan hasil ke file
            with open('test_output.jpg', 'wb') as f:
                f.write(response.content)
            print("Output saved to test_output.jpg")
            return True
        else:
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error testing process image endpoint: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Image Processing API ===")
    
    # Test health endpoint
    print("\n1. Testing Health Endpoint...")
    health_ok = test_health_endpoint()
    
    if health_ok:
        print("\n2. Testing Process Image Endpoint...")
        process_ok = test_process_image_endpoint()
        
        if process_ok:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Process image test failed!")
    else:
        print("\n❌ Health check failed! Server might not be running.")
        sys.exit(1)

