def upload_file(filename:str , content:bytes):
    file_path = f"uploads/{filename}"
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path

def write_file(content : str , name : str):
    file_path = f"reports/{name}.txt"
    with open(file_path , "a+") as f:
        f.write(content)