from datetime import datetime

from app import db
from .models import UserSession


class SessionManagementService:


    @staticmethod
    def create_session(
        user_id,
        jwt_jti,
        expires_at,
        ip_address=None,
        device_info=None
    ):

        session = UserSession(

            user_id=user_id,

            jwt_jti=jwt_jti,

            ip_address=ip_address,

            device_info=device_info,

            expires_at=expires_at,

            status="active"

        )


        db.session.add(session)

        db.session.commit()


        return session.to_dict()



    @staticmethod
    def get_active_sessions():

        sessions = UserSession.query.filter_by(
            status="active"
        ).all()


        return [

            session.to_dict()

            for session in sessions

        ]



    @staticmethod
    def terminate_session(session_id):

        session = UserSession.query.get(session_id)


        if not session:

            return {

                "error": "Session not found"

            }


        session.status = "terminated"

        db.session.commit()


        return {

            "message": "Session terminated",

            "session_id": session_id

        }



    @staticmethod
    def terminate_all_sessions(user_id):

        sessions = UserSession.query.filter_by(
            user_id=user_id,
            status="active"
        ).all()


        for session in sessions:

            session.status = "terminated"


        db.session.commit()


        return {

            "message": "All sessions terminated",

            "terminated_sessions": len(sessions)

        }



    @staticmethod
    def cleanup_expired_sessions():

        now = datetime.utcnow()


        sessions = UserSession.query.filter(
            UserSession.expires_at < now
        ).all()


        for session in sessions:

            session.status = "expired"


        db.session.commit()


        return {

            "expired_sessions": len(sessions)

        }
