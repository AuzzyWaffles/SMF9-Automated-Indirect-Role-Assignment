import random
import file_path


class AssignmentManager:
    def __init__(self, permissions_dict, nums_dict, scheduled_associates):
        self.permissions_dict = permissions_dict
        self.nums_dict = nums_dict
        self.nums_list = [key for key in self.nums_dict]
        self.scheduled_associates = scheduled_associates
        self.result_string = ''
        self.not_enough_string = ''
        self.chosen_associates = set()

    def assign_indirects(self):
        while self.nums_list:
            key = random.choice(self.nums_list)
            with open(file_path.get_txt(f'{key}.txt')) as file:
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
                        elif choice not in self.chosen_associates:
                            self.chosen_associates.add(choice)
                            self.result_string += f'{key.upper()}: {choice}\n'
                            found = True
                        trained_associates.remove(choice)

            self.nums_list.remove(key)

        return self.result_string, self.not_enough_string
