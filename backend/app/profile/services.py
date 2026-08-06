from app.extensions import db
from app.models.user import User
from app.audit.services import create_audit_log

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)


class ProfileService:


    @staticmethod
    def get_user_profile(user_id):

        user = User.query.get(user_id)

        if not user:
            return None

        return user



    @staticmethod
    def update_email(user_id, email):

        user = User.query.get(user_id)

        if not user:
            return None


        old_email = user.email
        if old_email == email:
            return user
        
        user.email = email


        create_audit_log(
            user_id=user.id,
            action="PROFILE_UPDATE",
            module="PROFILE",
            status="SUCCESS",
            description=(
                f"Email changed from "
                f"{old_email} to {email}"
            ),
        )


        db.session.commit()


        return user




    @staticmethod
    def change_password(
        user_id,
        old_password,
        new_password
    ):

        user = User.query.get(user_id)


        if not user:
            return False, "User not found"



        if not check_password_hash(
            user.password_hash,
            old_password
        ):

            return False, "Old password incorrect"



        user.password_hash = generate_password_hash(
            new_password
        )


        create_audit_log(
            user_id=user.id,
            action="PASSWORD_CHANGE",
            module="PROFILE",
            status="SUCCESS",
            description=(
                f"User {user.username} "
                "changed password"
            ),
        )


        db.session.commit()


        return True, "Password updated"
