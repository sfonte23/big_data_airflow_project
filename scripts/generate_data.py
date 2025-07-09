import os
import json
import random
from faker import Faker

fake = Faker('pt_BR')

def generate_user_data(num_users=100):
    users = []
    for _ in range(num_users):
        user = {
            "id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace('\n', ', '),
            "phone_number": fake.phone_number(),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            "cpf": fake.cpf(),
            "registration_timestamp_utc": fake.date_time_this_decade(tzinfo=None).isoformat() + "Z"
        }
        users.append(user)
    return users

def generate_user_data_error(num_users=100):
    users = []
    all_ids = [fake.uuid4() for _ in range(num_users)]

    for i in range(num_users):
        user = {
            "id": all_ids[i],
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address().replace('\n', ', '),
            "phone_number": fake.phone_number(),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
            "cpf": fake.cpf(),
            "registration_timestamp_utc": fake.date_time_this_decade(tzinfo=None).isoformat() + "Z"
        }
        if random.random() < 0.05:
            user['email'] = None
        elif random.random() < 0.05:
            user['email'] = user['name'].replace(" ", ".") + "@invalid-domain"
        if random.random() < 0.02:
            user['id'] = None
        if i == 50 and num_users > 50:
            user['id'] = all_ids[10]
        users.append(user)
    return users

def save_to_json(data, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Raw data for {len(data)} users saved to {filename}")

if __name__ == "__main__":
    NUM_USERS = 10000
    OUTPUT_FILE = os.path.join("data", "raw", "raw_users_with_error.json")
    user_data = generate_user_data_error(NUM_USERS)
    save_to_json(user_data, OUTPUT_FILE)
