import hashlib

def calculate_hashes(file_path):
  md5 = hashlib.md5()
  sha256 = hashlib.sha256()

  with open(file_path, "rb") as file:
    while chunk := file.read(8192):
      md5.update(chunk)
      sha256.update(chunk)

  return {
      "md5": md5.hexdigest(),
      "sha256": sha256.hexdigest()
  }
      
      
