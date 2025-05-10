import sys

def handle_1d_array_operation(op, arr):
    """Handle operations for 1D arrays with edge case handling."""
    if not arr:  # Handle empty array edge case
        if op == "sumofelements":
            return "0"  # Sum of empty array is 0
        elif op == "productofelements":
            return "1"  # Empty product is typically 1 (identity element)
        elif op == "maxminelement":
            return "N/A N/A"  # No max/min for empty array
        elif op == "reversearray":
            return ""  # Empty array reversed is still empty
        elif op == "sortarray":
            return ""  # Empty array sorted is still empty
        elif op == "prefixsum":
            return ""  # No prefix sum for empty array
        elif op == "suffixsum":
            return ""  # No suffix sum for empty array
        return "Empty array"
    
    # Normal operations on non-empty arrays
    if op == "sumofelements":
        return str(sum(arr))
    elif op == "productofelements":
        prod = 1
        for num in arr:
            prod *= num
        return str(prod)
    elif op == "maxminelement":
        return f"{max(arr)} {min(arr)}"
    elif op == "reversearray":
        return ' '.join(map(str, arr[::-1]))
    elif op == "sortarray":
        return ' '.join(map(str, sorted(arr)))
    elif op == "prefixsum":
        prefix = []
        total = 0
        for num in arr:
            total += num
            prefix.append(total)
        return ' '.join(map(str, prefix))
    elif op == "suffixsum":
        suffix = []
        total = 0
        for num in reversed(arr):
            total += num
            suffix.append(total)
        return ' '.join(map(str, reversed(suffix)))
    return "Invalid operation"

def handle_2d_array_operation(op, matrix):
    """Handle operations for 2D arrays with edge case handling."""
    if not matrix or len(matrix) == 0 or len(matrix[0]) == 0:  # Handle empty matrix edge cases
        if op == "diagonalsum":
            return "0"  # Sum of empty diagonal is 0
        elif op == "transpose":
            return []  # Empty matrix transpose is still empty
        elif op == "spiralprinting":
            return ""  # No spiral for empty matrix
        elif op == "zigzagprinting":
            return ""  # No zigzag for empty matrix
        elif op == "lowertriangularmatrix":
            return []  # No lower triangular for empty matrix
        return "Empty matrix"
    
    # Handle special case for 1x1 matrix
    if len(matrix) == 1 and len(matrix[0]) == 1:
        if op == "diagonalsum":
            return str(matrix[0][0])  # Sum of single element diagonal
        elif op == "transpose":
            return [' '.join(map(str, matrix[0]))]  # Transpose of 1x1 is itself
        elif op == "spiralprinting":
            return str(matrix[0][0])  # Spiral of 1x1 is just the element
        elif op == "zigzagprinting":
            return str(matrix[0][0])  # Zigzag of 1x1 is just the element
        elif op == "lowertriangularmatrix":
            return [' '.join(map(str, matrix[0]))]  # Lower triangular of 1x1 is itself
    
    # Normal operations on regular matrices
    if op == "diagonalsum":
        return str(sum(matrix[i][i] for i in range(min(len(matrix), len(matrix[0])))))
    elif op == "transpose":
        # Handle matrices with different numbers of rows/columns
        cols = len(matrix[0])
        transposed = [[matrix[j][i] if i < len(matrix[j]) else 0 for j in range(len(matrix))] for i in range(cols)]
        return [' '.join(map(str, row)) for row in transposed]
    elif op == "spiralprinting":
        result = []
        if not matrix or not matrix[0]:
            return ""
        top, bottom = 0, len(matrix)-1
        left, right = 0, len(matrix[0])-1
        while top <= bottom and left <= right:
            for i in range(left, right+1):
                result.append(matrix[top][i])
            top += 1
            for i in range(top, bottom+1):
                result.append(matrix[i][right])
            right -= 1
            if top <= bottom:
                for i in range(right, left-1, -1):
                    result.append(matrix[bottom][i])
                bottom -= 1
            if left <= right:
                for i in range(bottom, top-1, -1):
                    result.append(matrix[i][left])
                left += 1
        return ' '.join(map(str, result))
    elif op == "zigzagprinting":
        result = []
        for i in range(len(matrix)):
            row = matrix[i] if i % 2 == 0 else list(reversed(matrix[i]))
            result.extend(row)
        return ' '.join(map(str, result))
    elif op == "lowertriangularmatrix":
        output = []
        for i in range(len(matrix)):
            row = [(matrix[i][j] if j <= i and j < len(matrix[i]) else 0) for j in range(max(len(row) for row in matrix))]
            output.append(' '.join(map(str, row)))
        return output
    return "Invalid operation"

def handle_string_operation(op, s):
    """Handle operations for strings with edge case handling."""
    # Handle empty string edge case
    if s == "":
        if op == "stringreverse":
            return ""  # Empty string reversed is still empty
        elif op == "uppercase":
            return ""  # Empty string uppercase is still empty
        elif op == "lowercase":
            return ""  # Empty string lowercase is still empty
        elif op == "palindromecheck":
            return "true"  # Empty string is a palindrome by definition
        elif op == "vowelcount":
            return "0"  # No vowels in empty string
        elif op == "substringcount":
            return "\nCOUNT: 0"  # No substrings in empty string
        return "Empty string"
    
    # Normal operations on non-empty strings
    if op == "stringreverse":
        return s[::-1]
    elif op == "uppercase":
        return s.upper()
    elif op == "lowercase":
        return s.lower()
    elif op == "palindromecheck":
        return "true" if s == s[::-1] else "false"
    elif op == "vowelcount":
        return str(sum(1 for c in s.lower() if c in "aeiou"))
    elif op == "substringcount":
        # Generate all possible substrings and count them
        substrings = []
        for i in range(len(s)):
            for j in range(i + 1, len(s) + 1):
                substrings.append(s[i:j])
        
        count = len(substrings)
        # Format output as requested: display all substrings and the count
        return ', '.join(substrings) + f"\nCOUNT: {count}"
    return "Invalid operation"

def main():
    try:
        lines = [line.strip() for line in sys.stdin if line.strip()]
        if not lines:
            print("Error: No input provided")
            return

        # First line is the operation
        operation = lines[0]
        
        # Skip the operation line and look for input pattern
        i = 1
        while i < len(lines):
            if not lines[i].startswith("Input"):
                i += 1
                continue
                
            # Extract input number from "Input X" format
            input_num = lines[i].split()[1]
            i += 1  # Move to the actual input data
            
            try:
                if operation in [
                    "sumofelements", "productofelements", "maxminelement",
                    "reversearray", "sortarray", "prefixsum", "suffixsum"
                ]:
                    if i < len(lines):
                        # Handle empty array case
                        if not lines[i].strip():
                            arr = []
                        else:
                            arr = list(map(int, lines[i].split()))
                        i += 1
                        result = handle_1d_array_operation(operation, arr)
                        print(f"Input {input_num}")
                        print(f"{result}")
                        
                elif operation in [
                    "diagonalsum", "transpose", "spiralprinting",
                    "zigzagprinting", "lowertriangularmatrix"
                ]:
                    if i < len(lines):
                        try:
                            if not lines[i].strip():
                                # Empty input case
                                print(f"Input {input_num}")
                                print("Error: Empty matrix specification")
                                i += 1
                                continue
                                
                            rows, cols = map(int, lines[i].split())
                            i += 1
                            
                            matrix = []
                            for _ in range(rows):
                                if i < len(lines):
                                    if not lines[i].strip():  # Empty row
                                        matrix.append([])
                                    else:
                                        matrix.append(list(map(int, lines[i].split())))
                                    i += 1
                                else:
                                    break
                                    
                            print(f"Input {input_num}")
                            if operation == "transpose" or operation == "lowertriangularmatrix":
                                result = handle_2d_array_operation(operation, matrix)
                                if result:
                                    for row in result:
                                        print(row)
                                else:
                                    print("Empty result")
                            else:
                                result = handle_2d_array_operation(operation, matrix)
                                print(f"{result}")
                        except ValueError:
                            print(f"Input {input_num}")
                            print(f"Error: Invalid matrix format")
                            
                elif operation in [
                    "stringreverse", "uppercase", "lowercase",
                    "palindromecheck", "vowelcount", "substringcount"
                ]:
                    # Complete string operations handling
                    if i < len(lines):
                        input_str = lines[i]
                        i += 1
                        
                        print(f"Input {input_num}")
                        result = handle_string_operation(operation, input_str)
                        print(f"{result}")
                else:
                    print(f"Input {input_num}")
                    print(f"Error: Unknown operation '{operation}'")
            except Exception as e:
                print(f"Input {input_num}")
                print(f"Error: {str(e)}")
                
            # Skip any remaining input lines until the next "Input X" pattern
            while i < len(lines) and not lines[i].startswith("Input"):
                i += 1
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()