import psycopg2 as pg

from config import Config


def relevant_vacancies(user_specialization, user_key_skills):
    conn = pg.connect(Config.PG_CONNECTION)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM vacancy WHERE specialization='{user_specialization}'")
    data = cur.fetchall()

    relevant_list = []

    for vac in data:
        vac_key_skills = vac[10]
        if vac_key_skills:
            relevance = len(set(vac_key_skills).intersection(set(user_key_skills))) / len(set(vac_key_skills))
        else:
            relevance = 0.5
        relevant_list.append(vac + (relevance,))

    result = sorted(relevant_list, key=lambda x: x[-1], reverse=True)

    return result

