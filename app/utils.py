from typing import List

import psycopg2 as pg

from config import Config


def relevant_vacancies(user_specialization: str, user_key_skills: List[str]) -> List[str]:
    """
    Returns list of vacancies with addition of relevance coefficient,
    based on intersection of vacancy's key skills and target user's key skills

    """

    conn = pg.connect(Config.PG_CONNECTION)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM vacancy WHERE specialization = '{user_specialization}' AND is_actual = True")
    data = cur.fetchall()

    relevant_list = []

    for vac in data:
        vac_key_skills = vac[10]
        if vac_key_skills:
            coincident = set(vac_key_skills).intersection(set(user_key_skills))
            missing = set(vac_key_skills) - set(user_key_skills)
            c = len(coincident)
            v = len(set(vac_key_skills))
            relevance = (c / v) * v**(1/v) / (1/v + v)**(1/v)
        else:
            coincident, missing = set(), set()
            relevance = 0.1
        vac_plus = vac + (coincident,) + (missing,) + (relevance,)
        relevant_list.append(vac_plus)

    result = sorted(relevant_list, key=lambda x: x[-1], reverse=True)

    return result

