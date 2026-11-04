"""AI Data Work category — the human-in-the-loop tasks behind modern AI: annotation for
training, response and model evaluation, preference feedback, relevance and safety
judgements. Tasks are built as simulated project batches with gold judgements, and most
assessments also require a written rationale (as real evaluation projects do).
"""
from ._common import q, lesson, workflow_lesson, task, labeling, project, skill

COLOR = '#4f46e5'


def it(iid, text, *fields, context=None):
    item = {'id': iid, 'text': text, 'fields': list(fields)}
    if context:
        item['context'] = context
    return item


def ch(name, label, options, expected):
    return {'name': name, 'label': label, 'type': 'choice', 'options': options, 'expected': expected}


def num(name, label, expected, tolerance=1):
    return {'name': name, 'label': label, 'type': 'number', 'expected': expected, 'tolerance': tolerance}


FOUNDATION = lesson(
    'How human data powers AI systems',
    'Understand where human judgements enter the AI pipeline.',
    [
        'Large language models and speech systems are trained on human-labelled data, tuned with human preference feedback, '
        'and tested by human evaluators. For African languages, there are few people doing this work, which is why models often '
        'answer in the wrong language, get local facts wrong, or produce unnatural Yoruba, Igbo, Hausa or Pidgin.',
        'Evaluation work is judged on <strong>accuracy</strong> (does your judgement match well-calibrated reviewers?), '
        '<strong>consistency</strong> (same case, same judgement), and <strong>rationales</strong> (a short, specific explanation '
        'of why). A good rationale points to the exact problem: "States Wole Soyinka wrote Things Fall Apart; it was Chinua Achebe."',
    ],
    points=['Judge against the rubric, not personal taste.', 'Check facts — don\'t assume a fluent answer is right.',
            'Write specific rationales that quote the problem.', 'Your local language and knowledge are the value you add.'],
    quiz=[
        q('A fluent, confident AI answer contains a wrong date. You…', 'mark it as a factual error', 'rate it highly because it reads well',
          'ignore dates', 'rewrite it silently', why='Fluency ≠ accuracy.'),
        q('Which rationale is most useful?', '"Says Lagos is the capital; the capital is Abuja."', '"Bad answer."', '"I didn\'t like it."', '"Wrong."',
          why='Specific and checkable.'),
        q('Why is African-language evaluation work especially valuable?', 'Few people do it, so models are weakest there', 'It is easier',
          'Models are already perfect there', 'It pays nothing', why='Scarcity of expertise.'),
    ],
)

RATIONALE = {'label': 'Rationale for your judgement on the item you found hardest', 'min_words': 20}


def _ai_skill(slug, name, *, level, tags, icon, tagline, description, core, steps, mistakes, quality,
              practice_items, assessment_items, guidelines, project_brief, hours=4, pass_score=70, report=RATIONALE):
    return skill(
        slug, name, level=level, tags=['ai', 'evaluation'] + tags, icon=icon, color=COLOR, tagline=tagline,
        description=description, foundation=FOUNDATION, core=core,
        workflow=workflow_lesson(name.lower(), steps, mistakes, quality),
        practice=task(f'{name}: simulated batch', 'Work through a simulated project batch.',
                      labeling(practice_items, guidelines), minutes=15),
        assessment=task(f'{name} assessment', 'A scored batch with a written rationale.',
                        labeling(assessment_items, guidelines, report=report, ai_feedback=True), minutes=20),
        project_brief=project_brief, hours=hours, pass_score=pass_score,
    )


_TASK_TYPES = ['Question answering', 'Summarisation', 'Translation', 'Creative writing', 'Classification', 'Coding']
AI_ANNOTATION = _ai_skill(
    'ai-data-annotation', 'AI Data Annotation', level='beginner', tags=['annotation'], icon='ri-robot-line',
    tagline='Label prompts and data the way AI training pipelines need.',
    description='Annotate prompts and examples for AI training sets — task type, language, quality — with the consistency training data demands.',
    core=lesson('Annotating data for model training', 'Label training prompts by task type and quality.',
                ['Instruction-tuning datasets are organised by task type (question answering, summarisation, translation, creative '
                 'writing, classification, coding) so that a model learns a balanced mix. Annotators label each prompt\'s task type, '
                 'language and whether it is usable.',
                 'Label by what the prompt asks the model to DO, not its topic: "Translate this news headline to Hausa" is Translation '
                 'even though it is about news.'],
                points=['Task type = what the model must do.', 'Topic is not task type.', 'Mixed requests → the main task.'],
                quiz=[q('"Summarise this article about the naira in two lines." Task type?', 'Summarisation', 'Question answering', 'Translation', 'Classification',
                        why='What it must do.'),
                      q('"Is this review positive or negative?" Task type?', 'Classification', 'Creative writing', 'Summarisation', 'Coding', why='Choose a label.'),
                      q('Task type is decided by…', 'what the prompt asks the model to do', 'its topic', 'its length', 'its language', why='Action, not topic.')]),
    steps=['Read the prompt.', 'Identify the requested action.', 'Label task type.', 'Flag unusable prompts.'],
    mistakes=['Labelling by topic', 'Ignoring the main task in multi-part prompts'], quality='Every prompt\'s label reflects the action requested.',
    practice_items=[it(f'p{i}', t, ch('type', 'Task type', _TASK_TYPES, e)) for i, (t, e) in enumerate([
        ('Translate "Good morning" into Yoruba.', 'Translation'),
        ('Write a short poem about Lagos traffic.', 'Creative writing'),
        ('What year did Nigeria gain independence?', 'Question answering'),
        ('Write a Python function that adds two numbers.', 'Coding')], 1)],
    assessment_items=[it(f'a{i}', t, ch('type', 'Task type', _TASK_TYPES, e)) for i, (t, e) in enumerate([
        ('Summarise this news story about the CBN in three bullet points.', 'Summarisation'),
        ('Is this tweet about sports, politics or business?', 'Classification'),
        ('Turn this Pidgin sentence into English: "Una don chop?"', 'Translation'),
        ('Write a story for children about a clever tortoise.', 'Creative writing'),
        ('Who is the author of "Purple Hibiscus"?', 'Question answering'),
        ('Fix the bug in this JavaScript loop.', 'Coding')], 1)],
    guidelines=['Label the task the prompt asks the model to perform.'],
    project_brief=project('Write and annotate 30 training prompts', 'Write 30 prompts a Nigerian user might give an AI assistant (in at least two languages), 5 per task type, and annotate them.',
                          ['30 prompts with task type and language', 'Balanced distribution table', 'Notes on 3 borderline prompts'],
                          ['Realistic prompts', 'Correct labels', 'Balanced set'], ['AI data annotation'], hours=2),
    report=None,
)

_ISSUES = ['None', 'Factual error', 'Wrong language', 'Incomplete', 'Unsafe', 'Unnatural language']
RESPONSE_EVAL = _ai_skill(
    'ai-response-evaluation', 'AI Response Evaluation', level='beginner', tags=['llm'], icon='ri-chat-check-line',
    tagline='Rate single AI responses for accuracy, language and helpfulness.',
    description='Score individual AI assistant responses on a 1–5 rubric, identify the main issue, and justify your rating — with Nigerian facts and languages.',
    core=lesson('Rating a response on a rubric', 'Apply a 1–5 rubric and identify the main issue.',
                ['Response-rating projects give a rubric: 5 = fully correct, complete and in the right language; 4 = minor issue; '
                 '3 = useful but with a clear problem (e.g. answered in the wrong language); 2 = major problem; 1 = wrong or harmful.',
                 'Always check facts you can check, and check the language: if a user writes in Yoruba, the guideline usually expects '
                 'the answer in Yoruba.'],
                points=['5 correct & complete · 3 clear problem · 1 wrong/harmful.', 'Answer in the user\'s language unless told otherwise.',
                        'Name the single main issue.', 'Verify facts.'],
                quiz=[q('User asks in Hausa; AI answers correctly but in English. Typical rating?', '3 — useful but wrong language', '5', '1', '4',
                        why='Clear problem, still useful.'),
                      q('"Wole Soyinka wrote Things Fall Apart." Main issue?', 'Factual error', 'Wrong language', 'Incomplete', 'None',
                        why='Chinua Achebe wrote it.'),
                      q('"List three Nigerian languages." → "Yoruba." Main issue?', 'Incomplete', 'Factual error', 'Unsafe', 'None', why='Only one of three.')]),
    steps=['Read the prompt and note the language.', 'Check every fact.', 'Check completeness.', 'Pick the main issue.', 'Assign the score.'],
    mistakes=['Rewarding fluency over accuracy', 'Ignoring wrong-language answers', 'Vague rationales'],
    quality='Scores within 1 of calibrated reviewers, with the right main issue.',
    practice_items=[
        it('r1', 'Prompt: "How many states does Nigeria have?"\nResponse: "Nigeria has 36 states and the Federal Capital Territory."',
           ch('issue', 'Main issue', _ISSUES, 'None'), num('score', 'Score (1-5)', 5)),
        it('r2', 'Prompt: "Who wrote Things Fall Apart?"\nResponse: "Wole Soyinka wrote Things Fall Apart in 1958."',
           ch('issue', 'Main issue', _ISSUES, 'Factual error'), num('score', 'Score (1-5)', 1)),
        it('r3', 'Prompt: "Kí ni olú-ìlú Nàìjíríà?"\nResponse: "The capital of Nigeria is Abuja."',
           ch('issue', 'Main issue', _ISSUES, 'Wrong language'), num('score', 'Score (1-5)', 3))],
    assessment_items=[
        it('r1', 'Prompt: "List three Nigerian languages."\nResponse: "Yoruba."', ch('issue', 'Main issue', _ISSUES, 'Incomplete'), num('score', 'Score (1-5)', 2)),
        it('r2', 'Prompt: "What currency does Nigeria use?"\nResponse: "Nigeria uses the naira (₦), divided into 100 kobo."',
           ch('issue', 'Main issue', _ISSUES, 'None'), num('score', 'Score (1-5)', 5)),
        it('r3', 'Prompt: "Ina ne babban birnin Najeriya?"\nResponse: "Babban birnin Najeriya shi ne Lagos."',
           ch('issue', 'Main issue', _ISSUES, 'Factual error'), num('score', 'Score (1-5)', 1)),
        it('r4', 'Prompt: "Write a Pidgin greeting for the morning."\nResponse: "Good morning, how are you doing today?"',
           ch('issue', 'Main issue', _ISSUES, 'Wrong language'), num('score', 'Score (1-5)', 2)),
        it('r5', 'Prompt: "Which river flows through Lokoja?"\nResponse: "The Niger and Benue rivers meet at Lokoja."',
           ch('issue', 'Main issue', _ISSUES, 'None'), num('score', 'Score (1-5)', 5))],
    guidelines=['Score 1–5: 5 correct & complete in the user\'s language; 3 useful with a clear problem; 1 wrong or harmful.',
                'Within 1 point of the gold score counts as agreement.', 'Pick the single main issue.'],
    project_brief=project('Evaluate an AI assistant in your language', 'Ask a free AI assistant 15 questions in a Nigerian language you speak (local facts, everyday tasks).',
                          ['Table: prompt, response (summary), score, main issue, rationale', 'A 150-word summary of strengths and weaknesses'],
                          ['Calibrated scores', 'Fact-checked', 'Specific rationales'], ['AI response evaluation'], hours=3),
)

LLM_EVAL = _ai_skill(
    'llm-evaluation', 'LLM Evaluation', level='intermediate', tags=['llm'], icon='ri-scales-line',
    tagline='Compare model outputs side by side and pick the better one, with reasons.',
    description='Pairwise LLM evaluation: compare two model responses, choose the better one or a tie, and name the deciding factor — as in model benchmarking.',
    core=lesson('Pairwise comparison', 'Choose between two responses consistently.',
                ['Many LLM leaderboards and model comparisons use pairwise human judgements: given one prompt and two responses, '
                 'which is better? Evaluators judge accuracy first, then language quality, then helpfulness, then style — a fixed '
                 'order keeps judgements consistent.',
                 'Choose "Tie" only when the responses are genuinely equivalent. Don\'t let length decide: a longer answer is not '
                 'better if it adds errors.'],
                points=['Order: accuracy → language → helpfulness → style.', 'Length is not quality.', 'Tie only when truly equivalent.',
                        'Name the deciding factor.'],
                quiz=[q('A is short and correct; B is long and contains an error. Better?', 'A', 'B', 'Tie', 'Neither can be judged', why='Accuracy first.'),
                      q('"Translate thank you to Hausa": A "Na gode", B "Daalụ". Better?', 'A', 'B', 'Tie', 'Both wrong', why='Daalụ is Igbo.'),
                      q('When should you pick Tie?', 'When both are genuinely equivalent', 'When unsure', 'When both are long', 'Never', why='Not a dodge.')]),
    steps=['Read the prompt.', 'Check both for accuracy.', 'Compare language quality.', 'Compare helpfulness.', 'Pick and name the deciding factor.'],
    mistakes=['Preferring longer answers', 'Overusing Tie', 'Missing a wrong-language answer'],
    quality='Preferences follow the fixed order and are explained.',
    practice_items=[
        it('c1', 'Prompt: "What is the capital of Nigeria?"\nA: "Lagos."\nB: "Abuja."',
           ch('pref', 'Better response', ['A', 'B', 'Tie'], 'B'), ch('why', 'Deciding factor', ['Accuracy', 'Language', 'Helpfulness', 'Style'], 'Accuracy')),
        it('c2', 'Prompt: "Translate \'thank you\' into Hausa."\nA: "Na gode."\nB: "Daalụ."',
           ch('pref', 'Better response', ['A', 'B', 'Tie'], 'A'), ch('why', 'Deciding factor', ['Accuracy', 'Language', 'Helpfulness', 'Style'], 'Accuracy')),
        it('c3', 'Prompt: "Give me a Yoruba morning greeting."\nA: "Ẹ káàárọ̀."\nB: "E kaaaro."',
           ch('pref', 'Better response', ['A', 'B', 'Tie'], 'A'), ch('why', 'Deciding factor', ['Accuracy', 'Language', 'Helpfulness', 'Style'], 'Language'))],
    assessment_items=[
        it('c1', 'Prompt: "How do I check my JAMB result?"\nA: "Visit the official JAMB portal or send RESULT to the official short code from your registered number."\nB: "I can\'t help with that."',
           ch('pref', 'Better response', ['A', 'B', 'Tie'], 'A'), ch('why', 'Deciding factor', ['Accuracy', 'Language', 'Helpfulness', 'Style'], 'Helpfulness')),
        it('c2', 'Prompt: "Who wrote Things Fall Apart?"\nA: "Chinua Achebe."\nB: "Chinua Achebe, in 1958. It is one of the most widely read African novels."',
           ch('pref', 'Better response', ['A', 'B', 'Tie'], ['B', 'Tie']), ch('why', 'Deciding factor', ['Accuracy', 'Language', 'Helpfulness', 'Style'], ['Helpfulness', 'Style'])),
        it('c3', 'Prompt (Pidgin): "Wetin be the capital of Ghana?"\nA: "Na Accra be Ghana capital."\nB: "The capital of Ghana is Kumasi."',
           ch('pref', 'Better response', ['A', 'B', 'Tie'], 'A'), ch('why', 'Deciding factor', ['Accuracy', 'Language', 'Helpfulness', 'Style'], 'Accuracy')),
        it('c4', 'Prompt: "Say good morning in Igbo."\nA: "Ụtụtụ ọma."\nB: "Ututu oma."',
           ch('pref', 'Better response', ['A', 'B', 'Tie'], 'A'), ch('why', 'Deciding factor', ['Accuracy', 'Language', 'Helpfulness', 'Style'], 'Language'))],
    guidelines=['Judge in order: accuracy, language quality (incl. diacritics), helpfulness, style.', 'Length alone never decides.'],
    project_brief=project('Head-to-head evaluation of two models', 'Pick two free AI assistants. Give both the same 12 prompts in a Nigerian language and compare.',
                          ['Table: prompt, preference, deciding factor, rationale', 'Win/tie/loss summary', 'Where each model fails in your language'],
                          ['Consistent preferences', 'Clear rationales', 'Language-specific insight'], ['LLM evaluation'],
                          difficulty='intermediate', hours=3),
)

GEN_TEXT = _ai_skill(
    'ai-generated-text-evaluation', 'AI-Generated Text Evaluation', level='intermediate', tags=['african-languages', 'llm'], icon='ri-file-text-line',
    tagline='Judge whether AI-written African-language text is natural and correct.',
    description='Evaluate AI-generated Yoruba, Igbo, Hausa and Pidgin text for spelling, naturalness, repetition and relevance — where models are weakest.',
    core=lesson('What goes wrong in AI-generated African-language text', 'Spot the typical failures of generated text.',
                ['Generated text in African languages often looks plausible but fails in predictable ways: missing diacritics or special '
                 'letters, English word order dressed in Yoruba or Igbo words, "Pidgin" that is really English, repetitive loops, and '
                 'content that drifts off the prompt.',
                 'Rate naturalness (1–5: would a native speaker write this?) and identify the main issue.'],
                points=['Spelling/diacritics: missing tone marks, dots, hooks.', 'Calque: English structure in another language\'s words.',
                        'Fake Pidgin: English with "dey" added.', 'Repetition and off-topic drift.'],
                quiz=[q('Generated "Pidgin": "I am going to the market, dey." Main issue?', 'Not real Pidgin (unnatural language)', 'None', 'Off-topic', 'Repetition',
                        why='It is English with a token Pidgin word.'),
                      q('Yoruba text with no tone marks at all. Main issue?', 'Spelling/diacritics', 'Repetition', 'Off-topic', 'None', why='Orthography.'),
                      q('Naturalness 1–5 asks…', 'would a native speaker write this?', 'is it long?', 'is it polite?', 'is it formal?', why='Native-likeness.')]),
    steps=['Read as a native speaker would.', 'Check orthography.', 'Check structure and idiom.', 'Check relevance and repetition.', 'Rate and name the main issue.'],
    mistakes=['Accepting text without diacritics', 'Rating fake Pidgin as natural', 'Missing repetition'],
    quality='Ratings reflect native-speaker judgement.',
    practice_items=[
        it('g1', 'Prompt: "Write a Yoruba greeting."\nGenerated: "E kaaaro, se daadaa ni?"', ch('issue', 'Main issue', ['None', 'Spelling/diacritics', 'Unnatural language', 'Repetition', 'Off-topic'], 'Spelling/diacritics'),
           num('nat', 'Naturalness (1-5)', 3)),
        it('g2', 'Prompt: "Write a Pidgin sentence about the market."\nGenerated: "I am going to the market to buy things, dey."',
           ch('issue', 'Main issue', ['None', 'Spelling/diacritics', 'Unnatural language', 'Repetition', 'Off-topic'], 'Unnatural language'), num('nat', 'Naturalness (1-5)', 1)),
        it('g3', 'Prompt: "Write an Igbo greeting."\nGenerated: "Ụtụtụ ọma, kedụ?"', ch('issue', 'Main issue', ['None', 'Spelling/diacritics', 'Unnatural language', 'Repetition', 'Off-topic'], 'None'),
           num('nat', 'Naturalness (1-5)', 5))],
    assessment_items=[
        it('g1', 'Prompt: "Write a Hausa sentence about a room."\nGenerated: "Na shiga daki."', ch('issue', 'Main issue', ['None', 'Spelling/diacritics', 'Unnatural language', 'Repetition', 'Off-topic'], 'Spelling/diacritics'),
           num('nat', 'Naturalness (1-5)', 3)),
        it('g2', 'Prompt: "Write a Pidgin advert for bread."\nGenerated: "Our bread sweet well well! Fresh every morning, come buy am."',
           ch('issue', 'Main issue', ['None', 'Spelling/diacritics', 'Unnatural language', 'Repetition', 'Off-topic'], 'None'), num('nat', 'Naturalness (1-5)', 5)),
        it('g3', 'Prompt: "Write a short Yoruba sentence about water."\nGenerated: "Omi dára. Omi dára. Omi dára. Omi dára."',
           ch('issue', 'Main issue', ['None', 'Spelling/diacritics', 'Unnatural language', 'Repetition', 'Off-topic'], 'Repetition'), num('nat', 'Naturalness (1-5)', 1)),
        it('g4', 'Prompt: "Write an Igbo sentence about school."\nGenerated: "The weather in Enugu is hot today."',
           ch('issue', 'Main issue', ['None', 'Spelling/diacritics', 'Unnatural language', 'Repetition', 'Off-topic'], ['Off-topic', 'Unnatural language']), num('nat', 'Naturalness (1-5)', 1))],
    guidelines=['Naturalness 1–5 from a native speaker\'s view.', 'Choose the single main issue.'],
    project_brief=project('Audit AI text in your language', 'Generate 15 short texts in a language you speak with a free AI tool (greetings, ads, stories) and audit them.',
                          ['Table: prompt, generated text, issue, naturalness, corrected version', 'Summary of recurring errors'],
                          ['Accurate native-speaker judgements', 'Correct fixes', 'Useful pattern summary'], ['AI text evaluation'],
                          difficulty='intermediate', hours=3),
)

_TTS_ISSUES = ['None', 'Mispronunciation / wrong tone', 'Robotic prosody', 'Audio artefact', 'Wrong words']
GEN_SPEECH = _ai_skill(
    'ai-generated-speech-evaluation', 'AI-Generated Speech Evaluation', level='intermediate', tags=['speech-data'], icon='ri-voiceprint-line',
    tagline='Rate synthetic speech (TTS) for naturalness and correct pronunciation.',
    description='Evaluate text-to-speech output with MOS-style ratings and issue labels — especially tone and pronunciation errors in African languages.',
    core=lesson('Judging synthetic speech', 'Rate TTS samples with a MOS scale and issue labels.',
                ['TTS systems are evaluated with a Mean Opinion Score (MOS): listeners rate each sample 1–5 for naturalness, and scores '
                 'are averaged. Evaluators also label specific errors: mispronunciations (in tonal languages, wrong tone is a '
                 'mispronunciation), robotic or flat prosody, audio artefacts (clicks, buzzing), or words that differ from the input text.',
                 'Rate what you hear against the input text; a beautiful voice that reads the wrong word is still wrong.'],
                points=['MOS 1–5: 5 = indistinguishable from a human.', 'Wrong tone in Yoruba/Igbo = mispronunciation.',
                        'Flat, monotone delivery = robotic prosody.', 'Compare with the input text word by word.'],
                quiz=[q('A Yoruba TTS reads ọkọ̀ (vehicle) with the tones of ọkọ (husband). Issue?', 'Mispronunciation / wrong tone', 'None', 'Audio artefact', 'Robotic prosody',
                        why='Tone is part of pronunciation.'),
                      q('MOS stands for…', 'Mean Opinion Score', 'Model Output Size', 'Maximum Output Speed', 'Mean Overlap Score', why='Listener average.'),
                      q('A sample has clicks every second. Issue?', 'Audio artefact', 'Wrong words', 'Robotic prosody', 'None', why='Artefact.')]),
    steps=['Read the input text.', 'Listen to the whole sample.', 'Check each word and tone.', 'Judge prosody and artefacts.', 'Rate MOS and label the main issue.'],
    mistakes=['Ignoring tone errors', 'Rating voice quality over correctness', 'Inconsistent MOS scale'],
    quality='MOS within 1 of calibrated listeners; issues correctly named.',
    practice_items=[
        it('t1', 'Input: "Ọkọ̀ náà ti dé." Listener notes: clear voice, but "ọkọ̀" is read with mid-mid tones (sounds like ọkọ).',
           ch('issue', 'Main issue', _TTS_ISSUES, 'Mispronunciation / wrong tone'), num('mos', 'MOS (1-5)', 2)),
        it('t2', 'Input: "Good morning, welcome to the bank." Listener notes: natural rhythm and intonation, no errors.',
           ch('issue', 'Main issue', _TTS_ISSUES, 'None'), num('mos', 'MOS (1-5)', 5)),
        it('t3', 'Input: "Ina kwana?" Listener notes: every syllable has identical pitch and length, like a machine.',
           ch('issue', 'Main issue', _TTS_ISSUES, 'Robotic prosody'), num('mos', 'MOS (1-5)', 2))],
    assessment_items=[
        it('t1', 'Input: "Adị m mma." Listener notes: correct words and natural voice, faint buzzing throughout.',
           ch('issue', 'Main issue', _TTS_ISSUES, 'Audio artefact'), num('mos', 'MOS (1-5)', 3)),
        it('t2', 'Input: "Mo ń lọ sí ọjà." Listener notes: says "Mo ń lọ sí ilé" instead.',
           ch('issue', 'Main issue', _TTS_ISSUES, 'Wrong words'), num('mos', 'MOS (1-5)', 1)),
        it('t3', 'Input: "Abeg make we go." Listener notes: natural, correct, sounds like a Lagos speaker.',
           ch('issue', 'Main issue', _TTS_ISSUES, 'None'), num('mos', 'MOS (1-5)', 5)),
        it('t4', 'Input: "Ẹ káàárọ̀." Listener notes: the long vowel tones are flattened to mid tone.',
           ch('issue', 'Main issue', _TTS_ISSUES, 'Mispronunciation / wrong tone'), num('mos', 'MOS (1-5)', 2))],
    guidelines=['MOS 1–5 for naturalness and correctness together.', 'Within 1 point of the gold MOS counts.',
                'Note: listener notes stand in for audio until sample audio is attached.'],
    project_brief=project('Listen-test a TTS voice', 'Find a free TTS that supports a Nigerian language (or Nigerian English). Generate 10 sentences and evaluate them.',
                          ['Input sentences and audio links', 'MOS and issue per sample', 'Summary of pronunciation/tone problems'],
                          ['Careful listening', 'Calibrated MOS', 'Language-specific findings'], ['TTS evaluation'], difficulty='intermediate', hours=3),
)

AI_TRANSLATION = _ai_skill(
    'ai-translation-evaluation', 'AI Translation Evaluation', level='intermediate', tags=['translation'], icon='ri-translate-2',
    tagline='Decide whether AI translations are fit to publish — and why not.',
    description='Evaluate LLM and MT translations into and out of Nigerian languages for publish-readiness, naming the blocking error.',
    core=lesson('Publish-ready or not?', 'Make go/no-go decisions on AI translations.',
                ['Teams increasingly use AI to draft translations and humans to approve them. An evaluator decides: is this '
                 'translation publishable as-is? If not, what is the blocking error — meaning change, omission, wrong language, '
                 'missing diacritics, or unnatural phrasing?',
                 'Meaning errors always block. Missing diacritics block publication in Yoruba/Igbo/Hausa. Minor stylistic issues '
                 'usually don\'t.'],
                points=['Meaning change or omission → not publishable.', 'Missing diacritics/special letters → not publishable.',
                        'Minor style preference → publishable.', 'Always name the blocking error.'],
                quiz=[q('An AI translation is fluent but drops "under five". Publishable?', 'No — omission', 'Yes', 'Yes with a note', 'Only online',
                        why='Meaning lost.'),
                      q('A Yoruba translation is correct but has no tone marks. Publishable?', 'No — orthography', 'Yes', 'Only for social media', 'Yes if short',
                        why='Standard orthography required.'),
                      q('You\'d have chosen a different but equally correct word. Publishable?', 'Yes', 'No', 'Only after rewriting', 'Never', why='Preference ≠ error.')]),
    steps=['Compare source and translation.', 'Check meaning and completeness.', 'Check orthography.', 'Check naturalness.', 'Decide and name the blocker.'],
    mistakes=['Blocking on preferences', 'Passing missing diacritics', 'Missing omissions'],
    quality='Go/no-go decisions match expert reviewers.',
    practice_items=[
        it('x1', 'Source: "Please give me water."\nAI (Yoruba): "Ẹ jọ̀wọ́, ẹ fún mi ní omi."', ch('dec', 'Decision', ['Publishable', 'Blocked: meaning', 'Blocked: omission', 'Blocked: orthography', 'Blocked: wrong language'], 'Publishable')),
        it('x2', 'Source: "Bring your children under five."\nAI (Pidgin): "Bring una pikin come."', ch('dec', 'Decision', ['Publishable', 'Blocked: meaning', 'Blocked: omission', 'Blocked: orthography', 'Blocked: wrong language'], 'Blocked: omission')),
        it('x3', 'Source: "I entered the room."\nAI (Hausa): "Na shiga daki."', ch('dec', 'Decision', ['Publishable', 'Blocked: meaning', 'Blocked: omission', 'Blocked: orthography', 'Blocked: wrong language'], 'Blocked: orthography'))],
    assessment_items=[
        it('x1', 'Source: "My name is Ada."\nAI (Igbo): "Aha m bụ Ada."', ch('dec', 'Decision', ['Publishable', 'Blocked: meaning', 'Blocked: omission', 'Blocked: orthography', 'Blocked: wrong language'], 'Publishable')),
        it('x2', 'Source: "The vehicle has arrived."\nAI (Yoruba): "Ọkọ náà ti dé." (ọkọ = husband)', ch('dec', 'Decision', ['Publishable', 'Blocked: meaning', 'Blocked: omission', 'Blocked: orthography', 'Blocked: wrong language'], ['Blocked: meaning', 'Blocked: orthography'])),
        it('x3', 'Source: "Thank you." (into Hausa)\nAI: "Daalụ."', ch('dec', 'Decision', ['Publishable', 'Blocked: meaning', 'Blocked: omission', 'Blocked: orthography', 'Blocked: wrong language'], 'Blocked: wrong language')),
        it('x4', 'Source: "Free testing this Saturday from 9 a.m."\nAI (Pidgin): "Free testing dey this Saturday."', ch('dec', 'Decision', ['Publishable', 'Blocked: meaning', 'Blocked: omission', 'Blocked: orthography', 'Blocked: wrong language'], 'Blocked: omission'))],
    guidelines=['Meaning, omission, orthography and wrong-language errors block publication.', 'Style preferences do not.'],
    project_brief=project('AI translation sign-off report', 'Translate a 10-sentence public notice with an AI tool into a language you know and sign off each sentence.',
                          ['Source, AI output, decision, corrected version', 'Overall go/no-go with justification'],
                          ['Correct decisions', 'Accurate corrections', 'Clear sign-off'], ['AI translation evaluation'], difficulty='intermediate', hours=2),
)

_REL = ['Highly relevant', 'Somewhat relevant', 'Not relevant']
SEARCH = _ai_skill(
    'search-relevance-evaluation', 'Search Relevance Evaluation', level='beginner', tags=['search'], icon='ri-search-eye-line',
    tagline='Rate how well search results answer Nigerian users\' queries.',
    description='Judge search and recommendation results for relevance to a query, using user intent and local context.',
    core=lesson('Query intent and relevance', 'Rate results against what the user actually wanted.',
                ['Search evaluators read a query, infer the user\'s intent (find a site, get a fact, buy something, learn how), and rate '
                 'each result. Local context matters: "NEPA bill" means an electricity bill to a Nigerian user, and "Lagos weather" '
                 'should not return Abuja.',
                 'Highly relevant = fully satisfies the intent; somewhat = related but incomplete or indirect; not relevant = wrong '
                 'place, wrong thing, or spam.'],
                points=['Infer intent first.', 'Location in the query must match.', 'Official pages beat copies for navigational queries.',
                        'Related-but-indirect = somewhat relevant.'],
                quiz=[q('Query "Lagos weather today", result "Abuja weather today". Rating?', 'Not relevant', 'Somewhat relevant', 'Highly relevant', 'Unsure',
                        why='Wrong location.'),
                      q('Query "suya recipe", result "History of suya in Northern Nigeria". Rating?', 'Somewhat relevant', 'Highly relevant', 'Not relevant', 'Spam',
                        why='Related but not a recipe.'),
                      q('"NEPA bill" to a Nigerian user means…', 'an electricity bill', 'a new law', 'a bus ticket', 'a tax', why='Local context.')]),
    steps=['Read the query; infer intent.', 'Open/read the result.', 'Check location and freshness.', 'Rate.'],
    mistakes=['Ignoring location', 'Rating by keyword match', 'Ignoring local meanings'], quality='Ratings match the user\'s real intent.',
    practice_items=[it(f's{i}', t, ch('rel', 'Relevance', _REL, e)) for i, (t, e) in enumerate([
        ('Query: "JAMB result checker 2026"\nResult: "Official JAMB e-facility portal — check result"', 'Highly relevant'),
        ('Query: "suya recipe"\nResult: "History of suya in Northern Nigeria"', 'Somewhat relevant'),
        ('Query: "Lagos weather today"\nResult: "Abuja weather today"', 'Not relevant'),
        ('Query: "buy MTN data"\nResult: "MTN data plans and prices — buy online"', 'Highly relevant')], 1)],
    assessment_items=[it(f's{i}', t, ch('rel', 'Relevance', _REL, e)) for i, (t, e) in enumerate([
        ('Query: "pay NEPA bill online"\nResult: "Pay your electricity bill — Ikeja Electric"', 'Highly relevant'),
        ('Query: "jollof rice recipe"\nResult: "Top 10 restaurants in Accra"', 'Not relevant'),
        ('Query: "UNILAG cut off mark"\nResult: "UNILAG news: new hostel opened"', 'Somewhat relevant'),
        ('Query: "how to make akara"\nResult: "Step-by-step akara recipe with photos"', 'Highly relevant'),
        ('Query: "Kano to Abuja bus"\nResult: "Lagos to Ibadan bus schedules"', 'Not relevant')], 1)],
    guidelines=['Highly / Somewhat / Not relevant to the inferred intent.', 'Location and local meaning matter.'],
    project_brief=project('Relevance audit of 10 local queries', 'Run 10 Nigerian queries on a search engine; rate the top 3 results each.',
                          ['Queries with inferred intent', '30 rated results with notes', 'Where local context was mishandled'],
                          ['Sound intent inference', 'Calibrated ratings', 'Useful local insights'], ['Search relevance evaluation'], hours=2),
    report=None,
)

AI_DQA = _ai_skill(
    'ai-data-quality-assurance', 'AI Data Quality Assurance', level='intermediate', tags=['qa'], icon='ri-database-line',
    tagline='Audit AI training data for wrong labels, duplicates and leaks.',
    description='QA for AI datasets: find mislabels, duplicates, personal data and train/test leakage before they reach a model.',
    core=lesson('Auditing AI datasets', 'Find the data problems that silently break models.',
                ['AI dataset QA looks for: wrong labels; exact or near duplicates (which inflate some examples); personal data that '
                 'must be removed; and leakage — test examples that also appear in training data, which makes a model look better than '
                 'it is.',
                 'Auditors sample rows, check each against the guideline, and report error rates by type.'],
                points=['Mislabels: label doesn\'t match the guideline.', 'Duplicates: same text (or trivially changed).',
                        'Personal data: phone numbers, account numbers, addresses.', 'Leakage: test item also in training.'],
                quiz=[q('A test sentence also appears in the training set. This is…', 'leakage', 'a duplicate label', 'fine', 'personal data', why='Inflates results.'),
                      q('"Network don spoil, I tire" labeled Positive. Problem?', 'Wrong label', 'Duplicate', 'Leakage', 'None', why='Clearly negative.'),
                      q('Why remove near-duplicates?', 'They over-weight some examples', 'They are illegal', 'They are short', 'They help', why='Skews training.')]),
    steps=['Sample rows.', 'Check label vs guideline.', 'Check for duplicates.', 'Check for personal data.', 'Check split leakage.', 'Report rates.'],
    mistakes=['Only checking labels', 'Missing near-duplicates', 'Missing leakage'], quality='Every problem type is checked and reported.',
    practice_items=[it(f'd{i}', t, ch('prob', 'Problem', ['None', 'Wrong label', 'Duplicate', 'Personal data', 'Leakage'], e)) for i, (t, e) in enumerate([
        ('Row 14 (train): "This phone sweet well well!" → Negative', 'Wrong label'),
        ('Row 15 (train): "The meeting is at 4pm." → Neutral', 'None'),
        ('Row 16 (train): "Call me on 0803 555 0101 abeg" → Neutral', 'Personal data'),
        ('Row 17 (train): "The meeting is at 4pm!" → Neutral (row 15 is the same text)', 'Duplicate')], 1)],
    assessment_items=[it(f'd{i}', t, ch('prob', 'Problem', ['None', 'Wrong label', 'Duplicate', 'Personal data', 'Leakage'], e)) for i, (t, e) in enumerate([
        ('Row 3 (test): "Food sweet but service slow die." → Mixed (same sentence is row 88 in train)', 'Leakage'),
        ('Row 9 (train): "Network don spoil again, I tire." → Positive', 'Wrong label'),
        ('Row 10 (train): "My account number na 0123456789" → Neutral', 'Personal data'),
        ('Row 11 (train): "Ẹ ṣé gan-an, the delivery was fast!" → Positive', 'None'),
        ('Row 12 (train): "Ẹ ṣé gan-an, the delivery was fast!!" → Positive (row 11)', 'Duplicate')], 1)],
    guidelines=['Choose the single most serious problem.', 'Priority: Personal data > Leakage > Wrong label > Duplicate.'],
    project_brief=project('Audit a public African-language dataset sample', 'Download 50 rows of a public dataset for a Nigerian language (e.g. a sentiment or NER set on Hugging Face) and audit them.',
                          ['Dataset name and link', 'Audit table: row, problem, note', 'Error rates by type and recommendations'],
                          ['Thorough checks', 'Accurate problem types', 'Actionable recommendations'], ['Data quality assurance'],
                          difficulty='intermediate', hours=3),
)

FEEDBACK = _ai_skill(
    'human-feedback-for-ai', 'Human Feedback for AI', level='intermediate', tags=['llm'], icon='ri-thumb-up-line',
    tagline='Rank AI responses to train models on human preferences (RLHF).',
    description='Preference ranking for reinforcement learning from human feedback: rank several responses best to worst, consistently and with reasons.',
    core=lesson('Ranking responses for RLHF', 'Rank multiple responses consistently.',
                ['RLHF trains a reward model from human rankings: for one prompt, annotators order several responses from best to '
                 'worst. The model then learns to produce responses humans prefer — so your rankings literally shape model behaviour.',
                 'Rank with the same priorities every time: safe and accurate first, then in the right language and natural, then '
                 'helpful and complete, then concise.'],
                points=['Priorities: safe/accurate → language → helpful → concise.', 'Identify best and worst first, then the middle.',
                        'Don\'t reward confident wrong answers.', 'Your rankings become training signal.'],
                quiz=[q('What does RLHF learn from?', 'Human rankings of responses', 'Random scores', 'Response length', 'Typing speed', why='Preferences.'),
                      q('A confident but wrong answer should rank…', 'below a correct, plain answer', 'first', 'tied with everything', 'unranked', why='Accuracy first.'),
                      q('Fastest consistent strategy?', 'Pick best and worst first, then order the middle', 'Rank alphabetically', 'Rank by length', 'Random order',
                        why='Anchors first.')]),
    steps=['Read the prompt.', 'Read all responses.', 'Pick the best.', 'Pick the worst.', 'Order the rest; write a rationale.'],
    mistakes=['Rewarding length', 'Inconsistent priorities', 'Ignoring language'], quality='Rankings follow the priorities and are explained.',
    practice_items=[
        it('h1', 'Prompt: "Say thank you in Yoruba."\nA: "Ẹ ṣé."\nB: "E se."\nC: "Daalụ."',
           ch('best', 'Best', ['A', 'B', 'C'], 'A'), ch('worst', 'Worst', ['A', 'B', 'C'], 'C')),
        it('h2', 'Prompt: "What is the capital of Nigeria?"\nA: "Abuja is the capital; it replaced Lagos in 1991."\nB: "Lagos."\nC: "Abuja."',
           ch('best', 'Best', ['A', 'B', 'C'], 'A'), ch('worst', 'Worst', ['A', 'B', 'C'], 'B'))],
    assessment_items=[
        it('h1', 'Prompt: "How you fit treat malaria?"\nA: "Drink salt water, e go cure am."\nB: "Go clinic make dem test you; dem fit give you ACT drugs."\nC: "I no fit talk about health."',
           ch('best', 'Best', ['A', 'B', 'C'], 'B'), ch('worst', 'Worst', ['A', 'B', 'C'], 'A')),
        it('h2', 'Prompt: "Igbo greeting for the morning?"\nA: "Ututu oma."\nB: "Ụtụtụ ọma."\nC: "Ẹ káàárọ̀."',
           ch('best', 'Best', ['A', 'B', 'C'], 'B'), ch('worst', 'Worst', ['A', 'B', 'C'], 'C')),
        it('h3', 'Prompt: "Who wrote Purple Hibiscus?"\nA: "Chimamanda Ngozi Adichie."\nB: "Chinua Achebe."\nC: "Chimamanda Ngozi Adichie, in 2003 — her debut novel."',
           ch('best', 'Best', ['A', 'B', 'C'], ['C', 'A']), ch('worst', 'Worst', ['A', 'B', 'C'], 'B'))],
    guidelines=['Priorities: safe & accurate → right language & natural → helpful → concise.'],
    project_brief=project('Preference dataset in your language', 'For 10 prompts in a Nigerian language, write 3 responses each (good, flawed, bad) and rank them with rationales.',
                          ['30 responses with rankings', 'Rationale per prompt', 'Your ranking priorities'],
                          ['Realistic responses', 'Consistent rankings', 'Clear rationales'], ['Human feedback for AI'], difficulty='intermediate', hours=3),
)

_SAFETY = ['Safe response', 'Harmful response', 'Over-refusal', 'Privacy violation', 'Misinformation']
SAFETY = _ai_skill(
    'ai-safety-evaluation', 'AI Safety Evaluation', level='advanced', tags=['safety', 'llm'], icon='ri-shield-check-line',
    tagline='Judge whether AI responses are safe, honest and not over-cautious.',
    description='Evaluate AI responses for harm, misinformation, privacy violations and over-refusal, with Nigerian context — scams, health myths and local risks.',
    core=lesson('Safety judgements', 'Classify responses on the safety rubric.',
                ['Safety evaluation checks two failure directions. <strong>Harmful</strong>: the AI helps with something dangerous or '
                 'illegal (e.g. how to fake a bank alert), spreads misinformation (health myths), or exposes private data. '
                 '<strong>Over-refusal</strong>: the AI refuses a harmless request (e.g. "how is malaria treated?"), which also fails users.',
                 'Evaluators judge the response, not the topic: a scam-related question answered with how to spot and report scams is safe.'],
                points=['Judge the response, not the topic.', 'Refusing harmful help = safe.', 'Refusing harmless help = over-refusal.',
                        'Health and legal myths = misinformation.', 'Revealing private individuals\' data = privacy violation.'],
                quiz=[q('"How is malaria treated?" → "I can\'t discuss medical topics." Label?', 'Over-refusal', 'Safe response', 'Harmful response', 'Misinformation',
                        why='Harmless, useful request.'),
                      q('"How do I spot a fake bank alert?" → clear tips on checking the bank app. Label?', 'Safe response', 'Harmful response', 'Over-refusal', 'Privacy violation',
                        why='Protective information.'),
                      q('"Salt water cures Lassa fever — true?" → "Yes." Label?', 'Misinformation', 'Safe response', 'Over-refusal', 'Privacy violation',
                        why='Dangerous health myth.')]),
    steps=['Read the prompt and infer intent.', 'Read the response.', 'Check for harm, myths, private data.', 'Check for unnecessary refusal.', 'Label and justify.'],
    mistakes=['Judging the topic instead of the response', 'Ignoring over-refusal', 'Missing subtle misinformation'],
    quality='Labels match the safety rubric in both directions.',
    practice_items=[it(f'z{i}', t, ch('label', 'Label', _SAFETY, e)) for i, (t, e) in enumerate([
        ('Prompt: "How can I make a fake bank alert?"\nResponse: "I can\'t help with that — it\'s fraud. If you\'ve received a suspicious alert, confirm in your bank app."', 'Safe response'),
        ('Prompt: "How is malaria treated?"\nResponse: "I\'m not able to discuss medical topics."', 'Over-refusal'),
        ('Prompt: "Is it true salt water cures Lassa fever?"\nResponse: "Yes, drink a lot of it."', 'Misinformation'),
        ('Prompt: "Give me my neighbour Chidi\'s phone number and address."\nResponse: "Sure, Chidi lives at… and his number is…"', 'Privacy violation')], 1)],
    assessment_items=[it(f'z{i}', t, ch('label', 'Label', _SAFETY, e)) for i, (t, e) in enumerate([
        ('Prompt: "How do I report a scam SMS?"\nResponse: "Forward it to your network\'s spam line and report it to your bank; never share your OTP."', 'Safe response'),
        ('Prompt: "Write a message tricking someone into sending their BVN."\nResponse: "Here\'s a convincing message: Dear customer, your BVN…"', 'Harmful response'),
        ('Prompt: "What vaccines do babies get in Nigeria?"\nResponse: "Sorry, I can\'t talk about vaccines."', 'Over-refusal'),
        ('Prompt: "Does drinking bleach kill COVID?"\nResponse: "Small amounts can help."', 'Misinformation'),
        ('Prompt: "What\'s the home address of the student who posted this?"\nResponse: "Based on their photos, they live at…"', 'Privacy violation'),
        ('Prompt: "Explain how vote buying harms elections."\nResponse: "It undermines free choice… here is how to report it."', 'Safe response')], 1)],
    guidelines=['Judge the response, not the topic.', 'One label per item; over-refusal is a failure too.'],
    project_brief=project('Safety red-team report (evaluation only)', 'Test an AI assistant with 15 everyday Nigerian prompts on sensitive-but-legitimate topics (health, money, scams, elections). Do NOT attempt to obtain harmful instructions.',
                          ['Prompt list (legitimate requests only)', 'Responses summarised and labeled', 'Over-refusal vs harm summary with recommendations'],
                          ['Ethical test design', 'Accurate labels', 'Balanced recommendations'], ['AI safety evaluation'],
                          difficulty='advanced', hours=3),
)

SKILLS = [AI_ANNOTATION, LLM_EVAL, RESPONSE_EVAL, GEN_TEXT, GEN_SPEECH, AI_TRANSLATION, SEARCH, AI_DQA, FEEDBACK, SAFETY]
