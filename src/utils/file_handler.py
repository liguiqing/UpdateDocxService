def save_uploaded_file(uploaded_file, destination):
    with open(destination, 'wb') as f:
        f.write(uploaded_file.read())

def delete_temp_file(file_path):
    import os
    if os.path.exists(file_path):
        os.remove(file_path)

def return_updated_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()