FILTER_NPCS = ["8384"]


class TobNpcs:
    @staticmethod
    def run(source: str, vid, version: dict[str, str], docs: dict[str, dict]) -> (dict | None, str):
        npc_version = str(version.get("version", "").strip())

        if "Xarpus" in str(version["name"]).strip():
            npc_version = str(version.get("smwname", "").strip())

        if "Health" in npc_version:
            return None, None

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

        doc = {"__source__": source}
        if "Entry" in npc_version:
            version["attributes"] = "TobEntryMode"
        elif "Normal" in npc_version:
            version["attributes"] = "TobNormalMode"
        elif "Hard" in npc_version:
            version["attributes"] = "TobHardMode"
        else:
            version["attributes"] = "TobNormalMode"

        if npc_id in docs:
            npc_id += "_" + str(vid).replace("-", "")
        docs[npc_id] = doc

        name = version["name"].strip()
        if "Prinkipas" in name:
            name += " " + str(version["version"]).strip()
            version["attributes"] = "TobHardMode"
        elif "162" in npc_version:
            name += " " + "(small)"
        elif "260" in npc_version:
            name += " " + "(big)"
        elif "Verzik" in name:
            name += " (" + str(version.get("smwname", "").strip().lower().replace("hase ", "")) + ")"

        print(name + " - " + version["attributes"].strip())
        return doc, name
