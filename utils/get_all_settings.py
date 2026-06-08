def all_settings_to_machine(cur, comp_name):
    # Zamieniono JOIN na LEFT JOIN dla settings i rules
    query = """
        SELECT 
            c.id AS comp_id, c.name AS comp_name, c.version_of_collectors,
            srv.id AS srv_id, srv.ip AS srv_ip, srv.user AS srv_user, srv.password AS srv_password, srv.basic_path AS srv_basic_path,
            s.id AS set_id, s.watching_path, s.folder_in_server_name, s.slow_mode,
            r.id AS rule_id, r.path AS rule_path, r.rule AS rule_value, r.folder_name AS rule_folder, r.copy_file_force
        FROM public.datacollector_collectorcomputer c
        LEFT JOIN public.datacollector_collectorsservers srv 
          ON c.server_id = srv.id
        LEFT JOIN public.datacollector_collectorcomputersettings s 
          ON s.collector_computer_id = c.id
        LEFT JOIN public.datacollector_collectorrulesettings r 
          ON r.collector_computer_settings_id = s.id
        WHERE c.name = %s
    """

    cur.execute(query, (comp_name,))
    results = cur.fetchall()

    if not results:
        return []

    columns = [desc[0] for desc in cur.description]
    rows = [dict(zip(columns, row)) for row in results]

    computers_dict = {}

    for row in rows:
        c_id = row["comp_id"]

        if c_id not in computers_dict:
            server_info = None
            if row["srv_id"]:
                server_info = {
                    "id": row["srv_id"],
                    "ip": row["srv_ip"],
                    "user": row["srv_user"],
                    "password": row["srv_password"],
                    "basic_path": row["srv_basic_path"]
                }

            computers_dict[c_id] = {
                "id": c_id,
                "name": row["comp_name"],
                "version_of_collectors": row["version_of_collectors"],
                "server": server_info,
                "settings": {},
            }

        s_id = row["set_id"]
        if s_id is not None:
            if s_id not in computers_dict[c_id]["settings"]:
                computers_dict[c_id]["settings"][s_id] = {
                    "id": s_id,
                    "watching_path": row["watching_path"],
                    "folder_in_server_name": row["folder_in_server_name"],
                    "slow_mode": row["slow_mode"],
                    "rules": [],
                }

            if row["rule_id"]:
                computers_dict[c_id]["settings"][s_id]["rules"].append(
                    {
                        "id": row["rule_id"],
                        "path": row["rule_path"],
                        "rule": row["rule_value"],
                        "folder_name": row["rule_folder"],
                        "copy_file_force": row["copy_file_force"],
                    }
                )

    final_result = []
    for comp in computers_dict.values():
        comp["settings"] = list(comp["settings"].values())
        final_result.append(comp)

    return final_result