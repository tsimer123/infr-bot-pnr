from services.user import get_user_info, create_user



def start_user(id_user_tg, tg_name, full_name):
    
    users_id = check_user(id_user_tg, tg_name, full_name)
    
    return users_id
    

def check_user(id_user_tg, tg_name, full_name):
    
    user_info = get_user_info(id_user_tg)

    if user_info["users_id"] != 0:
        return user_info["users_id"]       
    else:
        dict_user = {
        "tg_id": id_user_tg,
        "tg_name": tg_name,
        "full_name": full_name        
        }

        users_id = create_user(dict_user)

        return users_id
    








