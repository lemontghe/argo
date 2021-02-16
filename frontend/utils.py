from time import sleep


def generate_ref_code(i):
    with open("frontend/user_id", 'r') as f:
        a = int(f.readline())
    if i:
        with open("frontend/user_id", 'w') as f:
            f.write(str(a+1))
        return a+1
    else:
        with open("frontend/user_id", 'w') as f:
            f.write(str(a-1))
        return a-1
