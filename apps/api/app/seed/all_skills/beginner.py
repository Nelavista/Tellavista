"""African Language Data Beginner — the first-cohort entry path for students who have
never done language-data work. One Skill whose LearningPath sequences seven short courses,
then a practice round, a practical assessment and a final (practice) verification project:

    1 Introduction to Language Data      5 Audio Quality
    2 Data Privacy & Confidentiality     6 Basic Annotation
    3 Following Annotation Guidelines    7 AI Data Fundamentals
    4 Transcription Fundamentals         8 Practice round -> 9 Practical Assessment
                                         10 Final Skill Verification (practice project)

After it, students branch into Transcription, Translation, Annotation, Speech Data,
AI Evaluation and QA.
"""
from ._common import q, lesson, task, labeling, choice_items, project

COLOR = '#2563eb'


def _course(title, lessons):
    return {'title': title, 'lessons': lessons}


C1 = _course('Introduction to Language Data', [lesson(
    'What language data is and who makes it', 'Explain what language data is, what it is used for and the roles involved.',
    ['Every AI system that understands or produces human language — a voice assistant, a translation app, a chatbot — '
     'is built from <strong>language data</strong>: recordings of people speaking, written text, and the labels and '
     'judgements people attach to them. A model learns only what that data shows it. That is why AI is usually much '
     'better in English than in Yoruba, Igbo, Hausa or Pidgin: far less good data exists for these languages.',
     'Language data is made by people in a handful of roles. <strong>Transcribers</strong> turn speech into text. '
     '<strong>Translators</strong> produce parallel sentences. <strong>Speech contributors</strong> record prompts. '
     '<strong>Annotators</strong> label text or audio (sentiment, intent, names). <strong>Evaluators</strong> judge AI output. '
     '<strong>QA reviewers</strong> check everyone else\'s work. Each role needs native-language skill <em>and</em> the discipline '
     'to follow a project\'s rules exactly.',
     'Projects usually run the same way: you read a guideline, pass a qualification test, work through batches on an online '
     'platform, and your quality is checked continuously. The paths on Nelavista mirror that process with practice tasks and '
     'simulated projects, so you can show what you can do. Completing them prepares you for this kind of work; it doesn\'t '
     'guarantee a project or a job.'],
    points=['Language data = speech, text, and the labels/judgements on them.', 'Roles: transcriber, translator, speech contributor, annotator, evaluator, QA reviewer.',
            'Projects run on guidelines → qualification → batches → continuous QA.', 'Your native language is valuable expertise.'],
    quiz=[q('Why is AI usually weaker in Yoruba than in English?', 'Much less good Yoruba data exists to learn from', 'Yoruba is harder for computers by nature',
            'Nobody speaks Yoruba online', 'AI cannot handle tone', why='Models learn from data.'),
          q('Who turns speech into text?', 'A transcriber', 'An evaluator', 'A localiser', 'A speech contributor', why='Transcription = speech → text.'),
          q('What usually comes first when you join a data project?', 'Reading the guideline and passing a qualification test', 'Getting paid',
            'Labelling as fast as possible', 'Writing your own rules', why='Guideline + qualification come first.')]),
])

C2 = _course('Data Privacy & Confidentiality', [lesson(
    'Protecting people and projects', 'Recognise personal data and confidential material and handle both correctly.',
    ['Language data often contains real people: their voices, names, phone numbers, addresses, account or BVN numbers, health '
     'details. This is <strong>personal data</strong>. In Nigeria the Data Protection Act 2023 requires a lawful basis (usually '
     'informed consent), collecting only what is needed, keeping it secure, and reporting breaches. International clients add '
     'their own rules (for example the EU GDPR).',
     'Projects are also <strong>confidential</strong>: you will often sign a non-disclosure agreement (NDA) covering the client, '
     'guidelines, tools and data. The most common ways contributors break confidentiality are ordinary ones — a screenshot in a '
     'WhatsApp group, sharing the guideline PDF with friends, or saving audio to a personal phone.',
     'Practical rules: work only inside approved tools; never copy data out; replace personal details exactly as the guideline '
     'says (e.g. [PHONE]); describe your experience generically on a CV unless you are allowed to name the client; and report '
     'any accidental exposure immediately. This is general guidance, not legal advice — always read your own agreement.'],
    points=['Personal data: names, numbers, addresses, IDs/BVN, health details, voices.', 'Consent + minimisation + security.',
            'No screenshots, no sharing guidelines, no copying data out.', 'Report accidental exposure immediately.'],
    quiz=[q('A transcript contains a caller\'s phone number. The guideline says to anonymise. You write…', '[PHONE] (or the tag the guideline specifies)',
            'the number as spoken', 'nothing, and delete the segment', 'only the last four digits', why='Follow the anonymisation rule.'),
          q('Which is a confidentiality breach?', 'Posting a screenshot of a task in a study group', 'Saying "I do transcription work" in an interview',
            'Asking the project lead a question', 'Reading the guideline twice', why='Screenshots leak project material.'),
          q('You emailed a file with names to the wrong person by mistake. You…', 'report it to the project lead immediately', 'hope nobody notices',
            'delete your sent folder', 'wait a week', why='Breaches must be reported quickly.')]),
])

C3 = _course('Following Annotation Guidelines', [lesson(
    'The guideline is the job', 'Read, apply and query a guideline the way top contributors do.',
    ['A guideline defines the task: the labels or format, a definition and examples for each, and — most importantly — the '
     '<strong>edge-case rules</strong> ("sarcasm counts as negative", "a greeting plus a request is labelled as the request"). '
     'Thousands of items from many people only become usable data if everyone applies the same rules.',
     'Good habits: read the whole guideline before item one; keep a one-page note of edge cases; re-read it whenever a new '
     'version is released (updates often change edge cases); and when something is not covered, ask in the official channel '
     'with the item ID — while following the guideline\'s instruction for unclear items (often "skip" or "flag"), never your own rule.',
     'Your instinct will sometimes disagree with the guideline. On a project, the guideline wins. If you think a rule is wrong, '
     'say so in the channel — but keep applying it until it is changed.'],
    points=['Read everything before starting; note edge cases.', 'Guideline beats instinct.', 'Re-read every new version.',
            'Unclear? Ask with an item ID; follow the "unclear item" rule meanwhile.'],
    example='Guideline: "Sarcasm is labelled by its real meaning."\nItem: "Nice one NEPA, light don go again 🙄"\nLabel: Negative (not Positive)',
    quiz=[q('Your instinct says Positive; the guideline\'s sarcasm rule says Negative. You label…', 'Negative', 'Positive', 'Unsure', 'whatever is faster',
            why='The guideline wins.'),
          q('A case keeps appearing that the guideline doesn\'t cover. You…', 'ask in the official channel with an example item ID', 'invent a rule',
            'label randomly', 'stop working', why='Ask; don\'t improvise.'),
          q('Version 2 of the guideline is released. You…', 'read what changed and apply it from now on', 'keep using version 1', 'ignore it until asked',
            'only skim the title', why='Updates change edge cases.')]),
])

C4 = _course('Transcription Fundamentals', [lesson(
    'Speech to text, the professional way', 'Apply the core conventions of transcription.',
    ['Transcription projects choose a style. <strong>Verbatim</strong> keeps everything spoken — fillers (um, ehn), repetitions, '
     'false starts. <strong>Clean</strong> removes those but never changes the speaker\'s words, grammar or language: Pidgin stays '
     'Pidgin. Non-speech events use only the project\'s tags, e.g. [laughter], [noise], [inaudible]. A word you cannot hear is '
     '[inaudible] — never a guess.',
     'Nigerian languages must be written in their standard spelling. Yoruba needs tone marks and under-dots (ẹ, ọ, ṣ); Igbo needs '
     'the dotted vowels ị, ọ, ụ; Hausa needs the hooked letters ɓ, ɗ, ƙ. Speech-recognition systems drop these marks, which is '
     'exactly why human transcribers are needed. Multi-speaker audio gets consistent speaker labels; many projects also need '
     'timestamps (start time of each segment).',
     'Quality is measured as <strong>word error rate</strong> (WER): substitutions + deletions + insertions, divided by the number of '
     'words in the correct transcript. 2 errors in 20 words is a WER of 0.1 (90% accuracy).'],
    points=['Verbatim keeps fillers; clean removes them — neither changes the words.', 'Unclear speech → [inaudible], never a guess.',
            'Standard spelling incl. Yoruba tone marks, Igbo dots, Hausa hooks.', 'WER = (S + D + I) ÷ reference words.'],
    example='ASR output:  how you day i day fine\nClean transcript:  How you dey? I dey fine.',
    quiz=[q('In clean style, the speaker says "Uh, I I no go fit come". You write…', 'I no go fit come.', "I won't be able to come.", 'Uh, I I no go fit come.',
            'I cannot come.', why='Remove fillers/repeats; keep the words and language.'),
          q('2 errors in a 20-word reference. WER?', '0.1', '0.2', '0.02', '2', why='2 ÷ 20.'),
          q('Which spelling is required in a Yoruba transcript?', 'Ẹ káàárọ̀', 'E kaaaro', 'E kaaro', 'Eh karo', why='Standard orthography with marks.')]),
])

C5 = _course('Audio Quality', [lesson(
    'What makes a recording usable', 'Record and judge audio by the checks reviewers use.',
    ['Speech datasets reject recordings for a few objective reasons: <strong>clipping</strong> (too loud — the waveform is cut off '
     'and sounds distorted), <strong>too quiet</strong> (average level below about −40 dBFS), <strong>noise</strong> (fans, generators, '
     'traffic close to the voice level), <strong>mostly silence</strong>, being <strong>cut off</strong>, or <strong>not matching the prompt</strong>.',
     'To record well with a phone: a quiet room with soft furnishings (curtains, a bed) to absorb echo; the phone about a '
     'hand-width (15–20 cm) from your mouth, slightly to the side; a half-second pause before and after speaking; read exactly '
     'the prompt; listen back to every take and re-record any with a slip or noise.',
     'Reviewers judge in a fixed order — format, then signal (clipping, level, noise), then content — and give the first failing '
     'reason. An accent or regional pronunciation is never a reason to reject: datasets need that variety.'],
    points=['Reject for: clipping, too quiet, noise, mostly silence, cut off, wrong words.', '15–20 cm from the mic; quiet, soft room.',
            'Listen back to every take.', 'Accent is never a reason to reject.'],
    quiz=[q('A recording sounds distorted because the speaker shouted. The problem is…', 'clipping', 'silence', 'wrong words', 'accent', why='Too loud.'),
          q('A clear recording of the right prompt with a strong Ibadan accent should be…', 'accepted', 'rejected', 're-recorded in another accent', 'skipped',
            why='Accent is not a defect.'),
          q('Best phone position for recording?', 'About 15–20 cm from the mouth, slightly to the side', 'Touching your lips', 'Across the room', 'In your pocket',
            why='Avoids pops and echo.')]),
])

C6 = _course('Basic Annotation', [lesson(
    'Labelling text consistently', 'Apply common label sets: sentiment, intent and named entities.',
    ['Annotation attaches labels so models can learn. Three common tasks: <strong>sentiment</strong> (positive / negative / neutral / '
     'mixed — the writer\'s attitude), <strong>intent</strong> (what a user wants a chatbot to do — label the goal, not the keywords), '
     'and <strong>named entities</strong> (PER people, LOC places, ORG organisations, DATE dates — decided by context: "Lagos" is a place '
     'in "I live in Lagos" but part of an organisation in "Lagos State University").',
     'Nigerian text needs local knowledge: Pidgin intensifiers ("sweet well well" = very good, "slow die" = very slow), sarcasm, and '
     'code-switching. Quality is measured against <strong>gold labels</strong> and by <strong>consistency</strong> — projects quietly '
     'repeat items to see whether you label the same thing the same way twice.'],
    points=['Sentiment: neutral = facts, no opinion; mixed = both clearly present.', 'Intent: label the request, not the greeting.',
            'Entities: decided by context; mark the whole name.', 'Consistency is measured with repeated items.'],
    quiz=[q('"Good morning, abeg check my balance" — intent?', 'check_balance', 'greeting', 'complaint', 'out_of_scope', why='Label the request.'),
          q('"The shop opens at 9am." — sentiment?', 'Neutral', 'Positive', 'Negative', 'Mixed', why='A fact, no opinion.'),
          q('"Dangote Group" in "She works at Dangote Group" is…', 'ORG', 'PER', 'LOC', 'DATE', why='An organisation.')]),
])

C7 = _course('AI Data Fundamentals', [lesson(
    'Judging what AI produces', 'Evaluate AI responses the way evaluation projects do.',
    ['Human judgement is how AI gets better: evaluators rate responses, compare two responses and pick the better one '
     '(preference data), and flag unsafe output. For African languages, evaluators catch failures models make constantly: '
     'answering in the wrong language, missing diacritics, "Pidgin" that is really English, and confident wrong facts '
     '(<strong>hallucinations</strong>).',
     'Judge in a fixed order: <strong>accuracy</strong> first (check facts — a fluent answer can be false), then <strong>language</strong> '
     '(right language, natural, correctly spelled), then <strong>helpfulness</strong>, then style. Length never decides. Every judgement '
     'needs a short, specific rationale that points to the problem: "Says Lagos is the capital; it is Abuja."',
     'Safety works in two directions: an AI that helps with fraud is unsafe, but an AI that refuses a harmless question ("How is '
     'malaria treated?") also fails users — that is <strong>over-refusal</strong>.'],
    points=['Accuracy → language → helpfulness → style.', 'Fluent ≠ correct: verify facts.', 'Specific rationales that quote the problem.',
            'Refusing harmless requests is a failure too.'],
    quiz=[q('An AI says "Wole Soyinka wrote Things Fall Apart." This is…', 'a factual error (it was Chinua Achebe)', 'correct', 'a language error',
            'over-refusal', why='Check facts.'),
          q('A user writes in Hausa; the AI answers correctly in English. Main issue?', 'Wrong language', 'Factual error', 'None', 'Unsafe',
            why='Answer in the user\'s language.'),
          q('Response A is short and correct; B is long with an error. Better?', 'A', 'B', 'Tie', 'Cannot say', why='Accuracy first; length never decides.')]),
])

_YN = ['Correct', 'Incorrect']

PRACTICE = task(
    'Practice round: language-data basics', 'Mixed practice across the seven topics. Answers are shown after you submit.',
    labeling(
        choice_items('a', 'Best answer', ['Positive', 'Negative', 'Neutral', 'Mixed'], [
            ('Sentiment: "This phone sweet well well!"', 'Positive'), ('Sentiment: "The meeting is at 4pm."', 'Neutral')])
        + choice_items('b', 'Decision', ['Accept', 'Reject'], [
            ('Recording: correct prompt, clear, strong regional accent.', 'Accept'), ('Recording: the speaker shouted and it sounds distorted.', 'Reject')])
        + choice_items('c', 'Acceptable?', ['Acceptable', 'Not acceptable'], [
            ('Sharing the project guideline with your study group.', 'Not acceptable'),
            ('Writing [inaudible] for a word you cannot hear.', 'Acceptable')])
        + [{'id': 't1', 'text': 'Correct this machine transcript of Nigerian Pidgin: "a beg make we go market"',
            'fields': [{'name': 'v', 'label': 'Corrected transcript', 'type': 'text', 'expected': 'Abeg make we go market'}]}],
        ['Use what you learned in the seven courses.', 'Pidgin spellings: abeg, dey, wetin, una.']),
    minutes=12)

ASSESSMENT = task(
    'Practical Assessment: language-data basics', 'A scored practical check across privacy, guidelines, transcription, audio, annotation and AI evaluation.',
    labeling(
        choice_items('p', 'Acceptable?', ['Acceptable', 'Not acceptable'], [
            ('Saving project audio to your personal Google Drive as a backup.', 'Not acceptable'),
            ('Replacing a caller\'s phone number with [PHONE] as the guideline says.', 'Acceptable')])
        + choice_items('g', 'Label (guideline: sarcasm = its real meaning)', ['Positive', 'Negative', 'Neutral', 'Mixed'], [
            ('"Wow, another fuel queue. Just what I needed 😒"', 'Negative'),
            ('"The jollof was nice but the place too hot."', 'Mixed')])
        + choice_items('i', 'Intent', ['check_balance', 'buy_airtime', 'greeting', 'complaint'], [
            ('"Good afternoon, abeg recharge ₦500 airtime for me"', 'buy_airtime')])
        + choice_items('e', 'Entity type of the quoted span', ['PER', 'LOC', 'ORG', 'DATE'], [
            ('"Lagos State University don resume." — "Lagos State University"', 'ORG')])
        + choice_items('r', 'Decision', ['Accept', 'Reject: clipped', 'Reject: too quiet', 'Reject: wrong words'], [
            ('Prompt "Please call me tonight"; heard "Please call me tomorrow".', 'Reject: wrong words'),
            ('Clear take, right words, average level −48 dBFS.', 'Reject: too quiet')])
        + choice_items('x', 'Main issue', ['None', 'Factual error', 'Wrong language', 'Over-refusal'], [
            ('User: "Who wrote Things Fall Apart?" AI: "Wole Soyinka."', 'Factual error'),
            ('User: "How is malaria treated?" AI: "I can\'t discuss medical topics."', 'Over-refusal')])
        + [{'id': 't1', 'text': 'Clean transcript of this machine output (Pidgin): "how you day i day fine"',
            'fields': [{'name': 'v', 'label': 'Corrected transcript', 'type': 'text', 'expected': 'How you dey I dey fine'}]},
           {'id': 't2', 'text': 'Clean transcript (remove fillers and repeats only): "Uh, I- I no go fit come tomorrow"',
            'fields': [{'name': 'v', 'label': 'Clean transcript', 'type': 'text', 'expected': 'I no go fit come tomorrow'}]},
           {'id': 'n1', 'text': 'A transcript has 3 errors against a 30-word reference.',
            'fields': [{'name': 'v', 'label': 'WER (decimal)', 'type': 'number', 'expected': 0.1, 'tolerance': 0.001}]}],
        ['Apply the rules from the seven courses.', 'Pidgin spellings: abeg, dey, wetin, una.', 'Punctuation and capitals are not scored.'],
        report={'label': 'In your own words: why is guessing a word you cannot hear worse than writing [inaudible]?', 'min_words': 20},
        ai_feedback=True),
    minutes=20)

PROJECT = project(
    'Practice Project: Mini language-data portfolio',
    'Simulation — a Nelavista practice project using data you create yourself. Choose a Nigerian language you speak (or Nigerian Pidgin/English). '
    'Produce a small sample of each kind of work covered in this path.',
    ['Record 5 short everyday sentences (no personal details), add the audio link, and transcribe them in standard spelling',
     'Write 10 sentences and label their sentiment, with a 3-rule guideline you wrote yourself',
     'Ask a free AI assistant 3 questions in your language; rate each 1–5 with a one-line rationale',
     'A 5-point privacy checklist you would follow on a real project'],
    ['Correct spelling and transcription conventions', 'Consistent labels that follow your own guideline',
     'Specific, accurate AI-evaluation rationales', 'Sound privacy practice'],
    ['Language data basics', 'Transcription', 'Annotation', 'AI evaluation'], hours=3)

BEGINNER = {
    'slug': 'african-language-data-beginner', 'name': 'African Language Data Beginner', 'level': 'beginner', 'language': None,
    'tags': ['transcription', 'annotation', 'ai', 'speech-data', 'data-privacy', 'beginner-path'],
    'icon': 'ri-flag-2-line', 'color': COLOR, 'estimated_hours': 8,
    'tagline': 'Handle the basics of African-language data work safely: privacy, guidelines, transcription, audio, annotation and AI evaluation.',
    'description': ('For students who have never done language-data work. Seven short courses — language data, privacy, '
                    'guidelines, transcription, audio quality, annotation and AI evaluation — then a practice round, a scored '
                    'practical assessment and a reviewed practice project. Afterwards, branch into Transcription, Translation, '
                    'Annotation, Speech Data, AI Evaluation or QA.'),
    'courses': [C1, C2, C3, C4, C5, C6, C7],
    'lessons': [l for c in (C1, C2, C3, C4, C5, C6, C7) for l in c['lessons']],
    'practice': PRACTICE, 'assessment': {**ASSESSMENT, 'pass_score': 70}, 'project': PROJECT,
}
