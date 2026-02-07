#!/usr/bin/env python3
import requests
import base64
import json
import os

# Imgur API endpoint
UPLOAD_URL = "https://api.imgur.com/3/image"
CLIENT_ID = "546c25a59c58ad7"  # Anonymous upload

def upload_image(image_path, title, description):
    """Upload image to imgur and return the URL"""
    try:
        with open(image_path, 'rb') as img_file:
            # Read and encode image
            img_data = base64.b64encode(img_file.read()).decode()
            
            # Prepare headers and data
            headers = {
                'Authorization': f'Client-ID {CLIENT_ID}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'image': img_data,
                'type': 'base64',
                'title': title,
                'description': description
            }
            
            # Upload to imgur
            response = requests.post(UPLOAD_URL, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            if result['success']:
                return result['data']['link']
            else:
                print(f"Upload failed: {result}")
                return None
                
    except Exception as e:
        print(f"Error uploading {image_path}: {e}")
        return None

if __name__ == "__main__":
    drawings_dir = "/root/jarvis-workspace/jobs/JOB-2026-0206-001/drawings"
    
    # Images to upload
    images = [
        {
            'path': f"{drawings_dir}/01-frame-assembly-v2.png",
            'title': "Frame Assembly - Top View",
            'description': "Professional engineering drawing showing frame construction with measurements"
        },
        {
            'path': f"{drawings_dir}/02-side-view-v2.png",
            'title': "Conveyor Side View - Elevation",
            'description': "Side elevation showing legs, rollers, motor mount and belt path"
        },
        {
            'path': f"{drawings_dir}/03-roller-detail-v2.png",
            'title': "Roller Assembly Detail",
            'description': "Detailed view of roller construction and mounting method"
        },
        {
            'path': f"{drawings_dir}/04-exploded-view-v2.png",
            'title': "Exploded View - All Components",
            'description': "Exploded view showing all parts and assembly sequence"
        },
        {
            'path': f"{drawings_dir}/05-parts-list-v3.png",
            'title': "Parts List - Bill of Materials",
            'description': "Complete parts list with quantities, materials and sources"
        }
    ]
    
    uploaded_urls = []
    
    for img_info in images:
        print(f"Uploading {img_info['title']}...")
        url = upload_image(img_info['path'], img_info['title'], img_info['description'])
        if url:
            print(f"Success: {url}")
            uploaded_urls.append({
                'title': img_info['title'],
                'url': url
            })
        else:
            print(f"Failed to upload {img_info['title']}")
    
    # Save URLs to file for reference
    with open(f"{drawings_dir}/imgur_urls.json", 'w') as f:
        json.dump(uploaded_urls, f, indent=2)
    
    print(f"\nUploaded {len(uploaded_urls)} images successfully!")
    print("URLs saved to imgur_urls.json")