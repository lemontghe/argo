from time import sleep


def generate_ref_code():
    with open("frontend/user_id", 'r') as f:
        a = int(f.readline())
    with open("frontend/user_id", 'w') as f:
        f.write(str(a+1))
    return a+1
