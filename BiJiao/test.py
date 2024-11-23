import os
import random
import string
import concurrent.futures

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def create_file(file_path):
    with open(file_path, 'w') as f:
        f.write(generate_random_string(100))  # Write random content to the file

def create_files_and_dirs(base_path, num_dirs=15, num_files=30, depth=3):
    if depth == 0:
        return

    # Create directories
    dirs = []
    for i in range(num_dirs):
        dir_path = os.path.join(base_path, generate_random_string())
        os.makedirs(dir_path, exist_ok=True)
        dirs.append(dir_path)
        
        # Create some files in the current directory
        files = []
        for _ in range(random.randint(1, num_files // num_dirs + 1)):
            file_name = generate_random_string() + '.txt'
            file_path = os.path.join(dir_path, file_name)
            files.append(file_path)
        
        # Use ThreadPoolExecutor to create files concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(create_file, files)

        # Recursively create subdirectories
        if i < num_dirs // 2:  # Limit recursion depth to keep it manageable
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(create_files_and_dirs, dir_path, num_dirs=num_dirs // 2, num_files=num_files // 2, depth=depth-1) for _ in range(num_dirs // 2)]
                concurrent.futures.wait(futures)

def create_test_directories(base_path_a, base_path_b):
    os.makedirs(base_path_a, exist_ok=True)
    os.makedirs(base_path_b, exist_ok=True)

    # Create test directories with threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(create_files_and_dirs, base_path_a, num_dirs=15, num_files=30, depth=3),
            executor.submit(create_files_and_dirs, base_path_b, num_dirs=15, num_files=30, depth=3)
        ]
        concurrent.futures.wait(futures)

# Define base paths for the test directories
base_path_a = 'D:/test_dir_a'
base_path_b = 'D:/test_dir_b'

# Create the test directories
create_test_directories(base_path_a, base_path_b)
print(f"Test directories created:\n{base_path_a}\n{base_path_b}")
