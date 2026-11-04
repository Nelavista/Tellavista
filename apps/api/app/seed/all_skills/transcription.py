"""Transcription category. Language-specific skills (Yoruba, Igbo, Hausa, Pidgin,
Nigerian English) each get their own orthography lesson and their own scored segments —
the core difficulty is different in each language (tone marks and under-dots in Yoruba,
dotted vowels in Igbo, hooked letters in Hausa, agreed spellings in Pidgin, accent-driven
ASR errors in Nigerian English), so they are not one generic skill with a label swapped.

No audio ships with the seed: segments run as machine-transcript correction (the draft is
realistic raw ASR output). An admin can attach `audio_url` to any task later.

NOTE FOR CONTENT REVIEW: every African-language sentence below should be checked by a
native-speaker linguist before wide release.
"""
from ._common import q, lesson, workflow_lesson, task, labeling, number_item, choice_items, project, skill

CAT = 'transcription'
COLOR = '#2563eb'

FOUNDATION = lesson(
    'How transcription work runs in AI data projects',
    'Understand what transcription data is used for and what a project expects from you.',
    [
        'Speech-recognition (ASR) systems learn from hours of audio paired with accurate text. When an '
        'African language has little transcribed audio, ASR quality for its speakers stays poor — so careful '
        'human transcription is one of the most valuable contributions to African-language AI.',
        'Every project ships a <strong>guideline document</strong>. It decides things you might otherwise '
        'guess: verbatim or clean style, which tags exist ([inaudible], [laughter], [noise], [crosstalk]), '
        'how to label speakers, how to write numbers, and how to spell borrowed words. Following the guideline '
        'exactly matters more than your personal style, because thousands of files from many transcribers must '
        'look as if one person wrote them.',
        'Your work is checked by a QA reviewer who measures errors (often as word error rate, WER) and '
        'guideline violations. Consistent, guideline-perfect work is what gets transcribers trusted with more tasks.',
    ],
    points=[
        'Verbatim = everything as spoken (fillers, repetitions); clean = readable, fillers removed, meaning unchanged.',
        'Never guess a word you cannot hear — tag it [inaudible].',
        'Write the language in its standard orthography, including tone marks or special letters the guideline requires.',
        'Speaker labels and timestamps are data too: wrong ones are counted as errors.',
    ],
    quiz=[
        q('A word is completely unclear in the audio. What should you write?', '[inaudible], as the guideline says',
          'Your best guess of the word', 'Nothing — skip it silently', 'The word that would make most sense',
          why='Guessing creates false training data; tags tell the model and the reviewer the audio was unclear.'),
        q('Who decides whether a project uses verbatim or clean transcription?', 'The project guideline',
          'The transcriber, per file', 'The speaker in the audio', 'Whichever is faster',
          why='Consistency across all transcribers comes from the guideline, not personal choice.'),
        q('What does word error rate (WER) measure?', 'How many word substitutions, insertions and deletions a transcript has compared with the reference',
          'How fast the transcriber typed', 'How loud the audio was', 'The number of speakers',
          why='WER = (substitutions + deletions + insertions) / words in the reference.'),
    ],
)

STD_GUIDELINES = [
    'Clean style: remove fillers (um, uh, ehn) unless the task says verbatim.',
    'Use standard spelling for the language, including required diacritics or special letters.',
    'Keep the words the speaker used — do not translate or "improve" them.',
    'Unclear words: [inaudible]. Non-speech sounds: [laughter], [noise], [cough].',
    'Punctuation and capitals are not scored here, but use them sensibly.',
]


def _lang_skill(key, name, slug, tagline, orthography_paras, orthography_points, example,
                core_quiz, practice_segments, assessment_segments, extra_guidelines, mistakes, level='beginner'):
    def segs(rows):
        return [{'id': f's{i}', 'reference': ref, 'draft': draft} for i, (ref, draft) in enumerate(rows, 1)]

    guidelines = STD_GUIDELINES + extra_guidelines
    return skill(
        slug, f'{name} Transcription', level=level, language=key,
        tags=['transcription', 'african-languages', 'speech-data'],
        icon='ri-file-text-line', color=COLOR, tagline=tagline,
        description=(f'Learn to produce guideline-perfect {name} transcripts for speech-recognition datasets: '
                     f'correct {name} orthography, tags, speaker labels and timestamps, and how your work is QA-scored.'),
        foundation=FOUNDATION,
        core=lesson(f'Writing {name} correctly', f'Apply standard {name} orthography in transcripts.',
                    orthography_paras, points=orthography_points, example=example, quiz=core_quiz),
        workflow=workflow_lesson(f'{name} transcription', [
            'Read the guideline and the tag list before opening any audio.',
            'Listen to the whole segment once without typing.',
            'Type what you hear, then replay at slower speed to fix gaps.',
            f'Do a dedicated pass only for {name} spelling and diacritics/special letters.',
            'Add tags, speaker labels and timestamps exactly as specified.',
            'Self-check against the guideline before submitting.',
        ], mistakes, f'A reviewer should find no guessed words, every {name} word in standard spelling, and tags '
                     'used only from the allowed list. Most projects expect word accuracy above 95%.'),
        practice=task(f'Correct a {name} machine transcript',
                      f'Fix raw speech-recognition output so it matches the {name} guideline.',
                      {'kind': 'transcription', 'mode': 'clean', 'guidelines': guidelines,
                       'brief': f'These segments are raw ASR output for {name} audio. Correct each one.',
                       'segments': segs(practice_segments)}, minutes=20),
        assessment=task(f'{name} transcription assessment',
                        f'Correct four {name} segments to the guideline. Scored on word accuracy, diacritics included.',
                        {'kind': 'transcription', 'mode': 'clean', 'guidelines': guidelines,
                         'brief': f'Correct each machine transcript so it is exactly right in standard {name}.',
                         'segments': segs(assessment_segments)}, minutes=25),
        project_brief=project(
            f'{name} conversation transcript',
            f'With their consent, record a 1-2 minute everyday conversation in {name} with a friend or family member '
            '(market, greetings, directions — no private information). Upload the audio to Google Drive with link '
            'sharing on and add it as a project link. Transcribe it in the project document following the guideline.',
            ['Audio link (Drive or similar) added under project links',
             'Transcript with a speaker label and start timestamp (m:ss) on every segment',
             f'Standard {name} orthography throughout, tags from the allowed list only',
             'A short note listing any words you were unsure of and how you resolved them'],
            ['Orthography and diacritics correct and consistent', 'Every segment has speaker label + timestamp',
             'Tags used correctly; nothing guessed', 'Clear self-review note'],
            [f'{name} transcription', 'Speaker labeling', 'Timestamping'], hours=3),
        hours=6,
    )


YORUBA = _lang_skill(
    'yoruba', 'Yoruba', 'yoruba-transcription',
    'Transcribe Yoruba speech with correct tone marks and under-dots.',
    ['Yoruba is a tonal language: the same letters with different tones are different words. Standard '
     'orthography marks high tone with an acute accent (á), low tone with a grave accent (à), and leaves mid '
     'tone unmarked. It also uses under-dotted letters ẹ, ọ and ṣ, which are distinct letters, not decorations.',
     'Speech-recognition systems and many keyboards drop these marks, which is why so much Yoruba text online '
     'is ambiguous. Transcription projects that build Yoruba datasets usually require full tone marking, so a '
     'transcript without them is counted as wrong.'],
    ['ọkọ (husband), ọkọ̀ (vehicle) and ọkọ́ (hoe) differ only in tone.',
     'ẹ, ọ, ṣ are separate letters: "ese" and "ẹsẹ̀" are not the same word.',
     'Long vowels are written doubled with each tone marked, e.g. káàárọ̀.',
     'Use a keyboard that supports Yoruba diacritics (e.g. Gboard with Yorùbá) rather than leaving them out.'],
    'Raw ASR:  E kaaaro, se daadaa ni?\nCorrect:  Ẹ káàárọ̀, ṣé dáadáa ni?',
    [q('Which mark shows a LOW tone in standard Yoruba orthography?', 'A grave accent (à)', 'An acute accent (á)',
       'No mark at all', 'An under-dot (ẹ)', why='Low = grave, high = acute, mid = unmarked.'),
     q('Why can\'t you leave out the dot in ọ?', 'ọ is a different letter (and sound) from o',
       'It is optional decoration', 'Only names use it', 'It marks a high tone', why='Dropping it changes the word.'),
     q('Which word means "vehicle"?', 'ọkọ̀', 'ọkọ', 'ọkọ́', 'oko', why='ọkọ̀ (mid-low) is vehicle.')],
    [('Ẹ káàárọ̀, ṣé dáadáa ni?', 'E kaaaro, se daadaa ni?'),
     ('Mo wà dáadáa, ẹ ṣé.', 'Mo wa daadaa, e se.'),
     ('Mo ń lọ sí ọjà láti ra ẹja.', 'Mo n lo si oja lati ra eja.')],
    [('Kí ni orúkọ rẹ?', 'Ki ni oruko re?'),
     ('Orúkọ mi ni Adé.', 'Oruko mi ni Ade.'),
     ('Ọkọ̀ náà ti dé.', 'Oko naa ti de.'),
     ('Ẹ jọ̀wọ́, ẹ fún mi ní omi.', 'E jowo, e fun mi ni omi.')],
    ['Mark every tone the standard orthography requires (high = á, low = à, mid unmarked).',
     'Always write ẹ, ọ, ṣ with their under-dots.'],
    ['Leaving out tone marks because "everyone knows the word"', 'Writing o for ọ or s for ṣ',
     'Marking only some syllables of a long vowel', 'Using a different character that only looks similar (e.g. ẹ typed as e + full stop)'],
)

IGBO = _lang_skill(
    'igbo', 'Igbo', 'igbo-transcription',
    'Transcribe Igbo speech with the correct dotted vowels and ṅ.',
    ['Standard Igbo orthography (Ọnwụ) has eight vowels. Three of them — ị, ọ, ụ — carry a dot below and are '
     'different vowels from i, o, u. It also has the consonant ṅ. Leaving these out turns a correct word into a '
     'different word or a non-word.',
     'Everyday Igbo writing usually leaves tone unmarked, and most transcription guidelines follow that: mark the '
     'dotted vowels always, and add tone marks only if the guideline asks for them.'],
    ['ị, ọ, ụ are distinct vowels — always type the dot below.', 'ṅ is a distinct consonant (as in ṅụọ).',
     'Tone marks are usually NOT required unless the guideline says so.',
     'Keep dialect words the speaker used; do not convert them to another dialect.'],
    'Raw ASR:  Ututu oma, kedu?\nCorrect:  Ụtụtụ ọma, kedụ?',
    [q('How many vowels does standard Igbo orthography have?', 'Eight', 'Five', 'Seven', 'Twelve',
       why='a, e, i, ị, o, ọ, u, ụ.'),
     q('Most Igbo transcription guidelines require which marks by default?', 'The dots on ị, ọ, ụ (and ṅ), but not tone marks',
       'Full tone marks on every syllable', 'No marks at all', 'Only marks on names', why='Dotted letters are part of spelling.'),
     q('A speaker uses a word from their own dialect. What do you write?', 'The word they actually said',
       'The closest standard Igbo word', 'An English translation', '[inaudible]', why='Transcribe, don\'t edit.')],
    [('Ụtụtụ ọma, kedụ?', 'Ututu oma, kedu?'),
     ('Adị m mma, daalụ.', 'Adi m mma, daalu.'),
     ('Ana m aga ahịa ugbu a.', 'Ana m aga ahia ugbu a.')],
    [('Aha m bụ Ada.', 'Aha m bu Ada.'),
     ('Nnọọ, bịa nọdụ ala.', 'Nnoo, bia nodu ala.'),
     ('Biko, nye m mmiri.', 'Biko, nye m mmiri.'),
     ('Ọ dị mma.', 'O di mma.')],
    ['Always write the dotted vowels ị, ọ, ụ and the consonant ṅ.',
     'Do not add tone marks — this project leaves tone unmarked.'],
    ['Typing i/o/u where the word needs ị/ọ/ụ', '"Correcting" a dialect word into another dialect',
     'Adding tone marks the guideline did not ask for', 'Changing words that were already correct'],
)

HAUSA = _lang_skill(
    'hausa', 'Hausa', 'hausa-transcription',
    'Transcribe Hausa speech with the correct hooked letters.',
    ['Standard Hausa in the Latin (Boko) script uses hooked letters for sounds English does not have: ɓ, ɗ, ƙ '
     'and ƴ (often typed \'y). They are separate letters: "daki" is not a word, "ɗaki" (room) is.',
     'Speech-recognition systems trained mostly on English often drop the hooks, and they mishear Hausa words as '
     'similar-sounding ones. Tone and vowel length are not written in everyday Hausa, and most guidelines leave them out.'],
    ['ɓ, ɗ, ƙ, ƴ are distinct letters — never replace them with b, d, k, y.',
     'Tone and vowel length are normally not marked.', 'Arabic-origin religious phrases keep their usual Boko spelling (e.g. "Don Allah").',
     'Ajami (Arabic-script Hausa) is a different task — only use it if the guideline asks.'],
    'Raw ASR:  Na shiga daki.\nCorrect:  Na shiga ɗaki.',
    [q('Which word is spelled correctly for "room"?', 'ɗaki', 'daki', 'dhaki', 'd\'aki', why='The hooked ɗ is required.'),
     q('Are tone marks normally written in Hausa transcription?', 'No, not unless the guideline asks',
       'Yes, on every vowel', 'Only on verbs', 'Only at the end of sentences', why='Everyday Boko Hausa leaves tone unmarked.'),
     q('What is ƙ?', 'A distinct Hausa consonant (an ejective k)', 'A k with a typo', 'A tone mark', 'A vowel',
       why='It is a separate letter and sound.')],
    [('Ina kwana? Lafiya lau.', 'Ina kwana? Lafia lau.'),
     ('Na shiga ɗaki.', 'Na shiga daki.'),
     ('Ina zuwa kasuwa yanzu.', 'Ina zuwa kaswa yanzu.')],
    [('Ƙasar Najeriya babba ce.', 'Kasar Najeriya babba ce.'),
     ('Na gode, sai an jima.', 'Na gode, sai anjima.'),
     ('Don Allah, ba ni ruwa.', 'Don Allah, bani ruwa.'),
     ('Ɓera ya shiga ɗaki.', 'Bera ya shiga daki.')],
    ['Always write the hooked letters ɓ, ɗ, ƙ, ƴ.', 'Write "sai an jima" and "ba ni" as separate words.'],
    ['Replacing ɓ/ɗ/ƙ with b/d/k', 'Joining words that the guideline writes separately',
     'Accepting the ASR\'s English-sounding substitutes', 'Adding tone marks that were not requested'],
)

PIDGIN = _lang_skill(
    'pidgin', 'Nigerian Pidgin', 'nigerian-pidgin-transcription',
    'Transcribe Naija (Nigerian Pidgin) consistently, without "correcting" it into English.',
    ['Nigerian Pidgin (Naija) is spoken by tens of millions of people, but it has no single official spelling, '
     'so every project fixes a spelling list. The most common mistake is writing what the speaker said as '
     'standard English — "How you dey" becomes "How are you" — which destroys exactly the data the project needs.',
     'English-trained ASR systems constantly mishear Pidgin as English words ("dey" → "day", "abeg" → "a beg"). '
     'Your job is to restore what was really said, spelled the project\'s way.'],
    ['Project spellings: dey, wetin, abeg, una, pikin, sabi, wahala, comot, chop, don.',
     'Never translate Pidgin into English, and never fix its grammar.',
     'Write English words that the speaker used in English as normal English.',
     'Be consistent: the same word is spelled the same way in every file.'],
    'Raw ASR:  how you day i day fine\nCorrect:  How you dey? I dey fine.',
    [q('A speaker says "How you dey?". What do you write?', 'How you dey?', 'How are you?', 'How you day?', 'How do you do?',
       why='Transcribe what was said with the project spelling.'),
     q('Why do Pidgin projects publish a spelling list?', 'Pidgin has no single official spelling, so consistency must be agreed',
       'To make it look like English', 'To shorten the transcripts', 'Because Pidgin has no grammar',
       why='Consistency is what makes the data usable.'),
     q('ASR output says "a beg make we go". What did the speaker most likely say?', 'Abeg make we go', 'I beg, make we go',
       'A bag make we go', 'Above make we go', why='"abeg" is one word in the spelling list.')],
    [('How you dey? I dey fine.', 'how you day i day fine'),
     ('Abeg make we go market.', 'a beg make we go market'),
     ('Wetin dey happen for there?', 'what in day happen for there')],
    [('Una don chop?', 'you now don chop'),
     ('The pikin sabi book well well.', 'the pickin savvy book well well'),
     ('No wahala, I go comot now.', 'no wahala i go come out now'),
     ('E don do, make una rest.', 'e don do make you now rest')],
    ['Use the project spellings: dey, wetin, abeg, una, pikin, sabi, wahala, comot, chop, don.',
     'Do not translate into or "correct" to standard English.'],
    ['Translating Pidgin into English', 'Accepting ASR\'s English look-alike words',
     'Spelling the same word two ways in one file', 'Fixing the speaker\'s grammar'],
)

NIG_ENGLISH = _lang_skill(
    'nigerian-english', 'Nigerian English', 'nigerian-english-transcription',
    'Transcribe Nigerian-accented English accurately, names and local words included.',
    ['Nigerian English has its own vocabulary ("flash me", "I\'m coming" meaning "I\'ll be right back", "well done" '
     'as a greeting), local place names, food and transport words, and frequent code-switching. ASR systems '
     'trained on American or British speech mishear all of these.',
     'Nigerian English is not "wrong English": transcribe the words the speaker used, spell local names and '
     'words correctly, and keep code-switched words in their own language\'s spelling.'],
    ['Spell Nigerian place names correctly (Ikeja, Oshodi, Yaba, Ibadan, Enugu, Kano).',
     'Keep local words as used: okada, suya, oga, naira, danfo, abeg.',
     'Write numbers as spoken words ("one thousand naira") unless the guideline says digits.',
     'Do not "standardise" Nigerian expressions into British or American phrasing.'],
    'Raw ASR:  flesh me when you rich\nCorrect:  Flash me when you reach.',
    [q('A speaker says "I\'m coming" while leaving the room. What do you write?', "I'm coming", "I'll be back",
       "I'm going", '[inaudible]', why='Transcribe the words, not your interpretation.'),
     q('ASR wrote "a cagey" in "I will be at a cagey by two". What is most likely correct?', 'Ikeja', 'a cage',
       'a key', 'Akure', why='Local place names are a classic ASR error.'),
     q('How should "1000 naira" be written if the guideline says numbers are spoken words?', 'one thousand naira',
       '1000 naira', '₦1,000', 'N1k', why='Follow the number rule exactly.')],
    [("I will be at Ikeja by two o'clock, flash me when you reach.", "i will be at a cagey by two o'clock flesh me when you rich"),
     ("Well done, ma. I'm coming, let me drop my bag.", "well done ma i'm coming let me drop my back"),
     ('The fuel price has gone up to one thousand naira per litre.', 'the fuel price has gone up to one thousand nyra per litre')],
    [('We are going to Oshodi to buy suya.', 'we are going to oh show the to buy sweet ya'),
     ('Abeg, how much is the okada to Yaba?', 'a beg how much is the okay that to yaba'),
     ('My oga said I should come back tomorrow.', 'my alga said i should come back tomorrow'),
     ('Make sure you send the money before Friday, please.', 'make sure you send the many before friday please')],
    ['Spell Nigerian names and local words correctly (Ikeja, okada, suya, oga, naira).',
     'Numbers as spoken words.'],
    ['Accepting ASR\'s guess for a local name', 'Rewriting Nigerian expressions as British/American English',
     'Writing digits when the guideline says words', 'Dropping code-switched words'],
)

AFRICAN = skill(
    'african-language-transcription', 'African Language Transcription', level='intermediate',
    tags=['transcription', 'african-languages', 'speech-data', 'code-switching'],
    icon='ri-file-list-3-line', color=COLOR,
    tagline='Transcribe multilingual, code-switched African conversations with speaker labels.',
    description=('Real African speech mixes languages in one sentence. Learn to transcribe code-switched, '
                 'multi-speaker conversations: each language in its own orthography, speaker labels, and tags.'),
    foundation=FOUNDATION,
    core=lesson('Code-switching and multi-speaker audio', 'Transcribe mixed-language speech correctly.',
                ['Many Nigerian conversations switch between English, Pidgin and Yoruba, Igbo or Hausa within one '
                 'turn. Guidelines almost always say: transcribe each word in the language it was spoken, using that '
                 'language\'s standard spelling — never translate the switched part.',
                 'Multi-speaker audio adds speaker labels. Label by role or number as the guideline says, keep labels '
                 'consistent across the file, and start a new segment whenever the speaker changes.'],
                points=['Each language keeps its own spelling (Yoruba tone marks, Igbo dots, Hausa hooks).',
                        'Never translate the code-switched words.', 'New speaker = new segment.',
                        'Use the same label for the same person throughout the file.'],
                example='Speaker 1: Ẹ káàárọ̀ o [laughter]\nSpeaker 2: Káàárọ̀, how was your night?',
                quiz=[q('A speaker switches from English to Yoruba mid-sentence. You…', 'transcribe the Yoruba words in Yoruba orthography',
                        'translate the Yoruba part to English', 'tag it [foreign]', 'skip the Yoruba part',
                        why='Code-switching is real data; keep it.'),
                      q('When should a new segment start in a conversation?', 'Whenever the speaker changes',
                        'Every 60 seconds only', 'Only at the end of the file', 'When the topic changes',
                        why='Segments must contain one speaker.'),
                      q('Speaker 2 is labelled "Speaker 2" at the start. Later you should…', 'keep labelling them "Speaker 2"',
                        'switch to their name once you learn it', 'label them "Speaker 3"', 'leave later turns unlabelled',
                        why='Consistency across the file.')]),
    workflow=workflow_lesson('multilingual transcription', [
        'Skim the guideline for the language list, tags and speaker-label rules.',
        'Listen once to identify speakers and which languages appear.',
        'Transcribe turn by turn, one segment per speaker turn.',
        'Do one spelling pass per language (diacritics/special letters).',
        'Check labels are consistent and tags are from the allowed list.'],
        ['Translating code-switched words', 'Merging two speakers into one segment',
         'Losing diacritics on the African-language words', 'Inventing speaker names'],
        'Every turn has the right speaker, every word is in the language and spelling it was spoken in.'),
    practice=task('Label and correct a code-switched conversation',
                  'Assign speakers and correct the machine transcript for each turn.',
                  {'kind': 'transcription', 'mode': 'verbatim', 'speakers': ['Speaker 1', 'Speaker 2'],
                   'guidelines': STD_GUIDELINES[1:] + ['Verbatim: keep "o" and other particles as spoken.',
                                                       'Speaker 1 opens the conversation.'],
                   'segments': [
                       {'id': 's1', 'speaker': 'Speaker 1', 'context': 'Turn 1 — the caller greets, then laughs.',
                        'reference': 'Ẹ káàárọ̀ o [laughter]', 'draft': 'E kaaaro o'},
                       {'id': 's2', 'speaker': 'Speaker 2', 'context': 'Turn 2 — the other person replies.',
                        'reference': 'Káàárọ̀, how was your night?', 'draft': 'kaaaro how was your night'},
                       {'id': 's3', 'speaker': 'Speaker 1', 'context': 'Turn 3 — the caller answers in Pidgin.',
                        'reference': 'I dey fine, abeg wetin dey happen?', 'draft': 'i day fine a beg what in day happen'}]},
                  minutes=20),
    assessment=task('Multilingual transcription assessment',
                    'Assign speakers and produce correct verbatim transcripts for a three-language conversation.',
                    {'kind': 'transcription', 'mode': 'verbatim', 'speakers': ['Speaker 1', 'Speaker 2'],
                     'guidelines': STD_GUIDELINES[1:] + ['Speaker 1 is the shop owner; Speaker 2 is the customer.'],
                     'segments': [
                         {'id': 's1', 'speaker': 'Speaker 2', 'context': 'The customer walks in and greets.',
                          'reference': 'Sannu, how far?', 'draft': 'sanu how far'},
                         {'id': 's2', 'speaker': 'Speaker 1', 'context': 'The shop owner replies; a car horn covers one word.',
                          'reference': 'I dey o [noise] wetin you wan buy?', 'draft': 'i day o what you want buy'},
                         {'id': 's3', 'speaker': 'Speaker 2', 'context': 'The customer answers in Yoruba and English.',
                          'reference': 'Mo fẹ́ ra bread àti ẹyin.', 'draft': 'mo fe ra bread ati eyin'},
                         {'id': 's4', 'speaker': 'Speaker 1', 'context': 'The shop owner thanks them.',
                          'reference': 'Ẹ ṣé, no wahala.', 'draft': 'e se no wahala'}]},
                    minutes=25),
    project_brief=project('Multilingual conversation transcript',
                          'With consent, record a 2-minute conversation where speakers naturally mix at least two languages. '
                          'Add the audio link and transcribe it in the project document.',
                          ['Audio link added under project links', 'Speaker-labelled, timestamped transcript',
                           'Each language in its own standard spelling', 'A note listing which languages appear and where'],
                          ['Correct spelling for every language used', 'Consistent speaker labels', 'Nothing translated or guessed'],
                          ['Multilingual transcription', 'Code-switching', 'Speaker labeling'], difficulty='intermediate', hours=4),
    hours=7,
)

_TIMING_1 = ('Word timings (seconds): 0.00 good | 0.31 morning | 0.72 everyone | [pause 1.6s] | 2.80 today | '
             '3.15 we | 3.30 will | 3.48 talk | 3.80 about | 4.10 farming | [pause 0.4s] | 5.05 and | 5.30 rain')
_TIMING_2 = ('Word timings (seconds): 0.00 thank | 0.25 you | 0.40 for | 0.55 coming | [pause 2.1s] | 3.40 please | '
             '3.70 sit | 3.95 down | [pause 0.9s] | 5.30 let | 5.48 us | 5.62 begin')
# Assessment-only recordings: never shown in a practice task, whose answers are revealed.
_TIMING_3 = ('Word timings (seconds): 0.00 welcome | 0.40 to | 0.55 the | 0.70 class | [pause 1.3s] | 2.60 open | '
             '2.95 your | 3.20 books | [pause 0.6s] | 4.30 and | 4.50 read | [pause 1.1s] | 6.10 quietly')
_TIMING_4 = ('Word timings (seconds): 0.00 the | 0.18 bus | 0.45 is | 0.60 late | [pause 0.7s] | 1.90 again | '
             '[pause 1.8s] | 4.40 we | 4.55 will | 4.70 walk')

SEGMENTATION = skill(
    'audio-segmentation', 'Audio Segmentation', level='beginner',
    tags=['transcription', 'speech-data', 'annotation'], icon='ri-scissors-cut-line', color=COLOR,
    tagline='Split long recordings into clean, correctly sized segments.',
    description='Learn the rules projects use to cut audio into segments — at pauses and speaker changes, within length limits — and apply them precisely.',
    foundation=FOUNDATION,
    core=lesson('Segmentation rules', 'Decide exactly where a segment should start and end.',
                ['Before audio can be transcribed or used to train a model, long recordings are cut into short segments. '
                 'Projects define the rules: typically, cut at pauses longer than a threshold (for example 0.8 s), never '
                 'cut inside a word, start a new segment when the speaker changes, and keep segments under a maximum length.',
                 'A segment\'s start is the start time of its first word; its end is the end of its last word, sometimes '
                 'with a small padding the guideline specifies.'],
                points=['Cut only at pauses at or above the threshold.', 'Never cut inside a word.',
                        'Speaker change = new segment, even without a pause.', 'Respect the maximum segment length.'],
                quiz=[q('The guideline says "cut at pauses of 0.8 s or more". A 0.4 s pause appears. You…', 'do not cut there',
                        'cut there', 'cut and tag [pause]', 'delete the pause', why='Below threshold = same segment.'),
                      q('Where does a segment start?', 'At the start time of its first word', 'At 0.00 always',
                        'In the middle of the pause before it', 'At the end of the previous segment', why='Unless padding is specified.'),
                      q('Two speakers talk with no pause between turns. You…', 'start a new segment at the speaker change',
                        'keep them in one segment', 'tag [crosstalk] and skip', 'cut only at the next pause', why='One speaker per segment.')]),
    workflow=workflow_lesson('audio segmentation', ['Read the pause threshold and maximum length.',
                             'Scan the waveform or timing log for pauses.', 'Mark cuts at qualifying pauses and speaker changes.',
                             'Check no segment exceeds the maximum length.', 'Record start/end times precisely.'],
                             ['Cutting at short breaths', 'Cutting mid-word', 'Ignoring a speaker change', 'Rounding times carelessly'],
                             'Every cut can be justified by a rule in the guideline.'),
    practice=task('Segment a short recording', 'Use the word-timing log to apply the segmentation rule.',
                  labeling([number_item('n1', 'Recording A', 'How many segments?', 2, context=_TIMING_1),
                            number_item('t1', 'Recording A', 'Start time of segment 2 (seconds)', 2.80, 0.05, _TIMING_1),
                            number_item('n2', 'Recording B', 'How many segments?', 3, context=_TIMING_2),
                            number_item('t2', 'Recording B', 'Start time of segment 3 (seconds)', 5.30, 0.05, _TIMING_2)],
                           ['Cut at every pause of 0.8 s or longer.', 'Do not cut at shorter pauses.',
                            'A segment starts at its first word\'s time.'],
                           brief='Hint: the 0.4 s pause in Recording A is shorter than the threshold.'), minutes=15),
    assessment=task('Segmentation assessment', 'Apply a stricter rule to two new recordings.',
                    labeling([number_item('n1', 'Recording C', 'How many segments?', 3, context=_TIMING_3),
                              number_item('t2', 'Recording C', 'Start time of segment 2 (seconds)', 2.60, 0.05, _TIMING_3),
                              number_item('t3', 'Recording C', 'Start time of segment 3 (seconds)', 6.10, 0.05, _TIMING_3),
                              number_item('n2', 'Recording D', 'How many segments?', 2, context=_TIMING_4),
                              number_item('n3', 'Recording D', 'How many segments would Recording D have under a 0.5 s rule?', 3, context=_TIMING_4)],
                             ['Cut at every pause of 1.0 s or longer (note: stricter than practice).', 'Do not cut at shorter pauses.',
                              'A segment starts at its first word\'s time.']), minutes=15),
    project_brief=project('Segment your own recording', 'Record a 1-minute monologue (with natural pauses), then segment it.',
                          ['Audio link', 'A table: segment number, start, end, first and last word',
                           'The rule you applied (threshold, max length)'],
                          ['Cuts follow the stated rule', 'Times are precise and consistent', 'No segment over the maximum length'],
                          ['Audio segmentation'], hours=2),
    hours=4,
)

SPEAKER_ID = skill(
    'speaker-identification', 'Speaker Identification', level='beginner',
    tags=['transcription', 'speech-data', 'annotation'], icon='ri-user-voice-line', color=COLOR,
    tagline='Label who is speaking, consistently, across a whole recording.',
    description='Learn diarization labeling: telling speakers apart from voice and context, keeping labels consistent, and handling overlap.',
    foundation=FOUNDATION,
    core=lesson('Telling speakers apart', 'Assign speaker labels accurately and consistently.',
                ['Speaker identification (diarization labeling) means marking who speaks each segment. Projects use '
                 'neutral labels (Speaker 1, Speaker 2) or roles (Interviewer, Respondent) — never guessed real names.',
                 'Use every cue: voice quality, who asks versus answers, how people address each other, and what they '
                 'say about themselves. When two people talk at once, guidelines usually ask for [crosstalk] on the overlap.'],
                points=['Use the label scheme in the guideline — roles or numbers.', 'Never invent names.',
                        'Context cues (questions, self-references) help as much as voice.', 'Mark overlap as [crosstalk].'],
                quiz=[q('A respondent says "My name is Bisi". The guideline uses roles. You label them…', 'Respondent',
                        'Bisi', 'Speaker Bisi', 'Unknown', why='Follow the label scheme; names may also be private data.'),
                      q('Two people speak at the same time. Usually you…', 'mark the overlap [crosstalk]',
                        'pick the louder one', 'delete the segment', 'merge both into one label', why='Standard overlap tag.'),
                      q('Who most likely says "So, how many hectares do you farm?" in a farm survey?', 'The interviewer',
                        'The farmer', 'A passer-by', 'Impossible to say', why='Questions in a survey come from the interviewer.')]),
    workflow=workflow_lesson('speaker identification', ['Listen to the opening to identify how many speakers there are.',
                             'Note a distinctive cue for each speaker.', 'Label each segment.',
                             'Re-check labels at every turn change.', 'Mark overlaps.'],
                             ['Swapping labels midway through', 'Using real names', 'Labelling overlap as one speaker'],
                             'Labels are consistent for the whole file and match the scheme.'),
    practice=task('Label an interview', 'Decide who says each line of a farm-survey interview.',
                  labeling(choice_items('speaker', 'Speaker', ['Interviewer', 'Farmer'], [
                      ('"Good afternoon, thank you for agreeing to talk to us."', 'Interviewer'),
                      ('"You are welcome. I farm cassava and maize here."', 'Farmer'),
                      ('"How has the rain been this season?"', 'Interviewer'),
                      ('"It came late, so I planted in June."', 'Farmer')]),
                           ['Labels: Interviewer, Farmer.', 'Use what is said, not just tone of voice.']), minutes=10),
    assessment=task('Speaker identification assessment', 'Label a three-person clinic conversation.',
                    labeling(choice_items('speaker', 'Speaker', ['Nurse', 'Patient', 'Relative'], [
                        ('"Please sit down, madam. What brings you to the clinic today?"', 'Nurse'),
                        ('"My head has been paining me since Monday."', 'Patient'),
                        ('"She has not been eating well either, I brought her here."', 'Relative'),
                        ('"Have you taken any medicine for the headache?"', 'Nurse'),
                        ('"Only paracetamol, two times."', 'Patient')]),
                             ['Labels: Nurse, Patient, Relative.', 'The relative speaks about the patient in the third person.']),
                    minutes=12),
    project_brief=project('Diarize a group conversation', 'Record (with consent) a 2-minute conversation with three people, then label every turn.',
                          ['Audio link', 'Turn-by-turn table: start time, speaker label, first few words',
                           'Your label scheme and the cue you used for each speaker'],
                          ['Labels consistent across the file', 'Overlaps marked', 'Clear cue notes'], ['Speaker identification'], hours=2),
    hours=4,
)

TIMESTAMPING = skill(
    'timestamping', 'Timestamping', level='beginner',
    tags=['transcription', 'speech-data'], icon='ri-time-line', color=COLOR,
    tagline='Align text to audio with accurate start and end times.',
    description='Learn how projects specify timestamps (format, precision, padding) and produce them accurately from audio or word timings.',
    foundation=FOUNDATION,
    core=lesson('Timestamp formats and precision', 'Produce timestamps in the exact format a project requires.',
                ['Timestamps connect each piece of text to its place in the audio. Projects specify the format '
                 '(seconds like 12.5, or m:ss.s like 0:12.5, or hh:mm:ss.mmm), the precision (often 0.1 s), and whether '
                 'to add padding before the first word.',
                 'Start = when the first word begins; end = when the last word ends. Off-by-a-second timestamps make '
                 'segments unusable for training because audio and text no longer match.'],
                points=['Use exactly the required format.', 'Start at the first word, end at the last word.',
                        'Precision matters: 0.1 s is typical.', '1:05.0 means 65 seconds.'],
                quiz=[q('How many seconds is 1:05.5?', '65.5', '105.5', '1.055', '15.5', why='1 minute = 60 s.'),
                      q('A segment\'s end time is…', 'when its last word ends', 'when the next segment starts',
                        'always start + 10 s', 'the end of the file', why='Unless padding is specified.'),
                      q('Why do wrong timestamps matter?', 'Text no longer matches the audio, so the data can\'t train a model',
                        'They don\'t, only text matters', 'They make files bigger', 'They change the speaker label', why='Alignment is the point.')]),
    workflow=workflow_lesson('timestamping', ['Confirm the format and precision.', 'Find the first word onset.',
                             'Find the last word offset.', 'Convert units carefully.', 'Re-play each boundary to check.'],
                             ['Mixing formats in one file', 'Using the pause time instead of the word time', 'Unit-conversion errors'],
                             'Every boundary is within the required precision of the true word time.'),
    practice=task('Timestamp from a word log', 'Read word timings and give segment boundaries.',
                  labeling([number_item('a', 'Segment: "today we will talk about farming and rain"', 'Start (s)', 2.80, 0.1, _TIMING_1),
                            number_item('b', 'Segment: "please sit down"', 'Start (s)', 3.40, 0.1, _TIMING_2),
                            number_item('c', 'Segment: "let us begin"', 'Start (s)', 5.30, 0.1, _TIMING_2)],
                           ['Answer in seconds, to 0.1 s.', 'Start = first word time.']), minutes=10),
    assessment=task('Timestamping assessment', 'Convert and compute boundaries precisely.',
                    labeling([number_item('a', 'Convert 2:07.4 to seconds.', 'Seconds', 127.4, 0.05),
                              number_item('b', 'Convert 0:48.0 to seconds.', 'Seconds', 48.0, 0.05),
                              number_item('c', 'Segment: "good morning everyone"', 'Start (s)', 0.0, 0.1, _TIMING_1),
                              number_item('d', 'Segment: "thank you for coming"', 'Start (s)', 0.0, 0.1, _TIMING_2),
                              number_item('e', 'Segment: "open your books and read"', 'Start (s)', 2.60, 0.1, _TIMING_3)],
                             ['Seconds, to 0.1 s.', 'Start = first word time.']), minutes=12),
    project_brief=project('Timestamp a 1-minute clip', 'Record or pick a 1-minute clip you have rights to, segment it, and timestamp every segment.',
                          ['Audio link', 'Segment table with start/end in m:ss.s', 'Your stated format and precision'],
                          ['Boundaries accurate to 0.1–0.2 s', 'One consistent format', 'Clear table'], ['Timestamping'], hours=2),
    hours=3,
)

VERBATIM = skill(
    'verbatim-transcription', 'Verbatim Transcription', level='intermediate',
    tags=['transcription', 'speech-data'], icon='ri-quill-pen-line', color=COLOR,
    tagline='Capture speech exactly as spoken — fillers, repeats and sounds included.',
    description='Learn strict verbatim conventions used for speech-recognition and linguistic research data.',
    foundation=FOUNDATION,
    core=lesson('Strict verbatim conventions', 'Apply verbatim rules for fillers, false starts and sounds.',
                ['Verbatim transcripts keep everything: fillers (um, uh, ehn), repetitions, false starts, stutters and '
                 'non-speech sounds. ASR models need this because real speech contains it.',
                 'Guidelines fix the spellings of fillers and the tag list, and usually mark false starts with a hyphen '
                 '("we- we will"). Nothing is tidied.'],
                points=['Keep every filler using the guideline\'s spellings.', 'Keep repetitions: "I I think".',
                        'False start: word + hyphen ("go- going").', 'Sounds as tags: [cough], [laughter], [noise].'],
                example='Um, we- we [cough] we will start the meeting by ten.',
                quiz=[q('In verbatim style, a speaker says "uh, I I think so". You write…', 'Uh, I I think so.',
                        'I think so.', 'Uh, I think so.', 'I I think so.', why='Verbatim keeps fillers and repetitions.'),
                      q('How is a false start usually marked?', 'With a hyphen after the cut-off word', 'In brackets',
                        'It is deleted', 'In capital letters', why='e.g. "we- we will".'),
                      q('The speaker coughs. You…', 'add [cough]', 'ignore it', 'write "cough cough"', 'end the segment',
                        why='Use the tag from the list.')]),
    workflow=workflow_lesson('verbatim transcription', ['Learn the filler spellings and tag list.', 'Transcribe every sound and word.',
                             'Mark false starts with hyphens.', 'Do a pass only for fillers and repeats you smoothed out by habit.'],
                             ['Unconsciously tidying speech', 'Inventing filler spellings', 'Using tags not in the list'],
                             'Another transcriber reading your text could reconstruct the audio\'s hesitations.'),
    practice=task('Write verbatim transcripts', 'Use the audio notes to write strict verbatim text.',
                  {'kind': 'transcription', 'mode': 'verbatim',
                   'guidelines': ['Fillers: um, uh, ehn.', 'Keep repetitions and false starts (hyphen).',
                                  'Tags: [cough], [laughter], [noise], [inaudible].'],
                   'segments': [
                       {'id': 's1', 'context': 'Audio notes: "um", starts "we", restarts, coughs, then "we will start the meeting by ten".',
                        'reference': 'Um, we- we [cough] we will start the meeting by ten.', 'draft': 'We will start the meeting by ten.'},
                       {'id': 's2', 'context': 'Audio notes: says "the the price", "ehn", "is too high", laughs.',
                        'reference': 'The the price, ehn, is too high [laughter]', 'draft': 'The price is too high.'}]},
                  minutes=15),
    assessment=task('Verbatim assessment', 'Write three strict verbatim segments.',
                    {'kind': 'transcription', 'mode': 'verbatim',
                     'guidelines': ['Fillers: um, uh, ehn.', 'Keep repetitions and false starts (hyphen).',
                                    'Tags: [cough], [laughter], [noise], [inaudible].'],
                     'segments': [
                         {'id': 's1', 'context': 'Audio notes: "uh", "I", "I want to", restarts "go-", "going to Lagos".',
                          'reference': 'Uh, I I want to go- going to Lagos.', 'draft': 'I want to go to Lagos.'},
                         {'id': 's2', 'context': 'Audio notes: a door bangs, then "so so we agreed", one unclear word, "yesterday".',
                          'reference': '[noise] So so we agreed [inaudible] yesterday.', 'draft': 'So we agreed yesterday.'},
                         {'id': 's3', 'context': 'Audio notes: "ehn", "my my brother", laughs, "is the one".',
                          'reference': 'Ehn, my my brother [laughter] is the one.', 'draft': 'My brother is the one.'}]},
                    minutes=15),
    project_brief=project('Verbatim transcript of natural speech', 'Record (with consent) 1 minute of unscripted speech and transcribe it strictly verbatim.',
                          ['Audio link', 'Verbatim transcript with fillers, repeats, false starts and tags'],
                          ['Nothing tidied', 'Consistent filler spellings', 'Tags from the list only'], ['Verbatim transcription'],
                          difficulty='intermediate', hours=2),
    hours=4,
)

CLEAN = skill(
    'clean-transcription', 'Clean Transcription', level='beginner',
    tags=['transcription', 'speech-data'], icon='ri-brush-line', color=COLOR,
    tagline='Produce readable transcripts that keep the speaker\'s meaning and words.',
    description='Learn clean-verbatim rules: what to remove (fillers, false starts), what never to change (the speaker\'s words, dialect, grammar).',
    foundation=FOUNDATION,
    core=lesson('What clean transcription removes — and keeps', 'Apply clean-verbatim rules correctly.',
                ['Clean (or "intelligent") verbatim makes a transcript readable: remove fillers, false starts, '
                 'stutters and repeated words, and non-speech tags (except [inaudible]).',
                 'It does NOT paraphrase, correct grammar, or turn Pidgin or dialect into standard English. If the '
                 'speaker said "I no go fit come", the clean transcript still says that.'],
                points=['Remove: um, uh, ehn, false starts, accidental repetitions.', 'Keep: every meaningful word, the speaker\'s grammar and language.',
                        'Keep [inaudible]; drop [laughter]/[cough] unless the guideline keeps them.', 'Never summarise.'],
                example='Verbatim: Uh, I- I no go fit come [cough] tomorrow.\nClean:    I no go fit come tomorrow.',
                quiz=[q('Clean style: "Uh, I I no go fit come". You write…', 'I no go fit come.', "I won't be able to come.",
                        'Uh, I no go fit come.', 'I cannot come.', why='Remove fillers/repeats, keep the words.'),
                      q('Which is removed in clean transcription?', 'A false start', 'A Pidgin word', 'A dialect word',
                        '[inaudible]', why='Meaning-bearing words stay.'),
                      q('Should you correct the speaker\'s grammar?', 'No', 'Yes, always', 'Only for English', 'Only if asked by the speaker',
                        why='Clean ≠ edited.')]),
    workflow=workflow_lesson('clean transcription', ['Transcribe what is said.', 'Remove fillers and false starts.',
                             'Remove accidental repetitions only.', 'Check that no meaning-bearing word was lost or changed.'],
                             ['Paraphrasing', 'Correcting grammar', 'Removing emphatic repetition ("very very")', 'Dropping [inaudible]'],
                             'Readable, but every word the speaker meant is still there, unchanged.'),
    practice=task('Clean up verbatim transcripts', 'Turn verbatim text into clean transcripts.',
                  {'kind': 'transcription', 'mode': 'clean',
                   'guidelines': ['Remove fillers (um, uh, ehn), false starts and accidental repetitions.',
                                  'Remove [laughter], [cough], [noise]; keep [inaudible].', 'Do not change any other word.'],
                   'segments': [
                       {'id': 's1', 'reference': 'I no go fit come tomorrow.', 'draft': 'Uh, I- I no go fit come [cough] tomorrow.'},
                       {'id': 's2', 'reference': 'We will start the meeting by ten.', 'draft': 'Um, we- we [cough] we will start the meeting by ten.'}]},
                  minutes=10),
    assessment=task('Clean transcription assessment', 'Produce clean transcripts without changing meaning.',
                    {'kind': 'transcription', 'mode': 'clean',
                     'guidelines': ['Remove fillers (um, uh, ehn), false starts and accidental repetitions.',
                                    'Remove [laughter], [cough], [noise]; keep [inaudible].', 'Do not change any other word.'],
                     'segments': [
                         {'id': 's1', 'reference': 'The price is too high.', 'draft': 'The the price, ehn, is too high [laughter]'},
                         {'id': 's2', 'reference': 'So we agreed [inaudible] yesterday.', 'draft': '[noise] So so we agreed [inaudible] yesterday.'},
                         {'id': 's3', 'reference': 'Abeg make una wait small.', 'draft': 'Ehn, abeg make- make una wait small.'},
                         {'id': 's4', 'reference': 'I want to go to Lagos.', 'draft': 'Uh, I I want to go- go to Lagos.'}]},
                    minutes=12),
    project_brief=project('Clean transcript of an interview', 'Transcribe (with consent) a 2-minute interview in clean style.',
                          ['Audio link', 'Clean transcript with speaker labels', 'Three examples of things you removed and why'],
                          ['Readable and faithful', 'Speaker\'s language and grammar unchanged', 'Correct removals'],
                          ['Clean transcription'], hours=2),
    hours=3,
)

SKILLS = [YORUBA, IGBO, HAUSA, PIDGIN, NIG_ENGLISH, AFRICAN, SEGMENTATION, SPEAKER_ID, TIMESTAMPING, VERBATIM, CLEAN]
