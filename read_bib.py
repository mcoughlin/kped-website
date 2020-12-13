
import os
import re 
import bibtexparser
from bibtexparser.bparser import BibTexParser
import copy

baseoutdir = "content/publication"
if not os.path.isdir(baseoutdir):
    os.makedirs(baseoutdir)

bibfile = 'references.bib' 
with open(bibfile) as bibtex_file:
    parser = BibTexParser(common_strings = True)
    bib_database = bibtexparser.load(bibtex_file, parser=parser)

bib_database_new = []
keys = []
for entry in bib_database.entries:
    keys.append(entry["ID"])
    if not entry["title"][:1] == "{{":
        entry["title"] = '{%s}'%entry["title"]

    bib_database_new = copy.copy(bib_database)
    bib_database_new.entries = [entry]

    outdir = os.path.join(baseoutdir, entry["ID"].replace(":","-"))
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    bibout = os.path.join(outdir, "%s.bib" % (entry["ID"].replace(":","-")))
    with open(bibout, 'w') as bibtex_file:
        bibtexparser.dump(bib_database_new, bibtex_file)

    title = entry["title"].replace('{','').replace('}','')
    authors = list(filter(None,entry["author"].replace('{','').replace('}','').split(" and ")))

    bibout = os.path.join(outdir, "index.md")
    fid = open(bibout, 'w')
    fid.write('+++\n')
    fid.write('title = "%s"\n' % title)
    fid.write('date = %s\n' % entry["year"])
    fid.write('authors = %s\n' % authors)
    fid.write('publication_types = ["2"]\n')
    fid.write('abstract = ""\n')
    fid.write('selected = "true"\n')
    if "journal" in entry:
        fid.write('publication = "%s "\n' % entry["journal"])
    else:
        fid.write('publication = "%s "\n' % 'arxiv')
    if "url" in entry:
        fid.write('url_pdf = "%s"\n' % entry["url"])
    else:
        fid.write('url_pdf = "http://www.arxiv.org/abs/%s"\n' % entry["eprint"])
    if "doi" in entry:
        fid.write('doi = "%s"\n' % entry["doi"])
    fid.write('+++\n')
    fid.write('\n')
