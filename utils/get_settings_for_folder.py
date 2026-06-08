def get_rules_by_watching_path(cur, watching_path, comp_name):
    query = """
        SELECT 
            s.id AS set_id, s.watching_path, s.folder_in_server_name, s.slow_mode, s.collector_computer_id,
            srv.id AS srv_id, srv.ip AS srv_ip, srv.user AS srv_user, srv.password AS srv_password, srv.basic_path AS srv_basic_path,
            r.id AS rule_id, r.path AS rule_path, r.rule AS rule_value, r.folder_name AS rule_folder, r.copy_file_force
        FROM public.datacollector_collectorcomputersettings s
        JOIN public.datacollector_collectorcomputer c 
          ON s.collector_computer_id = c.id
        LEFT JOIN public.datacollector_collectorsservers srv 
          ON c.server_id = srv.id
        LEFT JOIN public.datacollector_collectorrulesettings r 
          ON r.collector_computer_settings_id = s.id
        WHERE s.watching_path = %s AND c.name = %s
    """

    # Przekazujemy oba parametry do kwerendy
    cur.execute(query, (watching_path, comp_name))
    results = cur.fetchall()

    if not results:
        return []

    columns = [desc[0] for desc in cur.description]
    rows = [dict(zip(columns, row)) for row in results]

    settings_dict = {}

    for row in rows:
        s_id = row["set_id"]

        if s_id not in settings_dict:
            server_info = None
            if row["srv_id"]:
                server_info = {
                    "id": row["srv_id"],
                    "ip": row["srv_ip"],
                    "user": row["srv_user"],
                    "password": row["srv_password"],
                    "basic_path": row["srv_basic_path"],
                }

            settings_dict[s_id] = {
                "setting_id": s_id,
                "collector_computer_id": row["collector_computer_id"],
                "server": server_info,
                "watching_path": row["watching_path"],
                "folder_in_server_name": row["folder_in_server_name"],
                "slow_mode": row["slow_mode"],
                "rules": [],
            }

        if row["rule_id"]:
            settings_dict[s_id]["rules"].append(
                {
                    "rule_id": row["rule_id"],
                    "path": row["rule_path"],
                    "rule": row["rule_value"],
                    "folder_name": row["rule_folder"],
                    "copy_file_force": row["copy_file_force"],
                }
            )

    return list(settings_dict.values())