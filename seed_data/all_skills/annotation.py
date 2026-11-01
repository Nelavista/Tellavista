"""Language Annotation category. Every skill teaches how annotation guidelines work and
ends in gold-labelled practice and assessment items scored against expected labels.

NOTE FOR CONTENT REVIEW: non-English examples should be checked by native speakers.
"""
from ._common import q, lesson, workflow_lesson, task, labeling, choice_items, project, skill

COLOR = '#0891b2'

FOUNDATION = lesson(
    'How annotation guidelines work',
    'Read and apply an annotation guideline the way projects expect.',
    [
        'Annotation turns raw language into training data by attaching labels: a sentiment to a sentence, a type to a '
        'name, an intent to a request. Models learn whatever the labels say — so inconsistent labels teach inconsistent models.',
        'Every project has a <strong>guideline</strong>: the label set, a definition and examples for each label, '
        '<strong>edge-case rules</strong> ("sarcasm counts as negative"), and what to do when unsure (often a "skip" or '
        '"unsure" option). Annotators are measured on agreement with gold labels and with each other.',
        'The professional habit is simple: when the guideline and your instinct disagree, the guideline wins — and if the '
        'guideline is unclear, you raise it rather than inventing your own rule.',
    ],
    points=['Know the label set and each label\'s definition before starting.', 'Edge-case rules override intuition.',
            'Use "unsure/skip" only as the guideline allows.', 'Raise unclear cases; don\'t invent rules.'],
    quiz=[
        q('Your instinct says "positive" but the guideline says sarcasm is negative. You label…', 'negative', 'positive', 'unsure', 'skip',
          why='The guideline wins.'),
        q('The guideline doesn\'t cover a case you keep seeing. You…', 'raise it with the project lead', 'make up your own rule',
          'skip every such item silently', 'label randomly', why='Unclear guidelines get clarified, not improvised.'),
        q('Annotators are often measured on…', 'agreement with gold labels and other annotators', 'typing speed only', 'number of skips', 'item length',
          why='Consistency is the goal.'),
    ],
)


def _with_repeat(items):
    """Appends an unannounced repeat of the first item, as real projects do with gold
    repeats, so the assessment can report labelling consistency."""
    first = items[0]
    return items + [{**first, 'id': first['id'] + 'r', 'repeat_of': first['id']}]


def _label_skill(slug, name, *, level, tags, icon, tagline, description, core, steps, mistakes, quality,
                 field, label, options, guidelines, practice_rows, assessment_rows, project_brief,
                 report=None, language=None, hours=4, pass_score=70):
    return skill(
        slug, name, level=level, tags=['annotation'] + tags, icon=icon, color=COLOR, language=language,
        tagline=tagline, description=description, foundation=FOUNDATION, core=core,
        workflow=workflow_lesson(name.lower(), steps, mistakes, quality),
        practice=task(f'{name}: practice batch', f'Label each item using the {name.lower()} guideline.',
                      labeling(choice_items(field, label, options, practice_rows), guidelines), minutes=12),
        assessment=task(f'{name} assessment', 'Label every item; scored against gold labels.',
                        labeling(_with_repeat(choice_items(field, label, options, assessment_rows)), guidelines,
                                 report=report, ai_feedback=bool(report)), minutes=15),
        project_brief=project_brief, hours=hours, pass_score=pass_score,
    )


TEXT = _label_skill(
    'text-annotation', 'Text Annotation', level='beginner', tags=['nlp'], icon='ri-text',
    tagline='Screen and label text so only good data reaches a corpus.',
    description='The foundation annotation skill: screening text for language, personal data, spam and quality before it enters an African-language corpus.',
    core=lesson('Screening text for a corpus', 'Decide whether a text item is usable.',
                ['Before text is used to train a model, someone checks it: is it in the target language? Does it contain personal '
                 'data (phone numbers, account numbers, home addresses)? Is it spam or boilerplate (cookie banners, "click here")? '
                 'Is it readable?',
                 'Screening labels are usually exclusive and ordered: if an item has personal data, that label wins even if it is '
                 'also in the wrong language.'],
                points=['Usable: target language, readable, no personal data.', 'Personal data always wins.',
                        'Boilerplate and spam are not usable.', 'Mixed language may be usable if the guideline allows.'],
                quiz=[q('A Yoruba sentence contains a phone number. Label?', 'Contains personal data', 'Usable', 'Spam', 'Wrong language',
                        why='Personal data wins.'),
                      q('"Accept all cookies to continue" is…', 'boilerplate', 'usable', 'personal data', 'wrong language', why='Website boilerplate.'),
                      q('Why screen text before training?', 'Bad or private data would be learned by the model', 'To shorten it', 'To translate it', 'No reason',
                        why='Models memorise data.')]),
    steps=['Read the label definitions and their priority order.', 'Read each item fully.', 'Check personal data first.',
           'Then language, then spam/boilerplate.', 'Label; flag anything the guideline doesn\'t cover.'],
    mistakes=['Missing a phone number inside a long text', 'Accepting boilerplate', 'Rejecting mixed-language text the guideline allows'],
    quality='Every item labeled by the priority order, with personal data never let through.',
    field='label', label='Label', options=['Usable', 'Contains personal data', 'Wrong language', 'Spam/boilerplate'],
    guidelines=['Target language: Yoruba.', 'Priority: personal data > spam/boilerplate > wrong language > usable.',
                'Yoruba with a few English words is still usable.'],
    practice_rows=[('Mo ń lọ sí ọjà láti ra ẹja.', 'Usable'),
                   ('Ẹ pè mí ní 0803 123 4567 lálẹ́ yìí.', 'Contains personal data'),
                   ('Click here to accept all cookies.', 'Spam/boilerplate'),
                   ('Ana m aga ahịa ugbu a.', 'Wrong language')],
    assessment_rows=[('Orúkọ mi ni Adé, mo wà ní school.', 'Usable'),
                     ('WIN ₦1,000,000 NOW!!! Click the link to claim', 'Spam/boilerplate'),
                     ('Account number mi ni 0123456789, ẹ fi owó ránṣẹ́.', 'Contains personal data'),
                     ('Na shiga ɗaki.', 'Wrong language'),
                     ('Ẹ káàárọ̀, ṣé dáadáa ni?', 'Usable')],
    project_brief=project('Screen a 40-item text sample', 'Collect 40 short public sentences in a language you know (news comments, public posts — no private messages) and screen them.',
                          ['The 40 items with labels', 'Your guideline (labels, priority, examples)', 'Label counts and 3 hard cases explained'],
                          ['Correct, consistent labels', 'Clear guideline', 'No personal data left in the usable set'], ['Text annotation'], hours=2),
)

SPEECH = _label_skill(
    'speech-annotation', 'Speech Annotation', level='beginner', tags=['speech-data'], icon='ri-sound-module-line',
    tagline='Tag speech events — noise, music, overlap, laughter — consistently.',
    description='Label non-speech and paralinguistic events in audio with a fixed tag set, the way ASR and audio-event datasets need.',
    core=lesson('Speech event tags', 'Choose the right event tag for what is heard.',
                ['Speech annotation goes beyond words: it marks events that affect how audio is used — background noise, music, '
                 'overlapping speakers, laughter, coughs, and unintelligible stretches. Each project fixes a small tag set with '
                 'definitions, and you may only use those tags.',
                 'Choose the most specific tag the guideline defines. Music with singing is usually [music], not speech; two '
                 'people talking at once is [crosstalk].'],
                points=['Use only the project\'s tags.', '[crosstalk] = overlapping speakers.', '[music] covers singing and instruments.',
                        '[inaudible] = speech you can\'t make out.'],
                quiz=[q('Two speakers talk over each other. Tag?', '[crosstalk]', '[noise]', '[inaudible]', '[music]', why='Overlap.'),
                      q('A radio plays a song in the background. Tag?', '[music]', '[noise]', '[crosstalk]', '[laughter]', why='Music, including singing.'),
                      q('You hear speech but can\'t make out the words. Tag?', '[inaudible]', '[noise]', '[crosstalk]', 'nothing', why='Unintelligible speech.')]),
    steps=['Learn the tag set and definitions.', 'Listen through once.', 'Mark each event at the right position.', 'Check every tag is from the list.'],
    mistakes=['Inventing tags', 'Using [noise] for music', 'Missing short overlaps'],
    quality='Tags are from the list, correctly chosen and placed.',
    field='tag', label='Tag', options=['[noise]', '[music]', '[crosstalk]', '[laughter]', '[inaudible]'],
    guidelines=['Tags: [noise] (non-speech sounds: horns, doors, generators), [music], [crosstalk], [laughter], [inaudible].',
                'Choose the single best tag for the described event.'],
    practice_rows=[('A generator hums loudly under the speaker.', '[noise]'), ('Someone laughs after a joke.', '[laughter]'),
                   ('A church choir is singing in the distance.', '[music]'), ('Two people answer at the same time.', '[crosstalk]')],
    assessment_rows=[('A car horn blares mid-sentence.', '[noise]'), ('The speaker mumbles three words you cannot make out.', '[inaudible]'),
                     ('A Fuji song plays from a shop nearby.', '[music]'), ('The interviewer and respondent speak over each other.', '[crosstalk]'),
                     ('The audience bursts into laughter.', '[laughter]')],
    project_brief=project('Event-tag a recording', 'Record (with consent) 2 minutes of a lively setting — a market, a family meal — and tag every event with timestamps.',
                          ['Audio link', 'Event list: time, tag, short note'], ['Correct tags', 'Accurate times', 'Nothing invented'], ['Speech annotation'], hours=2),
)

INTENT = _label_skill(
    'intent-classification', 'Intent Classification', level='beginner', tags=['nlp', 'ai'], icon='ri-question-answer-line',
    tagline='Label what a user wants from a chatbot or voice assistant.',
    description='Classify user messages — in English, Pidgin and code-switched text — into intents for customer-service and voice-assistant datasets.',
    core=lesson('Intents and edge cases', 'Assign the right intent, including in Pidgin and mixed language.',
                ['Assistants route each user message by its <strong>intent</strong> — what the user wants done. The label is the goal, '
                 'not the words: "abeg my money never enter" and "I sent money but it has not arrived" are the same complaint.',
                 'Guidelines define each intent and an "out of scope" label for messages the assistant can\'t handle.'],
                points=['Label the goal, not the keywords.', 'Pidgin and English can express the same intent.',
                        'Greeting + request → label the request.', 'Unhandled requests → out_of_scope.'],
                quiz=[q('"Good evening, abeg how I fit check my balance?" Intent?', 'check_balance', 'greeting', 'complaint', 'out_of_scope',
                        why='Label the request, not the greeting.'),
                      q('Intent labels describe…', 'what the user wants', 'which words appear', 'the user\'s mood', 'message length', why='Goal.'),
                      q('"Recommend a good jollof spot" to a banking bot. Intent?', 'out_of_scope', 'check_balance', 'complaint', 'greeting',
                        why='The bot can\'t handle it.')]),
    steps=['Learn every intent definition.', 'Read the whole message.', 'Find the user\'s goal.', 'Pick the intent; use out_of_scope when none fit.'],
    mistakes=['Keyword matching', 'Labelling the greeting instead of the request', 'Forcing out-of-scope messages into an intent'],
    quality='Labels match the user\'s goal regardless of language or phrasing.',
    field='intent', label='Intent', options=['check_balance', 'buy_airtime', 'transfer_money', 'complaint', 'greeting', 'out_of_scope'],
    guidelines=['Bank/telco assistant intents: check_balance, buy_airtime, transfer_money, complaint, greeting, out_of_scope.',
                'If a message greets AND asks for something, label the request.'],
    practice_rows=[('How much remain for my account?', 'check_balance'), ('Abeg recharge ₦500 airtime for me', 'buy_airtime'),
                   ('Send 2k to my brother', 'transfer_money'), ('Hello, good morning', 'greeting')],
    assessment_rows=[('I sent money since morning and e never enter, this is not fair', 'complaint'),
                     ('Good afternoon, abeg buy data and airtime for ₦1000', 'buy_airtime'),
                     ('Wetin be my balance now?', 'check_balance'), ('Who won the match yesterday?', 'out_of_scope'),
                     ('Transfer ₦15,000 to Chika', 'transfer_money'), ('Ẹ káàsán o', 'greeting')],
    project_brief=project('Build an intent dataset', 'Write 40 realistic user messages (English, Pidgin, mixed) for a school-fees payment assistant, with 5–6 intents.',
                          ['Intent definitions with examples', 'The 40 labeled messages', 'Label distribution and 3 tricky cases'],
                          ['Clear intent definitions', 'Natural, varied messages', 'Consistent labels'], ['Intent classification'], hours=2),
)

SENTIMENT = _label_skill(
    'sentiment-annotation', 'Sentiment Annotation', level='beginner', tags=['nlp', 'ai'], icon='ri-emotion-line',
    tagline='Label sentiment in Nigerian English, Pidgin and code-switched text.',
    description='Annotate positive, negative, neutral and mixed sentiment — including sarcasm and Pidgin intensifiers — for African-language sentiment datasets.',
    core=lesson('Sentiment in Nigerian text', 'Label sentiment correctly, sarcasm and Pidgin included.',
                ['Sentiment annotation asks how the writer feels about what they describe. Nigerian social text is full of signals '
                 'models miss: Pidgin intensifiers ("sweet well well", "slow die"), sarcasm ("Nice one NEPA, light don go again"), and '
                 'code-switching.',
                 'Typical labels: positive, negative, neutral (no opinion, just facts), and mixed (clearly both).'],
                points=['Neutral = facts with no opinion.', 'Mixed = clear positive AND negative parts.', 'Sarcasm is labeled by its real meaning.',
                        '"Die", "well well", "no be small" are intensifiers.'],
                quiz=[q('"Nice one NEPA, light don go again 🙄" Sentiment?', 'Negative', 'Positive', 'Neutral', 'Mixed', why='Sarcasm.'),
                      q('"The shop opens at 9am." Sentiment?', 'Neutral', 'Positive', 'Negative', 'Mixed', why='Just a fact.'),
                      q('"Food sweet but the service slow die." Sentiment?', 'Mixed', 'Positive', 'Negative', 'Neutral', why='Both.')]),
    steps=['Read the whole text.', 'Decide if there is any opinion.', 'Check for sarcasm.', 'Check for both polarities.', 'Label.'],
    mistakes=['Taking sarcasm literally', 'Calling factual text negative', 'Missing Pidgin intensifiers'],
    quality='Labels reflect the writer\'s real attitude, including sarcasm.',
    field='sentiment', label='Sentiment', options=['Positive', 'Negative', 'Neutral', 'Mixed'],
    guidelines=['Positive / Negative / Neutral (no opinion) / Mixed (both clearly present).', 'Sarcasm = its real meaning.'],
    practice_rows=[('This phone sweet well well!', 'Positive'), ('Network don spoil again, I tire.', 'Negative'),
                   ('The meeting is at 4pm on Friday.', 'Neutral'), ('The jollof was nice but the place too hot.', 'Mixed')],
    assessment_rows=[('Wow, another fuel queue. Just what I needed today 😒', 'Negative'), ('Ẹ ṣé gan-an, the delivery was fast!', 'Positive'),
                     ('The new bus stop is at Ojota.', 'Neutral'), ('Na correct movie, but the ending no make sense.', 'Mixed'),
                     ('This lecturer no dey play, him class sweet die.', 'Positive')],
    project_brief=project('Sentiment mini-dataset', 'Collect 40 public product or service comments (Nigerian English/Pidgin/mixed, no usernames) and label them.',
                          ['The 40 comments with labels', 'Guideline with sarcasm and mixed rules', 'Distribution + 3 hard cases'],
                          ['Accurate labels', 'Sound edge-case rules', 'No personal data'], ['Sentiment annotation'], hours=2),
)

NER = _label_skill(
    'named-entity-annotation', 'Named Entity Annotation', level='intermediate', tags=['nlp'], icon='ri-bookmark-line',
    tagline='Label people, places, organisations and dates in African-language text.',
    description='Annotate named entities (PER, LOC, ORG, DATE) in Yoruba, Pidgin and English text, following MasakhaNER-style conventions.',
    core=lesson('Entity types and boundaries', 'Assign the right entity type to a span.',
                ['Named entity recognition (NER) datasets — such as MasakhaNER for African languages — label spans as PER (people), '
                 'LOC (places), ORG (organisations) and DATE. The same word can be different types: "Lagos" is LOC in "I live in Lagos" '
                 'but part of an ORG in "Lagos State University".',
                 'Label the whole name ("Lagos State University", not just "Lagos") and use context, not the word alone.'],
                points=['PER: people (and names with titles: "Dr. Bello").', 'LOC: cities, states, countries, landmarks.',
                        'ORG: companies, universities, agencies, teams.', 'DATE: days, dates, months, years.'],
                quiz=[q('"Lagos" in "Lagos State University admitted me" belongs to…', 'an ORG span (the whole university name)', 'LOC', 'PER', 'DATE',
                        why='Context decides.'),
                      q('"Monday" in "Adé travelled on Monday" is…', 'DATE', 'PER', 'LOC', 'not an entity', why='Days are DATE.'),
                      q('The best span for the organisation in "She works at Dangote Group" is…', 'Dangote Group', 'Dangote', 'Group', 'works at Dangote',
                        why='The whole name.')]),
    steps=['Read the sentence.', 'Find every candidate name or date.', 'Decide type from context.', 'Mark the full span.'],
    mistakes=['Labelling only part of a name', 'Typing by the word alone, not context', 'Missing dates'],
    quality='Each entity has the right type and full span.',
    field='type', label='Entity type of the quoted span', options=['PER', 'LOC', 'ORG', 'DATE', 'Not an entity'],
    guidelines=['PER, LOC, ORG, DATE as in the lesson.', 'Judge the quoted span in its sentence.'],
    practice_rows=[('Adé travelled to Ìbàdàn on Monday. — Span: "Ìbàdàn"', 'LOC'),
                   ('Adé travelled to Ìbàdàn on Monday. — Span: "Adé"', 'PER'),
                   ('She works at Dangote Group. — Span: "Dangote Group"', 'ORG'),
                   ('We go see for December. — Span: "December"', 'DATE')],
    assessment_rows=[('Lagos State University don resume. — Span: "Lagos State University"', 'ORG'),
                     ('Dr. Bello lives in Kano. — Span: "Kano"', 'LOC'),
                     ('Dr. Bello lives in Kano. — Span: "Dr. Bello"', 'PER'),
                     ('Super Eagles will play on 12 June 2026. — Span: "12 June 2026"', 'DATE'),
                     ('Super Eagles will play on 12 June 2026. — Span: "Super Eagles"', 'ORG'),
                     ('I dey go market now. — Span: "market"', 'Not an entity')],
    project_brief=project('NER-annotate 30 sentences', 'Take 30 sentences from public news in a language you know and annotate all PER/LOC/ORG/DATE entities.',
                          ['Sentences with entities marked [like this|LOC]', 'Entity counts by type', '3 ambiguous cases and your decision'],
                          ['Correct types', 'Full spans', 'Reasoned ambiguity decisions'], ['Named entity annotation'],
                          difficulty='intermediate', hours=3),
)

TOPIC = _label_skill(
    'topic-classification', 'Topic Classification', level='beginner', tags=['nlp'], icon='ri-folders-line',
    tagline='Sort news and posts into topics consistently.',
    description='Classify headlines and short texts by topic, as in African news topic-classification datasets.',
    core=lesson('Choosing the main topic', 'Pick the single best topic for a text.',
                ['Topic datasets (e.g. MasakhaNEWS) label each article with one main topic. Many texts touch several topics; '
                 'label what the text is mainly about. A story about a football club\'s finances is usually sports if it\'s on the '
                 'sports page, business if it\'s about company deals — the guideline decides.',
                 'Headlines are short and often use idioms or names, so domain knowledge (who is a footballer, who is a minister) helps.'],
                points=['One main topic per text.', 'Use the guideline\'s tie-break rules.', 'Names and context reveal the domain.'],
                quiz=[q('"CBN raises interest rate to curb inflation" topic?', 'Business', 'Politics', 'Sports', 'Health', why='Monetary policy.'),
                      q('A text covers two topics. You…', 'choose the main one, per the guideline', 'pick both', 'skip it', 'pick randomly', why='Single label.'),
                      q('"Osimhen scores twice as Super Eagles win" topic?', 'Sports', 'Entertainment', 'Politics', 'Business', why='Football.')]),
    steps=['Read the headline/text.', 'Identify the main subject.', 'Apply tie-break rules.', 'Label.'],
    mistakes=['Labelling a minor mention', 'Ignoring tie-break rules', 'Guessing from one word'],
    quality='Each text gets its main topic, consistent with the guideline.',
    field='topic', label='Topic', options=['Politics', 'Business', 'Sports', 'Health', 'Entertainment', 'Education'],
    guidelines=['One main topic.', 'Government decisions about money = Business; elections and parties = Politics.'],
    practice_rows=[('Osimhen scores twice as Super Eagles win', 'Sports'), ('Senate passes new electoral bill', 'Politics'),
                   ('Lassa fever cases rise in three states', 'Health'), ('WAEC releases 2026 results', 'Education')],
    assessment_rows=[('Naira gains against dollar at official window', 'Business'), ('Burna Boy announces world tour dates', 'Entertainment'),
                     ('Governorship candidates sign peace accord', 'Politics'), ('New vaccine drive targets children under five', 'Health'),
                     ('JAMB extends registration deadline', 'Education'), ('D\'Tigress qualify for Olympics', 'Sports')],
    project_brief=project('Topic-label 40 headlines', 'Collect 40 recent headlines from Nigerian outlets (any language) and label their topics.',
                          ['Headlines with labels', 'Tie-break rules you used', 'Distribution chart or table'], ['Correct labels', 'Clear rules'],
                          ['Topic classification'], hours=2),
)

LANG_ID = _label_skill(
    'language-identification', 'Language Identification', level='beginner', tags=['nlp', 'african-languages'], icon='ri-translate',
    tagline='Identify which Nigerian language a text is written in.',
    description='Label text by language — Yoruba, Igbo, Hausa, Pidgin, English or mixed — using orthographic and lexical clues.',
    core=lesson('Clues that reveal the language', 'Use spelling and vocabulary to identify languages.',
                ['Language identification is the first filter in most African-language data pipelines, and automatic tools confuse '
                 'closely related or under-resourced languages. Human labels fix that.',
                 'Clues: Yoruba uses ẹ, ọ, ṣ and tone accents; Igbo uses ị, ọ, ụ and ṅ; Hausa uses ɓ, ɗ, ƙ; Pidgin uses English-like '
                 'words with dey, wetin, abeg, una. Text that clearly mixes two languages is labeled Mixed (code-switched).'],
                points=['Yoruba: ẹ ọ ṣ + tone marks.', 'Igbo: ị ọ ụ ṅ.', 'Hausa: ɓ ɗ ƙ ƴ.', 'Pidgin: dey, wetin, abeg, una, don.'],
                quiz=[q('"Ụtụtụ ọma" is…', 'Igbo', 'Yoruba', 'Hausa', 'Pidgin', why='ụ is an Igbo letter.'),
                      q('"Na gode" is…', 'Hausa', 'Igbo', 'Yoruba', 'English', why='Hausa "thank you".'),
                      q('"I dey come, abeg wait" is…', 'Nigerian Pidgin', 'English', 'Yoruba', 'Hausa', why='dey, abeg.')]),
    steps=['Scan for special letters.', 'Look for function words.', 'Decide single vs mixed language.', 'Label.'],
    mistakes=['Calling Pidgin "English"', 'Confusing ọ (Yoruba and Igbo both use it) — check other clues', 'Ignoring code-switching'],
    quality='Labels are right even for short and mixed texts.',
    field='language', label='Language', options=['Yoruba', 'Igbo', 'Hausa', 'Nigerian Pidgin', 'English', 'Mixed'],
    guidelines=['Mixed = two languages clearly present in one text.', 'A single English loanword does not make text Mixed.'],
    practice_rows=[('Ẹ káàárọ̀, ṣé dáadáa ni?', 'Yoruba'), ('Adị m mma, daalụ.', 'Igbo'), ('Na shiga ɗaki.', 'Hausa'), ('Wetin dey happen?', 'Nigerian Pidgin')],
    assessment_rows=[('Ina zuwa kasuwa yanzu.', 'Hausa'), ('Nnọọ, bịa nọdụ ala.', 'Igbo'), ('Mo fẹ́ ra bread àti ẹyin.', 'Yoruba'),
                     ('Abeg, make una wait small.', 'Nigerian Pidgin'), ('The meeting has been moved to Friday.', 'English'),
                     ('Ẹ káàárọ̀ sir, how was your night? I hope say you dey fine.', 'Mixed')],
    project_brief=project('Language-ID sample', 'Collect 40 short public texts from Nigerian social media in at least 4 languages and label them.',
                          ['Texts with labels', 'The clues you used per language', 'Hard cases (short or mixed texts)'],
                          ['Accurate labels', 'Useful clue list', 'No personal data'], ['Language identification'], hours=2),
)

DIALECT_ID = _label_skill(
    'dialect-identification', 'Dialect Identification', level='intermediate', tags=['nlp', 'dialect', 'linguistics'], icon='ri-map-2-line',
    tagline='Identify language varieties from lexical and spelling cues.',
    description='Learn how variety and dialect identification works, practise on English and Pidgin varieties, and learn why African-language dialect labels need native-speaker evidence.',
    core=lesson('Varieties, dialects and evidence', 'Identify varieties from reliable cues.',
                ['Dialect identification labels which variety of a language a text or recording comes from. Reliable cues are '
                 'lexical (words used only in one variety), spelling conventions, and grammatical constructions — not stereotypes.',
                 'For African languages (e.g. Yoruba dialects like Ìjẹ̀bú or Èkìtì, Igbo varieties), dialect labels in datasets '
                 'should come from speakers\' self-reports or expert annotators who speak the variety. When the cues are not '
                 'decisive, the right label is "cannot tell".'],
                points=['Use lexical, spelling and grammar cues — never stereotypes.', 'Nigerian English: "flash me", "I\'m coming" (= back soon), "well done" (greeting).',
                        'Nigerian English shares British spelling and much vocabulary (colour, lorry, flat) — those cues are NOT decisive between them.', 'British: cuppa, mate, knackered. American: gas station, freeway.', 'Ghanaian Pidgin "chale" vs Nigerian Pidgin "abeg".',
                        'Not decisive → "Cannot tell".'],
                quiz=[q('"Chale, how far?" most likely comes from…', 'Ghanaian Pidgin', 'British English', 'Hausa', 'Nigerian Standard English',
                        why='"Chale" is a Ghanaian marker.'),
                      q('A sentence has no variety-specific cues. Label?', 'Cannot tell', 'Nigerian English', 'British English', 'Guess the most common',
                        why='Don\'t guess.'),
                      q('Where should Yoruba dialect labels in a speech dataset come from?', 'Speaker self-report or native-speaker experts', 'The annotator\'s guess from the speaker\'s name',
                        'The recording\'s file size', 'Automatic tools only', why='Evidence, not assumption.')]),
    steps=['List the variety cues in the guideline.', 'Find cues in the text.', 'Check they are decisive.', 'Label, or "Cannot tell".'],
    mistakes=['Labelling by stereotype', 'Over-confident guesses', 'Treating one shared word as decisive'],
    quality='Every label is backed by a decisive cue, or marked "Cannot tell".',
    field='variety', label='Variety', options=['Nigerian English', 'British English', 'American English', 'Nigerian Pidgin', 'Ghanaian Pidgin', 'Cannot tell'],
    guidelines=['Label only when a decisive cue is present; otherwise "Cannot tell".'],
    practice_rows=[('Flash me when you reach the junction.', 'Nigerian English'), ('Fancy a cuppa before we go, mate?', 'British English'),
                   ('Chale, how far? I dey come.', 'Ghanaian Pidgin'), ('The meeting starts at noon.', 'Cannot tell')],
    assessment_rows=[('I\'m coming, let me quickly drop this file.', 'Nigerian English'), ('We will fill up at the gas station on the freeway.', 'American English'),
                     ('Abeg, una don chop?', 'Nigerian Pidgin'), ('I am knackered, mate, let us grab a cuppa.', 'British English'), ('The colour of the flat is lovely.', 'Cannot tell'),
                     ('Please close the door.', 'Cannot tell')],
    project_brief=project('Variety cue sheet', 'Pick a language you speak with at least two varieties. With 2 speakers of different varieties (consent), document 10 cue words or phrases.',
                          ['Cue sheet: cue, variety A form, variety B form, meaning', 'How you confirmed each cue', 'Limits of your evidence'],
                          ['Evidence-based cues', 'Honest limits', 'Respectful framing'], ['Dialect identification'], difficulty='intermediate', hours=3),
)

LINGUISTIC = _label_skill(
    'linguistic-annotation', 'Linguistic Annotation', level='intermediate', tags=['linguistics', 'nlp'], icon='ri-node-tree',
    tagline='Tag parts of speech with Universal Dependencies labels.',
    description='Annotate parts of speech using the Universal Dependencies (UD) tag set — the standard behind treebanks for Yoruba, Naija and other African languages.',
    core=lesson('Universal POS tags', 'Assign UD part-of-speech tags in context.',
                ['Universal Dependencies (UD) is a cross-language annotation standard, with treebanks for Yoruba, Nigerian Pidgin '
                 '(Naija), Hausa and others. Its 17 universal POS tags include NOUN, PROPN, VERB, AUX, ADJ, ADV, PRON, ADP '
                 '(prepositions), DET, NUM and PUNCT.',
                 'Tags depend on the word\'s function in the sentence, not its dictionary entry: "run" is a VERB in "they run" and a '
                 'NOUN in "a long run".'],
                points=['Tag by function in context.', 'PROPN for names; NOUN for common nouns.', 'ADP for prepositions (to, in, for).',
                        'AUX for auxiliaries (will, can, has).'],
                quiz=[q('"run" in "She went for a run" is…', 'NOUN', 'VERB', 'ADJ', 'ADP', why='Function in context.'),
                      q('"Lagos" in "I live in Lagos" is…', 'PROPN', 'NOUN', 'ADP', 'DET', why='Proper noun.'),
                      q('"in" in "I live in Lagos" is…', 'ADP', 'ADV', 'VERB', 'PRON', why='Preposition = ADP.')]),
    steps=['Read the whole sentence.', 'Identify the head words first (verbs, nouns).', 'Tag function words.', 'Check context-dependent words.'],
    mistakes=['Dictionary tagging', 'NOUN vs PROPN confusion', 'Tagging auxiliaries as VERB'],
    quality='Tags match UD guidelines for the word\'s function.',
    field='pos', label='UD POS of the quoted word', options=['NOUN', 'PROPN', 'VERB', 'AUX', 'ADJ', 'ADV', 'PRON', 'ADP'],
    guidelines=['Use UD v2 universal tags.', 'Tag the quoted word in its sentence.'],
    practice_rows=[('"She went for a run." — run', 'NOUN'), ('"They run every morning." — run', 'VERB'),
                   ('"Adé lives in Ibadan." — Ibadan', 'PROPN'), ('"The market is very busy." — busy', 'ADJ')],
    assessment_rows=[('"We will travel tomorrow." — will', 'AUX'), ('"We will travel tomorrow." — tomorrow', 'ADV'),
                     ('"She gave him the book." — him', 'PRON'), ('"He walked to school." — to', 'ADP'),
                     ('"The children are playing." — children', 'NOUN'), ('"The children are playing." — playing', 'VERB')],
    project_brief=project('POS-tag 20 sentences', 'POS-tag 20 sentences in a language you know using UD tags (check the UD treebank for that language if one exists).',
                          ['Tagged sentences (word/TAG)', 'Language-specific decisions you made', 'Comparison with an existing UD treebank where possible'],
                          ['Correct UD tags', 'Consistent decisions', 'Clear notes'], ['Linguistic annotation', 'Universal Dependencies'],
                          difficulty='intermediate', hours=3),
)

SEMANTIC = _label_skill(
    'semantic-annotation', 'Semantic Annotation', level='intermediate', tags=['linguistics', 'nlp', 'ai'], icon='ri-links-line',
    tagline='Label meaning relations between sentences (entailment, contradiction, neutral).',
    description='Natural language inference (NLI) annotation — the meaning-level labeling used to test whether AI models understand African languages (e.g. AfriXNLI).',
    core=lesson('Entailment, contradiction, neutral', 'Label the meaning relation between a premise and a hypothesis.',
                ['NLI annotation gives a premise and a hypothesis. <strong>Entailment</strong>: if the premise is true, the hypothesis '
                 'must be true. <strong>Contradiction</strong>: they cannot both be true. <strong>Neutral</strong>: the hypothesis might be '
                 'true, but the premise doesn\'t tell us.',
                 'Use only the information in the premise plus common sense; don\'t add outside assumptions.'],
                points=['Entailment = must be true.', 'Contradiction = cannot both be true.', 'Neutral = possible but not stated.',
                        'No outside assumptions.'],
                quiz=[q('P: "Adé bought fish at the market." H: "Adé went to the market." Relation?', 'Entailment', 'Contradiction', 'Neutral', 'Unsure',
                        why='He must have gone there.'),
                      q('P: "The shop is closed today." H: "The shop is open today." Relation?', 'Contradiction', 'Entailment', 'Neutral', 'Unsure',
                        why='Cannot both be true.'),
                      q('P: "Chika is a nurse." H: "Chika works in Lagos." Relation?', 'Neutral', 'Entailment', 'Contradiction', 'Unsure',
                        why='Not stated.')]),
    steps=['Read the premise carefully.', 'Ask: must H be true? cannot be true? or unknown?', 'Avoid outside knowledge.', 'Label.'],
    mistakes=['Labelling likely-but-unstated as entailment', 'Using outside knowledge', 'Confusing negation'],
    quality='Labels follow strictly from the premise.',
    field='relation', label='Relation', options=['Entailment', 'Contradiction', 'Neutral'],
    guidelines=['Entailment / Contradiction / Neutral as defined in the lesson.', 'Use only the premise plus common sense.'],
    practice_rows=[('P: The children are playing football outside. H: The children are outside.', 'Entailment'),
                   ('P: The bus left at 7am. H: The bus has not left yet.', 'Contradiction'),
                   ('P: Musa is a teacher. H: Musa teaches mathematics.', 'Neutral'),
                   ('P: Ngozi sold all her tomatoes. H: Ngozi has no tomatoes left to sell.', 'Entailment')],
    assessment_rows=[('P: The pikin don sleep. H: The child is asleep.', 'Entailment'),
                     ('P: It rained all day in Enugu. H: Enugu was dry all day.', 'Contradiction'),
                     ('P: Bisi bought a new phone. H: Bisi\'s new phone is expensive.', 'Neutral'),
                     ('P: The market closes at 6pm. H: The market is open at 8pm.', 'Contradiction'),
                     ('P: Emeka passed all his exams. H: Emeka passed his mathematics exam.', 'Neutral'),
                     ('P: The lecture was cancelled. H: The lecture did not hold.', 'Entailment')],
    project_brief=project('Write and label 30 NLI pairs', 'Write 30 premise–hypothesis pairs in a language you know (10 per label), then have a friend label them blind.',
                          ['The 30 pairs with your labels', 'Your friend\'s labels and agreement %', 'Discussion of disagreements'],
                          ['Well-formed pairs', 'Correct labels', 'Insightful disagreement analysis'], ['Semantic annotation', 'NLI'],
                          difficulty='intermediate', hours=3),
    report={'label': 'Explain why item 5 is neutral rather than entailment', 'min_words': 15},
)

NLP_LABELING = _label_skill(
    'nlp-data-labeling', 'NLP Data Labeling', level='beginner', tags=['nlp', 'ai'], icon='ri-price-tag-3-line',
    tagline='Label NLP datasets accurately, fast and consistently on real tasks.',
    description='General NLP labeling practice on a realistic task — spam detection in Nigerian SMS — with throughput, consistency and unsure-handling habits.',
    core=lesson('Labeling at scale', 'Keep accuracy high while labeling many items.',
                ['Real labeling projects are long: thousands of short items. Quality drops when annotators rush, drift from the '
                 'guideline over time, or over-use "unsure". Good annotators re-read the guideline regularly, take breaks, and keep '
                 'a personal list of edge cases with the decisions they made.',
                 'Example task: label SMS as spam or not. Scam patterns in Nigeria include fake prizes, BVN/OTP requests, and '
                 'fake bank alerts.'],
                points=['Re-read the guideline every session.', 'Keep an edge-case log.', 'Use "unsure" only for truly ambiguous items.',
                        'Any request for BVN, OTP or PIN is a scam signal.'],
                quiz=[q('An SMS asks you to send your BVN to claim a prize. Label?', 'Spam', 'Not spam', 'Unsure', 'Skip', why='Classic scam.'),
                      q('Your accuracy drops after two hours. Best response?', 'Take a break and re-read the guideline', 'Label faster', 'Use unsure more', 'Keep going',
                        why='Fatigue causes drift.'),
                      q('Why keep an edge-case log?', 'To decide similar cases the same way every time', 'To show off', 'To slow down', 'It\'s required by law',
                        why='Consistency.')]),
    steps=['Review the guideline.', 'Label in focused batches.', 'Log edge cases.', 'Spot-check your earlier labels.', 'Take breaks.'],
    mistakes=['Rushing', 'Guideline drift', 'Overusing unsure'], quality='Accuracy stays high from the first item to the last.',
    field='label', label='Label', options=['Spam', 'Not spam'],
    guidelines=['Spam = unsolicited promotion or scam (fake prizes, BVN/OTP/PIN requests, fake alerts).',
                'Real transaction alerts and messages from contacts are not spam.'],
    practice_rows=[('CONGRATS! You won ₦5,000,000. Send your BVN to 0803xxxxxxx to claim.', 'Spam'),
                   ('Mummy, I don reach school. I go call you later.', 'Not spam'),
                   ('Your OTP is 482913. Do not share it with anyone.', 'Not spam'),
                   ('Dear customer, your account is blocked. Reply with your PIN to unblock.', 'Spam')],
    assessment_rows=[('Get 10GB for ₦100 only!!! Click bit.ly/xxxx now', 'Spam'),
                     ('Meeting moved to 3pm, please inform the others.', 'Not spam'),
                     ('Your bank: Credit alert ₦50,000. Call this number to confirm your PIN.', 'Spam'),
                     ('Abeg buy bread for house when you dey come.', 'Not spam'),
                     ('You have been selected for a federal grant. Pay ₦2,000 processing fee.', 'Spam'),
                     ('Your parcel is ready for pickup at the post office.', 'Not spam')],
    project_brief=project('Label and document a 50-item set', 'Create 50 realistic (fictional) SMS messages, half scam, in English/Pidgin/another language, and label them.',
                          ['The 50 labeled messages', 'Guideline with scam signals', 'Edge-case log'],
                          ['Realistic, varied items', 'Accurate labels', 'Useful edge-case log'], ['NLP data labeling'], hours=2),
)

SKILLS = [TEXT, SPEECH, INTENT, SENTIMENT, NER, TOPIC, LANG_ID, DIALECT_ID, LINGUISTIC, SEMANTIC, NLP_LABELING]
