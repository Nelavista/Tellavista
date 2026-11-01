"""Speech & Voice Data category. Recording skills use the 'recording' task kind: the
student records in the browser and each take is checked against the same technical
requirements speech-dataset projects use (length, clipping, level, silence). Checking/
validation skills are gold-labelled judgement tasks.
"""
from ._common import q, lesson, workflow_lesson, task, labeling, choice_items, project, skill

COLOR = '#7c3aed'
REQ = {'min_seconds': 1.5, 'max_seconds': 15, 'max_clip_pct': 0.5, 'min_rms_db': -40, 'max_silence_pct': 70}
REC_GUIDE = ['Quiet room, phone or mic about a hand-width (15–20 cm) from your mouth.',
             'Wait half a second after pressing Record before speaking, and after finishing before Stop.',
             'Read exactly the prompt — no extra words, no restarts. If you slip, re-record.',
             'Speak at your normal pace and volume; don\'t shout (that clips) or whisper.']

FOUNDATION = lesson(
    'How speech datasets are collected',
    'Understand what makes a recording usable training data.',
    [
        'Speech recognition and text-to-speech systems for African languages need many hours of recordings from many '
        'different speakers, ages, regions and environments. Contributors record prompts (scripted speech) or answer '
        'questions (spontaneous speech), and each recording is checked before it enters a dataset.',
        'A recording is rejected if it is too short or cut off, clipped (distorted because it was too loud), too quiet, '
        'mostly silence, noisy, or doesn\'t match the prompt. Projects also collect <strong>metadata</strong> — language, '
        'dialect, region, age range, environment — with the speaker\'s <strong>informed consent</strong>.',
    ],
    points=['Consent first: speakers must know how their voice will be used.', 'Match the prompt exactly in scripted tasks.',
            'Avoid clipping, background noise and long silences.', 'Accurate metadata is part of the data.'],
    quiz=[
        q('A recording sounds distorted because the speaker was too loud. This is called…', 'clipping', 'echo', 'silence', 'compression',
          why='The signal hit the maximum level.'),
        q('Before recording someone else\'s voice for a dataset you must…', 'get their informed consent', 'pay them first', 'record secretly for naturalness', 'nothing',
          why='Consent is required.'),
        q('Why do datasets collect speaker region and dialect?', 'So models work for every variety, and coverage can be measured', 'To identify people',
          'It is decoration', 'To sort files alphabetically', why='Diversity is measured through metadata.'),
    ],
)


def _rec_skill(slug, name, *, level, tagline, description, core, workflow, practice_prompts, assessment_prompts,
               project_brief, metadata=None, extra_tags=None, hours=3, requirements=None):
    def spec(prompts, brief):
        s = {'kind': 'recording', 'brief': brief, 'guidelines': REC_GUIDE, 'requirements': requirements or REQ,
             'prompts': [{'id': f'p{i}', 'text': t} for i, t in enumerate(prompts, 1)]}
        if metadata:
            s['metadata_fields'] = metadata
        return s
    return skill(slug, name, level=level, tags=['speech-data', 'african-languages'] + (extra_tags or []),
                 icon='ri-mic-line', color=COLOR, tagline=tagline, description=description,
                 foundation=FOUNDATION, core=core, workflow=workflow,
                 practice=task(f'{name}: practice takes', 'Record each prompt; each take is checked automatically.',
                               spec(practice_prompts, 'Record each prompt. Re-record any take that fails a check.'), minutes=10),
                 assessment=task(f'{name} assessment', 'Record every prompt so that each one meets the technical requirements.',
                                 spec(assessment_prompts, 'All takes must meet the requirements to score full marks.'), minutes=15),
                 project_brief=project_brief, hours=hours)


VOICE = _rec_skill(
    'voice-recording', 'Voice Recording', level='beginner',
    tagline='Record clean, usable voice audio with just a phone.',
    description='The practical basics of recording speech data: environment, microphone distance, levels and file hygiene.',
    core=lesson('Recording clean audio with a phone', 'Set up and record clean takes.',
                ['Most speech data today is recorded on phones. The biggest quality factors are not the phone but the room '
                 '(soft furnishings absorb echo; fans, generators and traffic add noise) and the distance to the microphone.',
                 'Too close and plosives (p, b) pop and peaks clip; too far and the room\'s echo and noise dominate. About a '
                 'hand-width away, slightly off to the side, is a good default.'],
                points=['Choose a quiet, furnished room; switch off fans if you can.', '15–20 cm from the mic, slightly off-axis.',
                        'Leave a short silence at start and end — but not seconds of it.', 'Listen back to every take.'],
                quiz=[q('Which room usually records cleanest?', 'A bedroom with curtains and a bed', 'An empty tiled kitchen',
                        'Outside near a road', 'A bathroom', why='Soft surfaces absorb echo.'),
                      q('Recording with your mouth touching the phone causes…', 'pops and clipping', 'cleaner audio', 'more echo', 'quieter audio',
                        why='Too close.'),
                      q('After pressing Stop you should…', 'listen back before submitting', 'submit straight away', 'delete it', 'record it twice anyway',
                        why='Catch problems early.')]),
    workflow=workflow_lesson('voice recording', ['Check the room for noise.', 'Position the phone 15–20 cm away.',
                             'Do a test take and listen.', 'Record each prompt with a short lead-in silence.', 'Re-record any take with a slip or noise.'],
                             ['Fan or generator noise', 'Clipping from shouting', 'Long silence before speaking', 'Not listening back'],
                             'Every take is clear, unclipped, and contains exactly the prompt.'),
    practice_prompts=['Good morning, how are you today?', 'The market opens at seven o\'clock.'],
    assessment_prompts=['Please call me when you get home.', 'The rain started early this morning.',
                        'Lagos, Kano and Enugu are large cities.'],
    project_brief=project('Record a clean 20-prompt set', 'Record 20 short sentences of your choice in a language you speak, in one session, to dataset quality.',
                          ['Link to a folder with 20 audio files named 01.wav/webm … 20', 'A text file listing each prompt',
                           'A note on your room, device and any takes you redid'],
                          ['Consistent quality across all files', 'Prompt list matches files', 'Clear setup notes'],
                          ['Voice recording'], hours=2),
)

SCRIPTED = _rec_skill(
    'scripted-speech-recording', 'Scripted Speech Recording', level='beginner',
    tagline='Read prompts exactly, naturally and consistently.',
    description='Record scripted prompts for speech-recognition and text-to-speech datasets — exact wording, natural delivery, no restarts.',
    core=lesson('Reading prompts for datasets', 'Read scripted prompts accurately and naturally.',
                ['In scripted collection the text is the label: if you add, skip or change a word, the audio no longer matches '
                 'its transcript and the pair is useless (or worse, it teaches the model a wrong mapping).',
                 'Read naturally, as if speaking to someone, at an even pace. Numbers, names and abbreviations are read as the '
                 'guideline says (e.g. "No. 5" → "number five"). If you stumble, stop and re-record the whole prompt.'],
                points=['Exact words — nothing added, skipped or changed.', 'Natural, even delivery.',
                        'Follow the reading rules for numbers and abbreviations.', 'Any stumble → re-record the whole prompt.'],
                quiz=[q('You say "um" in the middle of a scripted prompt. You…', 're-record the whole prompt', 'keep it — it sounds natural',
                        'note it in a comment', 'cut the "um" yourself', why='Audio must match the text.'),
                      q('Why must scripted recordings match the prompt exactly?', 'The prompt is the transcript the audio is paired with',
                        'For copyright reasons', 'To keep files short', 'It doesn\'t matter', why='Text = label.'),
                      q('Best delivery style?', 'Natural, even and clear', 'Very slow, word by word', 'As fast as possible', 'Whispered',
                        why='Natural speech trains better models.')]),
    workflow=workflow_lesson('scripted recording', ['Read the prompt silently first.', 'Check the reading rules for numbers/names.',
                             'Record once, naturally.', 'Listen back and compare with the text.', 'Re-record on any mismatch.'],
                             ['Adding or skipping words', 'Robotic word-by-word reading', 'Keeping a take with a stumble'],
                             'Audio and prompt match word for word, read naturally.'),
    practice_prompts=['Ẹ káàárọ̀, ṣé dáadáa ni?', 'How you dey? I dey fine.'],
    assessment_prompts=['Ụtụtụ ọma, kedụ?', 'Ina kwana? Lafiya lau.', 'Mo ń lọ sí ọjà láti ra ẹja.', 'Abeg make we go market.'],
    project_brief=project('Scripted prompt session', 'Record 25 prompts in one language you speak: write them (or take them from a public-domain text) and record each.',
                          ['Folder link with 25 recordings', 'Prompt list with file names', 'Reading rules you followed for numbers and names'],
                          ['Exact match between audio and text', 'Natural delivery', 'Consistent quality'], ['Scripted speech recording'], hours=2),
)

CONVERSATIONAL = _rec_skill(
    'conversational-speech-collection', 'Conversational Speech Collection', level='intermediate',
    tagline='Collect natural, spontaneous speech ethically and usefully.',
    description='Plan and record spontaneous answers and conversations — good questions, natural speech, consent and privacy.',
    core=lesson('Collecting spontaneous speech', 'Elicit natural speech without capturing private data.',
                ['Spontaneous speech — answering a question, chatting — is what real users sound like, so ASR systems need it. '
                 'Good collection uses open, everyday prompts ("Describe your journey to school") that get people talking without '
                 'touching sensitive topics.',
                 'Speakers must not say personal identifiers (full names, phone numbers, addresses, ID numbers). If they do, the '
                 'segment must be removed or bleeped, per the guideline.'],
                points=['Open, everyday prompts get natural speech.', 'Avoid sensitive topics: health, politics, religion, money.',
                        'No personal identifiers in the audio.', 'Record consent separately and store it safely.'],
                quiz=[q('Which prompt is best for spontaneous speech collection?', 'Describe how you prepare your favourite meal.',
                        'Who will you vote for?', 'Say your phone number.', 'Read this sentence.', why='Open, everyday, non-sensitive.'),
                      q('A speaker says their home address. You…', 'remove or bleep that part, as the guideline says', 'keep it — it is natural',
                        'publish it', 'ask them to repeat it', why='Personal data must not enter the dataset.'),
                      q('Spontaneous speech is valuable because…', 'it sounds like real users', 'it is easier to transcribe',
                        'it has no errors', 'it is shorter', why='Models must handle natural speech.')]),
    workflow=workflow_lesson('conversational collection', ['Prepare open, safe prompts.', 'Explain and record consent.',
                             'Let the speaker talk; don\'t interrupt.', 'Check for personal data and remove it.', 'Fill in metadata.'],
                             ['Yes/no questions', 'Sensitive topics', 'Leaving personal data in', 'Missing consent records'],
                             'Natural speech, safe topics, no personal data, consent on file.'),
    practice_prompts=['Answer in your own words: describe your journey to school or work.',
                      'Answer in your own words: what is your favourite food and how is it made?'],
    assessment_prompts=['Answer in your own words: describe a market near you.', 'Answer in your own words: what do you do on a rainy day?',
                        'Answer in your own words: describe a festival or celebration you enjoy.'],
    project_brief=project('Mini conversational corpus', 'With consent, record 5 people (or 5 sessions) answering 3 safe, open prompts each in a language they speak.',
                          ['Folder link with 15 recordings', 'Prompt list and consent template you used (no signed copies)',
                           'Metadata table: speaker code, language, region, age range — no names'],
                          ['Natural speech on safe topics', 'No personal data', 'Complete, anonymised metadata'],
                          ['Conversational speech collection', 'Data privacy'], difficulty='intermediate', hours=4),
    extra_tags=['data-privacy'], requirements={**REQ, 'min_seconds': 4, 'max_seconds': 45},
)

PRONUNCIATION = _rec_skill(
    'pronunciation-recording', 'Pronunciation Recording', level='beginner',
    tagline='Record careful word-level pronunciations, tones included.',
    description='Record words and minimal pairs clearly for pronunciation lexicons and text-to-speech — especially tone contrasts in African languages.',
    core=lesson('Recording pronunciations and tone contrasts', 'Record clear isolated words and minimal pairs.',
                ['Pronunciation lexicons and TTS voices need words recorded clearly and consistently, often in a carrier phrase '
                 '("Say ___ again") so every word has the same surrounding context.',
                 'For tonal languages, minimal pairs — words that differ only in tone, like Yoruba ọkọ / ọkọ̀ / ọkọ́ — must be '
                 'pronounced with clear, natural tone. Don\'t exaggerate; don\'t flatten.'],
                points=['Use the carrier phrase exactly if one is given.', 'Same pace and volume for every word.',
                        'Natural tone — not exaggerated, not flattened.', 'Pause briefly between repetitions.'],
                quiz=[q('Why use a carrier phrase?', 'So each word is spoken in the same context', 'To make files longer', 'To add meaning', 'To test the microphone',
                        why='Consistency.'),
                      q('ọkọ / ọkọ̀ / ọkọ́ are…', 'a tone minimal set', 'three spellings of one word', 'three dialects', 'English loanwords',
                        why='They differ only in tone.'),
                      q('When recording tonal contrasts you should…', 'pronounce tones naturally and clearly', 'exaggerate every tone', 'flatten them', 'whisper',
                        why='Natural, clear speech.')]),
    workflow=workflow_lesson('pronunciation recording', ['Review the word list and its tones/special letters.', 'Practise each word aloud.',
                             'Record in the carrier phrase at a steady pace.', 'Listen for mispronounced tones.', 'Re-record any unclear word.'],
                             ['Inconsistent pace', 'Flattened tones', 'Skipping the carrier phrase'], 'Each word is clear, natural and consistent with the others.'),
    practice_prompts=['Say each word with a pause: ọkọ — ọkọ̀ — ọkọ́', 'Say each word with a pause: ɗaki — ƙasa — ɓera'],
    assessment_prompts=['Say each word with a pause: ọmọ — ọjà — ẹja', 'Say each word with a pause: ụtụtụ — ọma — mmiri',
                        'Say "Say Ikeja again", then "Say Oshodi again".'],
    project_brief=project('Mini pronunciation lexicon', 'Choose 20 words in a language you speak, including at least 3 tone or sound contrasts. Record each in a carrier phrase.',
                          ['Folder link with 20 recordings', 'Word list with spelling (all marks) and English gloss', 'Which contrasts you included and why'],
                          ['Clear, natural pronunciation', 'Correct spelling of every word', 'Meaningful contrasts'],
                          ['Pronunciation recording'], hours=2),
)

ACCENT = _rec_skill(
    'accent-dialect-data-collection', 'Accent/Dialect Data Collection', level='intermediate',
    tagline='Record and document dialect and accent variation accurately.',
    description='Collect speech that represents dialects and accents, with the metadata that makes it useful — and without stereotyping speakers.',
    core=lesson('Documenting dialect and accent', 'Collect dialect data with accurate, respectful metadata.',
                ['Models that only hear one variety fail everyone else. Dialect collection deliberately records speakers from '
                 'different regions and backgrounds, and labels each recording with self-reported metadata: first language, '
                 'dialect, region/state, and sometimes other languages spoken.',
                 'Metadata should be what the speaker reports, not what the collector assumes from how they sound. Collect only '
                 'what the project needs, and never anything that identifies the person.'],
                points=['Metadata is self-reported, not guessed.', 'Record the same prompts across dialects so they can be compared.',
                        'Note the environment (quiet/noisy).', 'Collect only what is needed; nothing identifying.'],
                quiz=[q('Who decides a speaker\'s dialect label?', 'The speaker (self-reported)', 'The collector, from their accent', 'The software', 'Nobody',
                        why='Avoid assumptions.'),
                      q('Why read the same prompts across dialects?', 'So the varieties can be compared directly', 'To save time', 'To test the mic', 'No reason',
                        why='Controlled comparison.'),
                      q('Which metadata field should NOT be collected?', 'Home address', 'Region/state', 'First language', 'Recording environment',
                        why='Identifying information.')]),
    workflow=workflow_lesson('dialect collection', ['Explain the project and get consent.', 'Ask for self-reported metadata.',
                             'Record the shared prompt set.', 'Note environment.', 'Store metadata separately from any consent record.'],
                             ['Guessing dialects', 'Collecting identifying info', 'Different prompts per speaker'], 'Comparable recordings with accurate, minimal metadata.'),
    practice_prompts=['Read: "The children are playing outside after school."', 'Read: "Please bring the water to the house."'],
    assessment_prompts=['Read: "We will travel to the village next week."', 'Read: "The market is very busy on Saturday."',
                        'Say a greeting you would use with an elder, in your own dialect.'],
    metadata=[{'name': 'first_language', 'label': 'Your first language'},
              {'name': 'dialect', 'label': 'Your dialect (self-reported)'},
              {'name': 'region', 'label': 'State or region you grew up in'},
              {'name': 'environment', 'label': 'Recording environment', 'options': ['Quiet indoors', 'Some background noise', 'Outdoors']}],
    project_brief=project('Dialect sample set', 'With consent, record 4 speakers from different dialects or regions reading the same 5 prompts.',
                          ['Folder link with 20 recordings', 'Metadata table (speaker code, first language, dialect, region, environment)',
                           'A short note on the differences you hear'],
                          ['Same prompts across speakers', 'Self-reported, minimal metadata', 'Thoughtful observations'],
                          ['Dialect data collection'], difficulty='intermediate', hours=4),
    extra_tags=['dialect'],
)

DATA_COLLECTION = skill(
    'speech-data-collection', 'Speech Data Collection', level='intermediate',
    tags=['speech-data', 'african-languages', 'data-privacy'], icon='ri-database-2-line', color=COLOR,
    tagline='Plan and run a speech data collection the right way.',
    description='Design prompts, speaker sampling, consent and metadata for an African-language speech dataset — the coordinator\'s view.',
    foundation=FOUNDATION,
    core=lesson('Designing a collection', 'Plan a balanced, ethical speech collection.',
                ['A good speech dataset is balanced: many speakers (not a few speakers recording for hours), a spread of genders, '
                 'age ranges, regions and dialects, and a mix of quiet and realistic environments. Prompts should cover the '
                 'language\'s sounds and vocabulary, including numbers, names and common phrases.',
                 'Ethics are part of the design: informed consent in a language the speaker understands, a clear explanation '
                 'of use, the right to withdraw, fair pay where applicable, and no personal identifiers in data or metadata.'],
                points=['Many speakers > many hours from few speakers.', 'Balance gender, age, region, dialect, environment.',
                        'Prompts should cover sounds, numbers, names and common phrases.', 'Consent in the speaker\'s language; right to withdraw.'],
                quiz=[q('Which dataset is better balanced?', '200 speakers × 15 minutes', '5 speakers × 10 hours', '1 speaker × 50 hours', '2 speakers, studio only',
                        why='Speaker diversity.'),
                      q('Consent should be explained…', 'in a language the speaker understands', 'only in English', 'after recording', 'not at all for public data',
                        why='Informed consent.'),
                      q('A speaker asks to withdraw after recording. You…', 'remove their recordings as promised', 'refuse — they already agreed',
                        'keep them anonymously', 'charge them a fee', why='Right to withdraw.')]),
    workflow=workflow_lesson('speech data collection', ['Define the target speakers and quotas.', 'Write and review prompts.',
                             'Prepare consent and metadata forms.', 'Pilot with 3 speakers and fix problems.', 'Run collection and monitor quotas and quality.'],
                             ['Few speakers, many hours', 'Unbalanced gender or region', 'Consent only in English', 'Collecting names in metadata'],
                             'The dataset represents its speakers fairly and every speaker gave informed consent.'),
    practice=task('Collection design decisions', 'Decide whether each plan is acceptable.',
                  labeling(choice_items('ok', 'Acceptable?', ['Acceptable', 'Not acceptable'], [
                      ('Recruit 150 speakers across 6 states, 15 minutes each.', 'Acceptable'),
                      ('Collect each speaker\'s full name and phone number in the metadata file.', 'Not acceptable'),
                      ('Explain consent only in English to Hausa-only speakers.', 'Not acceptable'),
                      ('Pilot the prompts with 3 speakers before launching.', 'Acceptable')]),
                           ['Judge each plan against balance, consent and privacy.']), minutes=10),
    assessment=task('Speech collection assessment', 'Judge collection plans and justify one decision.',
                    labeling(choice_items('ok', 'Acceptable?', ['Acceptable', 'Not acceptable'], [
                        ('One volunteer records 20 hours alone to reach the target faster.', 'Not acceptable'),
                        ('Speakers can withdraw and have their recordings deleted.', 'Acceptable'),
                        ('Prompts include numbers, place names and everyday phrases.', 'Acceptable'),
                        ('Store consent forms in the same public folder as the audio.', 'Not acceptable'),
                        ('Track quotas for gender, age range and region during collection.', 'Acceptable')]),
                             ['Judge each plan against balance, consent and privacy.'],
                             report={'label': 'Why is "one volunteer records 20 hours" a problem?', 'min_words': 15}, ai_feedback=True), minutes=12),
    project_brief=project('Speech collection plan', 'Write a collection plan for a 50-speaker dataset in a language you know.',
                          ['Target speaker quotas', '30 sample prompts', 'Consent text in plain language', 'Metadata fields (no identifiers)', 'Quality checks'],
                          ['Balanced, realistic plan', 'Ethical consent and privacy', 'Good prompt coverage'],
                          ['Speech data collection', 'Data privacy'], difficulty='intermediate', hours=3),
    hours=4,
)

_QC_OPTS = ['Accept', 'Reject: clipped', 'Reject: too quiet', 'Reject: background noise', 'Reject: mostly silence']

QUALITY_CHECK = skill(
    'speech-quality-checking', 'Speech Quality Checking', level='intermediate',
    tags=['speech-data', 'qa'], icon='ri-equalizer-line', color=COLOR,
    tagline='Accept or reject recordings using objective audio-quality checks.',
    description='Learn the measurements audio QA uses — level, peak, clipping, signal-to-noise, silence — and apply them consistently.',
    foundation=FOUNDATION,
    core=lesson('Reading audio-quality measurements', 'Make accept/reject decisions from audio measurements.',
                ['QA tools report a few numbers for each recording. <strong>Peak</strong> and <strong>clipping %</strong> show whether it '
                 'was too loud; <strong>RMS level (dBFS)</strong> shows average loudness (speech is usually around −30 to −18 dBFS; below '
                 '−40 is too quiet); <strong>SNR</strong> (signal-to-noise ratio, dB) shows how much louder the voice is than the background '
                 '(under ~15 dB is noisy); <strong>silence %</strong> shows how much of the file has no speech.',
                 'Checks are applied in a fixed order so that two reviewers reach the same decision: clipping, then level, then noise, then silence.'],
                points=['Clipping > 0.5% → reject.', 'RMS below −40 dBFS → too quiet.', 'SNR below 15 dB → too noisy.', 'Silence above 70% → reject.'],
                quiz=[q('RMS −52 dBFS means the recording is…', 'too quiet', 'clipped', 'perfect', 'noisy', why='Below −40 dBFS.'),
                      q('SNR of 8 dB means…', 'background noise is close to the voice level', 'perfect audio', 'clipping', 'silence',
                        why='Low SNR = noisy.'),
                      q('Why apply checks in a fixed order?', 'So different reviewers reach the same decision', 'It is faster', 'The tool requires it', 'No reason',
                        why='Consistency.')]),
    workflow=workflow_lesson('speech quality checking', ['Read the thresholds.', 'Check clipping.', 'Check level.', 'Check SNR.', 'Check silence.', 'Record the first failing reason.'],
                             ['Rejecting good files on "feel"', 'Checking in random order', 'Ignoring clipping in loud speakers'],
                             'Every decision follows from the measurements and thresholds.'),
    practice=task('Accept or reject recordings', 'Use the measurements and thresholds to decide.',
                  labeling(choice_items('decision', 'Decision', _QC_OPTS, [
                      ('Clip 0.0% · RMS −24 dBFS · SNR 32 dB · Silence 25%', 'Accept'),
                      ('Clip 3.1% · RMS −14 dBFS · SNR 30 dB · Silence 20%', 'Reject: clipped'),
                      ('Clip 0.0% · RMS −48 dBFS · SNR 20 dB · Silence 30%', 'Reject: too quiet'),
                      ('Clip 0.0% · RMS −26 dBFS · SNR 9 dB · Silence 22%', 'Reject: background noise')]),
                           ['Order: clipping (>0.5%), level (<−40 dBFS), noise (SNR <15 dB), silence (>70%).',
                            'Give the FIRST failing reason.']), minutes=10),
    assessment=task('Speech quality assessment', 'Decide six recordings.',
                    labeling(choice_items('decision', 'Decision', _QC_OPTS, [
                        ('Clip 0.1% · RMS −22 dBFS · SNR 28 dB · Silence 35%', 'Accept'),
                        ('Clip 0.0% · RMS −30 dBFS · SNR 25 dB · Silence 88%', 'Reject: mostly silence'),
                        ('Clip 1.2% · RMS −45 dBFS · SNR 10 dB · Silence 20%', 'Reject: clipped'),
                        ('Clip 0.0% · RMS −43 dBFS · SNR 12 dB · Silence 30%', 'Reject: too quiet'),
                        ('Clip 0.0% · RMS −28 dBFS · SNR 14 dB · Silence 40%', 'Reject: background noise'),
                        ('Clip 0.4% · RMS −20 dBFS · SNR 18 dB · Silence 60%', 'Accept')]),
                        ['Order: clipping (>0.5%), level (<−40 dBFS), noise (SNR <15 dB), silence (>70%).',
                         'Give the FIRST failing reason.']), minutes=12),
    project_brief=project('Quality-check a recording batch', 'Record or gather 10 of your own takes with deliberate variety (quiet, loud, noisy). Check each one.',
                          ['Folder link', 'Table: file, your measurements or observations, decision, reason', 'Lessons for contributors (5 tips)'],
                          ['Decisions follow the thresholds', 'Clear table', 'Practical tips'], ['Speech quality checking'],
                          difficulty='intermediate', hours=2),
    hours=4,
)

AUDIO_VALIDATION = skill(
    'audio-validation', 'Audio Validation', level='beginner',
    tags=['speech-data', 'qa', 'annotation'], icon='ri-checkbox-circle-line', color=COLOR,
    tagline='Check that each recording really matches its prompt.',
    description='Validate crowd-sourced recordings: does the audio match the prompt, is it complete, one speaker, and in the right language?',
    foundation=FOUNDATION,
    core=lesson('Validating recordings against prompts', 'Decide whether a recording is valid for its prompt.',
                ['Crowd-sourced datasets (like community voice projects) rely on validators who listen to each clip and vote valid or '
                 'invalid. A clip is invalid if the words differ from the prompt, it is cut off, it contains a second voice, it is in '
                 'the wrong language, or it is unintelligible.',
                 'Accent, dialect and natural pronunciation are NOT reasons to reject — the dataset needs that variety. Only reject '
                 'for the reasons in the guideline.'],
                points=['Invalid: wrong words, cut off, two speakers, wrong language, unintelligible.',
                        'Valid even with: a strong accent, a regional pronunciation, a slow pace.',
                        'When unsure, follow the guideline\'s tie-break rule (often: skip).', 'Never reject for accent.'],
                quiz=[q('A speaker reads the prompt correctly with a strong regional accent. The clip is…', 'valid', 'invalid', 'invalid unless re-recorded', 'skipped always',
                        why='Variety is wanted.'),
                      q('The last word is cut off. The clip is…', 'invalid', 'valid', 'valid if the rest is good', 'valid if short',
                        why='Incomplete.'),
                      q('A second person speaks in the background over the prompt. The clip is…', 'invalid', 'valid', 'valid if quiet', 'irrelevant',
                        why='One speaker per clip.')]),
    workflow=workflow_lesson('audio validation', ['Read the prompt.', 'Listen to the whole clip.', 'Compare words exactly.',
                             'Check completeness, single speaker and language.', 'Vote, using only guideline reasons.'],
                             ['Rejecting for accent', 'Accepting clips with a changed word', 'Not listening to the end'],
                             'Votes follow the guideline exactly; accent never affects them.'),
    practice=task('Validate clips', 'Each line shows the prompt and what was heard. Decide.',
                  labeling(choice_items('valid', 'Decision', ['Valid', 'Invalid'], [
                      ('Prompt: "The market opens at seven." Heard: "The market opens at seven." (strong Ibadan accent)', 'Valid'),
                      ('Prompt: "Please call me tonight." Heard: "Please call me tomorrow."', 'Invalid'),
                      ('Prompt: "Ina kwana?" Heard: "Ina kwa—" (cut off)', 'Invalid'),
                      ('Prompt: "How you dey?" Heard: "How you dey?" (spoken slowly)', 'Valid')]),
                           ['Invalid only for: wrong words, cut off, second speaker, wrong language, unintelligible.']), minutes=8),
    assessment=task('Audio validation assessment', 'Validate six clips and give the reason when invalid.',
                    labeling([
                        {'id': f'v{i}', 'text': t, 'fields': [{'name': 'reason', 'label': 'Decision', 'type': 'choice',
                                                                'options': ['Valid', 'Wrong words', 'Cut off', 'Second speaker', 'Wrong language'],
                                                                'expected': e}]}
                        for i, (t, e) in enumerate([
                            ('Prompt: "Ẹ káàárọ̀." Heard: "Ẹ káàárọ̀." (clear)', 'Valid'),
                            ('Prompt: "Na gode." Heard: "Thank you."', 'Wrong language'),
                            ('Prompt: "Abeg make we go." Heard: "Abeg make we go." + a child shouting over it', 'Second speaker'),
                            ('Prompt: "Mo fẹ́ jẹun." Heard: "Mo fẹ́ jẹun." (Ekiti accent)', 'Valid'),
                            ('Prompt: "Biko nye m mmiri." Heard: "Biko nye m—"', 'Cut off'),
                            ('Prompt: "The bus is late." Heard: "The car is late."', 'Wrong words')], 1)],
                        ['Accent and dialect are never reasons to reject.']), minutes=10),
    project_brief=project('Validation log', 'Record 10 clips of a friend reading prompts (with consent), including a few deliberate mistakes, then validate them all.',
                          ['Folder link', 'Validation log: prompt, decision, reason', 'Agreement check: ask the friend to validate too and compare'],
                          ['Correct decisions', 'Reasons from the guideline only', 'Agreement analysis'], ['Audio validation'], hours=2),
    hours=3,
)

SKILLS = [VOICE, DATA_COLLECTION, SCRIPTED, CONVERSATIONAL, PRONUNCIATION, ACCENT, QUALITY_CHECK, AUDIO_VALIDATION]
