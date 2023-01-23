FILTER_NPCS = ["7526"]


class CoxNpcs:
    @staticmethod
    def run(source: str, vid, version: dict[str, str], docs: dict[str, str | bool]) -> (dict | None, str):
        ids = [npc_id for npc_id in
               map(lambda npc_id: npc_id.strip(), str(version["id"]).split(",")) if npc_id != "" and npc_id.isdigit()]

        npc_id = str(ids[0])
        if npc_id in FILTER_NPCS:
            return None, None

        if "id" not in version:
            print("page {} is missing an id".format(source))
            return None, None

        if len(ids) == 0:
            print("page {} is has an empty id".format(source))
            return None, None

        npc_version = str(version.get("version", "").strip())

        doc = {"__source__": source}
        if "Challenge Mode" in npc_version and "ChallengeMode" not in version["attributes"]:
            version["attributes"].append(",ChallengeMode")
        if npc_id in docs:
            npc_id += "_" + str(vid)
        docs[npc_id] = doc

        npc_version = str(version.get("version", "").strip())
        name = str(version["name"]).strip()
        if not any(filter_str in npc_version for filter_str in ["Normal", "claw", "Enraged"]):
            name += " " + str(version["version"]).strip()

        name = name.replace('(', '').replace(')', '').replace('Challenge Mode', '').strip()

        print(name + " - " + version["attributes"].strip().replace("\n", ""))
        return doc, name
