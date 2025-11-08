import os
import imagehash
from PIL import Image

def find_and_delete_visual_duplicates(folder_path, hash_size=8, threshold=5):

    seen_hashes = {}
    deleted_files = []

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp")):
                file_path = os.path.join(root, filename)
                try:
                    img = Image.open(file_path).convert("RGB")
                    img_hash = imagehash.average_hash(img, hash_size)

                    # Compare to existing hashes
                    duplicate_found = False
                    for existing_hash, existing_path in seen_hashes.items():
                        if abs(img_hash - existing_hash) <= threshold:
                            print(f"🗑️ Duplicate found:\n  {file_path}\n  -> same as {existing_path}\n")
                            os.remove(file_path)
                            deleted_files.append(file_path)
                            duplicate_found = True
                            break

                    if not duplicate_found:
                        seen_hashes[img_hash] = file_path

                except Exception as e:
                    print(f"⚠️ Could not process {file_path}: {e}")

    print("\n✅ Scan complete.")
    print(f"Total duplicates deleted: {len(deleted_files)}")
    return deleted_files


if __name__ == "__main__":
    folder = input("Enter the folder path to scan for duplicates: ").strip('"')
    if os.path.exists(folder):
        find_and_delete_visual_duplicates(folder)
    else:
        print("❌ Folder not found.")
