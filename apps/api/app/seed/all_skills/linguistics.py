"""Linguistics category — the academic foundation behind language-data work, aimed at
students of Linguistics, English, languages and communication. Each skill applies its
concepts to Nigerian languages and ends in gold-labelled analysis exercises.
"""
from ._common import q, lesson, workflow_lesson, task, labeling, choice_items, number_item, project, skill

COLOR = '#0d9488'

FOUNDATION = lesson(
    'Linguistics for language-data work',
    'See how linguistic knowledge makes AI-language data better.',
    [
        'Annotation guidelines, transcription conventions and evaluation rubrics for African languages are written by people '
        'who understand how those languages work. Knowing that Yoruba tone is phonemic explains why tone marks are required; '
        'knowing morphology explains how to tokenise Igbo verbs; knowing sociolinguistics explains how to treat code-switching.',
        'Linguistics students are therefore well placed to become guideline writers, QA leads and language experts on AI projects '
        '— roles that need both analysis and practical data skills.',
    ],
    points=['Phonetics/phonology → transcription and speech data.', 'Morphology/syntax → tokenisation and annotation.',
            'Semantics/pragmatics → evaluation of meaning.', 'Sociolinguistics/dialectology → sampling and fairness.'],
    quiz=[
        q('Why are tone marks required in Yoruba transcription?', 'Tone distinguishes words (it is phonemic)', 'For decoration', 'To slow readers', 'Only in poetry',
          why='Phonology in practice.'),
        q('Which linguistic area most directly informs speaker sampling across regions?', 'Dialectology / sociolinguistics', 'Syntax', 'Morphology', 'Phonetics only',
          why='Variation across groups.'),
        q('A role that combines linguistics with AI data work is…', 'guideline writer / language QA lead', 'graphic designer', 'accountant', 'driver',
          why='Analysis + data.'),
    ],
)


def _ling_skill(slug, name, *, level, icon, tagline, description, core, steps, mistakes, quality, practice_items,
                assessment_items, guidelines, project_brief, tags=None, hours=5, report=None):
    return skill(
        slug, name, level=level, tags=['linguistics'] + (tags or []), icon=icon, color=COLOR, tagline=tagline,
        description=description, foundation=FOUNDATION, core=core,
        workflow=workflow_lesson(name.lower(), steps, mistakes, quality),
        practice=task(f'{name} exercises', 'Analyse each item.', labeling(practice_items, guidelines), minutes=15),
        assessment=task(f'{name} assessment', 'Scored analysis exercises.',
                        labeling(assessment_items, guidelines, report=report, ai_feedback=bool(report)), minutes=20),
        project_brief=project_brief, hours=hours,
    )


_PLACE = ['Bilabial', 'Labiodental', 'Alveolar', 'Velar', 'Labial-velar', 'Glottal']
PHONETICS = _ling_skill(
    'phonetics', 'Phonetics', level='beginner', icon='ri-speak-line',
    tagline='Describe speech sounds precisely with the IPA.',
    description='Articulatory phonetics and the IPA, applied to Nigerian languages — including labial-velar and implosive sounds English doesn\'t have.',
    core=lesson('Describing consonants', 'Classify consonants by place and manner of articulation.',
                ['Phonetics describes how speech sounds are made. Consonants are classified by <strong>place</strong> (where the airflow '
                 'is blocked: lips, teeth, alveolar ridge, velum), <strong>manner</strong> (stop, fricative, nasal, approximant), and '
                 '<strong>voicing</strong>.',
                 'Nigerian languages include sounds English lacks: labial-velar stops [k͡p] and [ɡ͡b] (Yoruba "p" and "gb", Igbo "kp" '
                 'and "gb") are made at the lips and velum at the same time; Hausa ɓ and ɗ are implosives.'],
                points=['[p b m] bilabial · [f v] labiodental · [t d s n] alveolar · [k ɡ] velar · [h] glottal.',
                        'Yoruba orthographic "p" is pronounced [k͡p], a labial-velar stop.', 'Hausa ɓ = bilabial implosive [ɓ].',
                        'Voicing: [s] voiceless, [z] voiced.'],
                quiz=[q('Place of articulation of [m]?', 'Bilabial', 'Alveolar', 'Velar', 'Glottal', why='Both lips.'),
                      q('Yoruba "p" (as in "pupa") is pronounced as…', '[k͡p], a labial-velar stop', '[p], like English', '[f]', '[b]',
                        why='Yoruba has no plain [p].'),
                      q('[s] and [z] differ in…', 'voicing', 'place', 'manner', 'nasality', why='Same place and manner.')]),
    steps=['Say the sound slowly.', 'Feel where contact happens (place).', 'Notice how air escapes (manner).', 'Check vocal-fold vibration (voicing).'],
    mistakes=['Assuming spelling = sound', 'Forgetting double articulations', 'Mixing up place and manner'],
    quality='Every sound is described by place, manner and voicing.',
    practice_items=choice_items('place', 'Place of articulation', _PLACE, [('[p]', 'Bilabial'), ('[f]', 'Labiodental'), ('[s]', 'Alveolar'), ('[k]', 'Velar')]),
    assessment_items=choice_items('place', 'Place of articulation', _PLACE, [
        ('[m]', 'Bilabial'), ('[ɡ]', 'Velar'), ('[k͡p] (Yoruba "p", Igbo "kp")', 'Labial-velar'), ('[t]', 'Alveolar'),
        ('[v]', 'Labiodental'), ('[h]', 'Glottal')]),
    guidelines=['Choose the place of articulation for each IPA sound.'],
    project_brief=project('IPA transcription of 20 words', 'Choose 20 words in a Nigerian language you speak and transcribe them in the IPA.',
                          ['Word list with orthography, IPA and English gloss', 'Notes on any sounds absent from English'],
                          ['Accurate IPA', 'Correct symbols for special sounds', 'Clear notes'], ['Phonetics', 'IPA'], hours=3),
)

PHONOLOGY = _ling_skill(
    'phonology', 'Phonology', level='intermediate', icon='ri-music-2-line',
    tagline='Analyse sound systems — phonemes, tone and vowel harmony.',
    description='Phonemes, minimal pairs, tone systems and vowel harmony in Yoruba, Igbo and Hausa — and why they matter for transcription and TTS.',
    core=lesson('Phonemes, minimal pairs and tone', 'Use minimal pairs to find contrasts.',
                ['A <strong>phoneme</strong> is a sound that distinguishes meaning in a language. Phonologists find phonemes with '
                 '<strong>minimal pairs</strong>: words that differ in one sound only, like English "pin/bin" (p vs b).',
                 'In tone languages, tone itself is phonemic. Yoruba has three contrastive level tones (high, mid, low): ọkọ, ọkọ̀ and ọkọ́ '
                 'differ only in tone. Igbo has vowel harmony, where vowels in a word agree in tongue-root position.'],
                points=['Minimal pair = one sound difference, different meaning.', 'Yoruba: 3 contrastive level tones.',
                        'Tone can be phonemic, like consonants and vowels.', 'Igbo vowel harmony constrains which vowels co-occur.'],
                quiz=[q('"pin" and "bin" show that /p/ and /b/ are…', 'separate phonemes in English', 'the same phoneme', 'allophones', 'tones', why='Minimal pair.'),
                      q('How many contrastive level tones does Yoruba have?', 'Three', 'Two', 'Four', 'None', why='High, mid, low.'),
                      q('ọkọ vs ọkọ̀ differ in…', 'tone', 'a consonant', 'a vowel', 'length', why='Same segments.')]),
    steps=['Collect word pairs.', 'Check that only one feature differs.', 'Check that meanings differ.', 'Conclude contrast.'],
    mistakes=['Pairs differing in two sounds', 'Ignoring tone', 'Confusing spelling with sound'], quality='Each contrast is proven with a true minimal pair.',
    practice_items=[
        {'id': 'm1', 'text': 'pin / bin (English)', 'fields': [{'name': 'mp', 'label': 'Minimal pair?', 'options': ['Yes', 'No'], 'expected': 'Yes'}]},
        {'id': 'm2', 'text': 'ọkọ / ọkọ̀ (Yoruba)', 'fields': [{'name': 'mp', 'label': 'What distinguishes them?', 'options': ['Tone', 'Consonant', 'Vowel', 'Nothing'], 'expected': 'Tone'}]},
        {'id': 'm3', 'text': 'cat / dog (English)', 'fields': [{'name': 'mp', 'label': 'Minimal pair?', 'options': ['Yes', 'No'], 'expected': 'No'}]},
        number_item('m4', 'Yoruba level tones', 'Number of contrastive level tones', 3)],
    assessment_items=[
        {'id': 'a1', 'text': 'ship / sheep (English)', 'fields': [{'name': 'mp', 'label': 'Minimal pair?', 'options': ['Yes', 'No'], 'expected': 'Yes'}]},
        {'id': 'a2', 'text': 'ọkọ̀ / ọkọ́ (Yoruba)', 'fields': [{'name': 'mp', 'label': 'What distinguishes them?', 'options': ['Tone', 'Consonant', 'Vowel', 'Nothing'], 'expected': 'Tone'}]},
        {'id': 'a3', 'text': 'tin / din (English)', 'fields': [{'name': 'mp', 'label': 'What distinguishes them?', 'options': ['Voicing', 'Place', 'Tone', 'Nothing'], 'expected': 'Voicing'}]},
        {'id': 'a4', 'text': 'book / table (English)', 'fields': [{'name': 'mp', 'label': 'Minimal pair?', 'options': ['Yes', 'No'], 'expected': 'No'}]},
        {'id': 'a5', 'text': 'In Igbo, vowels within a word tend to agree in tongue-root position.', 'fields': [{'name': 'mp', 'label': 'This is called…', 'options': ['Vowel harmony', 'Tone sandhi', 'Assimilation of consonants', 'Elision'], 'expected': 'Vowel harmony'}]}],
    guidelines=['A minimal pair differs in exactly one sound (or tone) and has different meanings.'],
    project_brief=project('Minimal-pair inventory', 'Find 15 minimal pairs (including tone pairs if your language is tonal) in a Nigerian language you speak.',
                          ['Pairs with IPA, tone marks and glosses', 'Which contrasts they prove', 'Implications for transcription guidelines'],
                          ['Valid minimal pairs', 'Accurate glosses', 'Practical implications'], ['Phonology'], difficulty='intermediate', hours=3),
)

MORPHOLOGY = _ling_skill(
    'morphology', 'Morphology', level='beginner', icon='ri-puzzle-2-line',
    tagline='Break words into morphemes and identify word-formation processes.',
    description='Morphemes, inflection vs derivation, and processes like compounding and reduplication — with English and Nigerian Pidgin examples.',
    core=lesson('Morphemes and word formation', 'Segment words and name word-formation processes.',
                ['A morpheme is the smallest unit of meaning. "Unhappiness" = un + happy + ness (3 morphemes). <strong>Inflectional</strong> '
                 'morphemes mark grammar without changing the word class (-s plural, -ed past); <strong>derivational</strong> ones create '
                 'new words (-er in teacher, un- in unkind).',
                 'Processes include affixation, compounding (blackboard), and reduplication — common in Nigerian Pidgin ("small small" '
                 '= gradually; "well well" = very much). Morphology matters for NLP because tokenisers split words into sub-word pieces.'],
                points=['Count morphemes by meaning units, not syllables.', 'Inflection: -s, -ed, -ing. Derivation: un-, -ness, -er.',
                        'Compounding: two words → one.', 'Reduplication: repeating a form for new meaning.'],
                quiz=[q('How many morphemes in "unhappiness"?', '3', '2', '4', '5', why='un-happy-ness.'),
                      q('"-s" in "cats" is…', 'inflectional', 'derivational', 'a root', 'a compound', why='Plural marking.'),
                      q('Pidgin "small small" is an example of…', 'reduplication', 'compounding', 'suffixation', 'borrowing', why='Repeated form.')]),
    steps=['Find the root.', 'Peel off affixes.', 'Classify each affix.', 'Name the process.'],
    mistakes=['Counting syllables', 'Calling -er in "teacher" inflectional', 'Missing zero-change forms'], quality='Segmentation and classification are consistent.',
    practice_items=[number_item('n1', 'unhappiness', 'Number of morphemes', 3), number_item('n2', 'cats', 'Number of morphemes', 2),
                    {'id': 'c1', 'text': '"-er" in "teacher"', 'fields': [{'name': 't', 'label': 'Type', 'options': ['Inflectional', 'Derivational'], 'expected': 'Derivational'}]},
                    {'id': 'c2', 'text': '"blackboard"', 'fields': [{'name': 't', 'label': 'Process', 'options': ['Affixation', 'Compounding', 'Reduplication'], 'expected': 'Compounding'}]}],
    assessment_items=[number_item('n1', 'teachers', 'Number of morphemes', 3), number_item('n2', 'unkindly', 'Number of morphemes', 3),
                      {'id': 'c1', 'text': '"-ed" in "walked"', 'fields': [{'name': 't', 'label': 'Type', 'options': ['Inflectional', 'Derivational'], 'expected': 'Inflectional'}]},
                      {'id': 'c2', 'text': '"un-" in "unkind"', 'fields': [{'name': 't', 'label': 'Type', 'options': ['Inflectional', 'Derivational'], 'expected': 'Derivational'}]},
                      {'id': 'c3', 'text': 'Pidgin "well well"', 'fields': [{'name': 't', 'label': 'Process', 'options': ['Affixation', 'Compounding', 'Reduplication'], 'expected': 'Reduplication'}]},
                      {'id': 'c4', 'text': '"bookshop"', 'fields': [{'name': 't', 'label': 'Process', 'options': ['Affixation', 'Compounding', 'Reduplication'], 'expected': 'Compounding'}]}],
    guidelines=['Morphemes are meaning units.', 'Inflection keeps word class; derivation makes a new word.'],
    project_brief=project('Morphological analysis of 15 words', 'Analyse 15 words from a Nigerian language you speak (or Pidgin): segment, gloss and classify each morpheme.',
                          ['Segmented words with glosses (Leipzig style if possible)', 'Process for each word', 'One pattern you discovered'],
                          ['Accurate segmentation', 'Correct classification', 'Insightful pattern'], ['Morphology'], hours=3),
)

_PHRASES = ['Noun phrase (NP)', 'Verb phrase (VP)', 'Prepositional phrase (PP)', 'Adjective phrase (AP)']
SYNTAX = _ling_skill(
    'syntax', 'Syntax', level='intermediate', icon='ri-git-branch-line',
    tagline='Analyse sentence structure, constituents and word order.',
    description='Constituents, phrase types, grammatical functions and word order — comparing English with Yoruba, Igbo, Hausa and Pidgin (all SVO).',
    core=lesson('Constituents and word order', 'Identify phrases and grammatical functions.',
                ['Syntax studies how words group into constituents. A <strong>noun phrase</strong> (NP) is built around a noun ("the tall '
                 'boy"), a <strong>verb phrase</strong> (VP) around a verb ("ate rice"), a <strong>prepositional phrase</strong> (PP) around '
                 'a preposition ("to the market").',
                 'English, Yoruba, Igbo, Hausa and Nigerian Pidgin are all basically SVO (subject–verb–object), but they differ in details '
                 'such as where adjectives go: Yoruba places adjectives after the noun ("ilé ńlá" — house big).'],
                points=['NP = noun + modifiers; VP = verb + complements; PP = preposition + NP.', 'Subject usually precedes the verb in SVO languages.',
                        'Yoruba/Igbo adjectives follow the noun; English adjectives precede it.', 'Substitution test: can a pronoun replace it? → NP.'],
                quiz=[q('"to the market" is a…', 'Prepositional phrase', 'Noun phrase', 'Verb phrase', 'Clause', why='Headed by "to".'),
                      q('Basic word order of Yoruba?', 'SVO', 'SOV', 'VSO', 'OVS', why='Like English.'),
                      q('In "The tall boy ate rice", the subject is…', 'The tall boy', 'ate', 'rice', 'tall', why='The NP before the verb.')]),
    steps=['Find the main verb.', 'Find its subject and object.', 'Bracket phrases.', 'Label each phrase by its head.'],
    mistakes=['Labelling by meaning not head', 'Splitting a constituent', 'Assuming English adjective order'], quality='Every bracket is a real constituent, labelled by its head.',
    practice_items=choice_items('phrase', 'Phrase type of the bracketed part', _PHRASES, [
        ('[The tall boy] ate rice.', 'Noun phrase (NP)'), ('The tall boy [ate rice].', 'Verb phrase (VP)'),
        ('She went [to the market].', 'Prepositional phrase (PP)'), ('The food is [very sweet].', 'Adjective phrase (AP)')]),
    assessment_items=choice_items('phrase', 'Phrase type of the bracketed part', _PHRASES, [
        ('[My elder sister] lives in Kano.', 'Noun phrase (NP)'), ('My elder sister lives [in Kano].', 'Prepositional phrase (PP)'),
        ('The pikin [don chop the bread].', 'Verb phrase (VP)'), ('The exam was [extremely difficult].', 'Adjective phrase (AP)'),
        ('We [will travel tomorrow].', 'Verb phrase (VP)')]),
    guidelines=['Label the bracketed constituent by its head.'],
    project_brief=project('Comparative syntax notes', 'Compare 10 simple sentences in English and a Nigerian language you speak: word order, adjective position, question formation.',
                          ['Sentence pairs with glosses', 'Bracketed structures', 'A summary of differences'],
                          ['Accurate glosses', 'Correct bracketing', 'Clear comparison'], ['Syntax'], difficulty='intermediate', hours=3),
)

_REL = ['Synonymy', 'Antonymy', 'Hyponymy', 'Homonymy', 'Polysemy']
SEMANTICS = _ling_skill(
    'semantics', 'Semantics', level='intermediate', icon='ri-lightbulb-line',
    tagline='Analyse word and sentence meaning precisely.',
    description='Lexical relations, ambiguity and entailment — the meaning concepts behind semantic annotation and AI evaluation.',
    core=lesson('Lexical relations and ambiguity', 'Classify relations between word meanings.',
                ['Semantics studies meaning. Words relate as <strong>synonyms</strong> (big/large), <strong>antonyms</strong> (hot/cold), '
                 '<strong>hyponyms</strong> (mango is a kind of fruit). A single form can be <strong>homonymous</strong> (unrelated meanings: '
                 'bank of a river vs a bank for money) or <strong>polysemous</strong> (related meanings: head of the body vs head of department).',
                 'These distinctions matter in annotation (word-sense labels) and in evaluating whether a model\'s answer means the same as a reference.'],
                points=['Synonymy: same meaning.', 'Antonymy: opposite.', 'Hyponymy: kind-of.', 'Homonymy: unrelated meanings; polysemy: related meanings.'],
                quiz=[q('"mango" and "fruit" show…', 'Hyponymy', 'Synonymy', 'Antonymy', 'Homonymy', why='Kind-of.'),
                      q('"head" (body) and "head" (of department) show…', 'Polysemy', 'Homonymy', 'Antonymy', 'Synonymy', why='Related meanings.'),
                      q('"bank" (river) and "bank" (money) show…', 'Homonymy', 'Polysemy', 'Hyponymy', 'Synonymy', why='Unrelated meanings.')]),
    steps=['Identify both meanings.', 'Ask whether they are related.', 'Test kind-of and opposite relations.', 'Label.'],
    mistakes=['Confusing homonymy and polysemy', 'Calling near-synonyms antonyms'], quality='Labels follow the definitions.',
    practice_items=choice_items('rel', 'Relation', _REL, [('big / large', 'Synonymy'), ('hot / cold', 'Antonymy'), ('mango / fruit', 'Hyponymy'), ('bank (river) / bank (money)', 'Homonymy')]),
    assessment_items=choice_items('rel', 'Relation', _REL, [('begin / start', 'Synonymy'), ('alive / dead', 'Antonymy'), ('okada / vehicle', 'Hyponymy'),
                                                           ('mouth (person) / mouth (river)', 'Polysemy'), ('bat (animal) / bat (cricket)', 'Homonymy')]),
    guidelines=['Choose the relation between the two meanings.'],
    project_brief=project('Semantic field study', 'Map a semantic field (e.g. kinship, food, colours) in a Nigerian language you speak versus English.',
                          ['20 terms with glosses', 'Relations diagram or table', 'Mismatches with English and implications for translation'],
                          ['Accurate terms', 'Correct relations', 'Insightful mismatches'], ['Semantics'], difficulty='intermediate', hours=3),
)

_ACTS = ['Request', 'Question', 'Promise', 'Apology', 'Greeting', 'Thanks']
PRAGMATICS = _ling_skill(
    'pragmatics', 'Pragmatics', level='intermediate', icon='ri-chat-smile-3-line',
    tagline='Understand meaning in context — speech acts, politeness and implicature.',
    description='Speech acts, indirect requests, implicature and Nigerian politeness conventions — essential for evaluating chatbots and translations.',
    core=lesson('Speech acts and politeness', 'Identify what an utterance does in context.',
                ['Pragmatics studies meaning in context. A <strong>speech act</strong> is what an utterance does: request, promise, apologise, '
                 'greet. Many acts are indirect: "Can you pass the salt?" is a request, not a question about ability.',
                 'Politeness is culture-specific. In Nigeria, "Well done" greets someone at work; elders are addressed with respect forms '
                 '(Yoruba "Ẹ"); and directness that is fine in one culture may be rude in another — which is why literal translations of '
                 'chatbot replies can sound impolite.'],
                points=['Label the act by its function.', 'Indirect requests: "Can you…?", "Would you mind…?"', '"Well done" (to someone working) = greeting.',
                        'Respect forms carry pragmatic meaning.'],
                quiz=[q('"Can you close the door?" is mainly a…', 'Request', 'Question', 'Promise', 'Greeting', why='Indirect request.'),
                      q('"Well done, ma" said to a trader at work is a…', 'Greeting', 'Thanks', 'Apology', 'Request', why='Nigerian greeting.'),
                      q('"I go come tomorrow, no worry" is a…', 'Promise', 'Request', 'Apology', 'Question', why='Commits the speaker.')]),
    steps=['Read the context.', 'Ask what the speaker wants to achieve.', 'Check for indirectness.', 'Label the act.'],
    mistakes=['Labelling by grammatical form', 'Ignoring cultural conventions'], quality='Labels reflect function in context.',
    practice_items=choice_items('act', 'Speech act', _ACTS, [('"Can you pass the salt?"', 'Request'), ('"What time is it?"', 'Question'),
                                                             ('"I\'m sorry I came late."', 'Apology'), ('"Ẹ káàárọ̀ ma."', 'Greeting')]),
    assessment_items=choice_items('act', 'Speech act', _ACTS, [('"Would you mind lowering the volume?"', 'Request'), ('"I go call you tonight, I promise."', 'Promise'),
                                                               ('"Well done, sir." (to a mechanic working)', 'Greeting'), ('"Ẹ ṣé gan-an."', 'Thanks'),
                                                               ('"Abeg forgive me, I no mean am."', 'Apology'), ('"Where you dey?"', 'Question')]),
    guidelines=['Label the function of each utterance in its context.'],
    project_brief=project('Chatbot politeness review', 'Review 10 chatbot replies (real or written by you) for politeness in a Nigerian context and rewrite the problematic ones.',
                          ['Original replies', 'Speech-act and politeness analysis', 'Rewritten replies with reasons'],
                          ['Accurate analysis', 'Culturally appropriate rewrites'], ['Pragmatics'], difficulty='intermediate', hours=2),
)

SOCIOLING = _ling_skill(
    'sociolinguistics', 'Sociolinguistics', level='intermediate', icon='ri-group-line',
    tagline='Study language in society — code-switching, borrowing and register.',
    description='Code-switching, borrowing, register and language attitudes in Nigeria — and how they shape fair, representative datasets.',
    core=lesson('Code-switching, borrowing and register', 'Distinguish key sociolinguistic phenomena.',
                ['Nigeria is massively multilingual. <strong>Borrowing</strong> brings a word into a language permanently ("okada" in '
                 'English, "mọ́tò" from motor in Yoruba). <strong>Code-switching</strong> alternates between languages within a conversation '
                 'or sentence ("Mo fẹ́ lọ, but I no get money"). <strong>Register</strong> is variation by situation: formal, informal, religious.',
                 'Datasets that only include formal standard language under-represent how most people actually speak — a fairness problem.'],
                points=['Borrowing: one integrated word.', 'Code-switching: stretches in two languages.', 'Register: formal vs informal by situation.',
                        'Datasets should reflect real usage.'],
                quiz=[q('"I took an okada to school." "Okada" is…', 'a borrowing', 'code-switching', 'a register', 'an error', why='Integrated word.'),
                      q('"Mo fẹ́ lọ, but I no get money" shows…', 'code-switching', 'borrowing', 'diglossia', 'nothing', why='Two languages alternate.'),
                      q('A sermon vs a chat with friends differ in…', 'register', 'dialect', 'phonology', 'tone', why='Situation.')]),
    steps=['Identify languages present.', 'Single integrated word → borrowing.', 'Stretches in two languages → code-switching.', 'Note the situation → register.'],
    mistakes=['Calling every English word code-switching', 'Treating informal speech as "wrong"'], quality='Phenomena are distinguished correctly.',
    practice_items=choice_items('ph', 'Phenomenon', ['Borrowing', 'Code-switching', 'Formal register', 'Informal register'], [
        ('"I took an okada to school."', 'Borrowing'), ('"Mo fẹ́ lọ, but I no get money."', 'Code-switching'),
        ('"Distinguished guests, it is my honour to welcome you."', 'Formal register'), ('"Guy, how far? Wetin dey sup?"', 'Informal register')]),
    assessment_items=choice_items('ph', 'Phenomenon', ['Borrowing', 'Code-switching', 'Formal register', 'Informal register'], [
        ('Yoruba "mọ́tò" (from English "motor")', 'Borrowing'), ('"Biko come here, I want to show you something."', 'Code-switching'),
        ('"We regret to inform you that the application was unsuccessful."', 'Formal register'),
        ('"Ina kwana? I hope say you sleep well."', 'Code-switching'), ('"Omo, that match sweet!"', 'Informal register')]),
    guidelines=['Choose the main phenomenon shown.'],
    project_brief=project('Code-switching in the wild', 'Collect (with consent, anonymised) 20 code-switched utterances from conversations or public posts.',
                          ['Utterances with languages marked', 'Switch types (between/within sentences)', 'What this means for dataset design'],
                          ['Accurate marking', 'Sound analysis', 'Practical implications'], ['Sociolinguistics'], difficulty='intermediate', hours=3),
)

DIALECTOLOGY = _ling_skill(
    'dialectology', 'Dialectology', level='advanced', icon='ri-map-pin-line',
    tagline='Study dialect variation — continua, isoglosses and standard varieties.',
    description='Dialect continua, isoglosses, mutual intelligibility and standardisation — with care about evidence when labelling African dialects.',
    core=lesson('Mapping dialect variation', 'Use dialectology concepts correctly.',
                ['Dialectology studies regional variation. An <strong>isogloss</strong> is a line on a map separating areas that use different '
                 'forms of a feature. Many African languages form <strong>dialect continua</strong>, where neighbouring varieties are mutually '
                 'intelligible but distant ones may not be.',
                 'A <strong>standard variety</strong> (e.g. Standard Yoruba, largely based on Ọ̀yọ́ varieties) is a socially chosen norm, not a '
                 '"purer" form. Dialect data must be labelled from evidence — self-report or expert analysis — not stereotypes.'],
                points=['Isogloss = boundary of one feature.', 'Dialect continuum = gradual change across space.',
                        'Standard = socially chosen norm, not "more correct".', 'Labels need evidence.'],
                quiz=[q('A line separating areas using different words for the same thing is…', 'an isogloss', 'a phoneme', 'a register', 'a continuum',
                        why='Feature boundary.'),
                      q('Standard Yoruba is…', 'a socially selected norm', 'the oldest dialect', 'the only correct form', 'a separate language',
                        why='Standardisation is social.'),
                      q('Neighbouring varieties understand each other; distant ones struggle. This is…', 'a dialect continuum', 'diglossia', 'borrowing', 'pidginisation',
                        why='Gradual variation.')]),
    steps=['Define the feature.', 'Collect forms from each location.', 'Map them.', 'Draw isoglosses.', 'Interpret carefully.'],
    mistakes=['Ranking dialects as better/worse', 'Generalising from one speaker'], quality='Claims are evidence-based and respectful.',
    practice_items=choice_items('c', 'Concept', ['Isogloss', 'Dialect continuum', 'Standard variety', 'Mutual intelligibility'], [
        ('The boundary between areas that use different words for "corn".', 'Isogloss'),
        ('Village A understands B, B understands C, but A struggles with C.', 'Dialect continuum'),
        ('The variety used in schools, broadcasting and official writing.', 'Standard variety'),
        ('Speakers of two varieties can understand each other without learning.', 'Mutual intelligibility')]),
    assessment_items=choice_items('c', 'Best answer', ['Agree', 'Disagree'], [
        ('A standard variety is linguistically superior to other dialects.', 'Disagree'),
        ('Dialect labels in a dataset should be based on speaker self-report or expert analysis.', 'Agree'),
        ('One speaker is enough to describe a whole dialect.', 'Disagree'),
        ('Isoglosses for different features often do not line up exactly.', 'Agree'),
        ('Mutual intelligibility can be asymmetric.', 'Agree')]),
    guidelines=['Choose the best answer for each statement.'],
    report={'label': 'Explain why a standard variety is not "more correct"', 'min_words': 20},
    project_brief=project('Mini dialect survey', 'Survey 4 speakers (with consent) from different areas on 10 words in a language you know, and map the variation.',
                          ['Word list and responses', 'Simple map or table', 'Possible isoglosses and limits of your data'],
                          ['Careful data', 'Sound interpretation', 'Honest limitations'], ['Dialectology'], difficulty='advanced', hours=4),
)

_CORPUS_CTX = 'Text: "the market is busy and the market is loud"'
CORPUS = _ling_skill(
    'corpus-linguistics', 'Corpus Linguistics', level='intermediate', icon='ri-book-2-line', tags=['nlp'],
    tagline='Analyse language with counts, frequency lists and concordances.',
    description='Tokens, types, frequency, collocation and concordance — the quantitative methods behind every NLP dataset.',
    core=lesson('Tokens, types and frequency', 'Compute basic corpus statistics.',
                ['A corpus is a principled collection of texts. <strong>Tokens</strong> are running words; <strong>types</strong> are distinct '
                 'words. "the cat saw the dog" has 5 tokens and 4 types. The <strong>type–token ratio</strong> (types ÷ tokens) is a rough '
                 'measure of vocabulary variety.',
                 'Concordances (keyword-in-context lines) and collocations (words that co-occur more than chance) reveal how words are '
                 'actually used — vital for building dictionaries and checking datasets.'],
                points=['Tokens = running words; types = distinct words.', 'TTR = types / tokens.', 'Concordance = keyword in context.',
                        'Collocation = frequent co-occurrence.'],
                quiz=[q('Tokens in "the cat saw the dog"?', '5', '4', '3', '6', why='Count every word.'),
                      q('Types in "the cat saw the dog"?', '4', '5', '3', '2', why='"the" counts once.'),
                      q('A keyword-in-context display is a…', 'concordance', 'collocation', 'corpus', 'lemma', why='KWIC.')]),
    steps=['Tokenise consistently.', 'Count tokens.', 'Count types (case-normalised).', 'Compute ratios.', 'Inspect concordances.'],
    mistakes=['Inconsistent tokenisation', 'Counting punctuation as words without a rule', 'Comparing TTR across very different lengths'],
    quality='Counts are reproducible from the stated rules.',
    practice_items=[number_item('t1', 'Text: "the cat saw the dog"', 'Tokens', 5), number_item('t2', 'Text: "the cat saw the dog"', 'Types', 4),
                    number_item('t3', 'Text: "the cat saw the dog"', 'Type-token ratio (2 decimals)', 0.8, 0.01)],
    assessment_items=[number_item('a1', 'Count tokens.', 'Tokens', 9, context=_CORPUS_CTX), number_item('a2', 'Count types.', 'Types', 6, context=_CORPUS_CTX),
                      number_item('a3', 'Type-token ratio (2 decimals).', 'TTR', 0.67, 0.01, context=_CORPUS_CTX),
                      number_item('a4', 'How many times does "market" occur?', 'Frequency', 2, context=_CORPUS_CTX),
                      {'id': 'a5', 'text': 'Lines showing every use of "market" with words either side are a…', 'fields': [
                          {'name': 'c', 'label': 'Answer', 'options': ['Concordance', 'Collocation', 'Lemma', 'Frequency list'], 'expected': 'Concordance'}]}],
    guidelines=['Tokens split on spaces; ignore punctuation.', 'Types are case-insensitive.'],
    project_brief=project('Build a 2,000-word mini corpus', 'Collect 2,000 words of public text in a Nigerian language (with sources) and analyse it.',
                          ['Source list', 'Top-30 frequency list', 'TTR', '5 concordance lines for one interesting word'],
                          ['Principled sampling', 'Correct statistics', 'Insightful observations'], ['Corpus linguistics'],
                          difficulty='intermediate', hours=4),
)

COMPLING = _ling_skill(
    'computational-linguistics', 'Computational Linguistics', level='advanced', icon='ri-cpu-line', tags=['nlp', 'technology'],
    tagline='Formal methods for language: edit distance, n-grams and evaluation metrics.',
    description='The computational core of NLP — edit distance, n-grams, tokenisation and WER — worked by hand so you understand what tools compute.',
    core=lesson('Edit distance, n-grams and WER', 'Compute core NLP measures by hand.',
                ['<strong>Edit distance</strong> (Levenshtein) is the minimum number of insertions, deletions and substitutions to turn one '
                 'string into another: kitten → sitting = 3. <strong>N-grams</strong> are sequences of n items: "a b c d" has 3 bigrams.',
                 '<strong>WER</strong> (word error rate) = (substitutions + deletions + insertions) ÷ reference words — the standard ASR metric '
                 'you saw in transcription QA.'],
                points=['Levenshtein: insert, delete, substitute — each costs 1.', 'A sequence of N items has N−n+1 n-grams.',
                        'WER = (S + D + I) / N.', 'Tokenisation choices change every count.'],
                quiz=[q('Edit distance kitten → sitting?', '3', '2', '4', '7', why='k→s, e→i, insert g.'),
                      q('Bigrams in "a b c d"?', '3', '4', '2', '6', why='N−1.'),
                      q('Reference 10 words; 1 substitution, 1 deletion. WER?', '0.2', '0.1', '0.02', '2', why='2/10.')]),
    steps=['Define units (characters, words).', 'Apply the formula step by step.', 'Double-check counts.', 'Interpret.'],
    mistakes=['Mixing characters and words', 'Off-by-one n-gram counts', 'Dividing WER by the hypothesis length'],
    quality='Every number can be recomputed from the definition.',
    practice_items=[number_item('p1', 'Edit distance between "cat" and "cut"', 'Distance', 1), number_item('p2', 'Bigrams in "how you dey"', 'Count', 2),
                    number_item('p3', 'Reference: 5 words. Hypothesis has 1 substitution.', 'WER (decimal)', 0.2, 0.001)],
    assessment_items=[number_item('a1', 'Edit distance between "kitten" and "sitting"', 'Distance', 3),
                      number_item('a2', 'Edit distance between "oja" and "ọjà" (characters; ọ and à are single characters)', 'Distance', 2),
                      number_item('a3', 'Trigrams in "a b c d e"', 'Count', 3),
                      number_item('a4', 'Reference: 8 words. 1 substitution, 1 deletion, 2 insertions.', 'WER (decimal)', 0.5, 0.001),
                      number_item('a5', 'Word tokens in "Abeg, make we go." (split on spaces)', 'Tokens', 4)],
    guidelines=['Show your working on paper; enter only the final number.'],
    project_brief=project('Hand-checked ASR evaluation', 'Take 5 sentences, get an ASR transcript of yourself reading them (e.g. phone dictation), and compute WER by hand and with a script.',
                          ['References and hypotheses', 'Alignment and S/D/I counts per sentence', 'WER by hand vs script, and any differences explained'],
                          ['Correct alignment', 'Correct WER', 'Clear explanation'], ['Computational linguistics', 'WER'], difficulty='advanced', hours=3),
)

DOCUMENTATION = _ling_skill(
    'african-language-documentation', 'African Language Documentation', level='intermediate', icon='ri-archive-line', tags=['african-languages', 'data-privacy'],
    tagline='Document African languages ethically — recordings, metadata, glossing, archiving.',
    description='Language documentation methods: consent, metadata, interlinear glossing and archiving — preserving under-documented Nigerian languages.',
    core=lesson('Documenting a language', 'Plan documentation with good metadata and glossing.',
                ['Many of Nigeria\'s 500+ languages are under-documented. Documentation creates a lasting record: recordings of natural speech, '
                 'transcriptions, translations and <strong>interlinear glosses</strong> (word-by-word analysis using conventions such as the '
                 'Leipzig Glossing Rules), all with rich <strong>metadata</strong> and community consent.',
                 'Communities own their language data: consent covers how recordings are archived and who may access them. Archives such as '
                 'ELAR keep materials safe with access controls.'],
                points=['Record natural speech, not only word lists.', 'Interlinear gloss: line 1 text, line 2 morpheme glosses, line 3 translation.',
                        'Metadata: who, where, when, language, genre, consent terms.', 'Community consent and access conditions.'],
                quiz=[q('An interlinear gloss typically has…', 'text, morpheme glosses and a free translation', 'only a translation', 'only IPA', 'only metadata',
                        why='Three tiers.'),
                      q('Who should decide access to recordings of sacred stories?', 'The community, through consent terms', 'The researcher alone', 'Anyone online', 'The archive staff only',
                        why='Community rights.'),
                      q('Which is essential metadata?', 'Language, speaker code, date, place, consent terms', 'Speaker\'s bank details', 'Researcher\'s favourite food', 'File colour',
                        why='Context + ethics.')]),
    steps=['Agree goals and consent with the community.', 'Record natural speech.', 'Transcribe and translate.', 'Gloss.', 'Add metadata and archive.'],
    mistakes=['Word lists only', 'Missing consent terms', 'Metadata with personal identifiers'], quality='Materials are usable decades later and respect the community.',
    practice_items=choice_items('ok', 'Good practice?', ['Yes', 'No'], [
        ('Record natural conversations as well as word lists.', 'Yes'), ('Publish all recordings openly without asking.', 'No'),
        ('Include date, place, language and consent terms in metadata.', 'Yes'), ('Store speakers\' phone numbers in the public metadata.', 'No')]),
    assessment_items=choice_items('ok', 'Good practice?', ['Yes', 'No'], [
        ('Use the Leipzig Glossing Rules for interlinear glosses.', 'Yes'), ('Let the community set access conditions for sensitive recordings.', 'Yes'),
        ('Keep only the translation and delete the original-language transcription.', 'No'), ('Deposit materials in an archive with access controls.', 'Yes'),
        ('Skip consent for elders because they are hard to reach.', 'No')]),
    guidelines=['Judge each practice against documentation ethics and standards.'],
    project_brief=project('Document a short text', 'With consent, record a 1–2 minute story or explanation in a Nigerian language. Transcribe, translate and gloss 5 sentences.',
                          ['Audio link', 'Transcription and translation', '5 interlinear-glossed sentences', 'Metadata sheet (no personal identifiers)'],
                          ['Accurate glossing', 'Complete metadata', 'Ethical consent'], ['Language documentation'], difficulty='intermediate', hours=4),
)

SKILLS = [PHONETICS, PHONOLOGY, MORPHOLOGY, SYNTAX, SEMANTICS, PRAGMATICS, SOCIOLING, DIALECTOLOGY, CORPUS, COMPLING, DOCUMENTATION]
