import os

class FileService:
    """
    Handles file operations, such as checking existence and user confirmation for file transfers.
    """
    @staticmethod
    def file_exists(file_name):
        return os.path.exists(f"./files/{file_name}")

    @staticmethod
    def read_file_in_chunks(file_path, chunk_size=200):
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    @staticmethod
    def write_chunk_to_file(file_path, chunk, mode='a'):
        with open(file_path, mode, encoding='utf-8') as file:
            file.write(chunk)
            
    @staticmethod
    def prompt_user_confirmation():
        return input("Do you want to proceed with the file transfer? (y/n): ").lower() == 'y'
