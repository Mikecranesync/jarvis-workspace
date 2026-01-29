#!/usr/bin/env python3
"""
Batch process ride manual images to extract text content
"""
import os
import glob
from pathlib import Path

# Set up paths
base_path = Path("projects/factorylm/knowledge-base/ride-manual")
image_dir = base_path
extract_dir = base_path / "extracted"

# Get all images
image_files = sorted(glob.glob(str(image_dir / "PXL_*.jpg")))

print(f"Found {len(image_files)} images to process")
print("Images:")
for img in image_files[:10]:  # Show first 10
    print(f"  - {os.path.basename(img)}")

if len(image_files) > 10:
    print(f"  ... and {len(image_files) - 10} more")

# Create content structure for manual
sections = {
    "Department Overview": [],
    "Safety Procedures": [],
    "Operational Procedures": [],
    "Maintenance Requirements": [],
    "Emergency Procedures": [],
    "Specifications": [],
    "Leadership Roles": []
}

print(f"\nExtraction directory: {extract_dir}")
print("Ready to process images with image analysis tool...")