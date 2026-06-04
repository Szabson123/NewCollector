def check_version_of_settings(cur, comp_name):
    query = """SELECT version_of_collectors FROM public.datacollector_collectorcomputer
               WHERE name = %s
               ORDER BY id DESC
               LIMIT 1
               """
    
    cur.execute(query, (comp_name,))
    return cur.fetchone()