import random
from file_path import FilePath


class AssignmentManager:
    def __init__(self, permissions_dict, nums_dict, uncompliant_processors, scheduled_associates):
        self.permissions_dict = permissions_dict
        self.nums_dict = nums_dict
        self.nums_list = [key for key in self.nums_dict]
        self.uncompliant_processors = uncompliant_processors
        self.scheduled_associates = scheduled_associates
        self.result_string = ''
        self.uncompliant_string = ''
        self.not_enough_string = ''
        self.chosen_associates = set()
        self.declared_uncompliant = set()
        self.file_path = FilePath()

    def assign_indirects(self):
        while self.nums_list:
            key = random.choice(self.nums_list)
            with open(self.file_path.get_persistent_storage_path(f'{key}.txt')) as file:
                trained_associates = file.read()
                trained_associates = trained_associates.split('\n')
                trained_associates.remove('')

                empty = False
                for _ in range(self.nums_dict[key]):
                    found = False
                    while not found and not empty:
                        try:
                            choice = random.choice(trained_associates)
                        except IndexError:
                            self.not_enough_string += f'Not enough eligible AAs to fill {key.upper()}.\n'
                            empty = True
                            break
                        if choice not in self.scheduled_associates:
                            pass
                        elif choice in self.uncompliant_processors:
                            if choice not in self.declared_uncompliant:
                                self.uncompliant_string += (f'{choice} was put on {key.upper()} but is ineligible '
                                                            f'because they need to process.\n')
                                self.declared_uncompliant.add(choice)
                        elif choice not in self.chosen_associates:
                            self.chosen_associates.add(choice)
                            self.result_string += f'{key.upper()}: {choice}\n'
                            found = True
                        trained_associates.remove(choice)

            self.nums_list.remove(key)

        return self.result_string, self.uncompliant_string, self.not_enough_string
