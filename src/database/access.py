import json
from typing import Optional, List, Union
from .engine import get_db
from .models import Target, Log, Account, SavedMedia

class BaseRepo:

    def __init__(self):
        pass

    def add_saved_media(self, saved_media: SavedMedia):
        with get_db() as db:
            db.add(saved_media)
            db.commit()

    def update_saved_media(self, media_id: int, updated_data: dict):
        with get_db() as db:
            media = db.query(SavedMedia).filter(SavedMedia.id == media_id).first()
            if media:
                for key, value in updated_data.items():
                    setattr(media, key, value)
                db.commit()


    def delete_saved_media(self, media_id: int):
        with get_db() as db:
            media = db.query(SavedMedia).filter(SavedMedia.id == media_id).first()
            if media:
                db.delete(media)
                db.commit()

   
    def get_saved_media(self, media_id: int) -> Optional[SavedMedia]:
        with get_db() as db:
            media = db.query(SavedMedia).filter(SavedMedia.id == media_id).first()
        return media

    def get_all_media(self) -> List[SavedMedia]:
        with get_db() as db:
            media = db.query(SavedMedia).all()
        return media
    
    def get_account(self, username: str) -> Optional[Account]:
        with get_db() as db:
            acc = db.query(Account).filter(Account.username == username.lower()).first()
        return acc
    
    def get_all_account(self) -> List[Account]:
        with get_db() as db:
            accs = db.query(Account).all()
        return accs

    def add_account(self, username : str, password : str, credentials : dict):
        with get_db() as db:
            new_acc = Account(username=username.lower(), password=password, credentials=json.dumps(credentials))
            db.add(new_acc)
            db.commit()

    def delete_account(self, username : str):
        acc = self.get_account(username.lower())
        with get_db() as db:
            db.delete(acc)
            db.commit()

    def get_target(self, username: str) -> Optional[Target]:
        with get_db() as db:
            acc = db.query(Target).filter(Target.username == username.lower()).first()
        return acc
    
    def get_all_targets(self):
        with get_db() as db:
            accs = db.query(Target).all()
        return accs

    def add_target(self, username : str, user_id : str):
        with get_db() as db:
            new_acc = Target(username=username.lower(), user_id=user_id)
            db.add(new_acc)
            db.commit()
    
    def add_target_log(self, username : str, log : str):
        log_string = f"{username}_{log}"
        with get_db() as db:
            new_log = Log(username=username.lower(), log_string=log_string, log=log)
            db.add(new_log)
            db.commit()
    
    def get_target_logs(self, username : str, raw = True) -> List[Optional[Union[str, Log]]]:
        with get_db() as db:
            logs = db.query(Log).filter(Log.username == username.lower()).all()
        if raw:
            return [str(log.log) for log in logs]
        return logs

  

root = BaseRepo()