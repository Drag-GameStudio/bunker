from game.models import UserInfo
from lobby.models import Session, User
from bunker.settings import VARIABLE_OF_STATE
from .roles_handler import give_roles


def start_game(session: Session):
    all_users: list[User] = User.objects.filter(session=session)
    users_id = [user.id for user in all_users]

    session.set_line_of_users(users_id)
    session.state = VARIABLE_OF_STATE[1]
    session.current_user = session.get_line()[0]
    session.save()

    give_roles(session)


