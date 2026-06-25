from database.DB_connect import DBConnect
from model.arco import Arco
from model.attori import Attori


class DAO():
    @staticmethod
    def getAllVoti():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select r.avg_rating
from ratings r """

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(voto1, voto2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.*
from names n, role_mapping rm, movie m, ratings r 
where n.id = rm.name_id and rm.movie_id = m.id and m.id = r.movie_id 
and n.date_of_birth is not null and r.avg_rating between %s and %s"""

        cursor.execute(query, (voto1, voto2))

        for row in cursor:
            results.append(Attori(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(voto1, voto2, _idMapA):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.n1 as at1, t2.n1 as at2,  t1.p1 AS peso 
from(select n.id as n1, m.id as m1, CAST(REPLACE(REPLACE(REPLACE(m.worlwide_gross_income, '$', ''), ' ', ''), ',', '') AS UNSIGNED) AS p1 
from names n, role_mapping rm, movie m, ratings r 
where n.id = rm.name_id and rm.movie_id = m.id and r.movie_id = m.id and m.worlwide_gross_income is not null
and r.avg_rating between %s and %s
group by n.id, m.id) as t1,
(select n.id as n1, m.id as m1
from names n, role_mapping rm, movie m, ratings r 
where n.id = rm.name_id and rm.movie_id = m.id and r.movie_id = m.id and m.worlwide_gross_income is not null
and r.avg_rating between %s and %s
group by n.id, m.id) as t2
where t1.n1 <> t2.n1 and t1.m1=t2.m1
group by t1.n1, t2.n1"""

        cursor.execute(query, (voto1, voto2, voto1, voto2))

        for row in cursor:
            if row["at1"] in _idMapA and row["at2"] in _idMapA:
                results.append(Arco(_idMapA[row["at1"]], _idMapA[row["at2"]], row["peso"]))
        cursor.close()
        conn.close()
        return results