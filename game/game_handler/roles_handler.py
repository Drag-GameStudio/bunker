import random
from lobby.models import Session, User
from game.models import UserInfo

PROFESSIONS = ["Test1", "Test2"]
AGES = list(range(100))[10:]
ITEMS = ["Item1", "Item2"]
HOBBYS = ["Hobby1", "HObby2"]
FACTS = ["Fact1", "Fact2"]
HEALTHS = ["Health1", "health2"]


def get_random_el_from_array(arr: list) -> any:
    return arr[round((len(arr) - 1) * random.random())]

def generete_user_data():
    user_data = {}
    user_data["profession"] = get_random_el_from_array(PROFESSIONS)
    user_data["age"] = get_random_el_from_array(AGES)
    user_data["hobby"] = get_random_el_from_array(HOBBYS)
    user_data["item"] = get_random_el_from_array(ITEMS)
    user_data["fact"] = get_random_el_from_array(FACTS)
    user_data["health"] = get_random_el_from_array(HEALTHS)

    return user_data


def give_roles(session: Session):
    users_in_session: list[User] = User.objects.filter(session=session)
    for user in users_in_session:
        user_data = generete_user_data()
        user_info_model = UserInfo(user=user)
        user_info_model.profession = user_data["profession"]
        user_info_model.age = user_data["age"]
        user_info_model.hobby = user_data["hobby"]
        user_info_model.item = user_data["item"]
        user_info_model.fact = user_data["fact"]
        user_info_model.health = user_data["health"]

        user_info_model.save()



