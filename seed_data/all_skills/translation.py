"""Translation category. Language-pair skills are scored with chrF against several
reference translations plus key-term coverage; evaluation/QA/localization skills use
gold-labelled judgements. Students declare the languages they work in on their language
profile (/skills/languages) — each pair skill carries its own Skill.language.

NOTE FOR CONTENT REVIEW: all non-English sentences and references should be checked by
native-speaker translators before wide release; add more references where valid wordings differ.
"""
from ._common import q, lesson, workflow_lesson, task, labeling, choice_items, project, skill

COLOR = '#0284c7'

FOUNDATION = lesson(
    'How translation work runs in language-data projects',
    'Understand what translation data is used for and how it is judged.',
    [
        'Machine-translation systems for African languages are trained and tested on human translations. A '
        'project might ask you to translate sentences, check machine output, or review other translators. Because '
        'the output becomes training or test data, faithfulness to the source matters more than elegance.',
        'Projects judge translations on <strong>accuracy</strong> (same meaning, nothing added or left out), '
        '<strong>fluency</strong> (natural in the target language, correct spelling and diacritics), and '
        '<strong>terminology</strong> (the agreed terms used consistently).',
        'In practice tasks here, your translation is compared automatically with reference translations. '
        'Different correct wordings can score lower than an exact match, so read the references and the coach '
        'notes rather than chasing the number alone.',
    ],
    points=['Translate meaning, not word-by-word.', 'Never add or drop information.',
            'Use correct target-language orthography — tone marks, dotted vowels, hooked letters.',
            'Keep names, numbers and units exactly right.'],
    quiz=[
        q('A source sentence has a detail you think is unimportant. You…', 'translate it anyway — omissions are errors',
          'leave it out to sound natural', 'put it in a footnote', 'summarise it', why='Accuracy means nothing dropped.'),
        q('Which is a FLUENCY problem?', 'Correct meaning but unnatural word order in the target language',
          'A missing sentence', 'A wrong number', 'A mistranslated name', why='The others are accuracy errors.'),
        q('Why might a correct translation get a lower automatic score?', 'It uses different valid wording from the reference',
          'Automatic scores are random', 'It is too short', 'It used punctuation', why='Reference-based metrics reward overlap.'),
    ],
)

STD_GUIDELINES = ['Translate the full meaning; add nothing, drop nothing.',
                  'Use standard spelling in the target language, with all required marks.',
                  'Keep names and numbers exactly as in the source.', 'Use natural, everyday register.']


def _pair_skill(key, name, slug, core_paras, core_points, core_quiz, practice_items, assessment_items, mistakes):
    def items(rows):
        # By convention the last row of each list is the English -> {name} sentence.
        out = []
        for i, row in enumerate(rows, 1):
            source, refs = row[0], row[1]
            terms = row[2] if len(row) > 2 else []
            direction = f'English → {name}' if i == len(rows) else f'{name} → English'
            out.append({'id': f't{i}', 'source': source, 'references': refs, 'key_terms': terms, 'direction': direction})
        return out

    spec = lambda rows, brief: {'kind': 'translation', 'source_lang': name, 'target_lang': 'English',
                                'guidelines': STD_GUIDELINES, 'brief': brief, 'items': items(rows), 'ai_feedback': True}
    return skill(
        slug, f'{name} ↔ English Translation', level='beginner', language=key,
        tags=['translation', 'african-languages'], icon='ri-translate-2', color=COLOR,
        tagline=f'Translate accurately between {name} and English.',
        description=(f'Learn faithful {name}–English translation for language-data projects: meaning over '
                     'word-for-word, correct orthography, consistent terms, and how translations are judged.'),
        foundation=FOUNDATION,
        core=lesson(f'Translating between {name} and English', f'Handle the main {name}–English translation challenges.',
                    core_paras, points=core_points, quiz=core_quiz),
        workflow=workflow_lesson(f'{name}–English translation', [
            'Read the whole source before translating anything.', 'Draft a meaning-first translation.',
            'Check every name, number and term against the source.',
            f'Proofread {name} spelling and marks (or English grammar).', 'Read the translation aloud — does it sound natural?'],
            mistakes, 'A bilingual reviewer finds the same meaning, natural phrasing and correct spelling.'),
        practice=task(f'Translate {name} ↔ English sentences', 'Translate each sentence in the direction shown.',
                      spec(practice_items, 'Sentences in ' + name + ' go into English; English sentences go into ' + name + '.'), minutes=15),
        assessment=task(f'{name} ↔ English translation assessment', 'Translate four sentences. Scored against reference translations.',
                        spec(assessment_items, 'Translate each sentence in the direction shown.'), minutes=20),
        project_brief=project(
            f'Translate a community health notice into {name}',
            'Translate this notice for a community radio announcement:\n"Free malaria testing will hold at the Community '
            'Health Centre this Saturday from 9 a.m. to 2 p.m. Bring your children under five. Sleep under a treated net every '
            'night, and visit the health centre if anyone has a fever for more than two days."',
            [f'The full {name} translation', 'A glossary of 5 key terms (English → ' + name + ')',
             'Translator\'s notes: any phrase with no direct equivalent and how you handled it',
             'A back-translation into English of your own text'],
            ['Accuracy: every detail (day, times, ages, advice) preserved', f'Fluent, correctly spelled {name}',
             'Consistent terminology', 'Useful translator\'s notes'],
            [f'{name}–English translation', 'Terminology'], hours=3),
        hours=6, pass_score=55,
    )


YORUBA = _pair_skill(
    'yoruba', 'Yoruba', 'yoruba-english-translation',
    ['Yoruba greetings and politeness are richer than English ones: "Ẹ" (plural/respectful you) versus "o" signals '
     'respect, and greetings change with the time of day and activity. English renders these with tone of voice or '
     'not at all, so translators must decide what to keep.',
     'Into Yoruba, full tone marking is expected in data projects, and English idioms usually need a Yoruba '
     'equivalent rather than a literal rendering.'],
    ['"Ẹ" vs "o": respectful vs familiar "you" — keep the right one when translating into Yoruba.',
     'Yoruba has no grammatical gender: "ó" can be he, she or it — pick from context.',
     'Translate idioms by meaning, not word for word.', 'Into Yoruba: full tone marks and under-dots.'],
    [q('Yoruba "ó" in "Ó ti dé" can mean…', 'he, she or it — decided by context', 'only he', 'only she', 'they',
       why='Yoruba pronouns are not gendered.'),
     q('Translating "Thank you" for an elder into Yoruba, the respectful form is…', 'Ẹ ṣé', 'O ṣé', 'Ṣé', 'Ẹ káàbọ̀',
       why='Ẹ is the respectful/plural form.'),
     q('An English idiom has no Yoruba equivalent. You…', 'translate its meaning', 'translate word for word', 'leave it in English', 'skip it',
       why='Meaning first.')],
    [('Ẹ káàárọ̀, ṣé dáadáa ni?', ['Good morning, are you well?', 'Good morning, how are you?', 'Good morning, are you doing well?'], ['good morning']),
     ('Mo ń lọ sí ọjà láti ra ẹja.', ['I am going to the market to buy fish.', "I'm going to the market to buy fish."], ['market', 'fish']),
     ('What is your name?', ['Kí ni orúkọ rẹ?'], ['orúkọ'])],
    [('Orúkọ mi ni Adé.', ['My name is Ade.', 'My name is Adé.'], ['name']),
     ('Ọkọ̀ náà ti dé.', ['The vehicle has arrived.', 'The car has arrived.', 'The bus has arrived.'], ['arrived']),
     ('Ẹ jọ̀wọ́, ẹ fún mi ní omi.', ['Please give me water.', 'Please, give me some water.'], ['please', 'water']),
     ('Thank you.', ['Ẹ ṣé.', 'Ẹ ṣeun.', 'O ṣé.', 'O ṣeun.'])],
    ['Dropping tone marks in Yoruba output', 'Assigning a gender the source never stated',
     'Literal idiom translation', 'Using the familiar "o" where respect is required'],
)

IGBO = _pair_skill(
    'igbo', 'Igbo', 'igbo-english-translation',
    ['Igbo expresses many ideas with verb compounds and serial verbs ("bịa nọdụ ala" — come, sit down), which English '
     'often collapses into one verb or splits differently. Translate the action, not each verb.',
     'Into Igbo, the dotted vowels ị, ọ, ụ are part of spelling and must be correct; dialect choices should follow '
     'the guideline (usually standard Igbo).'],
    ['Serial verbs: translate the whole action.', 'Igbo "ọ" can mean he, she or it.',
     'Into Igbo: always the dotted vowels; standard Igbo unless told otherwise.', 'Greetings depend on time of day.'],
    [q('"Bịa nọdụ ala" is best translated as…', 'Come and sit down', 'Come sit ground', 'Sit come down', 'Come to the ground',
       why='Translate the combined action naturally.'),
     q('Into Igbo, which letters must never be dropped?', 'The dotted vowels ị, ọ, ụ', 'Tone marks', 'Capital letters', 'Apostrophes',
       why='They are distinct vowels.'),
     q('Igbo "ọ" in "Ọ bịara" refers to…', 'he, she or it, depending on context', 'only a man', 'only a woman', 'only an object',
       why='Not gendered.')],
    [('Ụtụtụ ọma, kedụ?', ['Good morning, how are you?', 'Good morning, how are you doing?'], ['good morning']),
     ('Ana m aga ahịa ugbu a.', ['I am going to the market now.', "I'm going to the market now."], ['market', 'now']),
     ('Thank you.', ['Daalụ.'])],
    [('Aha m bụ Ada.', ['My name is Ada.'], ['name']),
     ('Nnọọ, bịa nọdụ ala.', ['Welcome, come and sit down.', 'Welcome, come sit down.'], ['welcome', 'sit']),
     ('Biko, nye m mmiri.', ['Please give me water.', 'Please, give me some water.'], ['please', 'water']),
     ('I am fine.', ['Adị m mma.'])],
    ['Translating serial verbs one by one', 'Dropping dots on ị/ọ/ụ', 'Mixing dialects inconsistently', 'Adding a gender'],
)

HAUSA = _pair_skill(
    'hausa', 'Hausa', 'hausa-english-translation',
    ['Hausa greetings are often questions ("Ina kwana?" — literally "How did you sleep?") with set answers ("Lafiya lau"). '
     'Translating them literally sounds odd in English; translate their function ("Good morning" / "Fine").',
     'Hausa marks grammatical gender (ya = he, ta = she) where English may not, and into Hausa the hooked letters '
     'ɓ, ɗ, ƙ, ƴ are required.'],
    ['Translate greetings by function, not literally.', 'Hausa has gender: "ya" he, "ta" she — keep it right both ways.',
     'Into Hausa: hooked letters ɓ, ɗ, ƙ, ƴ.', 'Religious set phrases keep their usual form ("Don Allah").'],
    [q('The most natural English for "Ina kwana?" in a greeting is…', 'Good morning', 'Where is sleep?', 'How sleep?', 'Goodnight',
       why='Translate the function.'),
     q('"Ta tafi" — who left?', 'She did', 'He did', 'They did', 'It is unclear', why='"ta" marks feminine.'),
     q('Into Hausa, "room" must be written…', 'ɗaki', 'daki', 'dhaki', 'room', why='Hooked ɗ.')],
    [('Ina kwana? Lafiya lau.', ['Good morning. Fine.', 'Good morning. I am fine.', 'How did you sleep? Very well.']),
     ('Ina zuwa kasuwa yanzu.', ['I am going to the market now.', "I'm going to the market now."], ['market', 'now']),
     ('Thank you.', ['Na gode.'])],
    [('Na shiga ɗaki.', ['I entered the room.', 'I went into the room.'], ['room']),
     ('Don Allah, ba ni ruwa.', ['Please give me water.', 'Please, give me some water.'], ['please', 'water']),
     ('Ƙasar Najeriya babba ce.', ['Nigeria is a big country.', 'The country of Nigeria is big.'], ['nigeria']),
     ('See you later.', ['Sai an jima.'])],
    ['Literal greetings', 'Losing the gender Hausa marks', 'Dropping hooked letters', 'Over-formal English'],
)

PIDGIN = _pair_skill(
    'pidgin', 'Nigerian Pidgin', 'nigerian-pidgin-english-translation',
    ['Pidgin looks close to English, which is exactly what makes it easy to mistranslate: "sabi" is "know / be good at", '
     '"well well" is "very much", "small" can mean "a little", and "I go" is future ("I will"), not past.',
     'Into Pidgin, use the project spelling list (dey, wetin, abeg, una, pikin, sabi, comot) and natural Pidgin '
     'structure — not English with a few Pidgin words sprinkled in.'],
    ['"I go come" = I will come (future), "I don come" = I have come.', '"Well well" = very / a lot; "small" = a little.',
     '"Una" = you (plural).', 'Into Pidgin: real Pidgin grammar and the agreed spellings.'],
    [q('"I go come tomorrow" means…', 'I will come tomorrow', 'I went and came tomorrow', 'I came tomorrow', 'Go and come tomorrow',
       why='"go" marks future.'),
     q('"The pikin sabi book well well" means the child…', 'is very smart / good at school', 'reads many books', 'owns a book', 'is well',
       why='"sabi book" = good at studies; "well well" = very.'),
     q('"Una" is…', 'you (plural)', 'one', 'we', 'they', why='Second-person plural.')],
    [('How you dey? I dey fine.', ['How are you? I am fine.', "How are you? I'm fine."]),
     ('Abeg make we go market.', ["Please, let's go to the market.", 'Please let us go to the market.'], ['please', 'market']),
     ('What is happening there?', ['Wetin dey happen for there?', 'Wetin dey happen there?'], ['wetin'])],
    [('Una don chop?', ['Have you all eaten?', 'Have you eaten?'], ['eaten']),
     ('No wahala, I go comot now.', ['No problem, I will leave now.', "No problem, I'm leaving now."], ['no problem']),
     ('The pikin sabi book well well.', ['The child is very intelligent.', 'The child is very smart.', 'The child is very good at school.'], ['child']),
     ('Please wait a little.', ['Abeg wait small.', 'Abeg make you wait small.'], ['abeg', 'small'])],
    ['Reading "I go" as past tense', 'Leaving Pidgin words untranslated in English output',
     'English grammar with Pidgin words sprinkled in', 'Inconsistent Pidgin spelling'],
)

AFRICAN = skill(
    'african-language-translation', 'African Language Translation', level='intermediate',
    tags=['translation', 'african-languages'], icon='ri-global-line', color=COLOR,
    tagline='Translation techniques for any African language you work in.',
    description=('Language-independent translation skills for African-language work: idioms, honorifics, culture-specific '
                 'terms, register, and translator\'s notes. Use the language(s) on your language profile for the project.'),
    foundation=FOUNDATION,
    core=lesson('Hard cases in African-language translation', 'Choose the right strategy for difficult content.',
                ['Most translation errors in African-language data come from a small set of hard cases: idioms and proverbs, '
                 'honorifics and respect forms, culture-specific items (foods, titles, festivals), kinship terms that do not map '
                 'to English (e.g. one word for "elder sibling" of any gender), and new technical terms with no established equivalent.',
                 'Strategies: translate the meaning of idioms; keep culture-specific items and explain them if needed; choose the '
                 'kinship term the context supports; for new technical terms use the project glossary, or a descriptive phrase plus '
                 'a translator\'s note.'],
                points=['Idiom/proverb → translate the meaning.', 'Culture-specific item → keep it (borrow) and explain once if needed.',
                        'New technical term → glossary term, else a descriptive phrase + note.',
                        'Kinship/honorifics → follow the context, never guess gender.'],
                quiz=[q('A proverb has no equivalent in the target language. Best strategy:', 'translate its meaning', 'translate word for word',
                        'delete it', 'leave it in the source language', why='Meaning first.'),
                      q('"Jollof" in an English source going into Hausa:', 'keep the word (borrow it)', 'replace it with a different dish',
                        'delete it', 'describe it in 3 sentences', why='Culture-specific items are usually kept.'),
                      q('"Vaccine" has no agreed term in your target language and no glossary entry. You…',
                        'use a clear descriptive phrase and add a translator\'s note', 'invent a new word', 'skip it', 'use any word that sounds close',
                        why='Flag it so the team can agree a term.')]),
    workflow=workflow_lesson('African-language translation', ['Identify hard cases before translating.', 'Check the glossary.',
                             'Choose a strategy per hard case.', 'Write translator\'s notes for every judgement call.',
                             'Back-translate risky sentences to test them.'],
                             ['Literal proverbs', 'Silent guesses on new terms', 'Wrong respect level', 'Unexplained borrowings'],
                             'Every hard case was handled deliberately and documented.'),
    practice=task('Choose translation strategies', 'Pick the best strategy for each hard case.',
                  labeling(choice_items('strategy', 'Best strategy', ['Translate the meaning', 'Keep (borrow) the term', 'Use the glossary term', 'Descriptive phrase + note'], [
                      ('Idiom: "It is raining cats and dogs."', 'Translate the meaning'),
                      ('Food name: "suya"', 'Keep (borrow) the term'),
                      ('"Malaria" — the project glossary lists an agreed term.', 'Use the glossary term'),
                      ('"Two-factor authentication" — no agreed term, no glossary entry.', 'Descriptive phrase + note')]),
                           ['Choose one strategy per item.']), minutes=10),
    assessment=task('Translation strategy assessment', 'Choose strategies and explain one decision.',
                    labeling(choice_items('strategy', 'Best strategy', ['Translate the meaning', 'Keep (borrow) the term', 'Use the glossary term', 'Descriptive phrase + note'], [
                        ('Proverb: "A tree does not make a forest."', 'Translate the meaning'),
                        ('Title: "Oba" in an English text going into Igbo.', 'Keep (borrow) the term'),
                        ('"Polio" — the glossary lists an agreed term.', 'Use the glossary term'),
                        ('"Cloud storage" — no agreed term exists yet.', 'Descriptive phrase + note'),
                        ('Idiom: "to break the ice"', 'Translate the meaning')]),
                             ['Choose one strategy per item.'],
                             report={'label': 'Explain how you would translate "to break the ice" into a language you speak', 'min_words': 20},
                             ai_feedback=True), minutes=15),
    project_brief=project('Translate with translator\'s notes', 'Choose an African language on your profile. Translate a 150-word English public notice of your choice (no private data) and document every hard case.',
                          ['Source text', 'Translation', 'Translator\'s notes for each hard case', 'Back-translation of 3 risky sentences'],
                          ['Accurate and fluent', 'Hard cases handled with a sound strategy', 'Clear notes'],
                          ['African-language translation', 'Translator\'s notes'], difficulty='intermediate', hours=3),
    hours=5,
)

_MT_GUIDE = ['Adequacy 1–5: how much of the source meaning the MT output keeps (5 = all).',
             'Fluency 1–5: how natural and correct the output is in English, ignoring the source (5 = perfect).',
             'Within 1 point of the gold rating counts as agreement.']


def _mt_item(iid, source, reference, mt, adequacy, fluency):
    ctx = f'Source: {source}\nReference: {reference}\nMT output: {mt}'
    return {'id': iid, 'text': mt, 'context': ctx, 'fields': [
        {'name': 'adequacy', 'label': 'Adequacy (1-5)', 'type': 'number', 'expected': adequacy, 'tolerance': 1},
        {'name': 'fluency', 'label': 'Fluency (1-5)', 'type': 'number', 'expected': fluency, 'tolerance': 1}]}


MT_EVAL = skill(
    'machine-translation-evaluation', 'Machine Translation Evaluation', level='intermediate',
    tags=['translation', 'ai', 'evaluation'], icon='ri-scales-3-line', color=COLOR,
    tagline='Rate machine translation output the way MT research teams do.',
    description='Learn adequacy/fluency rating, direct assessment and error spotting for African-language machine translation — the human judgements MT systems are measured against.',
    foundation=FOUNDATION,
    core=lesson('Adequacy, fluency and automatic metrics', 'Rate MT output consistently and understand BLEU/chrF.',
                ['Human MT evaluation usually rates <strong>adequacy</strong> (is the meaning preserved?) and <strong>fluency</strong> '
                 '(is it natural?) separately, because a fluent sentence can be completely wrong, and a correct one can be clumsy.',
                 'Automatic metrics such as BLEU and chrF compare MT output with reference translations by word or character '
                 'overlap. They are cheap but miss valid paraphrases and can be fooled — which is why human judgements remain the '
                 'gold standard, and why raters must be consistent.'],
                points=['Rate adequacy and fluency independently.', 'A fluent but wrong output: high fluency, low adequacy.',
                        'BLEU/chrF measure overlap with references, not meaning directly.', 'Consistency across items matters most.'],
                quiz=[q('An MT output is perfect English but says the opposite of the source. Ratings?', 'High fluency, low adequacy',
                        'Low fluency, high adequacy', 'Both high', 'Both low', why='Fluency ignores the source.'),
                      q('chrF measures…', 'character n-gram overlap with reference translations', 'grammar errors', 'reading speed', 'meaning directly',
                        why='It is an overlap metric.'),
                      q('Why are human ratings still needed?', 'Metrics miss valid paraphrases and meaning errors', 'Metrics are illegal', 'Humans are faster', 'They are not needed',
                        why='Humans judge meaning.')]),
    workflow=workflow_lesson('MT evaluation', ['Read the source and reference first.', 'Rate adequacy against the source.',
                             'Rate fluency reading only the output.', 'Note the main error type.', 'Re-check your scale on earlier items.'],
                             ['Letting fluency drive adequacy', 'Drifting scale over a session', 'Penalising valid paraphrases'],
                             'Ratings are consistent and explainable item by item.'),
    practice=task('Rate MT outputs', 'Rate adequacy and fluency for each machine translation.',
                  labeling([_mt_item('m1', 'Mo ń lọ sí ọjà láti ra ẹja.', 'I am going to the market to buy fish.',
                                     'I am going to the market to buy fish.', 5, 5),
                            _mt_item('m2', 'Ọkọ̀ náà ti dé.', 'The vehicle has arrived.', 'The husband has arrived.', 2, 5),
                            _mt_item('m3', 'Una don chop?', 'Have you all eaten?', 'You have chop done?', 3, 1)], _MT_GUIDE), minutes=15),
    assessment=task('MT evaluation assessment', 'Rate five MT outputs and justify one.',
                    labeling([_mt_item('m1', 'Aha m bụ Ada.', 'My name is Ada.', 'My name is Ada.', 5, 5),
                              _mt_item('m2', 'Na shiga ɗaki.', 'I entered the room.', 'I entered the market.', 2, 5),
                              _mt_item('m3', 'Ẹ jọ̀wọ́, ẹ fún mi ní omi.', 'Please give me water.', 'Please me water give.', 4, 2),
                              _mt_item('m4', 'The pikin sabi book well well.', 'The child is very smart.', 'The child knows the book well.', 3, 4),
                              _mt_item('m5', 'Ana m aga ahịa ugbu a.', 'I am going to the market now.', 'Going.', 1, 2)],
                             _MT_GUIDE, report={'label': 'Explain your adequacy rating for item 4', 'min_words': 15}, ai_feedback=True),
                    minutes=20),
    project_brief=project('Evaluate an MT system on 10 sentences', 'Pick a language you know. Translate 10 everyday sentences with a free MT tool, then evaluate them.',
                          ['Table: source, MT output, your reference, adequacy, fluency, error type', 'A 150-word summary of the system\'s main weaknesses'],
                          ['Consistent ratings', 'Accurate references', 'Insightful error summary'], ['MT evaluation'],
                          difficulty='intermediate', hours=3),
    hours=5,
)

_QA_OPTS = ['No error', 'Mistranslation', 'Omission', 'Addition', 'Grammar/spelling', 'Terminology']

TRANSLATION_QA = skill(
    'translation-quality-assessment', 'Translation Quality Assessment', level='intermediate',
    tags=['translation', 'qa'], icon='ri-file-search-line', color=COLOR,
    tagline='Review translations with an error typology and severity scoring.',
    description='Learn MQM-style translation review: categorise errors, assign severity, compute a quality score and write a clear QA report.',
    foundation=FOUNDATION,
    core=lesson('Error typology and severity', 'Classify translation errors consistently.',
                ['Professional translation QA uses an error typology such as MQM. The core categories are accuracy errors '
                 '(mistranslation, omission, addition), fluency errors (grammar, spelling, diacritics), and terminology errors '
                 '(not using the agreed term).',
                 'Each error also gets a severity: <strong>minor</strong> (noticeable, meaning intact), <strong>major</strong> '
                 '(meaning changed or confusing), <strong>critical</strong> (could cause harm, e.g. a wrong dosage). A quality score '
                 'is computed from weighted error counts, often per 100 words.'],
                points=['Accuracy: mistranslation, omission, addition.', 'Fluency: grammar, spelling, missing diacritics.',
                        'Terminology: agreed term not used.', 'Severity changes the penalty; critical errors fail a file.'],
                quiz=[q('The translation leaves out "for more than two days". Category?', 'Omission', 'Addition', 'Grammar', 'Terminology',
                        why='Missing source content.'),
                      q('A medicine dose is translated as 20 ml instead of 2 ml. Severity?', 'Critical', 'Minor', 'Major', 'No error',
                        why='It could cause harm.'),
                      q('The glossary says use term X but the translator used a synonym Y. Category?', 'Terminology', 'Omission', 'Addition', 'Spelling',
                        why='Agreed term not used.')]),
    workflow=workflow_lesson('translation QA', ['Read source and translation side by side.', 'Mark each error with category and severity.',
                             'Count weighted errors and compute the score.', 'Write a report: summary, top issues, examples, pass/fail.'],
                             ['Marking preferences as errors', 'Missing omissions', 'Inconsistent severities', 'Reports without examples'],
                             'Another reviewer would mark the same errors with the same categories.'),
    practice=task('Categorise translation errors', 'Choose the error category for each translated sentence.',
                  labeling(choice_items('error', 'Error category', _QA_OPTS, [
                      ('Source: "Bring your children under five."\nTranslation: "Bring your children."', 'Omission'),
                      ('Source: "The vehicle has arrived."\nTranslation: "The vehicle has arrived."', 'No error'),
                      ('Source: "Free testing on Saturday."\nTranslation: "Free testing and free food on Saturday."', 'Addition'),
                      ('Source: "I entered the room."\nTranslation: "I entered the market."', 'Mistranslation')]),
                           ['Choose the single most important error per item.', 'Preferences are not errors.']), minutes=12),
    assessment=task('Translation QA assessment', 'Categorise errors, rate severity and write a short QA report.',
                    labeling([
                        {'id': 'e1', 'text': 'Source: "Take 2 ml twice a day."\nTranslation: "Take 20 ml twice a day."',
                         'fields': [{'name': 'error', 'label': 'Category', 'options': _QA_OPTS, 'expected': 'Mistranslation'},
                                    {'name': 'severity', 'label': 'Severity', 'options': ['Minor', 'Major', 'Critical'], 'expected': 'Critical'}]},
                        {'id': 'e2', 'text': 'Source (glossary term: "health centre"): "Visit the health centre."\nTranslation: "Visit the hospital building."',
                         'fields': [{'name': 'error', 'label': 'Category', 'options': _QA_OPTS, 'expected': 'Terminology'},
                                    {'name': 'severity', 'label': 'Severity', 'options': ['Minor', 'Major', 'Critical'], 'expected': 'Minor'}]},
                        {'id': 'e3', 'text': 'Source: "Sleep under a treated net every night."\nTranslation: "Sleep under a net."',
                         'fields': [{'name': 'error', 'label': 'Category', 'options': _QA_OPTS, 'expected': 'Omission'},
                                    {'name': 'severity', 'label': 'Severity', 'options': ['Minor', 'Major', 'Critical'], 'expected': 'Major'}]},
                        {'id': 'e4', 'text': 'Source: "Good morning."\nTranslation (Yoruba): "E kaaaro." (no tone marks or under-dots)',
                         'fields': [{'name': 'error', 'label': 'Category', 'options': _QA_OPTS, 'expected': 'Grammar/spelling'},
                                    {'name': 'severity', 'label': 'Severity', 'options': ['Minor', 'Major', 'Critical'], 'expected': ['Minor', 'Major']}]}],
                        ['Choose the main error and its severity.', 'Critical = could cause harm; Major = meaning changed; Minor = meaning intact.'],
                        report={'label': 'QA report: would you pass this file? Why?', 'min_words': 25}, ai_feedback=True), minutes=20),
    project_brief=project('Full QA report on a translation', 'Find or create a 200-word translation in a language you know (e.g. ask a classmate for one). Review it fully.',
                          ['Source and translation', 'Error log: segment, category, severity, comment', 'Score per 100 words', 'Pass/fail decision with justification'],
                          ['Accurate categorisation', 'Consistent severity', 'Clear, actionable report'], ['Translation QA'],
                          difficulty='intermediate', hours=3),
    hours=5,
)

LOCALIZATION = skill(
    'localization', 'Localization', level='intermediate',
    tags=['translation'], icon='ri-earth-line', color=COLOR,
    tagline='Adapt apps and content so they feel made for Nigerian and African users.',
    description='Go beyond translation: currency, dates, phone numbers, names, tone, cultural references and UI length limits for African markets.',
    foundation=FOUNDATION,
    core=lesson('What localization changes', 'Adapt formats, tone and references for a locale.',
                ['Localization adapts a product for a locale. Beyond translating words, it covers formats (currency ₦, dates '
                 'DD/MM/YYYY in Nigeria, phone numbers +234), measurement units, examples and names, tone and politeness, '
                 'images and cultural references, and UI constraints such as button length.',
                 'A localized string must still fit the interface: a translation that is three times longer than the English '
                 'can break a button. Localizers work with character limits, placeholders like {name} that must not be translated, '
                 'and context notes from developers.'],
                points=['Currency: ₦ / NGN for Nigeria.', 'Dates: DD/MM/YYYY.', 'Never translate placeholders like {name} or %s.',
                        'Respect character limits; use culturally familiar examples.'],
                quiz=[q('An English string is "Hello {name}!". In the translation, {name} should…', 'stay exactly as {name}',
                        'be translated', 'be removed', 'be replaced with a real name', why='Placeholders are code.'),
                      q('How is 5 March 2026 written in Nigerian date format?', '05/03/2026', '03/05/2026', '2026/05/03', '5-Mar',
                        why='Day first.'),
                      q('A button allows 12 characters and your translation has 25. You…', 'find a shorter natural wording or flag it',
                        'submit it anyway', 'cut it off at 12 characters', 'leave it in English', why='Fit the UI or raise it.')]),
    workflow=workflow_lesson('localization', ['Read context notes and limits.', 'Translate with locale formats.',
                             'Protect placeholders and tags.', 'Check length.', 'Review in context (screenshot) if possible.'],
                             ['Translating placeholders', 'US date/currency formats', 'Over-long strings', 'Foreign examples'],
                             'The product reads as if it was written for the user\'s locale.'),
    practice=task('Choose the right locale format', 'Pick the correctly localized version for Nigerian users.',
                  labeling(choice_items('best', 'Best localized version', ['A', 'B', 'C'], [
                      ('Price.\nA: $12.00   B: ₦12,000   C: 12000 NGN dollars', 'B'),
                      ('Date for 5 March 2026.\nA: 03/05/2026   B: 2026-5-3   C: 05/03/2026', 'C'),
                      ('Greeting string "Hello {name}!" in Pidgin.\nA: "How far {name}!"   B: "How far Ada!"   C: "How far {nem}!"', 'A'),
                      ('Phone field placeholder.\nA: +1 555 0100   B: +234 801 234 5678   C: 0044 20 7946', 'B')]),
                           ['Nigeria: ₦, DD/MM/YYYY, +234.', 'Placeholders stay unchanged.']), minutes=10),
    assessment=task('Localization assessment', 'Spot localization problems and explain one fix.',
                    labeling(choice_items('issue', 'Main problem', ['No problem', 'Wrong format', 'Placeholder broken', 'Too long for the UI', 'Culturally unsuitable'], [
                        ('Button (max 10 chars): "Ra báyìí kíákíá lónìí"', 'Too long for the UI'),
                        ('"Welcome back, {nme}!"', 'Placeholder broken'),
                        ('"Delivery on 12/25/2026" (for Nigerian users)', 'Wrong format'),
                        ('Example in a banking app: "Send $50 to your friend in Ohio"', 'Culturally unsuitable'),
                        ('"Pay ₦5,000 by 05/03/2026"', 'No problem')]),
                        ['Choose the main problem for Nigerian users.'],
                        report={'label': 'Rewrite the banking example for Nigerian users and explain', 'min_words': 15}, ai_feedback=True),
                    minutes=15),
    project_brief=project('Localize an app onboarding flow', 'Localize these strings for Nigerian users in Pidgin or another language you know: "Welcome to PayEasy, {name}!", '
                          '"Add money", "Send money to a friend", "Your balance is {amount}", "Verify your phone number", "Transaction failed. Try again."',
                          ['Localized strings with placeholders intact', 'Notes on tone, format and length decisions', 'One string you would push back on, and why'],
                          ['Natural, locale-appropriate wording', 'Placeholders and formats correct', 'Thoughtful notes'],
                          ['Localization'], difficulty='intermediate', hours=2),
    hours=4,
)

SKILLS = [YORUBA, IGBO, HAUSA, PIDGIN, AFRICAN, MT_EVAL, TRANSLATION_QA, LOCALIZATION]
