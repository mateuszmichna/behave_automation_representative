from utils.fake_persons.base_fake_person import FakePerson


class FakeClient(FakePerson):

    def __init__(self):
        super().__init__()
        self.provider = 'pl_PL'
        self.sex, \
        self.first_name, \
        self.last_name, \
        self.full_name, \
        self.email, \
        self.phone_number,\
        self.birthday = self.generate_basic_information(self.provider, 'client')
