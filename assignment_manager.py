import random
import file_path


def assign_indirects(nums_dict, scheduled_associates):
    """Assigns indirect roles based on user's inputs on main menu"""
    nums_list = list({key for key in nums_dict})
    result_string = not_enough_string = ''
    chosen_associates = set()

    while nums_list:
        key = random.choice(nums_list)
        with open(file_path.get_custom_text(key)) as file:
            trained_associates = file.read()
            trained_associates = trained_associates.split('\n')
            trained_associates.remove('')

            empty = False
            for _ in range(nums_dict[key]):
                found = False
                while not found and not empty:
                    try:
                        choice = random.choice(trained_associates)
                    except IndexError:
                        not_enough_string += f'Not enough eligible AAs to fill {key}.\n'
                        empty = True
                        break
                    if choice not in scheduled_associates:
                        pass
                    elif choice not in chosen_associates:
                        chosen_associates.add(choice)
                        result_string += f'{key}: {choice}\n'
                        found = True
                    trained_associates.remove(choice)

        nums_list.remove(key)

    return result_string, not_enough_string
