import argparse
import os
from collections import defaultdict
import hashlib

def file_as_bytes(file):
    with file:
        return file.read()

parser = argparse.ArgumentParser()
parser.add_argument("path", nargs="?")
args = parser.parse_args()
# args.path = r"C:\Users\gurunote\Desktop\New folder"
if args.path is not None:
    ext = input("Enter file format:")
    print("Size sorting options:\n1. Descending\n2. Ascending")
    while True:
        sort = input("Enter a sorting option:")
        if sort == "1":
            sort_mode = True
            break
        elif sort == "2":
            sort_mode = False
            break
        else:
            print("Wrong option")
    all_files = defaultdict(lambda: defaultdict(list))

    for root, dirs, files in os.walk(args.path, topdown=True):
        for name in files:
            size = os.path.getsize(os.path.join(root, name))
            file = os.path.join(root, name)
            hash = hashlib.md5(file_as_bytes(open(file, 'rb'))).hexdigest()
            if (ext != "" and os.path.splitext(file)[1][1:] == ext) or ext == "":
                all_files[size][hash].append(file)

    # Unpack all files from dict, format and print
    for k1 in sorted(all_files.keys(), reverse=sort_mode):
        sub = all_files[k1]
        count = sum([len(subElem) for subElem in sub.values()])
        if count > 1:
            print("\n" + str(k1) + " bytes")
            for k2 in sub.values():
                for k3 in k2:
                    print(k3)

    while True:
        chk_dup = input("Check for duplicates?")
        if chk_dup == "yes":
            # Output hash dict
            hash_dups = defaultdict(list)
            c_line = 0
            for k1 in sorted(all_files.keys(), reverse=sort_mode):
                # size
                sub = all_files[k1]
                count = sum([len(subElem) for subElem in sub.values()])
                if len(sub.keys()) != count:
                    print("\n" + str(k1) + " bytes")
                    for k2 in sub.keys():
                        sub_hash = sub[k2]
                        if len(sub_hash) > 1:
                            print("Hash: " + k2)
                            for k3 in sub_hash:
                                c_line += 1
                                print(str(c_line) + ". " + k3)
                                hash_dups[str(c_line)].append(k3)
            while (del_dup := input("Delete files?:\n")) not in ("yes", "no"):
                print("Wrong option\n")
            if del_dup == "no":
                exit()
            while True:
                del_size = 0
                del_nums = input("Enter file numbers to delete:\n")
                list_nums = del_nums.split(" ")
                if set(list_nums).issubset(list(hash_dups.keys())):
                    for num2 in list_nums:
                        del_size += os.path.getsize(hash_dups[num2][0])
                        os.remove(hash_dups[num2][0])
                    print("Total freed up space: " + str(del_size) + " bytes")
                else:
                    print("Wrong format\n")
            else:
                print("Wrong option\n")
        elif chk_dup == "no":
            exit()
        else:
            print("Wrong option")
else:
    print("Directory is not specified")
