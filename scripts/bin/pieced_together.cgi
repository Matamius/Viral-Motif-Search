#!/usr/local/bin/python3

import json
import jinja2
import re
import cgi
import cgitb
import mysql.connector
from utils import project_parse as pp

cgitb.enable()

## load jinja2
template_loader = jinja2.FileSystemLoader(searchpath="../html")
env = jinja2.Environment(loader=template_loader)
template = env.get_template('render.html')

print("Content-Type: application/json\n\n")
form = cgi.FieldStorage()

## connect to database with mysql
conn = mysql.connector.connect(user = 'jli462',
                               password ='MatamiusEats@112',
                               host='localhost',
                               database='jli462')
curs = conn.cursor()

## query the MySQL database
qry = """
SELECT 
    c.ELMIdentifier, 
    c.FunctionalSiteName, 
    c.Description, 
    c.Regex
FROM 
    elm_classes AS c
INNER JOIN 
    elm_instances AS i
ON 
    c.ELMIdentifier = i.ELMIdentifier;
    """
curs.execute(qry) 
regex_stuff = []
for row in curs.fetchall():
    ELMIdentifier, FunctionalSiteName, Description, Regex = row
    regex_stuff.append({'id':ELMIdentifier, 
                        'sitename':FunctionalSiteName, 
                        'description':Description, 
                        'regex':Regex})

## decode
input_file = form["file"]
file_content = input_file.file.read().decode('utf-8')

## parse and select for sequence
parsed_file = pp.parse_file(file_content)
sequence_raw = parsed_file[1]

## check if DNA or protein sequence
if pp.check_DNA_or_Prot(sequence_raw):
    rev_comp = pp.reverse_complement(sequence_raw)
else:
    peptide_segments = pp.parse_translation(sequence_raw)

## transcribe
sequence_raw = sequence_raw.replace('T', 'U')
rev_comp = rev_comp.replace('T', 'U')    

## parse frames and combine into single dictionary
forward_frames = pp.parse_frames(sequence_raw)
reverse_frames = pp.parse_frames(rev_comp)
for i in reverse_frames:
    reverse_frames[i+3] = reverse_frames.pop(i) 
forward_frames.update(reverse_frames)

## translate
translation = pp.translate(forward_frames)
peptide_segments = pp.parse_translation(translation)

## match each regex pattern for each peptide for each frame, sheesh
matches = []
for frame, peptides in peptide_segments.items():
    for peptide in peptides:
        for regex in regex_stuff:
            for match in  re.finditer(regex['regex'], peptide):
                start, end = match.start(), match.end()
                highlight_match = (
                    peptide[:start]+'<span class = "highlight">' +
                    peptide[start:end] + '</span>' + 
                    peptide[end:]
                )
                matches.append({
                    'frame': frame, 
                    'peptide': highlight_match, 
                    'regex_id': regex['id'], 
                    'regex_sitename': regex['sitename'], 
                    'regex_descr': regex['description'], 
                    'regex_pattern': regex['regex']
                    })
motif_returns = {"matches": matches}

## render in json
print(json.dumps(motif_returns))

curs.close()
conn.close()
