import os
import random
import subprocess
import re
import sys
import string
import time

class Error(Exception): pass
class EmptyFileException(Error): pass
class RunError(Error): pass

# List of 200 random words for string generation
WORD_LIST = [
    "apple", "banana", "orange", "grape", "kiwi", "mango", "lemon", "lime", "peach", "plum",
    "book", "page", "story", "novel", "chapter", "author", "reader", "library", "shelf", "cover",
    "house", "door", "window", "roof", "floor", "wall", "room", "kitchen", "bathroom", "bedroom",
    "car", "truck", "bike", "train", "plane", "boat", "ship", "motor", "wheel", "driver",
    "computer", "keyboard", "mouse", "screen", "laptop", "tablet", "phone", "camera", "printer", "router",
    "water", "fire", "earth", "wind", "storm", "rain", "snow", "sun", "moon", "star",
    "table", "chair", "desk", "lamp", "sofa", "bed", "drawer", "mirror", "clock", "picture",
    "dog", "cat", "bird", "fish", "rabbit", "horse", "cow", "sheep", "goat", "chicken",
    "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white",
    "run", "walk", "jump", "swim", "fly", "climb", "dance", "sing", "laugh", "cry",
    "happy", "sad", "angry", "afraid", "excited", "tired", "hungry", "thirsty", "hot", "cold",
    "big", "small", "tall", "short", "long", "wide", "narrow", "thick", "thin", "deep",
    "time", "day", "night", "week", "month", "year", "hour", "minute", "second", "moment",
    "music", "song", "dance", "art", "paint", "draw", "write", "read", "speak", "listen",
    "friend", "family", "parent", "child", "baby", "boy", "girl", "man", "woman", "people",
    "school", "teacher", "student", "class", "lesson", "learn", "teach", "study", "test", "grade",
    "food", "meal", "breakfast", "lunch", "dinner", "cook", "recipe", "taste", "flavor", "spice",
    "game", "play", "sport", "team", "win", "lose", "score", "player", "coach", "field",
    "city", "town", "street", "road", "building", "park", "garden", "bridge", "river", "mountain",
    "health", "doctor", "nurse", "hospital", "patient", "disease", "cure", "medicine", "symptom", "treatment"
]

DIRNAME = os.path.abspath(r"C:\Users\Md_Fa\Documents\MiniProject_Code_File\Testcase-Generator\Testcase-Generator\tc_generator")

def get_latest_attempt(operation, directory):
    pattern = re.compile(rf"{operation}attempt(\d+)\.txt")
    max_attempt = 0
    if os.path.exists(directory):
        for fname in os.listdir(directory):
            match = pattern.match(fname)
            if match:
                max_attempt = max(max_attempt, int(match.group(1)))
    return max_attempt + 1

def create_merged_dir(category, operation):
    base_dir = os.path.join(DIRNAME, 'Testcases', category, operation)
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

def generate_palindrome(length, use_words=False):
    if length == 0:  # Handle empty string case
        return ""
        
    if use_words:
        # Generate word-based palindrome
        if length < 5:  # For very short lengths, fall back to character-based
            return generate_palindrome(length, use_words=False)
        
        # Select a word that fits within half the length
        available_words = [w for w in WORD_LIST if len(w) <= length // 2]
        if not available_words:
            return generate_palindrome(length, use_words=False)
            
        word = random.choice(available_words)
        reversed_word = word[::-1]
        
        # For odd length, add a middle character
        if length % 2 == 1:
            middle = random.choice(string.ascii_letters)
            result = word + middle + reversed_word
        else:
            result = word + reversed_word
            
        # If result is too long, truncate
        if len(result) > length:
            result = result[:length]
            
        # Ensure it's at least a palindrome
        if len(result) < length:
            return result.ljust(length, 'a')
        return result
    else:
        # Original character-based palindrome generation
        if length == 0:
            return ""
            
        half_length = length // 2
        chars = random.choices(string.ascii_letters + string.digits, k=half_length)
        
        # For odd length, add a middle character
        if length % 2 == 1:
            middle = random.choice(string.ascii_letters + string.digits)
            return ''.join(chars) + middle + ''.join(reversed(chars))
        else:
            return ''.join(chars) + ''.join(reversed(chars))

def generate_non_palindrome(length, use_words=False):
    if length == 0:  # Handle empty string case
        return ""
        
    if length == 1:  # A single char is always a palindrome, so we can't make a non-palindrome
        return random.choice(string.ascii_letters)
        
    if use_words:
        # Generate word-based non-palindrome
        if length < 5:  # For very short lengths, fall back to character-based
            return generate_non_palindrome(length, use_words=False)
            
        # Take 2-3 random words
        words = []
        current_length = 0
        
        while current_length < length:
            word = random.choice(WORD_LIST)
            if current_length + len(word) + 1 > length:  # +1 for space
                if length - current_length > 1:
                    words.append(word[:length-current_length])
                break
            words.append(word)
            current_length += len(word) + 1  # +1 for space
            
        result = ' '.join(words)
        
        # Ensure it's not accidentally a palindrome
        if result == result[::-1]:
            # Make a small change to break the palindrome
            if len(result) > 1:
                char_index = random.randint(0, len(result) // 2 - 1)
                result_list = list(result)
                current_char = result_list[char_index]
                new_char = current_char
                while new_char == current_char:
                    new_char = random.choice(string.ascii_letters)
                result_list[char_index] = new_char
                result = ''.join(result_list)
                
        return result
    else:
        # Original character-based non-palindrome generation
        while True:
            s = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
            # Ensure it's not accidentally a palindrome
            if s != s[::-1]:
                return s
            # For very short strings, if we can't generate a non-palindrome easily, 
            # just make a minor addition to break the palindrome
            if length <= 3:
                s += random.choice(string.ascii_letters)
                return s[:length]

def generate_random_word_string(length, use_words=True):
    """Generate a random string using either words or characters."""
    if length == 0:  # Handle empty string case
        return ""
        
    if use_words:
        # Generate a string of random words
        result = []
        current_length = 0
        
        while current_length < length:
            # Pick a random word
            word = random.choice(WORD_LIST)
            
            # Check if we need to truncate the word to fit the exact length
            if current_length + len(word) > length:
                word = word[:length - current_length]
            
            result.append(word)
            current_length += len(word)
            
            # Add a space between words if there's room
            if current_length < length - 1:
                result.append(" ")
                current_length += 1
                
        return ''.join(result)
    else:
        # Generate a string of random characters
        char_set = string.ascii_letters + string.digits
        return ''.join(random.choice(char_set) for _ in range(length))

def generate_batch(operation, num_cases, array_type=None, min_val=None, max_val=None, rows=None, cols=None, 
                   min_length=None, max_length=None, use_words=False):
    # Start timing for generation
    start_time = time.time()
    
    category = 'array' if array_type else 'string'
    out_dir = create_merged_dir(category, operation)
    attempt_num = get_latest_attempt(operation, out_dir)

    merged_file = os.path.join(out_dir, f"{operation}attempt{attempt_num}.txt")

    inputs = []
    with open(merged_file, 'w') as f:
        f.write(f"Operation: {operation}\n\n")
        
        # Calculate number of edge cases to include (1 in 5 test cases)
        num_edge_cases = max(1, num_cases // 5)
        edge_case_indices = random.sample(range(1, num_cases+1), num_edge_cases)
        
        for i in range(1, num_cases+1):
            input_lines = []
            input_lines.append(f"Input {i}")

            # Check if this should be an edge case
            is_edge_case = i in edge_case_indices

            if array_type == "1d":
                if is_edge_case:
                    # Edge case: empty array or single element array
                    edge_type = random.choice(["empty", "single"])
                    if edge_type == "empty":
                        arr = []
                    else:
                        arr = [random.randint(min_val, max_val)]
                else:
                    arr = [random.randint(min_val, max_val) for _ in range(cols)]
                input_lines.append(' '.join(map(str, arr)))

            elif array_type == "2d":
                if is_edge_case:
                    # Edge case: 1x1 matrix or matrix with some empty rows
                    edge_type = random.choice(["tiny", "empty_row"])
                    if edge_type == "tiny":
                        rows_to_use, cols_to_use = 1, 1
                    else:
                        rows_to_use, cols_to_use = rows, 1
                else:
                    rows_to_use, cols_to_use = rows, cols
                    
                input_lines.append(f"{rows_to_use} {cols_to_use}")
                for _ in range(rows_to_use):
                    row = [random.randint(min_val, max_val) for _ in range(cols_to_use)]
                    input_lines.append(' '.join(map(str, row)))

            elif category == "string":
                if is_edge_case:
                    # Edge case: empty string, single character, or all same character
                    edge_type = random.choice(["empty", "single", "same"])
                    if edge_type == "empty":
                        random_string = ""
                    elif edge_type == "single":
                        random_string = random.choice(string.ascii_letters)
                    else:
                        char = random.choice(string.ascii_letters)
                        random_string = char * random.randint(2, 10)
                else:
                    # Regular case: Generate random string length within the specified range
                    string_length = random.randint(min_length, max_length)
                    
                    # Special handling for palindrome check to ensure 3:2 ratio (true:false)
                    if operation == "palindromecheck":
                        # Calculate true/false distribution for desired 3:2 ratio
                        true_count = int(num_cases * 0.6)  # 60% true (3/5)
                        false_count = num_cases - true_count  # 40% false (2/5)
                        
                        # Determine if this should be a palindrome based on current index
                        should_be_palindrome = i <= true_count
                        
                        # Generate string based on whether it should be palindrome or not
                        if should_be_palindrome:
                            random_string = generate_palindrome(string_length, use_words)
                        else:
                            random_string = generate_non_palindrome(string_length, use_words)
                    else:
                        # Check if we should use words or characters
                        if use_words:
                            random_string = generate_random_word_string(string_length, use_words=True)
                        else:
                            # Original character-based generation
                            if i <= 3:
                                random_string = ''.join(random.choice(string.ascii_letters) for _ in range(string_length))
                            elif i == 4:
                                random_string = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(string_length))
                            else:
                                random_string = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(string_length))
                
                input_lines.append(random_string)

            inputs.append(input_lines)
    
    # Calculate generation time
    generation_time = time.time() - start_time
    
    # Store inputs and generation time for later processing
    return merged_file, attempt_num, category, inputs, generation_time

def execute_solution(merged_file, operation, inputs, generation_time):
    # Start timing for execution
    start_time = time.time()
    
    results = []
    for i, input_lines in enumerate(inputs, 1):
        # Prepare input for the solution script
        solution_input = operation + "\n" + "\n".join(input_lines)
        
        # Run the solution script
        process = subprocess.run(
            ['python', os.path.join(DIRNAME, 'solution.py')],
            input=solution_input,
            capture_output=True,
            text=True
        )
        
        # Get output excluding the "Input X:" line which will be added separately
        output_lines = process.stdout.strip().split('\n')
        if len(output_lines) > 1:
            output_text = '\n'.join(output_lines[1:])  # Skip the "Input X:" line from solution output
        else:
            output_text = ""
            
        results.append(output_text)
    
    # Calculate execution time
    execution_time = time.time() - start_time
    total_time = generation_time + execution_time
    
    # Write the inputs, outputs, and time info to the file in the desired format
    with open(merged_file, 'w') as f:
        f.write(f"Operation: {operation}\n\n")
        
        for i, (input_lines, output) in enumerate(zip(inputs, results), 1):
            # Write input
            f.write(f"INPUT {i}\n")
            f.write('\n'.join(input_lines[1:]) + '\n')  # Skip the "Input X" header
            
            # Write output
            f.write(f"OUTPUT {i}\n")
            f.write(output + '\n\n')
        
        # Add execution time information at the end of the file
        f.write(f"EXECUTION TIME\n")
        f.write(f"Generation Time: {generation_time:.4f} seconds\n")
        f.write(f"Solution Execution Time: {execution_time:.4f} seconds\n")
        f.write(f"Total Time: {total_time:.4f} seconds\n")
    
    return merged_file, total_time

def get_valid_int_input(prompt, min_val=None, max_val=None):
    """Get a valid integer input from the user with range validation."""
    while True:
        try:
            value = input(prompt)
            int_value = int(value)
            
            if min_val is not None and int_value < min_val:
                print(f"❌ Error: Value must be at least {min_val}. Please try again.")
                continue
                
            if max_val is not None and int_value > max_val:
                print(f"❌ Error: Value must be at most {max_val}. Please try again.")
                continue
                
            return int_value
        except ValueError:
            print("❌ Error: Please enter a valid integer.")

def main():
    try:
        # Start timing the overall process
        overall_start_time = time.time()
        
        num_cases = get_valid_int_input("Number of test cases per attempt: ", min_val=1)

        print("\nChoose Operation Type:")
        print("1. Array Operations")
        print("2. String Operations")
        choice = get_valid_int_input("Enter choice (1/2): ", min_val=1, max_val=2)

        if choice == 1:
            print("\nArray Type:")
            print("1. 1D Array")
            print("2. 2D Array")
            array_type_choice = get_valid_int_input("Select type (1/2): ", min_val=1, max_val=2)
            array_type = "1d" if array_type_choice == 1 else "2d"

            arr_rows = get_valid_int_input("Rows (1D = 1 row, 2D = #rows): ", min_val=1) if array_type == "2d" else 1
            arr_cols = get_valid_int_input("Columns (1D = size, 2D = #columns): ", min_val=1)
            min_val = get_valid_int_input("Minimum value: ")
            max_val = get_valid_int_input("Maximum value: ", min_val=min_val)

            if array_type == "1d":
                operations = [
                    "sumofelements", "productofelements", "maxminelement",
                    "reversearray", "sortarray", "prefixsum", "suffixsum"
                ]
            else:
                operations = [
                    "diagonalsum", "transpose", "spiralprinting",
                    "zigzagprinting", "lowertriangularmatrix"
                ]

            print("\nAvailable Operations:")
            for idx, op in enumerate(operations, 1):
                print(f"{idx}. {op.title()}")
            op_choice = get_valid_int_input(f"Select operation (1-{len(operations)}): ", min_val=1, max_val=len(operations)) - 1
            operation = operations[op_choice]

            merged_file, attempt, category, inputs, generation_time = generate_batch(
                operation, num_cases, array_type, min_val, max_val, arr_rows, arr_cols
            )

        elif choice == 2:
            # MODIFIED PART: Ask for string length parameters BEFORE operation selection
            print("\nString Generation Parameters:")
            # Get min and max string length from user
            min_length = get_valid_int_input("Minimum string length: ", min_val=0)
            max_length = get_valid_int_input("Maximum string length: ", min_val=min_length)
            
            # Ask if we should use words or random characters
            print("\nString Generation Method:")
            print("1. Random Characters")
            print("2. Random Words")
            string_method = get_valid_int_input("Select method (1/2): ", min_val=1, max_val=2)
            use_words = (string_method == 2)
            
            if use_words:
                print("\n⭐ Using random words from a predefined list of 200 words")
            else:
                print("\n⭐ Using random characters")
            
            # Now ask for the operation selection
            string_operations = [
                "stringreverse", "uppercase", "lowercase",
                "palindromecheck", "vowelcount", "substringcount"
            ]
            print("\nAvailable String Operations:")
            for idx, op in enumerate(string_operations, 1):
                print(f"{idx}. {op.title()}")
            op_choice = get_valid_int_input(f"Select operation (1-{len(string_operations)}): ", min_val=1, max_val=len(string_operations)) - 1
            operation = string_operations[op_choice]

            merged_file, attempt, category, inputs, generation_time = generate_batch(
                operation, num_cases, min_length=min_length, max_length=max_length, use_words=use_words
            )

        merged_file, total_time = execute_solution(merged_file, operation, inputs, generation_time)

        print(f"\n✅ Success! Created attempt {attempt}")
        print(f"📄 File: {os.path.basename(merged_file)}")
        print(f"📁 Location: {os.path.dirname(merged_file)}")
        print(f"⏱ Total execution time: {total_time:.4f} seconds")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main()