import traceback
import re
import mwparserfromhell as mw
import api
import util
from typing import *
import copy

from cox_npcs import CoxNpcs
from tob_npcs import TobNpcs

# Modification here to include many more attributes
npc_trait_keys = ["hitpoints", "att", "str", "def", "mage", "range", "attbns", "strbns", "defbns", "amagic", "mbns",
				  "arange", "rngbns", "dstab", "dslash", "dcrush", "dmagic", "drange", "combat", "size"]


def run():
	npcs = {}

	npc_pages = api.query_category("Monsters")
	for name, page in npc_pages.items():
		if name.startswith("Category:"):
			continue

		try:
			code = mw.parse(page, skip_style_tags=True)

			for (vid, version) in util.each_version("Infobox Monster", code):
				if "removal" in version and not str(version["removal"]).strip().lower() in ["", "no"]:
					continue

				is_cox = util.has_template("Chambers of Xeric", code)
				is_tob = util.has_template("Theatre of Blood", code)
				if is_tob:
					doc = TobNpcs.run(name + str(vid), version, npcs)
				else:
					continue

				if is_cox:
					doc = CoxNpcs.run(name + str(vid), vid, version, npcs)
				elif is_tob:
					doc = TobNpcs.run(name + str(vid), version, npcs)
				else:
					doc = util.get_doc_for_id_string(name + str(vid), version, npcs)

				if not doc:
					continue

				util.copy("name", doc, version)
				if "name" not in doc:
					doc["name"] = name

				if "attributes" in version:
					attrs = [x.strip() for x in version["attributes"].split(",") if x.strip()]
					for attr in attrs:
						doc[f"is{attr[0].upper()}{attr[1:]}"] = True
				if is_cox:
					cox_version = str(version["version"]).strip()
					if not any(filter_str in cox_version for filter_str in ["Normal", "claw", "Enraged"]):
						doc["name"] += " " + str(version["version"]).strip()

					doc["name"] = doc["name"].replace('(', '').replace(')', '').replace('Challenge Mode', '').strip()

				for key in npc_trait_keys:
					try:
						util.copy(key, doc, version, lambda x: int(x))
					except ValueError:
						pass
						#print("NPC {} has an non integer {}".format(name, key))

		except (KeyboardInterrupt, SystemExit):
			raise
		except:
			print("NPC {} failed:".format(name))
			traceback.print_exc()

	util.write_json("npcs-dmg-sim.json", "npcs-dmg-sim.min.json", npcs)
