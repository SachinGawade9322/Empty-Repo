from utils.connection import get_db_connection
class Portfolio:
    def __init__(self, user_id, project_title, project_description, project_link):
        self.user_id = user_id
        self.project_title = project_title
        self.project_description = project_description
        self.project_link = project_link

    @staticmethod
    def create_portfolio(user_id, project_title, project_description, project_link):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO portfolios (user_id, project_title, project_description, project_link)
            VALUES (%s, %s, %s, %s) RETURNING id
        """, (user_id, project_title, project_description, project_link))
        portfolio_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return portfolio_id

    @staticmethod
    def get_all_portfolios():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM portfolios")
        portfolios = cur.fetchall()
        cur.close()
        conn.close()
        return portfolios