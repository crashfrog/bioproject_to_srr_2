#! /usr/bin/env python3

"Grab SRR numbers from BioProjects via the EMBL-ENA REST API's."

import requests
import sys

sra_exp_query = "http://www.ebi.ac.uk/ebisearch/ws/rest/sra-experiment?query={bioproject}"

sample = """{
    "hitCount": 2,
    "entries": [
        {
            "id": "SRX377510",
            "source": "sra-experiment"
        },
        {
            "id": "SRX583279",
            "source": "sra-experiment"
        }
    ],
    "facets": []
}"""

sra_run_query = "http://www.ebi.ac.uk/ebisearch/ws/rest/sra-run?query={experiment}"

sample = """{
    "hitCount": 1,
    "entries": [
        {
            "id": "SRR1029665",
            "source": "sra-run"
        }
    ],
    "facets": []
}"""

if __name__ == "__main__":
	try:
		bioproject = sys.argv[1]
		b_result = requests.get(sra_exp_query.format(bioproject=bioproject), headers=dict(Accept="application/json"))
		b_result.raise_for_status()
		if b_result.json()['entries']:
			for experiment in [d['id'] for d in b_result.json()['entries']]:
				r_result = requests.get(sra_run_query.format(experiment=experiment), headers=dict(Accept="application/json"))
				r_result.raise_for_status()
				for run in [d['id'] for d in r_result.json()['entries']]:
					print(run)
		else:
			print(f"No results found for '{bioproject}'.", file=sys.stderr)
			quit(1)
	except IndexError:
		raise ValueError("Please provide an NCBI BioProject, NCBI BioSample, EMBL Project, or EMBL Study accession.")
	except KeyError as e:
		raise ValueError() from e



