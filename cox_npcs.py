FILTER_NPCS = ["7526"]


class CoxNpcs:
    @staticmethod
    def run(source: str, vid, version: dict[str, str], docs: dict[str, str | bool]) -> dict | None:
        ids = [npc_id for npc_id in
               map(lambda npc_id: npc_id.strip(), str(version["id"]).split(",")) if npc_id != "" and npc_id.isdigit()]

        npc_id = str(ids[0])
        if npc_id in FILTER_NPCS:
            return None

        if "id" not in version:
            print("page {} is missing an id".format(source))
            return None

        if len(ids) == 0:
            print("page {} is has an empty id".format(source))
            return None

        doc = {"__source__": source}
        if "Challenge Mode" in version["version"]:
            version["attributes"].append(",ChallengeMode")
        if npc_id in docs:
            npc_id += "_" + str(vid)
        docs[npc_id] = doc

        return doc
