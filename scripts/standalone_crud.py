import requests
import json

def run_standalone_crud():
    print("--- STARTING STANDALONE CRUD SCRIPT ---")
    base_url = "https://dummyjson.com"
    
    # 1. CREATE (POST)
    print("\n1. CREATING A USER (POST)")
    payload = {"firstName": "Chandra", "lastName": "Shekar", "age": 28}
    create_response = requests.post(f"{base_url}/users/add", json=payload)
    print(f"Status Code: {create_response.status_code}")
    
    if create_response.status_code == 201:
        user_id = create_response.json().get('id')
        print(f"Success! Created User with ID: {user_id}")
    else:
        print("Failed to create user.")
        return

    # 2. READ (GET)
    print("\n2. READING THE USER (GET)")
    # Note: DummyJSON doesn't actually save our POST to their public DB, 
    # so we will GET a standard user (ID 1) just to prove the concept.
    get_response = requests.get(f"{base_url}/users/1")
    print(f"Status Code: {get_response.status_code}")
    print(f"User Data: {get_response.json().get('firstName')}")

    # 3. UPDATE (PUT)
    print("\n3. UPDATING THE USER (PUT)")
    update_payload = {"lastName": "UpdatedName"}
    update_response = requests.put(f"{base_url}/users/1", json=update_payload)
    print(f"Status Code: {update_response.status_code}")

    # 4. DELETE (DELETE)
    print("\n4. DELETING THE USER (DELETE)")
    delete_response = requests.delete(f"{base_url}/users/1")
    print(f"Status Code: {delete_response.status_code}")
    print(f"Deleted On: {delete_response.json().get('deletedOn')}")

    print("\n--- STANDALONE SCRIPT FINISHED ---")

if __name__ == "__main__":
    run_standalone_crud()
