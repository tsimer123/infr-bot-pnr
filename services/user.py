from sqlalchemy.orm import Session, sessionmaker

from sql.engine import engine
from sql.scheme import Users

Session = sessionmaker(engine)

session = Session()

def create_user(dict_user):

    user = Users(
        user_id_tg = dict_user["tg_id"],
        tg_name = dict_user["tg_name"],
        full_name = dict_user["full_name"]        
        )
    
    try:
        session.add(user)
        session.commit()
        user_id = user.users_id
    except Exception as ex:        
        raise ex
    finally:
        session.close()

    return user_id
    

def get_user_id(user_id_tg_in):

    try:
        # user_id = session.query(Users).filter(Users.user_id_tg == user_id_tg_in).first()
        user_id = session.query(Users.users_id).filter(Users.user_id_tg == user_id_tg_in).first()
        if user_id is not None:
            print(user_id[0])
        else:
            print(0)
    except Exception as ex:        
        raise ex
    finally:
        session.close()  


def get_user_info(user_id_tg_in):

    try:
        user_info = session.query(
            Users.users_id,
            Users.user_id_tg,
            Users.tg_name,
            Users.full_name
            ).filter(
            Users.user_id_tg == user_id_tg_in
            ).first()
    except Exception as ex:        
        raise ex
    finally:
        session.close()

    if user_info is not None:
        dict_user_info = {
            "users_id": user_info.users_id,
            "user_id_tg": user_info.user_id_tg,
            "tg_name": user_info.tg_name,
            "full_name": user_info.full_name            
        }        
    else:
        dict_user_info = {
            "users_id": 0,
            "user_id_tg": 0,
            "tg_name": "",
            "full_name": ""
        }  
    
    return dict_user_info

    