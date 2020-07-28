# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors and the HuggingFace NLP Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Reuters 21578"""

from __future__ import absolute_import, division, print_function

import csv
import os

import nlp


_CITATION = """\
@article{APTE94
 ,author = {Chidanand Apt{\'{e}} and Fred Damerau and Sholom M. Weiss}
 ,title = {Automated Learning of Decision Rules for Text Categorization}
 ,journal = {ACM Transactions on Information Systems}
 ,year = {1994}
 , note = {To appear.}
 }

@inproceedings{APTE94b
 ,author = {Chidanand Apt{\'{e}} and Fred Damerau and Sholom M. Weiss}
 ,title = {Toward Language Independent Automated Learning of Text Categorization Models}
 ,booktitle = {sigir94}
 ,year = {1994}
 ,note = {To appear.}
 }

@inproceedings{HAYES89
,author = {Philip J. Hayes and Peggy M. Anderson and Irene B. Nirenburg and 
Linda M. Schmandt}
,title = {{TCS}: A Shell for Content-Based Text Categorization}
,booktitle = {IEEE Conference on Artificial Intelligence Applications}
,year = {1990}
}

@inproceedings{HAYES90b
,author = {Philip J. Hayes and Steven P. Weinstein}
,title = {{CONSTRUE/TIS:} A System for Content-Based Indexing of a 
Database of News Stories}
,booktitle = {Second Annual Conference on Innovative Applications of
Artificial Intelligence}
,year = {1990}
}

@incollection{HAYES92 
 ,author = {Philip J. Hayes}
 ,title = {Intelligent High-Volume Text Processing using Shallow,
Domain-Specific Techniques}
 ,booktitle = {Text-Based Intelligent Systems}
 ,publisher = {Lawrence Erlbaum}
 ,address =  {Hillsdale, NJ}
 ,year = {1992}
 ,editor = {Paul S. Jacobs}
}

@inproceedings{LEWIS91c 
  ,author = {David D. Lewis}
  ,title = {Evaluating Text Categorization}
  ,booktitle = {Proceedings of Speech and Natural Language Workshop}
  ,year = {1991}
  ,month = {feb}
  ,organization = {Defense Advanced Research Projects Agency}
  ,publisher = {Morgan Kaufmann} 
  ,pages = {312--318}

}

@phdthesis{LEWIS91d
,author = {David Dolan Lewis}
,title = {Representation and Learning in Information Retrieval}
,school = {Computer Science Dept.; Univ. of Massachusetts; Amherst, MA 01003}
,year = 1992}
,note = {Technical Report 91--93.}
}

@inproceedings{LEWIS91e
,author = {David D. Lewis}
,title = {Data Extraction as Text Categorization: An Experiment with
the {MUC-3} Corpus}
,booktitle = {Proceedings of the Third Message Understanding Evaluation
and Conference}
,year = {1991}
,month = {may}
,organization = {Defense Advanced Research Projects Agency}
,publisher = {Morgan Kaufmann}
,address = {Los Altos, CA}

}

@inproceedings{LEWIS92b
 ,author = {David D. Lewis}
 ,title = {An Evaluation of Phrasal and Clustered Representations on a Text
Categorization Task}
 ,booktitle = {Fifteenth Annual International ACM SIGIR Conference on
Research and Development in Information Retrieval}
 ,year = {1992}
 ,pages = {37--50}
}

@inproceedings{LEWIS92d 
,author = {David D. Lewis and Richard M. Tong}
,title = {Text Filtering in {MUC-3} and {MUC-4}}
,booktitle = {Proceedings of the Fourth Message Understanding Conference ({MUC-4})}
,year = {1992}
,month = {jun}
,organization = {Defense Advanced Research Projects Agency}
,publisher = {Morgan Kaufmann}
,address = {Los Altos, CA}
}

@inproceedings{LEWIS92e
,author = {David D. Lewis}
,title = {Feature Selection and Feature Extraction for Text Categorization}
,booktitle = {Proceedings of Speech and Natural Language Workshop}
,year = {1992}
,month = {feb} 
,organization = {Defense Advanced Research Projects Agency}
,publisher = {Morgan Kaufmann}
,pages = {212--217}
}

@inproceedings{LEWIS94b
 ,author = {David D. Lewis and Marc Ringuette}
 ,title = {A Comparison of Two Learning Algorithms for Text Categorization}
 ,booktitle = {Symposium on Document Analysis and Information Retrieval}
 ,year = {1994}
 ,organization = {ISRI; Univ. of Nevada, Las Vegas}
 ,address = {Las Vegas, NV}
 ,month = {apr}
 ,pages = {81--93}
}

@article{LEWIS94d
, author       = {David D. Lewis and Philip J. Hayes}
, title        = {Guest Editorial}
, journal      = {ACM Transactions on Information Systems}
, year         = {1994}
, volume       = {12}
, number       = {3}
, pages        = {231}
, month        = {jul}
}

@article{SPARCKJONES76
,author = {K. {Sparck Jones} and  C. J. {van Rijsbergen}}
,title =  {Information Retrieval Test Collections}
,journal = {Journal of Documentation}
,year = {1976}
,volume = {32}
,number = {1}
,pages = {59--75}
  }

@book{WEISS91
 ,author = {Sholom M. Weiss and Casimir A. Kulikowski}
 ,title = {Computer Systems That Learn}
 ,publisher = {Morgan Kaufmann}
 ,year = {1991}
 ,address = {San Mateo, CA}
 }
"""

_DESCRIPTION = """\
The Reuters-21578 dataset  is one of the most widely used data collections for text
categorization research. It is collected from the Reuters financial newswire service in 1987.
"""

_DATA_URL = "https://kdd.ics.uci.edu/databases/reuters21578/reuters21578.tar.gz"


class Reuters21578(nlp.GeneratorBasedBuilder):
    """Reuters 21578"""

    def _info(self):
        return nlp.DatasetInfo(
            description=_DESCRIPTION,
            features=nlp.Features(
                {
                    "text": nlp.Value("string"),
                    "topics": nlp.Sequence(nlp.Value("string")),
                    "lewis_split": nlp.Value("string"),
                    "cgis_split": nlp.Value("string"),
                    "old_id": nlp.Value("string"),
                    "new_id": nlp.Value("string"),
                    "places": nlp.Sequence(nlp.Value("string")),
                    "people": nlp.Sequence(nlp.Value("string")),
                    "orgs": nlp.Sequence(nlp.Value("string")),
                    "exchanges": nlp.Sequence(nlp.Value("string")),
                    "date": nlp.Value("string"),
                    "title": nlp.Value("string"),
                }
            ),
            # No default supervised_keys (as we have to pass both premise
            # and hypothesis as input).
            supervised_keys=None,
            homepage="https://kdd.ics.uci.edu/databases/reuters21578/reuters21578.html",
            citation=_CITATION,
        )
    def _split_generators(self, dl_manager):
        dl_dir = dl_manager.download_and_extract(_DATA_URL)
        files = [os.path.join(dl_dir, "reut2-"+"%03d"% i+".sgm" ) for i in range(22)]
        return [
            nlp.SplitGenerator(
                name=nlp.Split.TEST, 
                gen_kwargs={
                    "filepath": files,
                    "split": "PUBLISHED-TESTSET"
                    }),
            nlp.SplitGenerator(
                name=nlp.Split.TRAIN, 
                gen_kwargs={
                    "filepath": files,
                    "split": "TRAINING-SET"
                    }),
        ]
    
    def _generate_examples(self, filepath, split):
        """This function returns the examples in the raw (text) form."""
        for file in filepath:
            with open(file,  errors='ignore') as f: # only the file reut2-017 has one line non UTF-8 encoded so we can ignore it
                print(file)
                print('=='*100)
                line = f.readline()
                lewis_split = ''
                cgis_split = ''
                old_id = ''
                new_id = ''
                topics = []
                places = []
                people = []
                orgs = []
                exchanges = []
                date = ''
                title = ''
                while line:
                    if line.startswith("<REUTERS"):
                        line = line.split()
                        lewis_split = line[2].split('=')[1]
                        cgis_split = line[3].split('=')[1]
                        old_id = line[4].split('=')[1]
                        new_id = line[5].split('=')[1][:-1]
                        line = f.readline()
                        if split not in cgis_split:  #skip example that are not in the current split
                            l = line
                            while l and not l.startswith("<REUTERS"):
                                l = f.readline()
                            if l:
                                line = l 
                    elif line.startswith("<TOPICS>"):
                        if line.replace("\n", "") != "<TOPICS></TOPICS>":
                            line = line.split("<D>")
                            topics = [topic.replace("</D>", "") for topic in line[1:-1]]
                            topics = [topic.replace("</TOPICS>", "") for topic in topics]
                        line = f.readline()
                    elif line.startswith("<PLACES>"):
                        if line.replace("\n", "") != "<PLACES></PLACES>":
                            line = line.split("<D>")
                            places = [place.replace("</D>", "") for place in line[1:-1]]
                            places = [place.replace("</PLACES>", "") for place in places]
                        line = f.readline()
                    elif line.startswith("<PEOPLE>"):
                        if line.replace("\n", "") != "<PEOPLE></PEOPLE>":
                            line = line.split("<D>")
                            people = [p.replace("</D>", "") for p in line[1:-1]]
                            people = [p.replace("</PEOPLE>", "") for p in people]
                        line = f.readline()
                    elif line.startswith("<ORGS>"):
                        if line.replace("\n", "") != "<ORGS></ORGS>":
                            line = line.split("<D>")
                            orgs = [org.replace("</D>", "") for org in line[1:-1]]
                            orgs = [org.replace("</ORGS>", "") for org in orgs]
                        line = f.readline()
                    elif line.startswith("<EXCHANGES>"):
                        if line.replace("\n", "") != "<EXCHANGES></EXCHANGES>":
                            line = line.split("<D>")
                            exchanges = [ex.replace("</D>", "") for ex in line[1:-1]]
                            exchanges = [ex.replace("</EXCHANGES>", "") for ex in exchanges]
                        line = f.readline()
                    elif line.startswith("<DATE>"):
                        date = line.replace("\n", "")
                        date = line[6:-8]   
                        line = f.readline()
                    elif line.startswith("<TITLE>"):
                        title = line[7:-9]
                        line = f.readline()
                    elif "<BODY>" in line:
                        text = line.split('<BODY>')[1]
                        line = f.readline()
                        while "</BODY>" not in line:
                            text += line
                            line = f.readline()
                        
                        yield new_id, {
                                "lewis_split": lewis_split,
                                "cgis_split": cgis_split,
                                "old_id": old_id,
                                "new_id":  new_id,
                                "topics":  topics,
                                "places":  places,
                                "people":  people,
                                "orgs":  orgs,
                                "exchanges":  exchanges,
                                "date":  date,
                                "title": title,
                                "text": text
                        }
                        line = f.readline()
                        
                    else:
                        line = f.readline()
