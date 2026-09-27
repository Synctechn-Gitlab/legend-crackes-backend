import urllib.request, json

# 1. Login
login_req = urllib.request.Request(
    'http://127.0.0.1:8000/api/auth/login',
    data=json.dumps({"username": "admin", "password": "admin123"}).encode(),
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(login_req) as resp:
    token = json.loads(resp.read())["access_token"]
print("Admin token verified!")

# 2. Create category
cat_req = urllib.request.Request(
    'http://127.0.0.1:8000/api/categories',
    data=json.dumps({"name": "Test Sky Rockets", "description": "High altitude fireworks"}).encode(),
    headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
)
with urllib.request.urlopen(cat_req) as resp:
    cat = json.loads(resp.read())
print("Category created:", cat["id"], cat["name"], cat["slug"])

# 3. Delete category
del_req = urllib.request.Request(
    f'http://127.0.0.1:8000/api/categories/{cat["id"]}',
    headers={"Authorization": f"Bearer {token}"},
    method="DELETE"
)
with urllib.request.urlopen(del_req) as resp:
    del_res = json.loads(resp.read())
print("Category deleted:", del_res)
