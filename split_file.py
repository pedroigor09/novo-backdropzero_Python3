import os

def split_file(file_path, chunk_size):
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        chunk_count = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            chunk_file = f"{file_path}.part.{chunk_count:03}"
            with open(chunk_file, 'wb') as chunk_f:
                chunk_f.write(chunk)
            chunk_count += 1
            print(f"Created: {chunk_file}")

if __name__ == "__main__":
    split_file('saved_models/u2net/u2net.pth', 100 * 1024 * 1024)  # 100 MB
