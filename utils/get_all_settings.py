def all_settings_to_machine(cur, comp_name):
    query = """SELECT * FROM public.datacollector_collectorcomputer c
               JOIN public.datacollector_collectorcomputersettings s 
                 ON s.collector_computer_id = c.id
               JOIN public.datacollector_collectorrulesettings r 
                 ON r.collector_computer_settings_id = s.id
               WHERE c.name = %s"""
    
    cur.execute(query, (comp_name, ))
    return cur.fetchall()