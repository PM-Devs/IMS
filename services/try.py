def get_password_hash(password):
    # Combine password and key
    rounds= 1000
    key="TTU_IMS"
    combined = password + key
    hashed = combined
    
    # Perform multiple rounds of a simple mixing function
    for _ in range(rounds):
        new_hash = ""
        for i in range(len(hashed)):
            char = hashed[i]
            # Simple mixing: rotate ASCII value and wrap around
            new_char = chr((ord(char) + i + len(hashed)) % 128)
            new_hash += new_char
        hashed = new_hash
    
    # Convert to a hexadecimal string
    return ''.join(format(ord(c), '02x') for c in hashed)

def verify_password(plain_password, hashed_password):
    return get_password_hash(plain_password) == hashed_password

password="Pmdj"
hash=get_password_hash(password)
print("IsCorrect:", verify_password("Pmdj",hash))
print(hash)
