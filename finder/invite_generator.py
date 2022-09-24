import random


def generate_invites(num:int) -> list:

    symbols = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    invite_len = 16

    invite_list=[]
    for i in range(num):
        invite_list +=  ["".join(random.sample(symbols, invite_len))]

    return invite_list


def save_invites(invite_list: list, filename='invites.txt') -> None:

    with open(filename,'w+') as f:
        for i in invite_list:
            f.write('{}\n'.format(i))
        f.close()

        print('Saved {} invite codes into invites.txt'.format(len(invite_list)))
    return None

if __name__ == '__main__':
    print('OK!')
    inv = generate_invites(16)
    save_invites(inv)
