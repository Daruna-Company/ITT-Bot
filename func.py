from config import data, users

def getProfileInfo(id):
    for i in users:
        if i["id"] == id:
            return [i["username"], id, i["tech"]]
        else: pass

def register(name, id):
    users.append({"username": name, "id": id, "tech": 1})

def getUsers():
    user = []

    for i in users:
        user.append(i["username"])

    return user

def add(sum, id):
    x = 0
    for i in users:
        if i["id"] == id:
            i["tech"] += sum
            x = 1
        else: pass

    if x == 0:
        return 0
    else:
        return 1
