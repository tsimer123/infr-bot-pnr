from sqlalchemy.orm import Session, sessionmaker

from sql.engine import engine
from sql.scheme import LogMessage

Session = sessionmaker(engine)

session = Session()

def create_log(dict_user, type_message, message):      
    
    add_log = LogMessage(
        users_id = dict_user['users_id'],
        type_message = type_message,
        message = message
    )

    try:    
        session.add(add_log)
        session.commit()
        log_id = add_log.logmessage_id
    except Exception as ex:        
        raise ex
    finally:
        session.close()   

    return log_id


def write_log(users_id_db, type_message, message):

    dict_user_info = {
            "users_id": users_id_db            
        } 

    log_id_db = create_log(dict_user_info, type_message, message)

    return log_id_db
