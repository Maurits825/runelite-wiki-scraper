CUSTOM_NAME_MAP = {
    "8060": "Vorkath (quest)",
    "8058": "Vorkath (quest)",
    "2042": "Zulrah (Serpentine/Ranged)",
    "2043": "Zulrah (Magma/Melee)",
    "2044": "Zulrah (Tanzanite/Mage)",
    "12077": "Phantom Muspah (Ranged)",
    "12078": "Phantom Muspah (Melee)",
    "12079": "Phantom Muspah (Shielded)",
}


class CustomNames:
    @staticmethod
    def get_custom_name(version: dict[str, str]):
        if "id" not in version:
            return None

        ids = [id for id in map(lambda id: id.strip(), str(version["id"]).split(",")) if id != "" and id.isdigit()]

        if len(ids) == 0:
            return None

        npc_id = ids[0]
        if npc_id:
            return CUSTOM_NAME_MAP.get(npc_id, None)
        else:
            return None
