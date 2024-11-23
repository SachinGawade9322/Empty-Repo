from utils.connection import get_db_connection

class FreelancerApplication:
    def __init__(self, user_id, application_details):
        self.user_id = user_id
        self.application_details = application_details

    @staticmethod
    def create_application(user_id, application_details):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO freelancer_applications (user_id, application_details)
            VALUES (%s, %s) RETURNING id
        """, (user_id, application_details))
        application_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return application_id

    @staticmethod
    def get_all_applications():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM freelancer_applications")
        applications = cur.fetchall()
        cur.close()
        conn.close()
        return applications