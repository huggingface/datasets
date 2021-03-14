# coding=utf-8
# Copyright 2020 The HuggingFace Datasets Authors and the current dataset script contributor.
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
"""The bAbI tasks dataset."""

from __future__ import absolute_import, division, print_function

import os

import datasets


_CITATION = """\
@misc{weston2015aicomplete,
      title={Towards AI-Complete Question Answering: A Set of Prerequisite Toy Tasks},
      author={Jason Weston and Antoine Bordes and Sumit Chopra and Alexander M. Rush and Bart van Merriënboer and Armand Joulin and Tomas Mikolov},
      year={2015},
      eprint={1502.05698},
      archivePrefix={arXiv},
      primaryClass={cs.AI}
}
"""


_DESCRIPTION = """\
The (20) QA bAbI tasks are a set of proxy tasks that evaluate reading
comprehension via question answering. Our tasks measure understanding
in several ways: whether a system is able to answer questions via chaining facts,
simple induction, deduction and many more. The tasks are designed to be prerequisites
for any system that aims to be capable of conversing with a human.
The aim is to classify these tasks into skill sets,so that researchers
can identify (and then rectify)the failings of their systems.
"""

_HOMEPAGE = "https://research.fb.com/downloads/babi/"

_LICENSE = """
CC License

bAbI tasks data

Copyright (c) 2015-present, Facebook, Inc. All rights reserved.

Creative Commons Legal Code

Attribution 3.0 Unported

    CREATIVE COMMONS CORPORATION IS NOT A LAW FIRM AND DOES NOT PROVIDE
    LEGAL SERVICES. DISTRIBUTION OF THIS LICENSE DOES NOT CREATE AN
    ATTORNEY-CLIENT RELATIONSHIP. CREATIVE COMMONS PROVIDES THIS
    INFORMATION ON AN "AS-IS" BASIS. CREATIVE COMMONS MAKES NO WARRANTIES
    REGARDING THE INFORMATION PROVIDED, AND DISCLAIMS LIABILITY FOR
    DAMAGES RESULTING FROM ITS USE.

License

THE WORK (AS DEFINED BELOW) IS PROVIDED UNDER THE TERMS OF THIS CREATIVE
COMMONS PUBLIC LICENSE ("CCPL" OR "LICENSE"). THE WORK IS PROTECTED BY
COPYRIGHT AND/OR OTHER APPLICABLE LAW. ANY USE OF THE WORK OTHER THAN AS
AUTHORIZED UNDER THIS LICENSE OR COPYRIGHT LAW IS PROHIBITED.

BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE
TO BE BOUND BY THE TERMS OF THIS LICENSE. TO THE EXTENT THIS LICENSE MAY
BE CONSIDERED TO BE A CONTRACT, THE LICENSOR GRANTS YOU THE RIGHTS
CONTAINED HERE IN CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND
CONDITIONS.

1. Definitions

 a. "Adaptation" means a work based upon the Work, or upon the Work and
    other pre-existing works, such as a translation, adaptation,
    derivative work, arrangement of music or other alterations of a
    literary or artistic work, or phonogram or performance and includes
    cinematographic adaptations or any other form in which the Work may be
    recast, transformed, or adapted including in any form recognizably
    derived from the original, except that a work that constitutes a
    Collection will not be considered an Adaptation for the purpose of
    this License. For the avoidance of doubt, where the Work is a musical
    work, performance or phonogram, the synchronization of the Work in
    timed-relation with a moving image ("synching") will be considered an
    Adaptation for the purpose of this License.
 b. "Collection" means a collection of literary or artistic works, such as
    encyclopedias and anthologies, or performances, phonograms or
    broadcasts, or other works or subject matter other than works listed
    in Section 1(f) below, which, by reason of the selection and
    arrangement of their contents, constitute intellectual creations, in
    which the Work is included in its entirety in unmodified form along
    with one or more other contributions, each constituting separate and
    independent works in themselves, which together are assembled into a
    collective whole. A work that constitutes a Collection will not be
    considered an Adaptation (as defined above) for the purposes of this
    License.
 c. "Distribute" means to make available to the public the original and
    copies of the Work or Adaptation, as appropriate, through sale or
    other transfer of ownership.
 d. "Licensor" means the individual, individuals, entity or entities that
    offer(s) the Work under the terms of this License.
 e. "Original Author" means, in the case of a literary or artistic work,
    the individual, individuals, entity or entities who created the Work
    or if no individual or entity can be identified, the publisher; and in
    addition (i) in the case of a performance the actors, singers,
    musicians, dancers, and other persons who act, sing, deliver, declaim,
    play in, interpret or otherwise perform literary or artistic works or
    expressions of folklore; (ii) in the case of a phonogram the producer
    being the person or legal entity who first fixes the sounds of a
    performance or other sounds; and, (iii) in the case of broadcasts, the
    organization that transmits the broadcast.
 f. "Work" means the literary and/or artistic work offered under the terms
    of this License including without limitation any production in the
    literary, scientific and artistic domain, whatever may be the mode or
    form of its expression including digital form, such as a book,
    pamphlet and other writing; a lecture, address, sermon or other work
    of the same nature; a dramatic or dramatico-musical work; a
    choreographic work or entertainment in dumb show; a musical
    composition with or without words; a cinematographic work to which are
    assimilated works expressed by a process analogous to cinematography;
    a work of drawing, painting, architecture, sculpture, engraving or
    lithography; a photographic work to which are assimilated works
    expressed by a process analogous to photography; a work of applied
    art; an illustration, map, plan, sketch or three-dimensional work
    relative to geography, topography, architecture or science; a
    performance; a broadcast; a phonogram; a compilation of data to the
    extent it is protected as a copyrightable work; or a work performed by
    a variety or circus performer to the extent it is not otherwise
    considered a literary or artistic work.
 g. "You" means an individual or entity exercising rights under this
    License who has not previously violated the terms of this License with
    respect to the Work, or who has received express permission from the
    Licensor to exercise rights under this License despite a previous
    violation.
 h. "Publicly Perform" means to perform public recitations of the Work and
    to communicate to the public those public recitations, by any means or
    process, including by wire or wireless means or public digital
    performances; to make available to the public Works in such a way that
    members of the public may access these Works from a place and at a
    place individually chosen by them; to perform the Work to the public
    by any means or process and the communication to the public of the
    performances of the Work, including by public digital performance; to
    broadcast and rebroadcast the Work by any means including signs,
    sounds or images.
 i. "Reproduce" means to make copies of the Work by any means including
    without limitation by sound or visual recordings and the right of
    fixation and reproducing fixations of the Work, including storage of a
    protected performance or phonogram in digital form or other electronic
    medium.

2. Fair Dealing Rights. Nothing in this License is intended to reduce,
limit, or restrict any uses free from copyright or rights arising from
limitations or exceptions that are provided for in connection with the
copyright protection under copyright law or other applicable laws.

3. License Grant. Subject to the terms and conditions of this License,
Licensor hereby grants You a worldwide, royalty-free, non-exclusive,
perpetual (for the duration of the applicable copyright) license to
exercise the rights in the Work as stated below:

 a. to Reproduce the Work, to incorporate the Work into one or more
    Collections, and to Reproduce the Work as incorporated in the
    Collections;
 b. to create and Reproduce Adaptations provided that any such Adaptation,
    including any translation in any medium, takes reasonable steps to
    clearly label, demarcate or otherwise identify that changes were made
    to the original Work. For example, a translation could be marked "The
    original work was translated from English to Spanish," or a
    modification could indicate "The original work has been modified.";
 c. to Distribute and Publicly Perform the Work including as incorporated
    in Collections; and,
 d. to Distribute and Publicly Perform Adaptations.
 e. For the avoidance of doubt:

     i. Non-waivable Compulsory License Schemes. In those jurisdictions in
        which the right to collect royalties through any statutory or
        compulsory licensing scheme cannot be waived, the Licensor
        reserves the exclusive right to collect such royalties for any
        exercise by You of the rights granted under this License;
    ii. Waivable Compulsory License Schemes. In those jurisdictions in
        which the right to collect royalties through any statutory or
        compulsory licensing scheme can be waived, the Licensor waives the
        exclusive right to collect such royalties for any exercise by You
        of the rights granted under this License; and,
   iii. Voluntary License Schemes. The Licensor waives the right to
        collect royalties, whether individually or, in the event that the
        Licensor is a member of a collecting society that administers
        voluntary licensing schemes, via that society, from any exercise
        by You of the rights granted under this License.

The above rights may be exercised in all media and formats whether now
known or hereafter devised. The above rights include the right to make
such modifications as are technically necessary to exercise the rights in
other media and formats. Subject to Section 8(f), all rights not expressly
granted by Licensor are hereby reserved.

4. Restrictions. The license granted in Section 3 above is expressly made
subject to and limited by the following restrictions:

 a. You may Distribute or Publicly Perform the Work only under the terms
    of this License. You must include a copy of, or the Uniform Resource
    Identifier (URI) for, this License with every copy of the Work You
    Distribute or Publicly Perform. You may not offer or impose any terms
    on the Work that restrict the terms of this License or the ability of
    the recipient of the Work to exercise the rights granted to that
    recipient under the terms of the License. You may not sublicense the
    Work. You must keep intact all notices that refer to this License and
    to the disclaimer of warranties with every copy of the Work You
    Distribute or Publicly Perform. When You Distribute or Publicly
    Perform the Work, You may not impose any effective technological
    measures on the Work that restrict the ability of a recipient of the
    Work from You to exercise the rights granted to that recipient under
    the terms of the License. This Section 4(a) applies to the Work as
    incorporated in a Collection, but this does not require the Collection
    apart from the Work itself to be made subject to the terms of this
    License. If You create a Collection, upon notice from any Licensor You
    must, to the extent practicable, remove from the Collection any credit
    as required by Section 4(b), as requested. If You create an
    Adaptation, upon notice from any Licensor You must, to the extent
    practicable, remove from the Adaptation any credit as required by
    Section 4(b), as requested.
 b. If You Distribute, or Publicly Perform the Work or any Adaptations or
    Collections, You must, unless a request has been made pursuant to
    Section 4(a), keep intact all copyright notices for the Work and
    provide, reasonable to the medium or means You are utilizing: (i) the
    name of the Original Author (or pseudonym, if applicable) if supplied,
    and/or if the Original Author and/or Licensor designate another party
    or parties (e.g., a sponsor institute, publishing entity, journal) for
    attribution ("Attribution Parties") in Licensor's copyright notice,
    terms of service or by other reasonable means, the name of such party
    or parties; (ii) the title of the Work if supplied; (iii) to the
    extent reasonably practicable, the URI, if any, that Licensor
    specifies to be associated with the Work, unless such URI does not
    refer to the copyright notice or licensing information for the Work;
    and (iv) , consistent with Section 3(b), in the case of an Adaptation,
    a credit identifying the use of the Work in the Adaptation (e.g.,
    "French translation of the Work by Original Author," or "Screenplay
    based on original Work by Original Author"). The credit required by
    this Section 4 (b) may be implemented in any reasonable manner;
    provided, however, that in the case of a Adaptation or Collection, at
    a minimum such credit will appear, if a credit for all contributing
    authors of the Adaptation or Collection appears, then as part of these
    credits and in a manner at least as prominent as the credits for the
    other contributing authors. For the avoidance of doubt, You may only
    use the credit required by this Section for the purpose of attribution
    in the manner set out above and, by exercising Your rights under this
    License, You may not implicitly or explicitly assert or imply any
    connection with, sponsorship or endorsement by the Original Author,
    Licensor and/or Attribution Parties, as appropriate, of You or Your
    use of the Work, without the separate, express prior written
    permission of the Original Author, Licensor and/or Attribution
    Parties.
 c. Except as otherwise agreed in writing by the Licensor or as may be
    otherwise permitted by applicable law, if You Reproduce, Distribute or
    Publicly Perform the Work either by itself or as part of any
    Adaptations or Collections, You must not distort, mutilate, modify or
    take other derogatory action in relation to the Work which would be
    prejudicial to the Original Author's honor or reputation. Licensor
    agrees that in those jurisdictions (e.g. Japan), in which any exercise
    of the right granted in Section 3(b) of this License (the right to
    make Adaptations) would be deemed to be a distortion, mutilation,
    modification or other derogatory action prejudicial to the Original
    Author's honor and reputation, the Licensor will waive or not assert,
    as appropriate, this Section, to the fullest extent permitted by the
    applicable national law, to enable You to reasonably exercise Your
    right under Section 3(b) of this License (right to make Adaptations)
    but not otherwise.

5. Representations, Warranties and Disclaimer

UNLESS OTHERWISE MUTUALLY AGREED TO BY THE PARTIES IN WRITING, LICENSOR
OFFERS THE WORK AS-IS AND MAKES NO REPRESENTATIONS OR WARRANTIES OF ANY
KIND CONCERNING THE WORK, EXPRESS, IMPLIED, STATUTORY OR OTHERWISE,
INCLUDING, WITHOUT LIMITATION, WARRANTIES OF TITLE, MERCHANTIBILITY,
FITNESS FOR A PARTICULAR PURPOSE, NONINFRINGEMENT, OR THE ABSENCE OF
LATENT OR OTHER DEFECTS, ACCURACY, OR THE PRESENCE OF ABSENCE OF ERRORS,
WHETHER OR NOT DISCOVERABLE. SOME JURISDICTIONS DO NOT ALLOW THE EXCLUSION
OF IMPLIED WARRANTIES, SO SUCH EXCLUSION MAY NOT APPLY TO YOU.

6. Limitation on Liability. EXCEPT TO THE EXTENT REQUIRED BY APPLICABLE
LAW, IN NO EVENT WILL LICENSOR BE LIABLE TO YOU ON ANY LEGAL THEORY FOR
ANY SPECIAL, INCIDENTAL, CONSEQUENTIAL, PUNITIVE OR EXEMPLARY DAMAGES
ARISING OUT OF THIS LICENSE OR THE USE OF THE WORK, EVEN IF LICENSOR HAS
BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

7. Termination

 a. This License and the rights granted hereunder will terminate
    automatically upon any breach by You of the terms of this License.
    Individuals or entities who have received Adaptations or Collections
    from You under this License, however, will not have their licenses
    terminated provided such individuals or entities remain in full
    compliance with those licenses. Sections 1, 2, 5, 6, 7, and 8 will
    survive any termination of this License.
 b. Subject to the above terms and conditions, the license granted here is
    perpetual (for the duration of the applicable copyright in the Work).
    Notwithstanding the above, Licensor reserves the right to release the
    Work under different license terms or to stop distributing the Work at
    any time; provided, however that any such election will not serve to
    withdraw this License (or any other license that has been, or is
    required to be, granted under the terms of this License), and this
    License will continue in full force and effect unless terminated as
    stated above.

8. Miscellaneous

 a. Each time You Distribute or Publicly Perform the Work or a Collection,
    the Licensor offers to the recipient a license to the Work on the same
    terms and conditions as the license granted to You under this License.
 b. Each time You Distribute or Publicly Perform an Adaptation, Licensor
    offers to the recipient a license to the original Work on the same
    terms and conditions as the license granted to You under this License.
 c. If any provision of this License is invalid or unenforceable under
    applicable law, it shall not affect the validity or enforceability of
    the remainder of the terms of this License, and without further action
    by the parties to this agreement, such provision shall be reformed to
    the minimum extent necessary to make such provision valid and
    enforceable.
 d. No term or provision of this License shall be deemed waived and no
    breach consented to unless such waiver or consent shall be in writing
    and signed by the party to be charged with such waiver or consent.
 e. This License constitutes the entire agreement between the parties with
    respect to the Work licensed here. There are no understandings,
    agreements or representations with respect to the Work not specified
    here. Licensor shall not be bound by any additional provisions that
    may appear in any communication from You. This License may not be
    modified without the mutual written agreement of the Licensor and You.
 f. The rights granted under, and the subject matter referenced, in this
    License were drafted utilizing the terminology of the Berne Convention
    for the Protection of Literary and Artistic Works (as amended on
    September 28, 1979), the Rome Convention of 1961, the WIPO Copyright
    Treaty of 1996, the WIPO Performances and Phonograms Treaty of 1996
    and the Universal Copyright Convention (as revised on July 24, 1971).
    These rights and subject matter take effect in the relevant
    jurisdiction in which the License terms are sought to be enforced
    according to the corresponding provisions of the implementation of
    those treaty provisions in the applicable national law. If the
    standard suite of rights granted under applicable copyright law
    includes additional rights not granted under this License, such
    additional rights are deemed to be included in the License; this
    License is not intended to restrict the license of any rights under
    applicable law.


Creative Commons Notice

    Creative Commons is not a party to this License, and makes no warranty
    whatsoever in connection with the Work. Creative Commons will not be
    liable to You or any party on any legal theory for any damages
    whatsoever, including without limitation any general, special,
    incidental or consequential damages arising in connection to this
    license. Notwithstanding the foregoing two (2) sentences, if Creative
    Commons has expressly identified itself as the Licensor hereunder, it
    shall have all rights and obligations of Licensor.

    Except for the limited purpose of indicating to the public that the
    Work is licensed under the CCPL, Creative Commons does not authorize
    the use by either party of the trademark "Creative Commons" or any
    related trademark or logo of Creative Commons without the prior
    written consent of Creative Commons. Any permitted use will be in
    compliance with Creative Commons' then-current trademark usage
    guidelines, as may be published on its website or otherwise made
    available upon request from time to time. For the avoidance of doubt,
    this trademark restriction does not form part of this License.

    Creative Commons may be contacted at https://creativecommons.org/.
"""

ZIP_URL = "http://www.thespermwhale.com/jaseweston/babi/tasks_1-20_v1-2.tar.gz"
paths = {
    "en": {
        "qa9": {
            "test": "tasks_1-20_v1-2/en/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/en/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/en/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/en/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/en/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/en/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/en/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/en/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/en/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/en/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/en/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/en/qa15_basic-deduction_train.txt",
        },
        "out.txt": {"out": "tasks_1-20_v1-2/en/out.txt"},
        "qa17": {
            "test": "tasks_1-20_v1-2/en/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/en/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/en/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/en/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/en/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/en/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/en/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/en/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/en/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/en/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/en/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/en/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/en/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/en/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/en/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/en/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/en/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/en/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/en/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/en/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/en/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/en/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/en/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/en/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/en/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/en/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/en/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/en/qa8_lists-sets_test.txt",
        },
    },
    "en-10k": {
        "qa9": {
            "test": "tasks_1-20_v1-2/en-10k/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/en-10k/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/en-10k/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/en-10k/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/en-10k/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/en-10k/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/en-10k/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/en-10k/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/en-10k/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/en-10k/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/en-10k/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/en-10k/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/en-10k/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/en-10k/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/en-10k/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/en-10k/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/en-10k/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/en-10k/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/en-10k/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/en-10k/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/en-10k/qa8_lists-sets_test.txt",
        },
    },
    "en-valid": {
        "qa5": {
            "train": "tasks_1-20_v1-2/en-valid/qa5_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa5_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa5_valid.txt",
        },
        "qa16": {
            "valid": "tasks_1-20_v1-2/en-valid/qa16_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa16_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa16_train.txt",
        },
        "qa2": {
            "valid": "tasks_1-20_v1-2/en-valid/qa2_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa2_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa2_train.txt",
        },
        "qa15": {
            "train": "tasks_1-20_v1-2/en-valid/qa15_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa15_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa15_valid.txt",
        },
        "qa9": {
            "test": "tasks_1-20_v1-2/en-valid/qa9_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa9_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa9_valid.txt",
        },
        "qa1": {
            "valid": "tasks_1-20_v1-2/en-valid/qa1_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa1_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa1_train.txt",
        },
        "qa4": {
            "test": "tasks_1-20_v1-2/en-valid/qa4_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa4_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa4_valid.txt",
        },
        "qa14": {
            "valid": "tasks_1-20_v1-2/en-valid/qa14_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa14_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa14_test.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/en-valid/qa3_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa3_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa3_valid.txt",
        },
        "qa6": {
            "valid": "tasks_1-20_v1-2/en-valid/qa6_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa6_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa6_train.txt",
        },
        "qa8": {
            "test": "tasks_1-20_v1-2/en-valid/qa8_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa8_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa8_train.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/en-valid/qa20_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa20_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa20_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/en-valid/qa11_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa11_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa11_valid.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/en-valid/qa12_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa12_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa12_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/en-valid/qa13_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa13_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa13_train.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/en-valid/qa7_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa7_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa7_valid.txt",
        },
        "qa19": {
            "valid": "tasks_1-20_v1-2/en-valid/qa19_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa19_test.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa19_train.txt",
        },
        "qa17": {
            "train": "tasks_1-20_v1-2/en-valid/qa17_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa17_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa17_valid.txt",
        },
        "qa10": {
            "test": "tasks_1-20_v1-2/en-valid/qa10_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid/qa10_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa10_train.txt",
        },
        "qa18": {
            "valid": "tasks_1-20_v1-2/en-valid/qa18_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid/qa18_train.txt",
            "test": "tasks_1-20_v1-2/en-valid/qa18_test.txt",
        },
    },
    "en-valid-10k": {
        "qa5": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa5_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa5_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa5_valid.txt",
        },
        "qa16": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa16_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa16_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa16_train.txt",
        },
        "qa2": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa2_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa2_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa2_train.txt",
        },
        "qa15": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa15_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa15_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa15_valid.txt",
        },
        "qa9": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa9_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa9_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa9_valid.txt",
        },
        "qa1": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa1_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa1_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa1_train.txt",
        },
        "qa4": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa4_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa4_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa4_valid.txt",
        },
        "qa14": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa14_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa14_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa14_test.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa3_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa3_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa3_valid.txt",
        },
        "qa6": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa6_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa6_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa6_train.txt",
        },
        "qa8": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa8_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa8_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa8_train.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa20_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa20_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa20_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa11_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa11_train.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa11_valid.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa12_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa12_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa12_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa13_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa13_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa13_train.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa7_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa7_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa7_valid.txt",
        },
        "qa19": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa19_valid.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa19_test.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa19_train.txt",
        },
        "qa17": {
            "train": "tasks_1-20_v1-2/en-valid-10k/qa17_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa17_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa17_valid.txt",
        },
        "qa10": {
            "test": "tasks_1-20_v1-2/en-valid-10k/qa10_test.txt",
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa10_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa10_train.txt",
        },
        "qa18": {
            "valid": "tasks_1-20_v1-2/en-valid-10k/qa18_valid.txt",
            "train": "tasks_1-20_v1-2/en-valid-10k/qa18_train.txt",
            "test": "tasks_1-20_v1-2/en-valid-10k/qa18_test.txt",
        },
    },
    "hn": {
        "qa9": {
            "test": "tasks_1-20_v1-2/hn/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/hn/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/hn/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/hn/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/hn/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/hn/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/hn/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/hn/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/hn/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/hn/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/hn/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/hn/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/hn/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/hn/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/hn/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/hn/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/hn/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/hn/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/hn/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/hn/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/hn/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/hn/qa8_lists-sets_test.txt",
        },
    },
    "hn-10k": {
        "qa9": {
            "test": "tasks_1-20_v1-2/hn-10k/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/hn-10k/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/hn-10k/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/hn-10k/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/hn-10k/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/hn-10k/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/hn-10k/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/hn-10k/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/hn-10k/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/hn-10k/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/hn-10k/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/hn-10k/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/hn-10k/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/hn-10k/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/hn-10k/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/hn-10k/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/hn-10k/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/hn-10k/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/hn-10k/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/hn-10k/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/hn-10k/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/hn-10k/qa8_lists-sets_test.txt",
        },
    },
    "shuffled": {
        "qa9": {
            "test": "tasks_1-20_v1-2/shuffled/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/shuffled/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/shuffled/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/shuffled/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/shuffled/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/shuffled/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/shuffled/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/shuffled/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/shuffled/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/shuffled/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/shuffled/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/shuffled/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/shuffled/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/shuffled/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/shuffled/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/shuffled/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/shuffled/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/shuffled/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/shuffled/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/shuffled/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/shuffled/qa8_lists-sets_test.txt",
        },
    },
    "shuffled-10k": {
        "qa9": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa9_simple-negation_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa9_simple-negation_train.txt",
        },
        "qa4": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa4_two-arg-relations_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa4_two-arg-relations_test.txt",
        },
        "qa6": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa6_yes-no-questions_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa6_yes-no-questions_test.txt",
        },
        "qa11": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa11_basic-coreference_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa11_basic-coreference_train.txt",
        },
        "qa3": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa3_three-supporting-facts_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa3_three-supporting-facts_train.txt",
        },
        "qa15": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa15_basic-deduction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa15_basic-deduction_train.txt",
        },
        "qa17": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa17_positional-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa17_positional-reasoning_train.txt",
        },
        "qa13": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa13_compound-coreference_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa13_compound-coreference_train.txt",
        },
        "qa1": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa1_single-supporting-fact_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa1_single-supporting-fact_test.txt",
        },
        "qa14": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa14_time-reasoning_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa14_time-reasoning_test.txt",
        },
        "qa16": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa16_basic-induction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa16_basic-induction_train.txt",
        },
        "qa19": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa19_path-finding_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa19_path-finding_train.txt",
        },
        "qa18": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa18_size-reasoning_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa18_size-reasoning_train.txt",
        },
        "qa10": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa10_indefinite-knowledge_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa10_indefinite-knowledge_test.txt",
        },
        "qa7": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa7_counting_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa7_counting_test.txt",
        },
        "qa5": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa5_three-arg-relations_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa5_three-arg-relations_train.txt",
        },
        "qa12": {
            "test": "tasks_1-20_v1-2/shuffled-10k/qa12_conjunction_test.txt",
            "train": "tasks_1-20_v1-2/shuffled-10k/qa12_conjunction_train.txt",
        },
        "qa2": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa2_two-supporting-facts_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa2_two-supporting-facts_test.txt",
        },
        "qa20": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa20_agents-motivations_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa20_agents-motivations_test.txt",
        },
        "qa8": {
            "train": "tasks_1-20_v1-2/shuffled-10k/qa8_lists-sets_train.txt",
            "test": "tasks_1-20_v1-2/shuffled-10k/qa8_lists-sets_test.txt",
        },
    },
}


class BabiQaConfig(datasets.BuilderConfig):
    def __init__(self, *args, type=None, task_no=None, **kwargs):
        super().__init__(
            *args,
            name=f"{type}-{task_no}",
            **kwargs,
        )
        self.type = type
        self.task_no = task_no


class BabiQa(datasets.GeneratorBasedBuilder):
    """The bAbI QA (20) tasks Dataset"""

    VERSION = datasets.Version("1.2.0")

    BUILDER_CONFIGS = [
        BabiQaConfig(
            type="en",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa2",
            version=VERSION,
            description="This part of the config handles the `qa2` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa3",
            version=VERSION,
            description="This part of the config handles the `qa3` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa4",
            version=VERSION,
            description="This part of the config handles the `qa4` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa5",
            version=VERSION,
            description="This part of the config handles the `qa5` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa6",
            version=VERSION,
            description="This part of the config handles the `qa6` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa7",
            version=VERSION,
            description="This part of the config handles the `qa7` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa8",
            version=VERSION,
            description="This part of the config handles the `qa8` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa9",
            version=VERSION,
            description="This part of the config handles the `qa9` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa10",
            version=VERSION,
            description="This part of the config handles the `qa10` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa11",
            version=VERSION,
            description="This part of the config handles the `qa11` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa12",
            version=VERSION,
            description="This part of the config handles the `qa12` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa13",
            version=VERSION,
            description="This part of the config handles the `qa13` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa14",
            version=VERSION,
            description="This part of the config handles the `qa14` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa15",
            version=VERSION,
            description="This part of the config handles the `qa15` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa16",
            version=VERSION,
            description="This part of the config handles the `qa16` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa17",
            version=VERSION,
            description="This part of the config handles the `qa17` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa18",
            version=VERSION,
            description="This part of the config handles the `qa18` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa19",
            version=VERSION,
            description="This part of the config handles the `qa19` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="en",
            task_no="qa20",
            version=VERSION,
            description="This part of the config handles the `qa20` task of the bAbI `en` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa2",
            version=VERSION,
            description="This part of the config handles the `qa2` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa3",
            version=VERSION,
            description="This part of the config handles the `qa3` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa4",
            version=VERSION,
            description="This part of the config handles the `qa4` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa5",
            version=VERSION,
            description="This part of the config handles the `qa5` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa6",
            version=VERSION,
            description="This part of the config handles the `qa6` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa7",
            version=VERSION,
            description="This part of the config handles the `qa7` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa8",
            version=VERSION,
            description="This part of the config handles the `qa8` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa9",
            version=VERSION,
            description="This part of the config handles the `qa9` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa10",
            version=VERSION,
            description="This part of the config handles the `qa10` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa11",
            version=VERSION,
            description="This part of the config handles the `qa11` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa12",
            version=VERSION,
            description="This part of the config handles the `qa12` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa13",
            version=VERSION,
            description="This part of the config handles the `qa13` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa14",
            version=VERSION,
            description="This part of the config handles the `qa14` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa15",
            version=VERSION,
            description="This part of the config handles the `qa15` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa16",
            version=VERSION,
            description="This part of the config handles the `qa16` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa17",
            version=VERSION,
            description="This part of the config handles the `qa17` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa18",
            version=VERSION,
            description="This part of the config handles the `qa18` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa19",
            version=VERSION,
            description="This part of the config handles the `qa19` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="hn",
            task_no="qa20",
            version=VERSION,
            description="This part of the config handles the `qa20` task of the bAbI `hn` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa2",
            version=VERSION,
            description="This part of the config handles the `qa2` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa3",
            version=VERSION,
            description="This part of the config handles the `qa3` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa4",
            version=VERSION,
            description="This part of the config handles the `qa4` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa5",
            version=VERSION,
            description="This part of the config handles the `qa5` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa6",
            version=VERSION,
            description="This part of the config handles the `qa6` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa7",
            version=VERSION,
            description="This part of the config handles the `qa7` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa8",
            version=VERSION,
            description="This part of the config handles the `qa8` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa9",
            version=VERSION,
            description="This part of the config handles the `qa9` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa10",
            version=VERSION,
            description="This part of the config handles the `qa10` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa11",
            version=VERSION,
            description="This part of the config handles the `qa11` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa12",
            version=VERSION,
            description="This part of the config handles the `qa12` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa13",
            version=VERSION,
            description="This part of the config handles the `qa13` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa14",
            version=VERSION,
            description="This part of the config handles the `qa14` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa15",
            version=VERSION,
            description="This part of the config handles the `qa15` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa16",
            version=VERSION,
            description="This part of the config handles the `qa16` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa17",
            version=VERSION,
            description="This part of the config handles the `qa17` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa18",
            version=VERSION,
            description="This part of the config handles the `qa18` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa19",
            version=VERSION,
            description="This part of the config handles the `qa19` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-10k",
            task_no="qa20",
            version=VERSION,
            description="This part of the config handles the `qa20` task of the bAbI `en-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa2",
            version=VERSION,
            description="This part of the config handles the `qa2` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa3",
            version=VERSION,
            description="This part of the config handles the `qa3` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa4",
            version=VERSION,
            description="This part of the config handles the `qa4` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa5",
            version=VERSION,
            description="This part of the config handles the `qa5` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa6",
            version=VERSION,
            description="This part of the config handles the `qa6` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa7",
            version=VERSION,
            description="This part of the config handles the `qa7` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa8",
            version=VERSION,
            description="This part of the config handles the `qa8` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa9",
            version=VERSION,
            description="This part of the config handles the `qa9` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa10",
            version=VERSION,
            description="This part of the config handles the `qa10` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa11",
            version=VERSION,
            description="This part of the config handles the `qa11` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa12",
            version=VERSION,
            description="This part of the config handles the `qa12` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa13",
            version=VERSION,
            description="This part of the config handles the `qa13` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa14",
            version=VERSION,
            description="This part of the config handles the `qa14` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa15",
            version=VERSION,
            description="This part of the config handles the `qa15` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa16",
            version=VERSION,
            description="This part of the config handles the `qa16` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa17",
            version=VERSION,
            description="This part of the config handles the `qa17` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa18",
            version=VERSION,
            description="This part of the config handles the `qa18` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa19",
            version=VERSION,
            description="This part of the config handles the `qa19` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid",
            task_no="qa20",
            version=VERSION,
            description="This part of the config handles the `qa20` task of the bAbI `en-valid` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa2",
            version=VERSION,
            description="This part of the config handles the `qa2` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa3",
            version=VERSION,
            description="This part of the config handles the `qa3` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa4",
            version=VERSION,
            description="This part of the config handles the `qa4` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa5",
            version=VERSION,
            description="This part of the config handles the `qa5` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa6",
            version=VERSION,
            description="This part of the config handles the `qa6` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa7",
            version=VERSION,
            description="This part of the config handles the `qa7` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa8",
            version=VERSION,
            description="This part of the config handles the `qa8` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa9",
            version=VERSION,
            description="This part of the config handles the `qa9` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa10",
            version=VERSION,
            description="This part of the config handles the `qa10` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa11",
            version=VERSION,
            description="This part of the config handles the `qa11` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa12",
            version=VERSION,
            description="This part of the config handles the `qa12` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa13",
            version=VERSION,
            description="This part of the config handles the `qa13` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa14",
            version=VERSION,
            description="This part of the config handles the `qa14` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa15",
            version=VERSION,
            description="This part of the config handles the `qa15` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa16",
            version=VERSION,
            description="This part of the config handles the `qa16` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa17",
            version=VERSION,
            description="This part of the config handles the `qa17` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa18",
            version=VERSION,
            description="This part of the config handles the `qa18` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa19",
            version=VERSION,
            description="This part of the config handles the `qa19` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="en-valid-10k",
            task_no="qa20",
            version=VERSION,
            description="This part of the config handles the `qa20` task of the bAbI `en-valid-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa2",
            version=VERSION,
            description="This part of the config handles the `qa2` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa3",
            version=VERSION,
            description="This part of the config handles the `qa3` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa4",
            version=VERSION,
            description="This part of the config handles the `qa4` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa5",
            version=VERSION,
            description="This part of the config handles the `qa5` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa6",
            version=VERSION,
            description="This part of the config handles the `qa6` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa7",
            version=VERSION,
            description="This part of the config handles the `qa7` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa8",
            version=VERSION,
            description="This part of the config handles the `qa8` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa9",
            version=VERSION,
            description="This part of the config handles the `qa9` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa10",
            version=VERSION,
            description="This part of the config handles the `qa10` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa11",
            version=VERSION,
            description="This part of the config handles the `qa11` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa12",
            version=VERSION,
            description="This part of the config handles the `qa12` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa13",
            version=VERSION,
            description="This part of the config handles the `qa13` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa14",
            version=VERSION,
            description="This part of the config handles the `qa14` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa15",
            version=VERSION,
            description="This part of the config handles the `qa15` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa16",
            version=VERSION,
            description="This part of the config handles the `qa16` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa17",
            version=VERSION,
            description="This part of the config handles the `qa17` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa18",
            version=VERSION,
            description="This part of the config handles the `qa18` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa19",
            version=VERSION,
            description="This part of the config handles the `qa19` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="hn-10k",
            task_no="qa20",
            version=VERSION,
            description="This part of the config handles the `qa20` task of the bAbI `hn-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa2",
            version=VERSION,
            description="This part of the config handles the `qa2` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa3",
            version=VERSION,
            description="This part of the config handles the `qa3` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa4",
            version=VERSION,
            description="This part of the config handles the `qa4` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa5",
            version=VERSION,
            description="This part of the config handles the `qa5` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa6",
            version=VERSION,
            description="This part of the config handles the `qa6` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa7",
            version=VERSION,
            description="This part of the config handles the `qa7` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa8",
            version=VERSION,
            description="This part of the config handles the `qa8` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa9",
            version=VERSION,
            description="This part of the config handles the `qa9` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa10",
            version=VERSION,
            description="This part of the config handles the `qa10` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa11",
            version=VERSION,
            description="This part of the config handles the `qa11` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa12",
            version=VERSION,
            description="This part of the config handles the `qa12` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa13",
            version=VERSION,
            description="This part of the config handles the `qa13` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa14",
            version=VERSION,
            description="This part of the config handles the `qa14` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa15",
            version=VERSION,
            description="This part of the config handles the `qa15` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa16",
            version=VERSION,
            description="This part of the config handles the `qa16` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa17",
            version=VERSION,
            description="This part of the config handles the `qa17` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa18",
            version=VERSION,
            description="This part of the config handles the `qa18` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa19",
            version=VERSION,
            description="This part of the config handles the `qa19` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled",
            task_no="qa20",
            version=VERSION,
            description="This part of the config handles the `qa20` task of the bAbI `shuffled` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa1",
            version=VERSION,
            description="This part of the config handles the `qa1` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa2",
            version=VERSION,
            description="This part of the config handles the `qa2` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa3",
            version=VERSION,
            description="This part of the config handles the `qa3` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa4",
            version=VERSION,
            description="This part of the config handles the `qa4` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa5",
            version=VERSION,
            description="This part of the config handles the `qa5` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa6",
            version=VERSION,
            description="This part of the config handles the `qa6` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa7",
            version=VERSION,
            description="This part of the config handles the `qa7` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa8",
            version=VERSION,
            description="This part of the config handles the `qa8` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa9",
            version=VERSION,
            description="This part of the config handles the `qa9` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa10",
            version=VERSION,
            description="This part of the config handles the `qa10` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa11",
            version=VERSION,
            description="This part of the config handles the `qa11` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa12",
            version=VERSION,
            description="This part of the config handles the `qa12` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa13",
            version=VERSION,
            description="This part of the config handles the `qa13` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa14",
            version=VERSION,
            description="This part of the config handles the `qa14` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa15",
            version=VERSION,
            description="This part of the config handles the `qa15` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa16",
            version=VERSION,
            description="This part of the config handles the `qa16` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa17",
            version=VERSION,
            description="This part of the config handles the `qa17` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa18",
            version=VERSION,
            description="This part of the config handles the `qa18` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa19",
            version=VERSION,
            description="This part of the config handles the `qa19` task of the bAbI `shuffled-10k` dataset",
        ),
        BabiQaConfig(
            type="shuffled-10k",
            task_no="qa20",
            version=VERSION,
            description="This part of the config handles the `qa20` task of the bAbI `shuffled-10k` dataset",
        ),
    ]

    DEFAULT_CONFIG_NAME = (
        "en-qa1"  # It's not mandatory to have a default configuration. Just use one if it make sense.
    )

    def _info(self):
        features = datasets.Features(
            {
                "story": datasets.Sequence(
                    {
                        "id": datasets.Value("string"),
                        "type": datasets.ClassLabel(names=["context", "question"]),
                        "text": datasets.Value("string"),
                        "supporting_ids": datasets.Sequence(datasets.Value("string")),
                        "answer": datasets.Value("string"),
                    }
                ),
            }
        )
        return datasets.DatasetInfo(
            # This is the description that will appear on the datasets page.
            description=_DESCRIPTION,
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features,
            # specify them here. They'll be used if as_supervised=True in
            # builder.as_dataset.
            supervised_keys=None,
            # Homepage of the dataset for documentation
            homepage=_HOMEPAGE,
            # License for the dataset if available
            license=_LICENSE,
            # Citation for the dataset
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        """Returns SplitGenerators."""
        my_urls = ZIP_URL
        data_dir = dl_manager.download_and_extract(my_urls)
        splits = [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, paths[self.config.type][self.config.task_no]["train"]),
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, paths[self.config.type][self.config.task_no]["test"]),
                },
            ),
        ]
        if "valid" in self.config.type:
            splits += [
                datasets.SplitGenerator(
                    name=datasets.Split.VALIDATION,
                    # These kwargs will be passed to _generate_examples
                    gen_kwargs={
                        "filepath": os.path.join(data_dir, paths[self.config.type][self.config.task_no]["valid"]),
                    },
                ),
            ]
        return splits

    def _generate_examples(self, filepath):

        with open(filepath, encoding="utf-8") as f:
            data = f.readlines()
            story = []
            example_idx = 0
            for idx, line in enumerate(data):
                if line.strip() == "" or idx == len(data) - 1:
                    if story != []:
                        yield example_idx, {"story": story}
                        example_idx += 1
                        story = []
                elif line.strip().split()[0] == "1":  # New story
                    if story != []:  # Already some story, flush it out
                        yield example_idx, {"story": story}
                        example_idx += 1
                        story = []
                    line_no = line.split()[0]
                    line_split = line[len(line_no) :].strip().split("\t")
                    if len(line_split) > 1:
                        story.append(
                            {
                                "id": line_no,
                                "type": 1,  # question
                                "supporting_ids": line_split[-1].split(" "),
                                "text": line_split[0].strip(),
                                "answer": line_split[1].strip(),
                            }
                        )
                    else:
                        story.append(
                            {
                                "id": line_no,
                                "type": 0,  # context
                                "supporting_ids": [],
                                "text": line_split[0].strip(),
                                "answer": "",
                            }
                        )
                    if idx == len(data) - 1:  # Last example and no new line, rare case
                        yield example_idx, {"story": story}
                else:
                    line_no = line.split()[0]
                    line_split = line[len(line_no) :].strip().split("\t")
                    if len(line_split) > 1:
                        story.append(
                            {
                                "id": line_no,
                                "type": 1,  # question
                                "supporting_ids": line_split[-1].split(" "),
                                "text": line_split[0].strip(),
                                "answer": line_split[1].strip(),
                            }
                        )
                    else:
                        story.append(
                            {
                                "id": line_no,
                                "type": 0,  # context
                                "supporting_ids": [],
                                "text": line_split[0].strip(),
                                "answer": "",
                            }
                        )
