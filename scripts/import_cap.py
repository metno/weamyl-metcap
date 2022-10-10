import logging
import platform
import sys

from getpass import getpass
from pathlib import Path
from typing import Union, Dict, Tuple
from shapely.geometry import Polygon

import couchdb
import xmltodict

from lxml import etree
from tqdm import tqdm

from geojson_rewind import rewind

logging.basicConfig(level="INFO")
log = logging.getLogger(__name__)

def getBbox(coordinateList):
    """
    input: list of lon/lat coordinate pairs for CAP polygon as [[lat,lon],[lat,log],...]
    output: two points defining the bounding box as [lon,lat,lon,lat]
    """
    return list(Polygon(coordinateList).bounds)


class CapToDB:
    def __init__(self):
        self._xmlschema = Path("cap_v1.2_schema.xml").read_text()
        self._xml_validator = None  # set at first usage

    def run(self, path: Union[str, Path],
            db_warnings: couchdb.client.Database,
            db_incidents: couchdb.client.Database):
        """Run conversion and upload to db for all xml files in path

        Args:
            path: Path to xml files to be stored in DB
            db_warnings: CouchDB database to store warnings
            db_incidents: CouchDB database to store incident (number / names)
        """
        capdir = Path(path)
        for fn in tqdm(list(capdir.glob("**/METfare*.xml"))):
            dic = self.xml_to_dict(fn)
            warning, incident = self.map_dict(dic)

            try:
                log.debug("\n\nSaving to warnings DB for fn: %s", fn)
                log.debug("content %s", warning)
                id = warning["_id"]
                if id in db_warnings:
                    print(id, "**** already exists, deleting")
                    db_warnings.delete(db_warnings[id])
            
                else:
                    db_warnings.save(warning)
                    log.debug("upload attachment")
                    db_warnings.put_attachment(warning, fn.read_bytes(),
                                           fn.name)
            except couchdb.http.ResourceConflict:
                log.exception("Could not update for %s. See log.", fn.name)
                pass

            # store incident number & update name, if available
            # if incident is None:
            #     log.debug("No incident info")
            #     continue
            # saved_entry = db_incidents.get(incident["_id"])
            # if saved_entry is None:
            #     log.debug("Creating incidents database")
            #     db_incidents.save(incident)
            # elif "name" not in saved_entry and "name" in incident:
            #     log.debug("Updating incidents database")
            #     saved_entry.update(incident)
            #     db_incidents.save(saved_entry)
            # else:
            #     log.debug("Entry in db_incident exists already. No changes.")

    def xml_to_dict(self, fn: Union[Path, str]) -> Dict:
        """Convert xml to dictionary.

        Args:
            fn: Input filename
        """
        string = Path(fn).read_text()
        try:
            self.validate(string)
        except etree.XMLSyntaxError as e:
            log.warning("fn: %s is not a valid xml: %s.", fn, e)
        return xmltodict.parse(string)

    def validate(self, string: str) -> None:
        """Validates xml string against schema.
        Args:
            string: String to be validated.

        Raises:
            lxml.etree.XMLSyntaxError: If string is not a valid according to
                the provided schema
        """
        if self._xml_validator is None:
            log.debug("Attempt to process xml schema")
            schema_root = etree.XML(self._xmlschema.encode())
            schema = etree.XMLSchema(schema_root)
            self._xml_validator = etree.XMLParser(schema=schema)
            log.info("Processed xml schema")
        etree.fromstring(string.encode(), self._xml_validator)

    def map_dict(self, event: Dict) -> Tuple[Dict, Union[None, Dict]]:
        """Maps xml-dict to DB keys

        Results:
            warning: Information for warnings DB
            incident: Information for incidents DB. None if no incident number.
        """
        warning = {}
        alert = event['alert']
        info = self.single_lang_evt_from_cap(alert)

        # Variable keys
        # format: "partition:name"
        # warning["_id"] = f'metfare:{alert["identifier"]}'
        warning["_id"] = f'{alert["identifier"]}'

        warning["saved_at"] = alert["sent"]
        warning["transmitted_at"] = alert["sent"]
        warning["onset"] = info["onset"]
        warning["expires"] = info["expires"]
        warning["phenomenon"] = info["eventCode"]["value"]

        # Info may not exist
        if "incidents" in alert:
            warning["incident"] = alert["incidents"]

        # Fixed keys:
        warning["archived"] = True
        warning["author"] = f"{__file__}@{platform.node()}"
        warning["transmission_state"] = "transmitted"
        warning["source"] = "lustre_archive"

        # new keys
        warning["status"] = alert["status"]
        if "references" in warning:
            warning["references"] = alert["references"]
        warning["certainty"] = info["certainty"]
        warning["severity"] = info["severity"]
        warning["msgType"] = alert["msgType"]
        warning["altitude"] = info["area"]["altitude"]
        warning["ceiling"] = info["area"]["ceiling"]
        warning["areaDesc"] = {
            "en": info["area"]["areaDesc"],
            "nb": info["area"]["areaDesc"],
        }
        warning["type"] = "FeatureCollection"
        orig_polygon = info["area"]["polygon"].split()
        polygon = []
        for coor in orig_polygon:
            lon, lat = coor.split(",")
            polygon.append((float(lat), float(lon)))
        coordinates = [
            polygon,
        ]
        geometry = {
            "type": "Polygon",
            "coordinates": coordinates,
        }

        bbox = getBbox(coordinates[0])
        feature = {
                "geometry": geometry,
                "type": "Feature",
                "properties": {"customArea": False, "bbox":bbox},
            }

        feature = rewind(feature)

        warning["features"] = [feature,]
        # warning["color"]
        # warning["ref_by"]

        # keys that are not relevant:
        # "transmitted_at", "drafted_at", "author"

        # incident-info
        incident = None
        if "incidents" in alert:
            incident = {}
            incident["_id"] = warning["incident"].zfill(10)
        for parameter in info["parameter"]:
            if parameter["valueName"] == "incidentName":
                incident["name"] = parameter["value"]

        return warning, incident

    def single_lang_evt_from_cap(self, evt: Dict, lang="no") -> Dict:
        """Gets `events` of one language from mutlilang-CAP file"""
        evt_no = evt["info"][0]
        if evt_no["language"].lower() != lang:
            raise ValueError("CAPs XML file scheme must have changed")
        for evt_other_lang in evt["info"][1:]:
            if evt_other_lang["language"] == lang:
                raise ValueError("CAPs XML file scheme must have changed")
        return evt_no

    def save_incident(self, event: Dict):
        alert = event['alert']
        info = self.single_lang_evt_from_cap(alert)


if __name__ == "__main__":
    user = input("user:")
    password = getpass("password:")
    couch = couchdb.Server("http://%s:%s@127.0.0.1:5984/"% (user, password))

    
    captodb = CapToDB()
    path = "test_data" if len(sys.argv) == 1 else sys.argv[1]
    captodb.run(path, couch["archive_warnings"], couch["archive_incidents"])


