import random
import time

from trans import trans
from faker import Faker


class FakePerson(object):

    def __init__(self):
        self.fake = Faker

    @staticmethod
    def _generate_sex():
        sex = random.choice(['male', 'female'])
        return sex

    @staticmethod
    def _generate_full_name(faker: Faker, sex, last_name_param=None):
        fake = faker
        if sex == 'male':
            first_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()
        if last_name_param:
            last_name = last_name_param
        else:
            last_name = fake.last_name()
        return str(first_name), str(last_name)

    @staticmethod
    def _generate_email(first_name: str, last_name: str, role: str):
        random_number = str(round(time.time() * 1000))
        email = f"{trans(first_name.lower())}.{trans(last_name.lower())}.{role.lower()}.test{random_number[8:12]}@niepodam.pl"
        return email

    @staticmethod
    def _generate_phone_number(faker: Faker):
        fake = faker
        phone_num = fake.phone_number()
        return phone_num

    @staticmethod
    def pick_birthday(faker: Faker, min_age: int, max_age: int):
        fake = faker
        date_time = str(
            fake.date_of_birth(tzinfo=None, minimum_age=min_age, maximum_age=max_age))
        date = date_time[0:4] + '-' + date_time[5:7] + '-' + date_time[8:10]
        return str(date)

    def generate_basic_information(self, faker_provider: str, role: str):
        faker = self.fake(faker_provider)
        sex = self._generate_sex()
        first_name, last_name = self._generate_full_name(sex=sex, faker=faker)
        full_name = first_name + ' ' + last_name
        email = self._generate_email(first_name, last_name, role)
        phone_number = self._generate_phone_number(faker=faker)
        birthday = self.pick_birthday(faker, min_age=18, max_age=80)
        return sex, first_name, last_name, full_name, email, phone_number, birthday
