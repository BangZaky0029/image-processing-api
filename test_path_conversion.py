import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the image_path module
from image_controller_api.image_utils.image_path import get_image_path, path_to_url, get_brand_from_path

def test_path_conversion():
    # Test get_image_path
    print("\nTesting get_image_path:")
    path = get_image_path('Marsoto', 'NM', 'HM0049')
    print(f"Path: {path}")
    print("Contains backslashes: " + str('\\' in path))
    
    # Test path_to_url
    print("\nTesting path_to_url:")
    url = path_to_url(path)
    print(f"URL: {url}")
    print("Contains backslashes or %5C: " + str('\\' in url or '%5C' in url))
    
    # Test get_brand_from_path
    print("\nTesting get_brand_from_path:")
    brand = get_brand_from_path(path)
    print(f"Brand: {brand}")

if __name__ == "__main__":
    test_path_conversion()