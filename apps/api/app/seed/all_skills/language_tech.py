"""Language Technology category, with an explicit beginner -> advanced progression:
Python for NLP -> NLP Fundamentals -> Dataset Creation -> Corpus Creation -> Natural
Language Processing (also sequenced as a CareerTrack in __init__.py).
"""
from ._common import q, lesson, workflow_lesson, task, labeling, choice_items, number_item, project, skill

COLOR = '#1d4ed8'

FOUNDATION = lesson(
    'Language technology for African languages',
    'See the main technologies and why African languages need specialists.',
    [
        'Language technology covers the systems that process human language: text NLP (classification, NER, search), speech '
        'recognition (ASR), text-to-speech (TTS), machine translation (MT) and large language models (LLMs). For most African '
        'languages these systems are weaker because there is less clean, labelled data — the "low-resource" problem.',
        'Community efforts such as Masakhane have shown that native speakers who can also handle data and code make the biggest '
        'difference. You don\'t need to be a research scientist: building clean datasets, evaluation sets and small tools is '
        'valuable work.',
    ],
    points=['Low-resource = little digital data, not a "simple" language.', 'Data quality often matters more than model size.',
            'Unicode normalisation is essential for diacritics.', 'Evaluation sets in your language are a real contribution.'],
    quiz=[
        q('"Low-resource language" means…', 'little digital/labelled data exists for it', 'it has a simple grammar', 'few people speak it', 'it has no writing system',
          why='Yoruba has tens of millions of speakers but little data.'),
        q('Which often improves a low-resource system the most?', 'More clean, well-labelled data', 'A new logo', 'Longer prompts', 'Removing diacritics',
          why='Data quality.'),
        q('Why does Unicode normalisation matter for Yoruba text?', 'The same letter with diacritics can be encoded in different ways', 'It translates text', 'It removes tones', 'It doesn\'t',
          why='NFC vs NFD.'),
    ],
)


def _tech_skill(slug, name, *, level, icon, tags, tagline, description, core, steps, mistakes, quality,
                practice_items, assessment_items, guidelines, project_brief, hours=6, report=None):
    return skill(
        slug, name, level=level, tags=['technology', 'nlp'] + tags, icon=icon, color=COLOR, tagline=tagline,
        description=description, foundation=FOUNDATION, core=core,
        workflow=workflow_lesson(name, steps, mistakes, quality),
        practice=task(f'{name}: exercises', 'Work through each exercise.', labeling(practice_items, guidelines), minutes=20),
        assessment=task(f'{name} assessment', 'Scored exercises.', labeling(assessment_items, guidelines, report=report, ai_feedback=bool(report)), minutes=25),
        project_brief=project_brief, hours=hours,
    )


def _text(iid, prompt, label, expected, context=None):
    item = {'id': iid, 'text': prompt, 'fields': [{'name': 'v', 'label': label, 'type': 'text', 'expected': expected}]}
    if context:
        item['context'] = context
    return item


PYTHON = _tech_skill(
    'python-for-nlp', 'Python for NLP', level='beginner', icon='ri-terminal-box-line', tags=['python'],
    tagline='The Python you need to process African-language text.',
    description='Strings, lists, dictionaries, files and Unicode normalisation in Python — the toolkit for cleaning and counting Yoruba, Igbo, Hausa and Pidgin text.',
    core=lesson('Strings, Unicode and counting in Python', 'Process text with Python safely, diacritics included.',
                ['Python strings are Unicode, but the same visible letter can be stored differently: "ọ̀" can be one precomposed character plus '
                 'a combining accent, or "o" plus two combining marks. Always normalise with <code>unicodedata.normalize("NFC", text)</code> '
                 'before comparing or counting.',
                 'Core tools: <code>text.lower()</code>, <code>text.split()</code> for tokens, <code>collections.Counter</code> for '
                 'frequencies, and reading files with <code>open(path, encoding="utf-8")</code> — never rely on the default encoding on Windows.'],
                points=['Normalise to NFC before comparing.', 'Open files with encoding="utf-8".', 'Counter(tokens).most_common(10) gives top words.',
                        'split() with no argument splits on any whitespace.'],
                example='import unicodedata\nfrom collections import Counter\ntext = unicodedata.normalize("NFC", open("yo.txt", encoding="utf-8").read())\nprint(Counter(text.lower().split()).most_common(5))',
                quiz=[q('Why call unicodedata.normalize("NFC", text)?', 'So identical-looking letters are stored the same way', 'To translate it', 'To remove accents', 'To speed it up',
                        why='Consistent encoding.'),
                      q('Safest way to open a Yoruba text file?', 'open(path, encoding="utf-8")', 'open(path)', 'open(path, "rb") and print', 'Copy-paste into Excel', why='Explicit UTF-8.'),
                      q('"a b  c".split() returns…', "['a', 'b', 'c']", "['a', 'b', '', 'c']", "'abc'", "['a b c']", why='Any whitespace.')]),
    steps=['Read the file as UTF-8.', 'Normalise to NFC.', 'Lower-case if the task allows.', 'Tokenise.', 'Count / transform.', 'Write output as UTF-8.'],
    mistakes=['Default file encoding', 'Comparing un-normalised strings', 'Lower-casing when case matters'],
    quality='Scripts give the same result on any machine for any diacritic encoding.',
    practice_items=[number_item('p1', 'What does len("How you dey".split()) return?', 'Result', 3),
                    number_item('p2', 'What does "abeg make we go".count("e") return?', 'Result', 3),
                    _text('p3', 'What does " ".join(["mo", "fẹ́", "jẹun"]) return?', 'Result (without quotes)', 'mo fẹ́ jẹun'),
                    number_item('p4', 'What does len("Ẹ káàárọ̀".split()) return?', 'Result', 2)],
    assessment_items=[number_item('a1', 'len(unicodedata.normalize("NFC", "ọjà")) returns?', 'Result', 3),
                      number_item('a2', 'len(unicodedata.normalize("NFD", "ọjà")) returns? (ọ and à each decompose into 2)', 'Result', 5),
                      _text('a3', 'sorted(set("the market is busy and the market is loud".split()))[0] returns?', 'Result (without quotes)', 'and'),
                      number_item('a4', 'Counter("the market is busy and the market is loud".split())["market"] returns?', 'Result', 2),
                      _text('a5', '"Wetin Dey Happen".lower() returns?', 'Result (without quotes)', 'wetin dey happen')],
    guidelines=['Work out the result as Python 3 would print it.', 'Assume "import unicodedata" and "from collections import Counter".'],
    project_brief=project('Yoruba word-frequency script', 'Write a Python script that reads a UTF-8 text file in a Nigerian language, normalises it, and prints the top 20 words with counts.',
                          ['Script in the code workspace', 'A sample input text (public domain)', 'Output and a note on any normalisation issue you hit'],
                          ['Correct normalisation and UTF-8 handling', 'Clean, readable code', 'Correct output'],
                          ['Python', 'Text processing'], hours=3, workspace='developer'),
)

NLP_FUND = _tech_skill(
    'nlp-fundamentals', 'NLP Fundamentals', level='beginner', icon='ri-brain-line', tags=[],
    tagline='Tokenisation, stop words, stemming and text representations explained.',
    description='The core concepts of natural language processing — tokenisation, normalisation, stop words, lemmas, bag-of-words and embeddings — with African-language pitfalls.',
    core=lesson('From text to features', 'Explain how text becomes something a model can use.',
                ['NLP pipelines turn text into numbers. Steps include <strong>tokenisation</strong> (splitting into words or sub-words), '
                 '<strong>normalisation</strong> (case, Unicode), optional <strong>stop-word</strong> removal, and representation as '
                 '<strong>bag-of-words</strong> counts, TF-IDF weights, or dense <strong>embeddings</strong>.',
                 'African languages add pitfalls: stripping diacritics merges different Yoruba words; English stop-word lists are useless for '
                 'Hausa; and sub-word tokenisers trained mostly on English split Igbo words into many tiny pieces.'],
                points=['Tokenisation choices change everything downstream.', 'Never strip diacritics to "simplify" Yoruba.',
                        'Stop-word lists are language-specific.', 'Embeddings place similar words near each other.'],
                quiz=[q('Removing Yoruba tone marks before training causes…', 'different words to merge', 'better accuracy always', 'nothing', 'faster translation',
                        why='ọkọ/ọkọ̀/ọkọ́ collapse.'),
                      q('Bag-of-words represents a text as…', 'word counts, ignoring order', 'a picture', 'a single number', 'its translation', why='Counts.'),
                      q('An English stop-word list applied to Hausa text…', 'won\'t remove Hausa function words', 'works perfectly', 'translates it', 'adds tones',
                        why='Language-specific.')]),
    steps=['Inspect raw text.', 'Choose tokenisation.', 'Normalise.', 'Decide on stop words.', 'Choose a representation.'],
    mistakes=['Stripping diacritics', 'Using English resources for other languages', 'Ignoring tokenisation effects'],
    quality='Every preprocessing step is justified for the language.',
    practice_items=choice_items('a', 'Answer', ['Tokenisation', 'Normalisation', 'Stop-word removal', 'Embedding'], [
        ('Splitting "Mo fẹ́ jẹun" into ["Mo", "fẹ́", "jẹun"]', 'Tokenisation'), ('Converting all text to NFC and lower case', 'Normalisation'),
        ('Dropping very common words like "the", "is"', 'Stop-word removal'), ('Representing "king" as a 300-number vector', 'Embedding')]),
    assessment_items=[
        *choice_items('a', 'Good idea?', ['Yes', 'No'], [
            ('Strip all Yoruba diacritics to reduce vocabulary size.', 'No'), ('Build a Hausa stop-word list from Hausa text frequencies.', 'Yes'),
            ('Normalise text to NFC before counting words.', 'Yes'), ('Apply an English lemmatiser to Igbo text.', 'No')]),
        number_item('n1', 'Bag-of-words: how many distinct words in "abeg abeg make we go"?', 'Count', 4)],
    guidelines=['Choose the best answer for each item.'],
    project_brief=project('Preprocessing notebook', 'Write a short notebook or script that tokenises, normalises and counts words in a Nigerian-language text, with a stop-word list you derive from the data.',
                          ['Code', 'Derived stop-word list (top function words)', 'Before/after vocabulary sizes and a note on diacritics'],
                          ['Correct preprocessing', 'Language-aware decisions', 'Clear explanation'], ['NLP fundamentals'], hours=3, workspace='developer'),
)

NLP = _tech_skill(
    'natural-language-processing', 'Natural Language Processing', level='advanced', icon='ri-node-tree', tags=['ai'],
    tagline='Build and evaluate NLP models for African-language tasks.',
    description='Text classification and NER pipelines, transfer learning with multilingual African models, and honest evaluation with precision, recall and F1.',
    core=lesson('Models, transfer and evaluation', 'Build and evaluate a low-resource NLP model.',
                ['For low-resource languages, the practical approach is <strong>transfer learning</strong>: start from a pre-trained '
                 'multilingual model that includes African languages (for example AfriBERTa or AfroXLMR) and fine-tune it on a small labelled '
                 'dataset for your task.',
                 'Evaluate on a held-out test set with <strong>precision</strong> (of the predicted positives, how many are right), '
                 '<strong>recall</strong> (of the true positives, how many were found) and <strong>F1</strong> (their harmonic mean). '
                 'Accuracy alone misleads on unbalanced data.'],
                points=['Precision = TP / (TP + FP).', 'Recall = TP / (TP + FN).', 'F1 = 2PR / (P + R).', 'Never tune on the test set.'],
                quiz=[q('TP = 8, FP = 2. Precision?', '0.8', '0.2', '0.6', '1.0', why='8/10.'),
                      q('Why not just report accuracy on unbalanced data?', 'A model predicting the majority class can look good while being useless', 'Accuracy is illegal',
                        'It is always too low', 'It ignores the test set', why='Class imbalance.'),
                      q('Fine-tuning a multilingual pre-trained model on your task is…', 'transfer learning', 'tokenisation', 'data cleaning', 'stemming', why='Transfer.')]),
    steps=['Define the task and labels.', 'Split train/dev/test.', 'Fine-tune a multilingual model.', 'Tune on dev only.', 'Report P/R/F1 on test.', 'Analyse errors.'],
    mistakes=['Tuning on the test set', 'Reporting only accuracy', 'No error analysis'], quality='Results are reproducible and honestly reported.',
    practice_items=[number_item('p1', 'TP = 8, FP = 2, FN = 4. Precision?', 'Precision (3 decimals)', 0.8, 0.005),
                    number_item('p2', 'TP = 8, FP = 2, FN = 4. Recall?', 'Recall (3 decimals)', 0.667, 0.005),
                    number_item('p3', 'TP = 8, FP = 2, FN = 4. F1?', 'F1 (3 decimals)', 0.727, 0.005)],
    assessment_items=[number_item('a1', 'TP = 45, FP = 5, FN = 15. Precision?', 'Precision (3 decimals)', 0.9, 0.005),
                      number_item('a2', 'TP = 45, FP = 5, FN = 15. Recall?', 'Recall (3 decimals)', 0.75, 0.005),
                      number_item('a3', 'TP = 45, FP = 5, FN = 15. F1?', 'F1 (3 decimals)', 0.818, 0.005),
                      *choice_items('c', 'Good practice?', ['Yes', 'No'], [
                          ('Choose hyperparameters by the best test-set score.', 'No'),
                          ('Start from a multilingual model that includes your language.', 'Yes')])],
    guidelines=['Round to 3 decimals.', 'Answer the practice questions from the definitions.'],
    report={'label': 'Explain the precision/recall trade-off for a scam-SMS detector', 'min_words': 25},
    project_brief=project('Train a small African-language classifier', 'Fine-tune (or train a simple baseline for) a text classifier on a public African-language dataset (e.g. a sentiment or news-topic set).',
                          ['Code or notebook link', 'Data splits and sizes', 'P/R/F1 on test', 'Error analysis of 10 mistakes'],
                          ['Sound methodology', 'Honest evaluation', 'Insightful error analysis'], ['NLP', 'Model evaluation'],
                          difficulty='advanced', hours=8, workspace='developer'),
    hours=10,
)

ASR = _tech_skill(
    'speech-recognition', 'Speech Recognition', level='intermediate', icon='ri-mic-2-line', tags=['speech-data', 'ai'],
    tagline='How ASR works, what data it needs, and how it is measured.',
    description='Automatic speech recognition for African languages: acoustic and language models, data requirements, WER and common failure modes.',
    core=lesson('Inside an ASR system', 'Explain how ASR works and fails.',
                ['An ASR system maps audio to text. Modern systems (e.g. Whisper-style or wav2vec-style models) learn from paired audio and '
                 'transcripts; many can be fine-tuned on a few hours of a new language. A language model helps pick likely word sequences.',
                 'ASR fails on accents and languages under-represented in training, on noisy audio, on code-switching and on names. It is '
                 'measured with WER on a held-out test set that matches real users.'],
                points=['Training data = audio + accurate transcripts.', 'Fine-tuning on a few hours can help a new language a lot.',
                        'WER = (S + D + I) / N on a representative test set.', 'Test sets must include real accents and noise.'],
                quiz=[q('What does ASR training data consist of?', 'Audio paired with accurate transcripts', 'Only audio', 'Only text', 'Images',
                        why='Paired data.'),
                      q('An ASR test set recorded only in a studio by one speaker will…', 'overestimate real-world accuracy', 'be perfect', 'underestimate it', 'not matter',
                        why='Not representative.'),
                      q('Reference 20 words, 3 errors total. WER?', '0.15', '0.3', '0.03', '3', why='3/20.')]),
    steps=['Collect representative audio.', 'Transcribe accurately.', 'Split by speaker.', 'Fine-tune.', 'Evaluate WER per group (accent, noise).'],
    mistakes=['Same speakers in train and test', 'Unrepresentative test sets', 'Ignoring code-switching'], quality='WER is reported honestly per user group.',
    practice_items=[number_item('p1', 'Reference 20 words, 3 errors.', 'WER (decimal)', 0.15, 0.001),
                    *choice_items('c', 'Good practice?', ['Yes', 'No'], [('Put the same speakers in train and test.', 'No'),
                                                                         ('Include noisy, real-world audio in the test set.', 'Yes')])],
    assessment_items=[number_item('a1', 'Reference 40 words; 4 substitutions, 2 deletions, 2 insertions.', 'WER (decimal)', 0.2, 0.001),
                      *choice_items('c', 'Most likely cause', ['Accent/language not in training', 'Noisy audio', 'Code-switching', 'Unknown names'], [
                          ('ASR writes "a cagey" for "Ikeja".', 'Unknown names'),
                          ('Accuracy drops sharply for Hausa speakers but not American English speakers.', 'Accent/language not in training'),
                          ('Errors cluster in recordings made beside a generator.', 'Noisy audio'),
                          ('Yoruba words inside English sentences come out as English nonsense.', 'Code-switching')])],
    guidelines=['Use the definitions from the lesson.'],
    project_brief=project('ASR accuracy check in your language', 'Test a free ASR tool (e.g. phone dictation) on 10 sentences you read in Nigerian English or a Nigerian language.',
                          ['Your 10 references and the ASR outputs', 'WER per sentence and overall', 'Error categories and recommendations'],
                          ['Correct WER', 'Clear error categories', 'Useful recommendations'], ['Speech recognition evaluation'], difficulty='intermediate', hours=3),
)

TTS = _tech_skill(
    'text-to-speech', 'Text-to-Speech', level='intermediate', icon='ri-volume-up-line', tags=['speech-data', 'ai'],
    tagline='How TTS turns text into speech — normalisation, pronunciation, tone.',
    description='Text-to-speech pipelines for African languages: text normalisation, grapheme-to-phoneme conversion, tone, and voice data needs.',
    core=lesson('The TTS pipeline', 'Explain TTS stages and prepare text for them.',
                ['A TTS system first <strong>normalises</strong> text (₦500 → "five hundred naira", Dr. → "doctor"), then converts letters to '
                 'sounds (<strong>grapheme-to-phoneme</strong>), predicts prosody (and tone, in tonal languages), and generates audio with a '
                 'neural vocoder.',
                 'Yoruba TTS depends on tone-marked input: without diacritics, the system has to guess tones and often gets them wrong. '
                 'Training a voice needs hours of clean, consistent studio-quality recordings from one speaker.'],
                points=['Normalisation expands numbers, currency, abbreviations.', 'G2P maps spelling to sounds.',
                        'Tone-marked input = correct tones.', 'One consistent voice, many clean hours.'],
                quiz=[q('"₦500" should be normalised to…', 'five hundred naira', '500 N', 'naira five hundred', 'N five zero zero', why='Spoken form.'),
                      q('Yoruba TTS input without tone marks leads to…', 'guessed (often wrong) tones', 'perfect speech', 'faster speech', 'no speech', why='Ambiguity.'),
                      q('Converting spelling to sounds is called…', 'grapheme-to-phoneme', 'normalisation', 'vocoding', 'tokenisation', why='G2P.')]),
    steps=['Normalise text.', 'Check tone marks/diacritics.', 'Run G2P.', 'Synthesize.', 'Listen-test with native speakers.'],
    mistakes=['Unnormalised numbers', 'Untoned Yoruba input', 'Mixed-quality voice data'], quality='Output is intelligible, natural and correctly toned.',
    practice_items=[_text('p1', 'Normalise for TTS: "₦500"', 'Spoken form', 'five hundred naira'),
                    _text('p2', 'Normalise for TTS: "Dr. Bello"', 'Spoken form', 'doctor bello'),
                    *choice_items('c', 'Pipeline stage', ['Text normalisation', 'Grapheme-to-phoneme', 'Vocoder'], [
                        ('Turns "No. 5" into "number five"', 'Text normalisation'), ('Generates the audio waveform', 'Vocoder')])],
    assessment_items=[_text('a1', 'Normalise for TTS: "₦2,000"', 'Spoken form', 'two thousand naira'),
                      _text('a2', 'Normalise for TTS: "5 km"', 'Spoken form', ['five kilometres', 'five kilometers']),
                      *choice_items('c', 'Pipeline stage', ['Text normalisation', 'Grapheme-to-phoneme', 'Vocoder'], [
                          ('Maps "ọkọ̀" to its phonemes and tones', 'Grapheme-to-phoneme'), ('Expands "St." to "street"', 'Text normalisation'),
                          ('Produces the final sound', 'Vocoder')])],
    guidelines=['Write spoken forms in lower case words.'],
    project_brief=project('TTS text-normalisation rules', 'Write normalisation rules for a Nigerian language or Nigerian English TTS: numbers, currency, dates, abbreviations, with 20 test cases.',
                          ['Rule list', '20 input → spoken-form test cases', 'Edge cases you couldn\'t resolve'],
                          ['Correct rules', 'Good coverage', 'Honest edge cases'], ['TTS text normalisation'], difficulty='intermediate', hours=3),
)

MT = _tech_skill(
    'machine-translation', 'Machine Translation', level='intermediate', icon='ri-translate', tags=['translation', 'ai'],
    tagline='How MT systems are built and improved for low-resource languages.',
    description='Neural machine translation for African languages: parallel data, back-translation, multilingual models, evaluation and domain shift.',
    core=lesson('Building MT for low-resource languages', 'Explain the main techniques for low-resource MT.',
                ['Neural MT learns from <strong>parallel corpora</strong> (sentence pairs). African languages have few, so researchers use '
                 '<strong>back-translation</strong> (translate monolingual target text into the source with an existing model to create synthetic '
                 'pairs), <strong>multilingual models</strong> that share knowledge across languages (e.g. NLLB-style models), and careful '
                 'evaluation with chrF/BLEU plus human judgement.',
                 'Systems trained on religious texts (a common source of African parallel data) perform badly on news or health — '
                 '<strong>domain shift</strong>.'],
                points=['Parallel corpus = aligned sentence pairs.', 'Back-translation creates synthetic training pairs.',
                        'Multilingual models transfer across languages.', 'Domain shift: training domain ≠ use domain.'],
                quiz=[q('Translating monolingual Yoruba into English with an existing model to make training pairs is…', 'back-translation', 'tokenisation',
                        'domain shift', 'evaluation', why='Synthetic data.'),
                      q('A model trained on Bible text struggles with health news because of…', 'domain shift', 'tokenisation', 'back-translation', 'chrF', why='Different domain.'),
                      q('A parallel corpus contains…', 'aligned sentence pairs in two languages', 'one language only', 'audio', 'images', why='Pairs.')]),
    steps=['Gather parallel and monolingual data.', 'Clean and align.', 'Start from a multilingual model.', 'Add back-translated data.', 'Evaluate in the target domain.'],
    mistakes=['Evaluating only on training-domain text', 'Unaligned pairs', 'Trusting BLEU alone'], quality='Gains are demonstrated in the real use domain with human checks.',
    practice_items=choice_items('t', 'Technique', ['Back-translation', 'Multilingual transfer', 'Data cleaning', 'Domain adaptation'], [
        ('Use an English→Hausa model to turn English news into synthetic Hausa–English pairs.', 'Back-translation'),
        ('Fine-tune a model trained on 200 languages for Igbo.', 'Multilingual transfer'),
        ('Remove misaligned sentence pairs.', 'Data cleaning'),
        ('Add health-domain pairs to a Bible-trained model.', 'Domain adaptation')]),
    assessment_items=choice_items('t', 'Best explanation', ['Domain shift', 'Misaligned data', 'Too little data', 'Metric limitation'], [
        ('A model scores well on scripture but poorly on SMS messages.', 'Domain shift'),
        ('Translations are fluent but about the wrong sentence, as if pairs were shuffled.', 'Misaligned data'),
        ('A correct translation scores low BLEU because it uses synonyms.', 'Metric limitation'),
        ('A new language with 2,000 sentence pairs performs poorly everywhere.', 'Too little data'),
        ('A model trained on news handles health leaflets badly.', 'Domain shift')]),
    guidelines=['Choose the best answer.'],
    project_brief=project('Mini parallel corpus', 'Create 100 aligned sentence pairs (English ↔ a Nigerian language) in a domain you choose (health, farming, finance), with a data card.',
                          ['The 100 pairs (CSV-style table)', 'Data card: source, domain, licence, translator notes', 'Plan for evaluating an MT system on it'],
                          ['Accurate alignment', 'Clear documentation', 'Sound evaluation plan'], ['Machine translation data'], difficulty='intermediate', hours=5),
)

LM = _tech_skill(
    'language-models', 'Language Models', level='intermediate', icon='ri-bar-chart-2-line', tags=['ai', 'llm'],
    tagline='Probabilities, tokens and perplexity — how language models work.',
    description='From n-gram models to transformers: next-token probability, tokenisation costs for African languages, and perplexity.',
    core=lesson('Predicting the next token', 'Compute and interpret language-model probabilities.',
                ['A language model assigns probabilities to sequences by predicting the next token: P(sentence) = P(w1) × P(w2|w1) × … . '
                 'Transformers do this with attention over a long context; n-gram models use only the last few words.',
                 '<strong>Perplexity</strong> measures how surprised a model is by real text (lower is better). Tokenisers trained mostly on '
                 'English split African-language words into many more tokens, making models slower, costlier and often worse in those languages.'],
                points=['Chain rule: multiply conditional probabilities.', 'Lower perplexity = better fit.', 'More tokens per word = higher cost.',
                        'Context window limits how much text the model sees.'],
                quiz=[q('P(a) = 0.5 and P(b|a) = 0.4. P(a b)?', '0.2', '0.9', '0.1', '0.45', why='0.5 × 0.4.'),
                      q('Lower perplexity means…', 'the model predicts the text better', 'the text is longer', 'the model is bigger', 'worse fit', why='Less surprise.'),
                      q('A Yoruba word split into 6 tokens vs an English word in 1 means…', 'Yoruba text costs more to process', 'Yoruba is simpler', 'nothing', 'English is longer',
                        why='Tokenisation inequity.')]),
    steps=['Tokenise.', 'Look up conditional probabilities.', 'Multiply (or add logs).', 'Compare models by perplexity on the same text.'],
    mistakes=['Adding probabilities instead of multiplying', 'Comparing perplexity across different tokenisers'], quality='Calculations follow the chain rule.',
    practice_items=[number_item('p1', 'P(a) = 0.5, P(b|a) = 0.4. P(a b)?', 'Probability', 0.2, 0.001),
                    number_item('p2', 'P(how) = 0.1, P(you|how) = 0.5, P(dey|how you) = 0.8. P(how you dey)?', 'Probability', 0.04, 0.001)],
    assessment_items=[number_item('a1', 'P(mo) = 0.2, P(fẹ́|mo) = 0.3, P(jẹun|mo fẹ́) = 0.5. P(mo fẹ́ jẹun)?', 'Probability', 0.03, 0.001),
                      number_item('a2', 'A sentence of 10 words needs 25 tokens. Tokens per word?', 'Ratio', 2.5, 0.01),
                      *choice_items('c', 'Answer', ['Lower', 'Higher'], [('Model A has perplexity 20, B has 35 on the same Hausa text. Which fits better: the one with lower or higher perplexity?', 'Lower')]),
                      *choice_items('d', 'True or false', ['True', 'False'], [('More tokens per word usually means higher cost per sentence.', 'True')])],
    guidelines=['Multiply conditional probabilities.'],
    project_brief=project('Tokenisation cost study', 'Use a public tokenizer (e.g. an online LLM tokenizer tool) on the same 10 sentences in English and a Nigerian language.',
                          ['Token counts per sentence in both languages', 'Tokens-per-word ratios', 'What this means for cost and quality'],
                          ['Careful measurement', 'Correct ratios', 'Clear implications'], ['Language models'], difficulty='intermediate', hours=2),
)

LLM_FUND = _tech_skill(
    'llm-fundamentals', 'LLM Fundamentals', level='beginner', icon='ri-sparkling-line', tags=['ai', 'llm'],
    tagline='What large language models can and can\'t do — and how to use them well.',
    description='Prompts, context, temperature, hallucination and limitations of LLMs, especially in African languages.',
    core=lesson('Using LLMs well', 'Understand LLM behaviour and limits.',
                ['LLMs generate text one token at a time from patterns in training data. They can draft, summarise, translate and explain, '
                 'but they <strong>hallucinate</strong> — produce confident, false statements — and are usually weaker in African languages.',
                 'Clear prompts with context and examples help. <strong>Temperature</strong> controls randomness (low = more predictable). '
                 'Everything important must be verified, and private data should not be pasted into public tools.'],
                points=['Hallucination: fluent but false.', 'Low temperature = more consistent output.', 'Give context and examples in prompts.',
                        'Verify facts; protect private data.'],
                quiz=[q('An LLM confidently cites a book that doesn\'t exist. This is…', 'hallucination', 'tokenisation', 'temperature', 'fine-tuning', why='Fabrication.'),
                      q('For consistent, factual output, set temperature…', 'low', 'high', 'randomly', 'it doesn\'t matter', why='Less randomness.'),
                      q('Should you paste a classmate\'s exam results into a public chatbot?', 'No — that is private data', 'Yes', 'Only at night', 'Only if anonymous chatbots', why='Privacy.')]),
    steps=['State the task clearly.', 'Give context and an example.', 'Set constraints (language, length).', 'Verify the output.'],
    mistakes=['Trusting output without checking', 'Vague prompts', 'Sharing private data'], quality='Outputs are verified and prompts are reproducible.',
    practice_items=choice_items('c', 'Answer', ['Hallucination', 'Good prompt practice', 'Privacy risk', 'Temperature effect'], [
        ('The model invents a quote from the Governor.', 'Hallucination'), ('Adding "Answer in Yoruba with full tone marks" to the prompt.', 'Good prompt practice'),
        ('Uploading customer phone numbers to a public chatbot.', 'Privacy risk'), ('Same prompt gives very different answers each time at 1.2.', 'Temperature effect')]),
    assessment_items=choice_items('c', 'Good practice?', ['Yes', 'No'], [
        ('Verify every date and name an LLM gives you.', 'Yes'), ('Cite an LLM as the source of a historical fact.', 'No'),
        ('Give the model an example of the output format you want.', 'Yes'), ('Assume Yoruba output is correct because it looks fluent.', 'No'),
        ('Use low temperature for data-labelling prompts.', 'Yes')]),
    guidelines=['Choose the best answer.'],
    project_brief=project('Prompt playbook for language work', 'Design 8 prompts that help with a language-data task (e.g. drafting annotation examples) and test them.',
                          ['The prompts', 'Sample outputs', 'What you had to verify or correct'], ['Clear prompts', 'Honest verification'],
                          ['LLM fundamentals'], hours=2),
    hours=4,
)

AI_RESEARCH = _tech_skill(
    'ai-assisted-linguistic-research', 'AI-Assisted Linguistic Research', level='intermediate', icon='ri-search-2-line', tags=['ai', 'linguistics'],
    tagline='Use AI tools in linguistic research responsibly and rigorously.',
    description='Use LLMs and NLP tools to speed up linguistic research — literature search, data exploration, draft glossing — while keeping rigour, citation and ethics.',
    core=lesson('Rigour with AI tools', 'Decide when AI help is appropriate in research.',
                ['AI tools can speed up research: finding candidate examples in a corpus, drafting glosses for a human to check, summarising '
                 'papers you have read, or writing analysis code. They cannot replace evidence: an LLM\'s claim about a language is not data.',
                 'Rigorous practice: verify everything against primary sources or native speakers, disclose AI use, never invent citations, and '
                 'protect participants\' data.'],
                points=['AI output is a draft, not evidence.', 'Verify with primary sources and speakers.', 'Disclose AI use in methods.',
                        'Never put participant data into public tools without consent.'],
                quiz=[q('An LLM says a Yoruba dialect has 7 tones. You…', 'check published sources and speakers before using it', 'cite the LLM',
                        'publish it', 'ignore all AI tools', why='Not evidence.'),
                      q('Using AI to draft glosses is acceptable if…', 'a linguist checks every gloss', 'never', 'you don\'t tell anyone', 'the AI is expensive',
                        why='Human verification.'),
                      q('In your methods section, AI assistance should be…', 'disclosed', 'hidden', 'exaggerated', 'irrelevant', why='Transparency.')]),
    steps=['Define the question.', 'Use AI for drafts and search.', 'Verify against primary sources.', 'Record what AI did.', 'Disclose.'],
    mistakes=['Citing AI as a source', 'Unverified AI glosses', 'Sharing participant data'], quality='Every claim traces to real evidence.',
    practice_items=choice_items('c', 'Acceptable?', ['Acceptable', 'Not acceptable'], [
        ('Using AI to write a script that counts word frequencies in your corpus.', 'Acceptable'),
        ('Citing an LLM\'s answer as evidence of a grammatical rule.', 'Not acceptable'),
        ('Asking AI to summarise a paper you have read, then checking the summary.', 'Acceptable'),
        ('Pasting interview recordings of named participants into a public AI tool without consent.', 'Not acceptable')]),
    assessment_items=choice_items('c', 'Acceptable?', ['Acceptable', 'Not acceptable'], [
        ('Letting AI invent example sentences and presenting them as speaker data.', 'Not acceptable'),
        ('Using AI-drafted glosses that a native-speaker linguist verified.', 'Acceptable'),
        ('Disclosing AI tools used in the methods section.', 'Acceptable'),
        ('Including AI-suggested references without checking they exist.', 'Not acceptable'),
        ('Using AI to search your own corpus for candidate examples.', 'Acceptable')]),
    guidelines=['Judge each use against research rigour and ethics.'],
    report={'label': 'Describe one way you would use AI in a linguistics project, and how you would verify it', 'min_words': 25},
    project_brief=project('AI-assisted mini study', 'Answer a small research question about a Nigerian language with AI help (e.g. finding reduplication patterns in a corpus), documenting every AI step and verification.',
                          ['Research question', 'Method with AI steps disclosed', 'Findings with verified examples', 'Limitations'],
                          ['Rigour', 'Transparency', 'Verified evidence'], ['AI-assisted research'], difficulty='intermediate', hours=4),
    hours=4,
)

CORPUS_CREATION = _tech_skill(
    'corpus-creation', 'Corpus Creation', level='intermediate', icon='ri-stack-line', tags=['dataset'],
    tagline='Build a clean, documented, legally usable text corpus.',
    description='Source, license, filter, deduplicate and document a corpus for an African language, ready for NLP use.',
    core=lesson('From web pages to a corpus', 'Plan a legal, clean, documented corpus.',
                ['Building a corpus means: choosing sources you\'re allowed to use (check licences and terms), collecting text, filtering by '
                 'language (language ID), removing boilerplate and duplicates, normalising Unicode, and documenting everything in a '
                 '<strong>data card/datasheet</strong>: sources, size, licence, language varieties, known biases.',
                 'Web-crawled African-language data is often noisy — wrong language, machine-translated pages, boilerplate. Quality filtering '
                 'matters more than raw size.'],
                points=['Licence first: only use text you may use.', 'Language-ID filter.', 'Remove boilerplate and duplicates; normalise.',
                        'Document in a data card.'],
                quiz=[q('First step before collecting web text?', 'Check licences/terms of use', 'Train a model', 'Translate it', 'Remove diacritics', why='Legality.'),
                      q('Why filter machine-translated pages?', 'They add unnatural language that models learn', 'They are too short', 'They are illegal', 'They have no words',
                        why='Quality.'),
                      q('A data card documents…', 'sources, size, licence, varieties and known biases', 'only the file name', 'the author\'s CV', 'nothing', why='Transparency.')]),
    steps=['Choose and license sources.', 'Collect.', 'Language-ID filter.', 'Clean and deduplicate.', 'Normalise.', 'Write the data card.'],
    mistakes=['Ignoring licences', 'Keeping boilerplate', 'No documentation'], quality='Anyone can see where every sentence came from and whether it may be used.',
    practice_items=choice_items('c', 'Keep in the corpus?', ['Keep', 'Remove'], [
        ('A Hausa news paragraph from a site with an open licence.', 'Keep'), ('"Accept cookies | Login | Subscribe" repeated on every page.', 'Remove'),
        ('An English paragraph in a Hausa corpus.', 'Remove'), ('The same Hausa paragraph appearing 40 times.', 'Remove')]),
    assessment_items=choice_items('c', 'Best action', ['Keep', 'Remove', 'Check licence first'], [
        ('Yoruba blog posts from a site with no stated licence.', 'Check licence first'), ('Clearly machine-translated Igbo product pages.', 'Remove'),
        ('Public-domain Yoruba folktales, cleaned and normalised.', 'Keep'), ('A navigation menu text block.', 'Remove'),
        ('Pidgin news under a Creative Commons licence.', 'Keep')]),
    guidelines=['Only keep clean, in-language text you are allowed to use.'],
    project_brief=project('Build a 5,000-word corpus with a data card', 'Build a small corpus for a Nigerian language from openly licensed sources.',
                          ['Corpus link (Drive/GitHub)', 'Cleaning steps', 'Data card: sources, licence, size, varieties, limitations'],
                          ['Legal sources', 'Clean text', 'Complete data card'], ['Corpus creation'], difficulty='intermediate', hours=5),
)

DATASET_CREATION = _tech_skill(
    'dataset-creation', 'Dataset Creation', level='intermediate', icon='ri-table-line', tags=['dataset'],
    tagline='Design labelled datasets: schema, labels, splits and documentation.',
    description='Design an NLP dataset end to end: task definition, schema, label guidelines, train/dev/test splits and a datasheet.',
    core=lesson('Designing a dataset', 'Design a dataset others can trust and reuse.',
                ['A dataset starts with a precise task definition and a schema (columns, types, allowed labels). Then: write label guidelines, '
                 'collect and label data, measure agreement, and split into <strong>train/dev/test</strong> — with no overlap, and ideally '
                 'stratified so each split has a similar label balance.',
                 'Common split: 80/10/10. Split by source or speaker when items from the same source are similar, to avoid leakage.'],
                points=['Schema: columns, types, label set.', 'Guidelines before labelling.', 'Splits: no overlap; stratify labels.',
                        'Split by speaker/source to avoid leakage.'],
                quiz=[q('1,000 items, 80/10/10 split. Test set size?', '100', '80', '10', '800', why='10%.'),
                      q('Why split by speaker for speech data?', 'To stop the model seeing test speakers in training', 'To save space', 'For alphabetical order', 'It is required by law',
                        why='Leakage.'),
                      q('Stratified splitting keeps…', 'similar label proportions in each split', 'the same items in every split', 'all items in train', 'only positives in test',
                        why='Balance.')]),
    steps=['Define the task.', 'Design the schema.', 'Write guidelines.', 'Label and measure agreement.', 'Split without leakage.', 'Write a datasheet.'],
    mistakes=['Labelling before guidelines', 'Overlapping splits', 'Unstratified tiny test sets'], quality='Splits are leak-free and the dataset is documented.',
    practice_items=[number_item('p1', '1,000 items, 80/10/10. Training set size?', 'Items', 800), number_item('p2', '1,000 items, 80/10/10. Dev set size?', 'Items', 100),
                    *choice_items('c', 'Good practice?', ['Yes', 'No'], [('Write label guidelines before labelling.', 'Yes'), ('Let the same sentence appear in train and test.', 'No')])],
    assessment_items=[number_item('a1', '2,500 items, 80/10/10. Test set size?', 'Items', 250),
                      number_item('a2', 'Test set has 250 items, 30% negative. How many negative?', 'Items', 75),
                      *choice_items('c', 'Good practice?', ['Yes', 'No'], [
                          ('Split speech data by speaker.', 'Yes'), ('Tune your model on the test set.', 'No'),
                          ('Document label definitions in the datasheet.', 'Yes')])],
    guidelines=['Use the definitions from the lesson.'],
    project_brief=project('Design and build a 200-item dataset', 'Design a small labelled dataset for a Nigerian-language task (sentiment, intent or topic).',
                          ['Task and schema', 'Guidelines', '200 labelled items with splits', 'Datasheet'],
                          ['Clear design', 'Leak-free splits', 'Good documentation'], ['Dataset creation'], difficulty='intermediate', hours=6),
)

DATASET_CLEANING = _tech_skill(
    'dataset-cleaning', 'Dataset Cleaning', level='intermediate', icon='ri-brush-3-line', tags=['dataset', 'qa'],
    tagline='Fix encoding, duplicates, noise and Unicode problems in language data.',
    description='Clean real African-language data: mojibake, mixed Unicode forms, HTML, duplicates, empty and mislabelled rows.',
    core=lesson('Common data problems and fixes', 'Diagnose and fix dirty text data.',
                ['Real language data is messy. <strong>Mojibake</strong> ("áº¹" where "ẹ" should be) means text was decoded with the wrong '
                 'encoding — fix by re-decoding as UTF-8, not by deleting characters. Mixed NFC/NFD forms make identical words look different. '
                 'HTML tags, URLs, empty rows and duplicates must be removed.',
                 'Cleaning must be logged and reversible: keep the raw data, write scripted steps, and record how many rows each step changed.'],
                points=['Mojibake → re-decode as UTF-8.', 'Normalise to NFC.', 'Strip HTML/URLs per the spec.', 'Log every step; keep raw data.'],
                quiz=[q('"áº¹" appears where "ẹ" should be. Problem?', 'Encoding (mojibake)', 'Duplicate', 'Wrong label', 'HTML', why='Wrong decoding.'),
                      q('Best fix for mojibake?', 'Re-decode the bytes as UTF-8', 'Delete the odd characters', 'Translate the text', 'Ignore it', why='Recover the text.'),
                      q('Why keep the raw data?', 'So cleaning can be checked and redone', 'It is prettier', 'For storage costs', 'No reason', why='Reversibility.')]),
    steps=['Profile the data.', 'Fix encoding.', 'Normalise Unicode.', 'Remove markup/noise.', 'Deduplicate.', 'Log counts.'],
    mistakes=['Deleting mojibake', 'Cleaning by hand without a log', 'Over-cleaning (removing valid diacritics)'],
    quality='Every change is scripted, logged and justified.',
    practice_items=choice_items('a', 'Action', ['Keep as is', 'Fix encoding', 'Strip HTML', 'Remove (duplicate/empty)'], [
        ('"Mo nÃ­ ilÃ©" (should be "Mo ní ilé")', 'Fix encoding'), ('"<p>Ẹ káàárọ̀</p>"', 'Strip HTML'),
        ('"" (empty row)', 'Remove (duplicate/empty)'), ('"Ẹ káàárọ̀, ṣé dáadáa ni?"', 'Keep as is')]),
    assessment_items=choice_items('a', 'Action', ['Keep as is', 'Fix encoding', 'Strip HTML', 'Remove (duplicate/empty)', 'Normalise Unicode'], [
        ('"áº¸ kÃ¡Ã Ã¡rá»Ì€" (garbled Yoruba)', 'Fix encoding'), ('Row 52 identical to row 17', 'Remove (duplicate/empty)'),
        ('"ọ̀" stored as o + combining dot + combining grave, while the rest of the file uses precomposed forms', 'Normalise Unicode'),
        ('"<br>Na gode<br>"', 'Strip HTML'), ('"Adị m mma, daalụ."', 'Keep as is')]),
    guidelines=['Choose the single correct cleaning action.'],
    project_brief=project('Clean a messy dataset', 'Take a messy African-language text file (or create one with mojibake, HTML, duplicates) and clean it with a script.',
                          ['Raw and cleaned files', 'Cleaning script', 'Log: rows changed per step'], ['Correct fixes', 'Reproducible script', 'Clear log'],
                          ['Dataset cleaning'], difficulty='intermediate', hours=4, workspace='developer'),
)

DATASET_MGMT = _tech_skill(
    'dataset-management', 'Dataset Management', level='intermediate', icon='ri-folder-settings-line', tags=['dataset', 'data-privacy'],
    tagline='Version, document, license and protect language datasets.',
    description='Manage datasets over time: versioning, documentation, licences, access control and safe storage of language and speech data.',
    core=lesson('Managing data over its life', 'Keep datasets versioned, documented and protected.',
                ['Datasets change: new rows, fixed labels, removed withdrawals. Good management uses <strong>versioning</strong> (v1.0, v1.1 with '
                 'a changelog), <strong>documentation</strong> (README/data card), a clear <strong>licence</strong>, and <strong>access control</strong> '
                 'for anything sensitive (speech recordings, consent forms).',
                 'Never overwrite the only copy; keep backups; record who can access what and why.'],
                points=['Version with a changelog.', 'README/data card with every release.', 'Licence states how others may use it.',
                        'Restrict access to sensitive data; keep backups.'],
                quiz=[q('You fixed 200 labels. Next step?', 'Release a new version with a changelog', 'Overwrite silently', 'Delete the old labels', 'Email the file', why='Traceability.'),
                      q('Consent forms should be stored…', 'separately, with restricted access', 'in the public dataset folder', 'in a group chat', 'nowhere', why='Privacy.'),
                      q('A dataset licence tells users…', 'how they may use and share it', 'its file size', 'who labelled each row', 'nothing', why='Usage rights.')]),
    steps=['Set up versioned storage.', 'Write the README and licence.', 'Separate sensitive files.', 'Log changes per release.', 'Back up.'],
    mistakes=['Single copy, no backup', 'Silent overwrites', 'Public consent forms'], quality='Anyone can tell what changed, why, and who may use it.',
    practice_items=choice_items('c', 'Good practice?', ['Yes', 'No'], [
        ('Keep a CHANGELOG for each dataset release.', 'Yes'), ('Store the only copy on your phone.', 'No'),
        ('Put a licence file in the dataset folder.', 'Yes'), ('Share speaker consent forms publicly with the audio.', 'No')]),
    assessment_items=choice_items('c', 'Good practice?', ['Yes', 'No'], [
        ('Remove a withdrawn speaker\'s files and note it in the changelog.', 'Yes'), ('Rename v1.0 files without telling users.', 'No'),
        ('Give every annotator write access to the master dataset.', 'No'), ('Keep backups in two locations.', 'Yes'),
        ('Describe known limitations in the README.', 'Yes')]),
    guidelines=['Judge each practice.'],
    project_brief=project('Dataset release package', 'Package a dataset you created (or a small sample) as a proper release.',
                          ['Folder structure', 'README/data card', 'Licence', 'CHANGELOG with two versions', 'Access policy for sensitive parts'],
                          ['Complete documentation', 'Sensible structure', 'Clear access policy'], ['Dataset management'], difficulty='intermediate', hours=3),
    hours=4,
)

SKILLS = [PYTHON, NLP_FUND, DATASET_CREATION, CORPUS_CREATION, NLP, ASR, TTS, MT, LM, LLM_FUND, AI_RESEARCH, DATASET_CLEANING, DATASET_MGMT]
