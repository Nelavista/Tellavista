"""Quality Assurance category — reviewing other people's work: finding errors, applying
quality standards, scoring consistently, adjudicating disagreements and measuring
agreement. Every assessment uses gold QA judgements; several require a QA report.
"""
from ._common import q, lesson, workflow_lesson, task, labeling, choice_items, number_item, project, skill

COLOR = '#16a34a'

FOUNDATION = lesson(
    'What a QA reviewer does',
    'Understand the reviewer\'s role and standards.',
    [
        'On language-data projects, QA reviewers check other contributors\' transcripts, translations, labels and recordings against '
        'the guideline. They find and categorise errors, score the work, decide pass/fail, and give feedback that helps the contributor '
        'improve. Reviewers are usually the most trusted — and best-paid — people on a project.',
        'Good QA is <strong>consistent</strong> (same error, same decision, every time), <strong>evidence-based</strong> (every error points '
        'to a guideline rule), and <strong>constructive</strong> (feedback is specific and actionable, never personal).',
    ],
    points=['Review against the guideline, not personal preference.', 'Categorise every error and cite the rule.',
            'Score with the project\'s formula.', 'Feedback: specific, actionable, respectful.'],
    quiz=[
        q('You prefer a different but equally correct word in a translation. As QA you…', 'don\'t mark it as an error', 'mark it as major',
          'fail the file', 'rewrite it silently', why='Preference ≠ error.'),
        q('Which is good QA feedback?', '"Segment 4: [laughter] should be [noise] per guideline 3.2."', '"Bad work."', '"Be more careful."', '"Redo everything."',
          why='Specific, cites the rule.'),
        q('Consistency in QA means…', 'the same error gets the same decision every time', 'reviewing fast', 'always passing files', 'always failing files',
          why='Fairness and reliability.'),
    ],
)


def _qa_skill(slug, name, *, level, icon, tagline, description, core, steps, mistakes, quality, practice_items,
              assessment_items, guidelines, project_brief, tags=None, report=None, hours=5):
    return skill(
        slug, name, level=level, tags=['qa'] + (tags or []), icon=icon, color=COLOR, tagline=tagline, description=description,
        foundation=FOUNDATION, core=core, workflow=workflow_lesson(name, steps, mistakes, quality),
        practice=task(f'{name}: review practice', 'Review each item against the guideline.', labeling(practice_items, guidelines), minutes=15),
        assessment=task(f'{name} assessment', 'Scored review with a QA report.',
                        labeling(assessment_items, guidelines, report=report, ai_feedback=bool(report)), minutes=20),
        project_brief=project_brief, hours=hours,
    )


QA_REPORT = {'label': 'QA report: summarise the main problems and your pass/fail decision', 'min_words': 25}

DATA_QA = _qa_skill(
    'data-quality-assurance', 'Data Quality Assurance', level='intermediate', icon='ri-shield-star-line', tags=['dataset'],
    tagline='Run QA on whole language datasets with sampling and error rates.',
    description='Plan and run dataset-level QA: sampling, error categories, error rates, acceptance thresholds and QA reports.',
    core=lesson('Sampling and acceptance', 'Run QA on a sample and decide acceptance.',
                ['Large batches are rarely reviewed in full. QA reviews a <strong>random sample</strong> (e.g. 10% or a fixed number), records '
                 'errors by category, computes an error rate, and compares it with an <strong>acceptance threshold</strong> (e.g. ≤ 5% items with '
                 'errors). Batches above the threshold are returned for rework.',
                 'Sampling must be random — reviewing only the first rows, or only one annotator\'s rows, gives a biased estimate.'],
                points=['Random sample, not the first rows.', 'Error rate = items with errors ÷ items sampled.', 'Compare with the acceptance threshold.',
                        'Report by category so rework is targeted.'],
                quiz=[q('Sample 200 items, 12 have errors. Error rate?', '6%', '12%', '2%', '0.6%', why='12/200.'),
                      q('Threshold ≤ 5%, observed 6%. Decision?', 'Return for rework', 'Accept', 'Accept with praise', 'Delete', why='Above threshold.'),
                      q('Why random sampling?', 'To get an unbiased estimate of quality', 'It is faster', 'It looks fair', 'No reason', why='Representativeness.')]),
    steps=['Agree categories and threshold.', 'Draw a random sample.', 'Review each sampled item.', 'Compute rates.', 'Decide and report.'],
    mistakes=['Non-random samples', 'No categories', 'Ignoring the threshold'], quality='Decisions follow from a random sample and a stated threshold.',
    practice_items=[number_item('p1', 'Sample 200 items; 12 have errors.', 'Error rate (%)', 6, 0.1),
                    number_item('p2', 'Batch of 5,000 items; 10% sample.', 'Sample size', 500),
                    *choice_items('d', 'Decision', ['Accept', 'Return for rework'], [('Threshold ≤ 5%; observed 3.5%.', 'Accept')])],
    assessment_items=[number_item('a1', 'Sample 300 items; 21 have errors.', 'Error rate (%)', 7, 0.1),
                      *choice_items('d', 'Decision', ['Accept', 'Return for rework'], [('Threshold ≤ 5%; observed 7%.', 'Return for rework'),
                                                                                       ('Threshold ≤ 8%; observed 7%.', 'Accept')]),
                      *choice_items('s', 'Valid sampling?', ['Valid', 'Not valid'], [('Reviewing only the first 100 rows of the file.', 'Not valid'),
                                                                                    ('Randomly selecting 100 rows across all annotators.', 'Valid')])],
    guidelines=['Use the formulas from the lesson.'],
    report=QA_REPORT,
    project_brief=project('Sample-based QA of a dataset', 'Take a public African-language dataset, randomly sample 100 rows, and QA them.',
                          ['Dataset and sampling method', 'Error log by category', 'Error rate and accept/rework decision', 'QA report'],
                          ['Random sampling', 'Accurate categories', 'Clear report'], ['Data quality assurance'], difficulty='intermediate', hours=4),
)

_TQA = ['No error', 'Substitution', 'Omission', 'Insertion', 'Missing diacritics', 'Wrong tag']
TRANSCRIPTION_QA = _qa_skill(
    'transcription-qa', 'Transcription QA', level='intermediate', icon='ri-file-search-line', tags=['transcription'],
    tagline='Review transcripts, categorise errors and compute WER.',
    description='QA other transcribers\' work: substitutions, omissions, insertions, diacritic errors and tag misuse, with WER-based scoring.',
    core=lesson('Reviewing a transcript', 'Find and categorise transcription errors.',
                ['A transcription reviewer compares a transcript with the audio (or a gold reference) and logs each error: '
                 '<strong>substitution</strong> (wrong word), <strong>omission</strong> (missing word), <strong>insertion</strong> (extra word), '
                 '<strong>diacritic</strong> errors (missing tone marks or under-dots), and <strong>tag</strong> errors (wrong or invented tags).',
                 'WER counts substitutions, omissions and insertions; diacritic and tag errors are often tracked separately because projects '
                 'weight them differently.'],
                points=['Substitution / omission / insertion → WER.', 'Diacritic and tag errors tracked separately.',
                        'Every error cites the guideline.', 'Score with the project formula.'],
                quiz=[q('Reference "Mo ń lọ sí ọjà", transcript "Mo lọ sí ọjà". Error?', 'Omission', 'Substitution', 'Insertion', 'Wrong tag', why='"ń" missing.'),
                      q('Transcript writes "oja" for "ọjà". Error?', 'Missing diacritics', 'Omission', 'Insertion', 'No error', why='Marks missing.'),
                      q('Reference 10 words; 1 substitution + 1 insertion. WER?', '0.2', '0.1', '0.11', '2', why='2/10.')]),
    steps=['Read the guideline.', 'Compare segment by segment.', 'Log each error with category.', 'Compute WER and other counts.', 'Write feedback.'],
    mistakes=['Counting diacritic errors twice', 'Missing insertions', 'Unspecific feedback'], quality='Error logs are complete and categories consistent.',
    practice_items=choice_items('e', 'Main error', _TQA, [
        ('Reference: "Mo ń lọ sí ọjà." Transcript: "Mo lọ sí ọjà."', 'Omission'),
        ('Reference: "Ẹ káàárọ̀." Transcript: "E kaaaro."', 'Missing diacritics'),
        ('Reference: "How you dey?" Transcript: "How you dey?"', 'No error'),
        ('Reference: "I dey come." Transcript: "I dey come now."', 'Insertion')]),
    assessment_items=[*choice_items('e', 'Main error', _TQA, [
        ('Reference: "Abeg make we go market." Transcript: "Abeg make we go school."', 'Substitution'),
        ('Reference: "Na shiga ɗaki." Transcript: "Na shiga daki."', 'Missing diacritics'),
        ('Reference: "[laughter] I don tire" Transcript: "[giggles] I don tire" (allowed tags: [laughter], [noise], [inaudible])', 'Wrong tag'),
        ('Reference: "Ụtụtụ ọma, kedụ?" Transcript: "Ụtụtụ ọma."', 'Omission')]),
        number_item('w1', 'Reference 20 words; 2 substitutions, 1 omission, 1 insertion.', 'WER (decimal)', 0.2, 0.001)],
    guidelines=['Choose the main error for each segment.', 'Allowed tags: [laughter], [noise], [inaudible], [crosstalk].'],
    report=QA_REPORT,
    project_brief=project('QA a classmate\'s transcript', 'Swap transcripts with a classmate (from the transcription skills) and QA theirs against the audio.',
                          ['Their transcript (with permission)', 'Error log', 'WER and diacritic error counts', 'Constructive feedback'],
                          ['Accurate error log', 'Correct WER', 'Helpful feedback'], ['Transcription QA'], difficulty='intermediate', hours=3),
)

TRANSLATION_QA = _qa_skill(
    'translation-qa', 'Translation QA', level='intermediate', icon='ri-file-check-line', tags=['translation'],
    tagline='Score translations with weighted error penalties and pass/fail rules.',
    description='Quantitative translation QA: weighted penalties per error severity, normalised per 100 words, compared against pass thresholds.',
    core=lesson('Weighted error scoring', 'Compute a translation quality score.',
                ['Translation QA often uses weighted penalties: e.g. minor = 1, major = 5, critical = 10 points. The penalty total is normalised '
                 'per 100 words: (sum of penalties ÷ word count) × 100. A file passes if the normalised penalty is under the threshold, and '
                 'any critical error may fail it automatically.',
                 'Reviewers must apply severities consistently and document each error so the translator can dispute it if needed.'],
                points=['Minor 1 · Major 5 · Critical 10 (typical).', 'Normalised penalty = penalties ÷ words × 100.',
                        'Critical error may auto-fail.', 'Document every error.'],
                quiz=[q('3 minor + 1 major in 250 words. Normalised penalty per 100 words?', '3.2', '8', '0.32', '32', why='(3+5)/250×100.'),
                      q('Threshold 5; file scores 3.2 with no critical errors. Decision?', 'Pass', 'Fail', 'Rework', 'Unsure', why='Under threshold.'),
                      q('One critical error (wrong dosage) in an otherwise clean file. Typical decision?', 'Fail', 'Pass', 'Pass with note', 'Ignore', why='Auto-fail.')]),
    steps=['Log errors with severity.', 'Sum weighted penalties.', 'Normalise per 100 words.', 'Apply threshold and critical rule.', 'Report.'],
    mistakes=['Wrong normalisation', 'Inconsistent severity', 'Passing files with critical errors'], quality='Scores are reproducible from the error log.',
    practice_items=[number_item('p1', '3 minor + 1 major in 250 words.', 'Penalty per 100 words', 3.2, 0.05),
                    number_item('p2', '2 major in 500 words.', 'Penalty per 100 words', 2, 0.05),
                    *choice_items('d', 'Decision', ['Pass', 'Fail'], [('Threshold 5; penalty 3.2; no critical errors.', 'Pass')])],
    assessment_items=[number_item('a1', '4 minor + 2 major in 400 words.', 'Penalty per 100 words', 3.5, 0.05),
                      number_item('a2', '1 critical + 1 minor in 220 words.', 'Penalty per 100 words', 5, 0.05),
                      *choice_items('d', 'Decision', ['Pass', 'Fail'], [('Threshold 5; penalty 3.5; no critical errors.', 'Pass'),
                                                                        ('Threshold 6; penalty 5.0; one critical error (auto-fail rule).', 'Fail'),
                                                                        ('Threshold 4; penalty 4.8; no critical errors.', 'Fail')])],
    guidelines=['Minor = 1, Major = 5, Critical = 10. Normalise per 100 words. Any critical error fails the file.'],
    report=QA_REPORT,
    project_brief=project('Scored QA of a translation', 'QA a 300-word translation (a classmate\'s, with permission, or your own from an earlier skill) with weighted scoring.',
                          ['Error log with severities', 'Score calculation', 'Pass/fail decision and feedback'],
                          ['Correct scoring', 'Consistent severities', 'Constructive feedback'], ['Translation QA'], difficulty='intermediate', hours=3),
)

ANNOTATION_QA = _qa_skill(
    'annotation-qa', 'Annotation QA', level='intermediate', icon='ri-price-tag-line', tags=['annotation'],
    tagline='Review other annotators\' labels against the guideline.',
    description='QA annotation batches: check labels against guideline rules, find systematic annotator errors, and give targeted feedback.',
    core=lesson('Reviewing labels', 'Spot wrong labels and systematic patterns.',
                ['Annotation QA checks whether each label follows the guideline — including edge-case rules — and looks for <strong>systematic</strong> '
                 'errors: one annotator always calling sarcasm positive, or always skipping Pidgin items. Systematic errors are fixed with targeted '
                 'feedback and guideline clarification, not just row-by-row corrections.'],
                points=['Check each label against the rule, including edge cases.', 'Look for patterns by annotator.',
                        'Systematic error → targeted feedback + guideline update.', 'Cite the rule in every correction.'],
                quiz=[q('Annotator B labels every sarcastic item positive. This is…', 'a systematic error', 'random noise', 'fine', 'a guideline', why='Pattern.'),
                      q('Best fix for a systematic error?', 'Targeted feedback and guideline clarification', 'Silently fix rows', 'Remove the annotator immediately', 'Ignore it',
                        why='Fix the cause.'),
                      q('Guideline: "Sarcasm = negative." Label "Nice one NEPA, light don go again" as positive. QA verdict?', 'Incorrect', 'Correct', 'Unsure', 'Skip',
                        why='Edge-case rule.')]),
    steps=['Load the guideline.', 'Check each label.', 'Tally errors by annotator and type.', 'Identify patterns.', 'Give feedback.'],
    mistakes=['Fixing rows without feedback', 'Missing patterns', 'Overriding the guideline with opinion'], quality='Corrections cite rules and patterns are reported.',
    practice_items=choice_items('v', 'QA verdict', ['Correct', 'Incorrect'], [
        ('Guideline: sarcasm = negative.\nText: "Nice one NEPA, light don go again 🙄" → Positive', 'Incorrect'),
        ('Text: "The shop opens at 9am." → Neutral', 'Correct'),
        ('Intent guideline: greeting + request → label the request.\nText: "Good morning, abeg check my balance" → greeting', 'Incorrect'),
        ('Entity: "Kano" in "Dr. Bello lives in Kano" → LOC', 'Correct')]),
    assessment_items=[*choice_items('v', 'QA verdict', ['Correct', 'Incorrect'], [
        ('Text: "Food sweet but service slow die." → Positive', 'Incorrect'),
        ('Entity: "Lagos State University" → ORG', 'Correct'),
        ('Language: "Ẹ káàárọ̀ sir, how was your night?" → Yoruba (guideline: two clear languages = Mixed)', 'Incorrect'),
        ('Intent: "Transfer ₦15,000 to Chika" → transfer_money', 'Correct')]),
        *choice_items('p', 'Pattern?', ['Systematic', 'Random'], [('Annotator C mislabels 18 of 20 Pidgin items as English.', 'Systematic')])],
    guidelines=['Judge each label against the guideline rule shown.'],
    report=QA_REPORT,
    project_brief=project('Annotation QA with feedback', 'QA 40 labels from a classmate\'s annotation project (with permission).',
                          ['Verdict per label with rule cited', 'Error patterns', 'Feedback message to the annotator', 'Suggested guideline clarification'],
                          ['Accurate verdicts', 'Pattern analysis', 'Constructive feedback'], ['Annotation QA'], difficulty='intermediate', hours=3),
)

_AQA = ['Accept', 'Reject: wrong format', 'Reject: clipped', 'Reject: noisy', 'Reject: wrong content']
AUDIO_QA = _qa_skill(
    'audio-qa', 'Audio QA', level='intermediate', icon='ri-headphone-line', tags=['speech-data'],
    tagline='Check audio batches against technical specs and content rules.',
    description='Reviewer-level audio QA: format specs (sample rate, channels, file type), signal quality, content match and file naming.',
    core=lesson('Audio specs and batch review', 'Review audio files against a technical spec.',
                ['Projects specify technical formats: e.g. WAV, 16 kHz, 16-bit, mono, named LANG_SPEAKER_0001.wav. Files outside spec are '
                 'rejected even if they sound fine, because pipelines depend on consistent formats. Then signal quality (clipping, noise) and '
                 'content (matches the prompt) are checked.',
                 'Order: format → signal → content. Record the first failing check.'],
                points=['Format: type, sample rate, bit depth, channels, naming.', 'Signal: clipping, level, noise.', 'Content: matches the prompt.',
                        'First failing check is the reason.'],
                quiz=[q('Spec: 16 kHz mono WAV. File: 8 kHz mono WAV, clear speech. Decision?', 'Reject: wrong format', 'Accept', 'Reject: noisy', 'Reject: clipped',
                        why='Format first.'),
                      q('Check order?', 'Format → signal → content', 'Content → format', 'Random', 'Signal only', why='Fixed order.'),
                      q('File named "voice final (2).wav" when spec says YO_S012_0001.wav. Issue?', 'Naming/format', 'Clipping', 'Content', 'None', why='Spec.')]),
    steps=['Check the format metadata.', 'Check signal metrics.', 'Listen for content.', 'Record decision and first reason.'],
    mistakes=['Accepting off-spec formats', 'Skipping content checks', 'Inconsistent order'], quality='Every decision follows the spec and order.',
    practice_items=choice_items('d', 'Decision', _AQA, [
        ('WAV · 16 kHz · mono · clean · matches prompt', 'Accept'), ('MP3 · 44.1 kHz · stereo · clean · matches prompt', 'Reject: wrong format'),
        ('WAV · 16 kHz · mono · 4% clipped · matches prompt', 'Reject: clipped'), ('WAV · 16 kHz · mono · clean · reads a different sentence', 'Reject: wrong content')]),
    assessment_items=choice_items('d', 'Decision', _AQA, [
        ('WAV · 8 kHz · mono · clean · matches prompt', 'Reject: wrong format'), ('WAV · 16 kHz · mono · SNR 7 dB (generator) · matches prompt', 'Reject: noisy'),
        ('WAV · 16 kHz · mono · SNR 31 dB · no clipping · matches prompt', 'Accept'), ('WAV · 16 kHz · stereo · clean · matches prompt', 'Reject: wrong format'),
        ('WAV · 16 kHz · mono · clean · skips the last word', 'Reject: wrong content')]),
    guidelines=['Spec: WAV, 16 kHz, mono, no clipping (>0.5%), SNR ≥ 15 dB, content must match the prompt.', 'Order: format → signal → content.'],
    project_brief=project('Audio batch QA', 'Collect 15 recordings (yours or volunteers\', with consent), with some deliberate problems, and QA the batch.',
                          ['File list with format metadata', 'Decision and reason per file', 'Batch summary and contributor tips'],
                          ['Correct decisions', 'Spec-based reasons', 'Useful tips'], ['Audio QA'], difficulty='intermediate', hours=3),
)

_LQA = ['No error', 'Spelling/diacritics', 'Grammar', 'Register', 'Terminology']
LING_QA = _qa_skill(
    'linguistic-qa', 'Linguistic QA', level='intermediate', icon='ri-spell-check', tags=['linguistics'],
    tagline='Review language quality — spelling, grammar, register and terms.',
    description='Language-quality review for African-language content: orthography, grammar, register (formal vs informal) and terminology consistency.',
    core=lesson('Language quality review', 'Categorise language-quality issues.',
                ['Linguistic QA looks at how the language is written, regardless of the source: correct orthography (tone marks, dotted vowels, '
                 'hooked letters), grammar, appropriate <strong>register</strong> (formal bank notice vs casual chat), and consistent '
                 '<strong>terminology</strong>.',
                 'Register errors are common when casual Pidgin appears in a formal notice, or when a respectful form (Yoruba "Ẹ") is replaced '
                 'with a familiar one for an elder audience.'],
                points=['Orthography: all required marks.', 'Grammar: agreement, word order, particles.', 'Register: fits audience and context.',
                        'Terminology: the agreed term every time.'],
                quiz=[q('A formal bank letter says "Abeg pay una money sharp sharp." Issue?', 'Register', 'Spelling', 'Terminology', 'No error', why='Too casual.'),
                      q('"Ẹ kaaaro" with only some marks. Issue?', 'Spelling/diacritics', 'Register', 'Grammar', 'No error', why='Incomplete marks.'),
                      q('"Health centre" in line 1, "clinic building" in line 5 for the same glossary term. Issue?', 'Terminology', 'Grammar', 'Register', 'No error',
                        why='Inconsistent term.')]),
    steps=['Read for orthography.', 'Read for grammar.', 'Check register against the brief.', 'Check terms against the glossary.', 'Log and report.'],
    mistakes=['Ignoring register', 'Passing partial diacritics', 'Not checking the glossary'], quality='Issues are categorised and justified.',
    practice_items=choice_items('e', 'Main issue', _LQA, [
        ('Formal notice: "Abeg pay una money sharp sharp."', 'Register'), ('"Ẹ kaaaro, ṣé dáadáa ni?"', 'Spelling/diacritics'),
        ('"Ẹ káàárọ̀, ṣé dáadáa ni?"', 'No error'), ('Glossary: "health centre"; text: "Visit the clinic building."', 'Terminology')]),
    assessment_items=choice_items('e', 'Main issue', _LQA, [
        ('"Na shiga daki."', 'Spelling/diacritics'), ('Message to an elder in Yoruba using familiar "o ṣé" (brief requires respectful forms)', 'Register'),
        ('"Adị m mma, daalụ."', 'No error'), ('Glossary term "mobile money" translated three different ways in one leaflet', 'Terminology'),
        ('Pidgin: "Him go came yesterday."', 'Grammar')]),
    guidelines=['Choose the main issue.'],
    report=QA_REPORT,
    project_brief=project('Language QA of public content', 'QA a public notice, flyer or app screen written in a Nigerian language (or Pidgin).',
                          ['The text (or screenshot link)', 'Issue log by category', 'Corrected version', 'Report'],
                          ['Accurate issues', 'Correct fixes', 'Clear report'], ['Linguistic QA'], difficulty='intermediate', hours=2),
)

DOUBLE = _qa_skill(
    'double-annotation', 'Double Annotation', level='intermediate', icon='ri-git-compare-line', tags=['annotation'],
    tagline='Run double annotation and adjudicate disagreements.',
    description='Design double-annotation workflows: independent labelling, disagreement detection and adjudication against the guideline.',
    core=lesson('Two annotators and an adjudicator', 'Adjudicate disagreements correctly.',
                ['In double annotation, two annotators label the same items <strong>independently</strong> (without seeing each other\'s labels). '
                 'Disagreements go to an <strong>adjudicator</strong>, who decides the final label by the guideline — not by majority, seniority '
                 'or by splitting the difference — and records which rule decided it.',
                 'Frequent disagreements on the same kind of item usually mean the guideline needs clarifying.'],
                points=['Independence: no peeking.', 'Adjudicate by the guideline.', 'Record the deciding rule.', 'Patterns → guideline update.'],
                quiz=[q('Annotator A: Positive, B: Negative. Guideline: sarcasm = negative; text is sarcastic. Final?', 'Negative', 'Positive', 'Mixed', 'Skip',
                        why='The guideline decides.'),
                      q('Why must annotators label independently?', 'So agreement measures real consistency', 'To save time', 'It is cheaper', 'No reason', why='Unbiased.'),
                      q('Many disagreements on code-switched items suggest…', 'the guideline needs a code-switching rule', 'annotators are lazy', 'nothing', 'removing those items',
                        why='Fix the guideline.')]),
    steps=['Assign items to two annotators.', 'Collect labels independently.', 'Find disagreements.', 'Adjudicate by rule.', 'Update the guideline.'],
    mistakes=['Letting annotators confer', 'Adjudicating by seniority', 'Not recording the rule'], quality='Final labels are rule-based and traceable.',
    practice_items=choice_items('f', 'Final label', ['Positive', 'Negative', 'Neutral', 'Mixed'], [
        ('A: Positive · B: Negative\nText: "Wow, another fuel queue. Just what I needed 😒" (sarcasm = negative)', 'Negative'),
        ('A: Neutral · B: Positive\nText: "The bus stop is at Ojota."', 'Neutral'),
        ('A: Positive · B: Mixed\nText: "Na correct movie, but the ending no make sense."', 'Mixed'),
        ('A: Negative · B: Negative\nText: "Network don spoil again, I tire."', 'Negative')]),
    assessment_items=[*choice_items('f', 'Final label', ['Positive', 'Negative', 'Neutral', 'Mixed'], [
        ('A: Mixed · B: Positive\nText: "This lecturer no dey play, him class sweet die."', 'Positive'),
        ('A: Positive · B: Neutral\nText: "The meeting is at 4pm on Friday."', 'Neutral'),
        ('A: Negative · B: Mixed\nText: "The jollof was nice but the place too hot."', 'Mixed')]),
        *choice_items('w', 'Good practice?', ['Yes', 'No'], [('Let annotators discuss items before labelling to agree.', 'No'),
                                                            ('Record the guideline rule used in each adjudication.', 'Yes')])],
    guidelines=['Positive / Negative / Neutral / Mixed; sarcasm = its real meaning.', 'Adjudicate by the guideline only.'],
    project_brief=project('Run a double-annotation round', 'With a classmate, double-annotate 40 items independently, then adjudicate.',
                          ['Both label sets', 'Disagreement list with adjudicated labels and rules', 'Agreement % and guideline improvements'],
                          ['True independence', 'Rule-based adjudication', 'Useful improvements'], ['Double annotation', 'Adjudication'],
                          difficulty='intermediate', hours=3),
)

_ERR = ['No error', 'Wrong label', 'Missing diacritics', 'Mistranslation', 'Wrong speaker', 'Personal data left in']
ERROR_ID = _qa_skill(
    'error-identification', 'Error Identification', level='beginner', icon='ri-bug-line', tags=['annotation', 'transcription', 'translation'],
    tagline='Spot errors fast across transcription, translation and annotation work.',
    description='A cross-task reviewer skill: quickly identifying what is wrong in transcripts, translations, labels and data rows.',
    core=lesson('Seeing what\'s wrong', 'Identify the main error in any language-data item.',
                ['Reviewers switch between task types all day. A fast, reliable habit: first check for anything that must never pass (personal '
                 'data, harmful content), then meaning (mistranslation, wrong label), then form (diacritics, tags, speaker labels).',
                 'Name the single most important error; secondary issues can be noted in comments.'],
                points=['Order: must-never-pass → meaning → form.', 'One main error per item.', 'Personal data always counts.'],
                quiz=[q('A transcript is perfect but contains a caller\'s phone number. Main error?', 'Personal data left in', 'No error', 'Wrong speaker', 'Missing diacritics',
                        why='Must never pass.'),
                      q('A translation is fluent but says "husband" for "vehicle". Main error?', 'Mistranslation', 'Missing diacritics', 'No error', 'Wrong label',
                        why='Meaning.'),
                      q('Why check personal data first?', 'It must never pass, regardless of other quality', 'It is easiest', 'Alphabetical order', 'No reason', why='Priority.')]),
    steps=['Check for must-never-pass issues.', 'Check meaning.', 'Check form.', 'Name the main error.'],
    mistakes=['Fixating on form and missing meaning', 'Missing personal data'], quality='The main error is right every time.',
    practice_items=choice_items('e', 'Main error', _ERR, [
        ('Transcript: "Call me on 0803 123 4567 tonight." (guideline: remove phone numbers)', 'Personal data left in'),
        ('Translation of "Ọkọ̀ náà ti dé": "The husband has arrived."', 'Mistranslation'),
        ('Sentiment label for "This phone sweet well well!": Negative', 'Wrong label'),
        ('Yoruba transcript: "Mo n lo si oja."', 'Missing diacritics')]),
    assessment_items=choice_items('e', 'Main error', _ERR, [
        ('Interview line "What brings you to the clinic?" labelled Patient', 'Wrong speaker'),
        ('Translation of "Biko, nye m mmiri": "Please give me water."', 'No error'),
        ('Hausa transcript: "Bera ya shiga daki."', 'Missing diacritics'),
        ('Dataset row includes "my BVN is 22123456789"', 'Personal data left in'),
        ('Topic label for "Osimhen scores twice": Politics', 'Wrong label'),
        ('Translation of "Na shiga ɗaki": "I entered the market."', 'Mistranslation')]),
    guidelines=['Name the single most important error.'],
    project_brief=project('Error-spotting challenge set', 'Create 30 items across task types with one planted error each (and 5 clean items), plus an answer key.',
                          ['30 items', 'Answer key with explanations', 'Difficulty rating per item'], ['Realistic errors', 'Correct key', 'Good variety'],
                          ['Error identification'], hours=2),
    hours=3,
)

SCORING = _qa_skill(
    'quality-scoring', 'Quality Scoring', level='intermediate', icon='ri-star-half-line', tags=['dataset'],
    tagline='Turn error logs into consistent, defensible quality scores.',
    description='Compute accuracy, weighted error scores, averages and pass/fail decisions from QA logs — consistently, every time.',
    core=lesson('From errors to scores', 'Compute quality scores correctly.',
                ['Scoring formulas vary by project, but the common ones are: <strong>accuracy</strong> = correct ÷ total; <strong>weighted error '
                 'score</strong> = Σ(errors × weight); <strong>quality score</strong> = 100 − normalised penalty; and averages across files '
                 'weighted by size.',
                 'A score is only useful if it is reproducible: always state the formula, the weights, and the threshold.'],
                points=['Accuracy = correct ÷ total.', 'Weighted errors: minor 1, major 5, critical 10 (example).', 'Quality = 100 − penalty per 100 words.',
                        'State formula, weights and threshold.'],
                quiz=[q('46 of 50 labels correct. Accuracy?', '92%', '46%', '8%', '96%', why='46/50.'),
                      q('2 minor (1) + 1 major (5). Weighted score?', '7', '3', '8', '10', why='2 + 5.'),
                      q('Why state the formula with the score?', 'So anyone can reproduce it', 'Tradition', 'To make it longer', 'No reason', why='Reproducible.')]),
    steps=['Confirm the formula.', 'Count errors by severity.', 'Compute.', 'Compare with the threshold.', 'Report with the formula.'],
    mistakes=['Mixing formulas between files', 'Unweighted averages of different-sized files', 'Rounding too early'], quality='Scores are reproducible.',
    practice_items=[number_item('p1', '46 of 50 labels correct.', 'Accuracy (%)', 92, 0.1),
                    number_item('p2', '2 minor (weight 1) + 1 major (weight 5).', 'Weighted error score', 7),
                    number_item('p3', 'Penalty 3.5 per 100 words. Quality score = 100 − penalty?', 'Quality score', 96.5, 0.05)],
    assessment_items=[number_item('a1', '188 of 200 segments correct.', 'Accuracy (%)', 94, 0.1),
                      number_item('a2', '3 minor (1) + 2 major (5) + 1 critical (10).', 'Weighted error score', 23),
                      number_item('a3', 'File A: 100 items, 90% accurate. File B: 300 items, 80% accurate. Size-weighted accuracy?', 'Accuracy (%)', 82.5, 0.1),
                      *choice_items('d', 'Decision', ['Pass', 'Fail'], [('Threshold: accuracy ≥ 95%. Observed 94%.', 'Fail')])],
    guidelines=['Use the formulas from the lesson; weight averages by item count.'],
    project_brief=project('Scoring sheet for a project', 'Design a quality-scoring sheet (formula, weights, thresholds) for a language-data task and apply it to 3 sample files.',
                          ['Scoring rules', 'Calculations for 3 files', 'Pass/fail decisions'], ['Clear rules', 'Correct maths', 'Sound thresholds'],
                          ['Quality scoring'], difficulty='intermediate', hours=2),
    hours=3,
)

_FB = ['A', 'B', 'C']
REVIEWER = _qa_skill(
    'reviewer-training', 'Reviewer Training', level='advanced', icon='ri-user-star-line', tags=['annotation'],
    tagline='Calibrate yourself and coach other reviewers.',
    description='Become a reviewer others trust: calibration against gold sets, writing feedback that improves contributors, and handling disputes.',
    core=lesson('Calibration and feedback', 'Calibrate to gold standards and write effective feedback.',
                ['New reviewers <strong>calibrate</strong> by reviewing gold items (with known answers) until their decisions match. Ongoing '
                 'calibration sessions keep a team consistent.',
                 'Effective feedback is <strong>specific</strong> (which item, what\'s wrong), <strong>rule-based</strong> (which guideline), '
                 '<strong>actionable</strong> (what to do next time) and <strong>respectful</strong>. Disputes are resolved by the guideline and, '
                 'if it is unclear, escalated and documented.'],
                points=['Calibrate on gold items.', 'Feedback: specific, rule-based, actionable, respectful.', 'Disputes: guideline first, then escalate.',
                        'Track your own agreement with gold over time.'],
                quiz=[q('Best way to align a new reviewer?', 'Calibrate on gold items with known answers', 'Let them guess', 'Give them the hardest batch', 'Skip training',
                        why='Calibration.'),
                      q('A contributor disputes a correction and the guideline is unclear. You…', 'escalate and document, then update the guideline', 'insist you\'re right',
                        'accept everything', 'ignore them', why='Fair process.'),
                      q('Which feedback is best?', '"Item 7: sarcasm should be Negative (rule 4.2). Re-check items with emojis."', '"Wrong again."', '"Try harder."', '"Fine."',
                        why='Specific + rule + action.')]),
    steps=['Review gold items.', 'Compare with gold.', 'Discuss differences.', 'Write feedback.', 'Track calibration over time.'],
    mistakes=['Vague feedback', 'Personal tone', 'No calibration'], quality='Your decisions match gold and your feedback changes behaviour.',
    practice_items=choice_items('best', 'Best feedback', _FB, [
        ('A: "Bad job."\nB: "Segment 3: "oja" needs diacritics → "ọjà" (rule 2.1). Do a diacritics-only pass before submitting."\nC: "Please be careful."', 'B'),
        ('A: "Items 4 and 9: greetings with requests should be labelled by the request (rule 1.3)."\nB: "You don\'t understand intents."\nC: "Redo all."', 'A'),
        ('A: "Why are you so slow?"\nB: "OK."\nC: "Your accuracy dropped after item 60 — take a break mid-batch and re-read rule 3."', 'C')]),
    assessment_items=[*choice_items('best', 'Best feedback', _FB, [
        ('A: "Item 12: [giggles] isn\'t an allowed tag — use [laughter] (rule 5)."\nB: "Wrong tag."\nC: "Use better tags."', 'A'),
        ('A: "Terrible translation."\nB: "Sentence 2 omits \'under five\' (accuracy, major). Check numbers and ages against the source."\nC: "Fix it."', 'B')]),
        *choice_items('a', 'Best action', ['Apply the guideline', 'Escalate and document', 'Accept the contributor\'s view'], [
            ('A contributor disputes a correction; the guideline clearly supports your correction.', 'Apply the guideline'),
            ('A contributor disputes a correction; the guideline doesn\'t cover the case.', 'Escalate and document')]),
        number_item('g1', 'You matched gold on 27 of 30 calibration items.', 'Agreement (%)', 90, 0.1)],
    guidelines=['Choose the most specific, rule-based, actionable, respectful option.'],
    report={'label': 'Write feedback for a contributor whose Yoruba transcripts keep missing tone marks', 'min_words': 30},
    project_brief=project('Reviewer training pack', 'Create a training pack for new reviewers on one task type.',
                          ['15 gold items with answers and explanations', 'Feedback templates', 'A dispute-handling procedure'],
                          ['High-quality gold items', 'Useful templates', 'Fair procedure'], ['Reviewer training'], difficulty='advanced', hours=4),
)

_IAA_CTX = ('Two annotators labelled 100 items Yes/No.\nBoth Yes: 40 · A Yes/B No: 20 · A No/B Yes: 10 · Both No: 30\n'
            '(A said Yes 60 times; B said Yes 50 times.)')
_IAA_CTX2 = ('Two annotators labelled 50 items Yes/No.\nBoth Yes: 18 · A Yes/B No: 12 · A No/B Yes: 2 · Both No: 18\n'
             '(A said Yes 30 times; B said Yes 20 times.)')
IAA = _qa_skill(
    'inter-annotator-agreement', 'Inter-Annotator Agreement', level='advanced', icon='ri-team-line', tags=['annotation', 'dataset'],
    tagline='Measure annotation consistency with percent agreement and Cohen\'s kappa.',
    description='Compute and interpret inter-annotator agreement — observed agreement, chance agreement and Cohen\'s kappa — to judge dataset reliability.',
    core=lesson('Percent agreement and Cohen\'s kappa', 'Compute and interpret Cohen\'s kappa.',
                ['<strong>Percent agreement</strong> (p<sub>o</sub>) is the share of items where two annotators agree. But some agreement '
                 'happens by chance, so <strong>Cohen\'s kappa</strong> corrects for it: κ = (p<sub>o</sub> − p<sub>e</sub>) ÷ (1 − p<sub>e</sub>), '
                 'where p<sub>e</sub> = Σ over labels of (A\'s share of that label × B\'s share of that label).',
                 'Common interpretation (Landis & Koch): 0.21–0.40 fair, 0.41–0.60 moderate, 0.61–0.80 substantial, 0.81+ almost perfect. '
                 'Low kappa usually means the guideline is unclear.'],
                points=['p_o = agreements ÷ items.', 'p_e = Σ (pA(label) × pB(label)).', 'κ = (p_o − p_e) / (1 − p_e).',
                        '0.41–0.60 moderate · 0.61–0.80 substantial.'],
                example='p_o = (40 + 30) / 100 = 0.70\np_e = 0.6×0.5 + 0.4×0.5 = 0.50\nκ = (0.70 − 0.50) / (1 − 0.50) = 0.40',
                quiz=[q('Why use kappa instead of percent agreement?', 'It corrects for agreement expected by chance', 'It is always higher', 'It is easier', 'It ignores disagreements',
                        why='Chance correction.'),
                      q('κ = 0.72 is usually called…', 'substantial', 'poor', 'fair', 'perfect', why='0.61–0.80.'),
                      q('Low kappa most often means…', 'the guideline is unclear or annotators need training', 'the data is perfect', 'too many items', 'nothing',
                        why='Fix the process.')]),
    steps=['Build the agreement table.', 'Compute p_o.', 'Compute each annotator\'s label shares.', 'Compute p_e.', 'Compute κ and interpret.'],
    mistakes=['Using percent agreement alone', 'Computing p_e from the agreement cells only', 'Over-interpreting small samples'], quality='κ is computed correctly and interpreted soberly.',
    practice_items=[number_item('p1', 'Observed agreement p_o', 'p_o (2 decimals)', 0.70, 0.005, _IAA_CTX),
                    number_item('p2', 'Chance agreement p_e', 'p_e (2 decimals)', 0.50, 0.005, _IAA_CTX),
                    number_item('p3', "Cohen's kappa", 'κ (2 decimals)', 0.40, 0.005, _IAA_CTX)],
    assessment_items=[number_item('a1', 'Observed agreement p_o', 'p_o (2 decimals)', 0.72, 0.005, _IAA_CTX2),
                      number_item('a2', 'Chance agreement p_e', 'p_e (2 decimals)', 0.48, 0.005, _IAA_CTX2),
                      number_item('a3', "Cohen's kappa", 'κ (2 decimals)', 0.46, 0.01, _IAA_CTX2),
                      *choice_items('i', 'Interpretation (Landis & Koch)', ['Fair', 'Moderate', 'Substantial', 'Almost perfect'], [('κ = 0.46', 'Moderate'), ('κ = 0.85', 'Almost perfect')])],
    guidelines=['Use the formulas in the lesson; round only at the end.'],
    project_brief=project('Measure agreement on a real task', 'With a classmate, independently label 50 items on any annotation task, then compute agreement.',
                          ['Both label sets', 'Agreement table', 'p_o, p_e and κ with working', 'Interpretation and guideline fixes'],
                          ['Correct maths', 'Sound interpretation', 'Actionable fixes'], ['Inter-annotator agreement'], difficulty='advanced', hours=3),
)

SKILLS = [DATA_QA, TRANSCRIPTION_QA, TRANSLATION_QA, ANNOTATION_QA, AUDIO_QA, LING_QA, DOUBLE, ERROR_ID, SCORING, REVIEWER, IAA]
