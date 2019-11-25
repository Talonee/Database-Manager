import random


def encode(content):
    leet = {"o": "0", "l": "1", "z": "2", "e": "3", "a": "4",
            "s": "5", "g": "6", "t": "7", "b": "8", "j": "9"}

    content = str(content).split(" ")

    def func(item):
        res = ""
        # Remove periods, prevent commas due to CSV
        item = item.replace(".", "")

        # Check content type and modify
        try:
            if int(item):  # if pure int, indicate
                item = ">" + item
        except:
            if not any(char.isdigit() for char in item):  # if pure str, indicate and relace
                item = "<" + item.lower()

                # 0. 1337 code
                for i in item:
                    item = item.replace(
                        i, leet[i]) if i in leet.keys() else item
            # do nothing if mixed input

        # 1. Modify ASCII
        for i in item:
            i = chr(ord(i) - 2)
            res += i

        # 2. Flip
        res = res[::-1]

        # 3. Indices swap
        i = 0
        s = list(res)
        while i + 1 < len(s):
            hold = s[i + 1]
            s[i + 1] = s[i]
            s[i] = hold
            i += 2
        res = "".join(s)

        # 4. Random capitalization
        res = "".join(random.choice([i.upper(), i]) for i in res)

        return res

    res = " ".join(list(map(func, content)))

    return res


# if __name__ == "__main__":
    # code = encode("Corcuera")
    # print("Encode: {}\nDecode: {}\n".format(code, decode(code)))
    # code = encode("12020 Caballero Street, Victorville CA 92395")
    # print("Encode: {}\nDecode: {}\n".format(code, decode(code)))
    # code = encode("Plate 5JXK123")
    # print("Encode: {}\nDecode: {}\n".format(code, decode(code)))
    # code = encode("shit . i'm bobbing n weavin , yuh ,")
    # print("Encode: {}\nDecode: {}\n".format(code, decode(code)))
