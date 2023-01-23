class TobNpcs:
    @staticmethod
    def run(source: str, version: dict[str, str], docs: dict[str, dict]):
        return None
        if not "id" in version:
            print("page {} is missing an id".format(source))
            return None

        ids = [id for id in map(lambda id: id.strip(), str(version["id"]).split(",")) if id != "" and id.isdigit()]

        if len(ids) == 0:
            print("page {} is has an empty id".format(source))
            return None

        doc = {}
        doc["__source__"] = source
        for id in ids:
            if id in docs:
                print("page {} is has the same id as something".format(source))
                return None

            docs[id] = doc

        return doc