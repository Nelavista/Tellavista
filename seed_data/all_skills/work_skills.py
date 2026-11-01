"""Project & Work Skills category — the professional habits language-data projects
actually check: following guidelines, confidentiality, privacy, remote work, time and task
management, communication and issue reporting. Practical scenario judgements, not
motivational content. (General professional guidance, not legal advice.)
"""
from ._common import q, lesson, workflow_lesson, task, labeling, choice_items, number_item, project, skill

COLOR = '#475569'

FOUNDATION = lesson(
    'How remote language-data projects run',
    'Know what a project expects from a contributor beyond the task itself.',
    [
        'Language-data work is usually remote and task-based: you join a project, sign agreements, pass a qualification test, receive '
        'batches on an annotation platform, and are measured on quality, throughput and reliability. Many projects remove contributors '
        'for confidentiality breaches or missed deadlines even when their work is accurate.',
        'The professional basics — reading the guideline, protecting data, communicating early, reporting problems clearly, and '
        'delivering what was asked — are what get contributors invited back.',
    ],
    points=['Quality, throughput and reliability are all measured.', 'Confidentiality breaches end contracts.',
            'Communicate problems early, in writing.', 'Deliver exactly the requirement — format, deadline, scope.'],
    quiz=[
        q('Your work is accurate but you often miss deadlines. Likely outcome?', 'You may be removed from the project', 'Nothing', 'A promotion', 'More tasks',
          why='Reliability is measured.'),
        q('When should you tell the project lead you\'ll miss a deadline?', 'As soon as you know', 'After the deadline', 'Never', 'Only if asked', why='Early warning.'),
        q('Which is usually part of joining a data project?', 'Agreements and a qualification test', 'A public interview', 'Buying equipment for the client', 'Nothing',
          why='Standard onboarding.'),
    ],
)


def _work_skill(slug, name, *, icon, tagline, description, core, steps, mistakes, quality, options, practice_rows, assessment_rows,
                guidelines, project_brief, level='beginner', tags=None, report=None, extra_items=None, hours=2):
    assessment_items = choice_items('a', 'Best response', options, assessment_rows) + (extra_items or [])
    return skill(
        slug, name, level=level, tags=['work-skills'] + (tags or []), icon=icon, color=COLOR, tagline=tagline, description=description,
        foundation=FOUNDATION, core=core, workflow=workflow_lesson(name.lower(), steps, mistakes, quality),
        practice=task(f'{name}: scenarios', 'Choose the most professional response to each scenario.',
                      labeling(choice_items('a', 'Best response', options, practice_rows), guidelines), minutes=10),
        assessment=task(f'{name} assessment', 'Scored scenarios.', labeling(assessment_items, guidelines, report=report, ai_feedback=bool(report)), minutes=12),
        project_brief=project_brief, hours=hours,
    )


GUIDELINES = _work_skill(
    'following-annotation-guidelines', 'Following Annotation Guidelines', icon='ri-book-read-line', tags=['annotation'],
    tagline='Read, apply and query guidelines like a top-rated contributor.',
    description='How to study a guideline, apply edge-case rules, track updates, and ask good clarification questions.',
    core=lesson('Working from a guideline', 'Apply guidelines precisely and handle updates.',
                ['Top contributors read the full guideline before starting, keep it open while working, and re-read it whenever a new version '
                 'is released. Updates often change edge cases, and work done under the old rule may need fixing.',
                 'When something isn\'t covered, ask a clear question in the project\'s official channel with an example — and don\'t invent '
                 'your own rule meanwhile (follow the instruction for unclear items, often "skip" or "flag").'],
                points=['Read it all before item 1.', 'Re-read every new version; note what changed.', 'Ask with an example in the official channel.',
                        'Follow the "unclear item" instruction while waiting.'],
                quiz=[q('Version 2 of the guideline changes the sarcasm rule. You…', 'apply it from now and check if earlier items need fixing', 'ignore it',
                        'apply it only to new projects', 'ask friends what they think', why='Track updates.'),
                      q('Good clarification question?', '"Item 4512: \'E don do\' — is this Neutral or Negative under rule 3?"', '"I don\'t understand."', '"Rules are confusing."', '"?"',
                        why='Specific with example.'),
                      q('While waiting for an answer on an unclear case you…', 'follow the guideline\'s instruction for unclear items', 'invent a rule', 'stop working entirely', 'guess randomly',
                        why='Stay consistent.')]),
    steps=['Read the full guideline.', 'Make a one-page cheat sheet of edge cases.', 'Work with it open.', 'Re-read on updates.', 'Ask precise questions.'],
    mistakes=['Starting before reading', 'Ignoring version updates', 'Private rules'], quality='Your labels always match the current guideline.',
    options=['Follow the guideline', 'Ask in the official channel', 'Use your own judgement', 'Skip silently'],
    practice_rows=[('The guideline clearly covers the case, but you disagree with the rule.', 'Follow the guideline'),
                   ('A frequent case isn\'t covered by the guideline at all.', 'Ask in the official channel'),
                   ('An item is in a language you don\'t speak; the guideline says "flag non-target-language items".', 'Follow the guideline')],
    assessment_rows=[('A new guideline version changes how [noise] is used.', 'Follow the guideline'),
                     ('Two rules seem to contradict each other on one item.', 'Ask in the official channel'),
                     ('You think a label set is missing a category.', 'Ask in the official channel'),
                     ('The rule is clear but slower to apply.', 'Follow the guideline')],
    guidelines=['Pick the most professional response.'],
    project_brief=project('Guideline cheat sheet', 'Take the guideline from any annotation or transcription skill you completed and write a one-page cheat sheet plus 3 clarification questions.',
                          ['Cheat sheet of rules and edge cases', '3 well-formed clarification questions with examples'],
                          ['Accurate summary', 'Useful edge cases', 'Precise questions'], ['Following guidelines'], hours=1),
)

NDA = _work_skill(
    'nda-confidentiality', 'NDA & Confidentiality', icon='ri-lock-line', tags=['data-privacy'],
    tagline='Understand NDAs and keep client data and projects confidential.',
    description='What non-disclosure agreements usually cover, what you can and can\'t share, and everyday confidentiality habits. General guidance, not legal advice.',
    core=lesson('What an NDA usually means for you', 'Apply confidentiality rules in everyday situations.',
                ['A non-disclosure agreement (NDA) is a contract in which you promise not to share confidential information — typically '
                 'the client\'s name (sometimes), project details, guidelines, data, and tools. Breaking it can end your contract and may '
                 'have legal consequences. Always read what YOUR NDA covers; if unsure, ask the project lead (and get legal advice for '
                 'anything serious).',
                 'Everyday risks: posting screenshots, sharing guidelines in WhatsApp groups, discussing tasks publicly, or using project data '
                 'in your own work.'],
                points=['Read your NDA; it defines what\'s confidential.', 'No screenshots, no sharing guidelines or data.',
                        'Describe experience generically in CVs ("speech data annotation for an AI company") unless allowed.', 'When unsure, ask before sharing.'],
                quiz=[q('A friend asks for the project guideline to "learn from it". You…', 'decline — it is confidential', 'send it privately', 'send a summary', 'post it online',
                        why='Guidelines are usually confidential.'),
                      q('How can you mention the work on your CV?', 'Generically, unless the NDA allows naming the client', 'Name the client and paste data', 'Upload screenshots', 'You can\'t mention it at all',
                        why='Generic description.'),
                      q('Is this legal advice?', 'No — read your own NDA and seek legal advice for serious questions', 'Yes', 'Only in Lagos', 'Only for clients', why='General guidance.')]),
    steps=['Read the NDA before starting.', 'Note what is confidential.', 'Work only in approved tools.', 'Never copy data out.', 'Ask when unsure.'],
    mistakes=['Screenshots in group chats', 'Sharing guidelines', 'Using project data elsewhere'], quality='Nothing confidential ever leaves the project.',
    options=['Acceptable', 'Breach of confidentiality'],
    practice_rows=[('Posting a screenshot of a task on social media to show your new job.', 'Breach of confidentiality'),
                   ('Saying "I do speech-data annotation remotely" in a job interview.', 'Acceptable'),
                   ('Sharing the guideline PDF with a study group.', 'Breach of confidentiality')],
    assessment_rows=[('Copying audio clips to your phone to listen later outside the platform.', 'Breach of confidentiality'),
                     ('Asking the project lead whether you can name the client on LinkedIn.', 'Acceptable'),
                     ('Discussing a specific task\'s content in a public Telegram group.', 'Breach of confidentiality'),
                     ('Listing "Yoruba transcription and QA" as a skill on your CV.', 'Acceptable')],
    guidelines=['Assume a standard NDA covering client identity, guidelines and data.'],
    project_brief=project('Confidentiality checklist', 'Write a personal confidentiality checklist for remote data work and a CV-safe description of one skill you verified.',
                          ['10-point checklist', 'CV-safe description', 'What you would ask a project lead before sharing anything'],
                          ['Practical checklist', 'Safe description'], ['Confidentiality'], hours=1),
)

PRIVACY = _work_skill(
    'data-privacy', 'Data Privacy', icon='ri-shield-user-line', tags=['data-privacy'], level='beginner',
    tagline='Handle personal data lawfully and respectfully in language-data work.',
    description='Personal data, consent, minimisation and Nigeria\'s Data Protection Act 2023 basics, applied to recordings, transcripts and datasets. General guidance, not legal advice.',
    core=lesson('Personal data in language work', 'Recognise and protect personal data.',
                ['Personal data is anything that identifies a person: names, phone numbers, addresses, ID/BVN numbers, faces, and often voices. '
                 'Nigeria\'s Data Protection Act 2023 (and laws like the EU GDPR for international clients) require a lawful basis such as consent, '
                 'collecting only what is needed (<strong>minimisation</strong>), keeping it secure, and respecting people\'s rights.',
                 'In practice: anonymise transcripts per the guideline, never collect more metadata than needed, store data only in approved places, '
                 'and report any accidental exposure immediately.'],
                points=['Personal data: names, numbers, addresses, IDs, voices.', 'Consent and minimisation.', 'Anonymise as the guideline says.',
                        'Report exposures immediately.'],
                quiz=[q('Which is personal data?', 'A BVN number', 'The word "market"', 'A public-domain proverb', 'A tone mark', why='Identifies a person.'),
                      q('"Minimisation" means…', 'collect only the data you need', 'compress files', 'delete everything', 'use small fonts', why='Least data.'),
                      q('You accidentally emailed a file with names to the wrong person. You…', 'report it immediately to the project lead', 'hide it', 'wait', 'delete your email account',
                        why='Exposure must be reported.')]),
    steps=['Identify personal data in the task.', 'Apply anonymisation rules.', 'Store only in approved tools.', 'Collect minimal metadata.', 'Report incidents.'],
    mistakes=['Leaving phone numbers in transcripts', 'Over-collecting metadata', 'Personal storage of data'], quality='No personal data leaves the approved process.',
    options=['Correct', 'Privacy problem'],
    practice_rows=[('Replacing a caller\'s phone number with [PHONE] as the guideline says.', 'Correct'),
                   ('Collecting speakers\' home addresses "just in case".', 'Privacy problem'),
                   ('Keeping consent forms in a restricted folder.', 'Correct')],
    assessment_rows=[('Saving project audio to your personal Google Drive for backup.', 'Privacy problem'),
                     ('Using speaker codes (S012) instead of names in metadata.', 'Correct'),
                     ('Not reporting that a file with names was shared by mistake.', 'Privacy problem'),
                     ('Collecting age range instead of exact date of birth.', 'Correct')],
    guidelines=['Judge each action against consent, minimisation and security.'],
    project_brief=project('Privacy review of a dataset plan', 'Review a speech or text dataset plan (yours from another skill, or a sample) for privacy risks.',
                          ['Personal data found', 'Minimisation changes', 'Anonymisation rules', 'Incident procedure'],
                          ['Complete risk list', 'Practical fixes'], ['Data privacy'], hours=2),
)

REMOTE = _work_skill(
    'remote-project-work', 'Remote Project Work', icon='ri-home-wifi-line',
    tagline='Work reliably on remote projects — setup, power, data and communication.',
    description='Practical remote-work setup for Nigerian contributors: power and internet backups, workspace, availability and async communication.',
    core=lesson('Being reliable remotely', 'Set up for dependable remote work.',
                ['Remote projects judge you on reliability. In Nigeria that means planning around power cuts and data costs: a charged power bank '
                 'or inverter, a backup data line, offline-capable tools where allowed, and knowing your quiet hours for recording tasks.',
                 'Communicate asynchronously: post status updates, state your availability honestly, and respond within the agreed time.'],
                points=['Backup power and a second data line.', 'Honest availability.', 'Async updates in the official channel.', 'Quiet time for audio work.'],
                quiz=[q('NEPA takes light during a timed task. Best prevention?', 'A charged power bank/inverter and saving work often', 'Hope it doesn\'t', 'Work only at night', 'Use one phone only',
                        why='Plan for outages.'),
                      q('You\'ll be travelling for 3 days. You…', 'tell the project lead in advance', 'disappear quietly', 'take tasks and finish late', 'nothing', why='Availability.'),
                      q('Async communication means…', 'clear written updates others can read later', 'calling everyone at once', 'only meetings', 'no communication', why='Remote norm.')]),
    steps=['Set up power and data backups.', 'Agree availability.', 'Post status updates.', 'Save work often.', 'Flag blockers early.'],
    mistakes=['No backup plan', 'Silent absences', 'Taking more tasks than you can finish'], quality='The project can always rely on you.',
    options=['Professional', 'Unprofessional'],
    practice_rows=[('Telling the lead on Monday that you\'ll be offline Friday.', 'Professional'), ('Accepting 500 tasks when you can do 100 this week.', 'Unprofessional'),
                   ('Posting a short daily update in the project channel.', 'Professional')],
    assessment_rows=[('Going silent for a week mid-batch.', 'Unprofessional'), ('Keeping a backup data line for deadlines.', 'Professional'),
                     ('Recording speech tasks next to a running generator.', 'Unprofessional'), ('Stating your real weekly availability in hours.', 'Professional')],
    guidelines=['Judge each behaviour.'],
    project_brief=project('Remote work plan', 'Write your personal remote-work plan for a 4-week project.',
                          ['Weekly availability', 'Power/data backup plan', 'Communication routine', 'Risks and mitigations'],
                          ['Realistic plan', 'Concrete backups'], ['Remote project work'], hours=1),
)

TASKS = _work_skill(
    'task-management', 'Task Management', icon='ri-task-line',
    tagline='Plan, prioritise and track batches of work.',
    description='Break projects into tasks, prioritise by deadline and value, track progress, and avoid over-commitment.',
    core=lesson('Managing batches', 'Plan and track task batches.',
                ['Data projects come in batches with deadlines and quotas. Manage them like a mini project: list tasks, estimate time from your '
                 'measured speed (e.g. 20 items/hour), schedule them, and track done vs remaining daily.',
                 'Prioritise by deadline and importance; don\'t start new batches while urgent ones are unfinished.'],
                points=['Estimate from measured speed.', 'Schedule against deadlines.', 'Track daily.', 'Finish urgent work first.'],
                quiz=[q('400 items at 20 items/hour takes…', '20 hours', '8 hours', '40 hours', '2 hours', why='400/20.'),
                      q('Batch A due tomorrow, Batch B due next week. You start…', 'A', 'B', 'both halfway', 'neither', why='Deadline.'),
                      q('Why track done vs remaining daily?', 'To spot delays early', 'For fun', 'Not needed', 'To slow down', why='Early warning.')]),
    steps=['List tasks.', 'Estimate time.', 'Schedule.', 'Track daily.', 'Re-plan when slipping.'],
    mistakes=['Guessing time', 'Starting everything at once', 'No tracking'], quality='Batches finish on time without last-minute rushes.',
    options=['Good practice', 'Poor practice'],
    practice_rows=[('Estimating batch time from your measured items-per-hour.', 'Good practice'), ('Starting a new batch while one is due tomorrow.', 'Poor practice'),
                   ('Checking progress against plan each evening.', 'Good practice')],
    assessment_rows=[('Accepting work without checking its deadline.', 'Poor practice'), ('Splitting a 600-item batch into daily targets.', 'Good practice'),
                     ('Re-planning as soon as you fall behind.', 'Good practice')],
    extra_items=[number_item('n1', '600 items at 25 items/hour, working 4 hours/day.', 'Days needed', 6)],
    guidelines=['Judge each practice; compute the number.'],
    project_brief=project('Batch plan', 'Plan a realistic 2-week schedule for a 1,200-item annotation batch using your own measured speed from a practice task.',
                          ['Measured speed', 'Daily targets', 'Buffer for problems', 'Tracking table'], ['Realistic estimates', 'Clear tracking'],
                          ['Task management'], hours=1),
)

TIME = _work_skill(
    'time-management', 'Time Management', icon='ri-timer-line',
    tagline='Balance studies and paid data work without missing either.',
    description='Time-blocking, focus sessions and realistic weekly planning for students doing language-data work alongside classes.',
    core=lesson('Making time work', 'Plan focused work around your studies.',
                ['Students doing data work must protect both their grades and their deadlines. Time-blocking — reserving specific hours for '
                 'specific work — plus focused sessions (e.g. 45 minutes on, 10 off) beats working "whenever".',
                 'Quality drops with fatigue: long unbroken sessions produce more errors, which cost more time in rework than the breaks would have.'],
                points=['Block time on a weekly calendar.', 'Focused sessions with short breaks.', 'Exams come first — tell the project in advance.',
                        'Fatigue causes errors and rework.'],
                quiz=[q('Exams start in two weeks. You…', 'reduce your task load and tell the project lead now', 'take extra tasks', 'say nothing', 'quit without notice',
                        why='Plan ahead.'),
                      q('Why take short breaks?', 'Fatigue increases errors', 'They are required by law', 'To look busy', 'No reason', why='Quality.'),
                      q('Time-blocking means…', 'reserving set hours for specific work', 'working all night', 'random work', 'blocking websites', why='Planned time.')]),
    steps=['List fixed commitments (classes, exams).', 'Block work hours.', 'Use focused sessions.', 'Review weekly.'],
    mistakes=['All-night sessions', 'Ignoring exam periods', 'No weekly review'], quality='Deadlines and studies are both met.',
    options=['Good choice', 'Poor choice'],
    practice_rows=[('Blocking 7–9pm on weekdays for project work.', 'Good choice'), ('Doing 8 hours non-stop the night before a deadline.', 'Poor choice'),
                   ('Telling the lead about exam weeks a month ahead.', 'Good choice')],
    assessment_rows=[('Taking new tasks during exam week without telling anyone.', 'Poor choice'), ('45-minute focus sessions with 10-minute breaks.', 'Good choice'),
                     ('Reviewing your week every Sunday.', 'Good choice'), ('Skipping classes to finish tasks.', 'Poor choice')],
    guidelines=['Judge each choice.'],
    project_brief=project('Weekly plan', 'Create your real weekly plan combining classes, study and 10 hours of project work.',
                          ['Weekly calendar', 'Focus-session routine', 'Exam-period plan'], ['Realistic plan', 'Protects studies'], ['Time management'], hours=1),
)

COMMS = _work_skill(
    'professional-communication', 'Professional Communication', icon='ri-mail-line',
    tagline='Write clear, polite, effective messages to project leads and clients.',
    description='Professional written communication for remote projects: clear subject lines, context, specific asks and the right tone.',
    core=lesson('Writing clear work messages', 'Write messages that get quick, useful replies.',
                ['Good work messages are short and complete: context (which project/batch), the specific question or update, what you need and by when. '
                 'Use a polite, professional tone — no slang in formal channels, no all-caps, no voice notes unless the project uses them.',
                 'One message, one topic. Include item IDs or screenshots only if allowed by confidentiality rules.'],
                points=['Context → point → ask.', 'One topic per message.', 'Polite and professional; no slang in formal channels.', 'Include IDs, not data.'],
                quiz=[q('Best message?', '"Batch 12, item 4512: is \'E don do\' Neutral or Negative under rule 3? Thanks."', '"pls help"', '"WHY IS THIS SO HARD"', '"Call me"',
                        why='Context, specific ask.'),
                      q('In a formal project channel, "Oga abeg how far with my payment" is…', 'too informal', 'perfect', 'required', 'rude but fine', why='Register.'),
                      q('You have two unrelated questions. You…', 'send two clear messages (or numbered points)', 'mix them in one sentence', 'ask none', 'call at midnight',
                        why='Clarity.')]),
    steps=['State context.', 'Make your point.', 'Make a specific ask with timing.', 'Proofread.', 'Send in the right channel.'],
    mistakes=['Vague asks', 'Slang in formal channels', 'Pasting confidential data'], quality='Readers can act on your message without follow-up questions.',
    options=['A', 'B', 'C'],
    practice_rows=[('Which update is best?\nA: "done"\nB: "Batch 7 done: 300/300 items, 2 flagged for unclear audio (IDs 7_118, 7_240)."\nC: "I finished some."', 'B'),
                   ('Which question is best?\nA: "Rule 4 vs rule 6 conflict on item 3_051 (greeting + complaint). Which applies?"\nB: "confused"\nC: "Explain the guideline again."', 'A')],
    assessment_rows=[('Asking about a late payment.\nA: "Where is my money??"\nB: "Hello, invoice #14 (June batch) shows as unpaid. Could you confirm the expected date? Thank you."\nC: "Oga abeg pay me."', 'B'),
                     ('Reporting a delay.\nA: "I will finish Batch 9 on Thursday instead of Wednesday because of a power outage. 220/300 done."\nB: "Delay."\nC: "Sorry."', 'A'),
                     ('Requesting clarification.\nA: "?"\nB: "This guideline is bad."\nC: "Item 5_210: should Pidgin \'abeg\' be tagged as English or Pidgin?"', 'C')],
    guidelines=['Pick the clearest, most professional message.'],
    report={'label': 'Write a message to a project lead asking for a 2-day extension, with reason and status', 'min_words': 30},
    project_brief=project('Message templates', 'Write 5 reusable message templates: status update, clarification question, delay notice, payment query, issue report.',
                          ['5 templates', 'A filled-in example for each'], ['Clear, professional, reusable'], ['Professional communication'], hours=1),
)

ISSUES = _work_skill(
    'reporting-issues', 'Reporting Issues', icon='ri-flag-line',
    tagline='Report data, tool and guideline problems so they actually get fixed.',
    description='Write issue reports that teams can act on: what, where, how to reproduce, impact and suggested fix.',
    core=lesson('Writing a useful issue report', 'Report problems clearly and safely.',
                ['Projects rely on contributors to report problems: corrupted audio, broken tools, unclear guideline rules, suspicious data '
                 '(e.g. personal data that shouldn\'t be there). A useful report has: a clear title, where it happens (batch/item ID), what '
                 'you expected vs what happened, steps to reproduce, impact, and a suggested fix if you have one.',
                 'Report through the official channel; don\'t include confidential data beyond IDs.'],
                points=['Title + location (IDs).', 'Expected vs actual.', 'Steps to reproduce and impact.', 'Official channel; IDs, not data.'],
                quiz=[q('Most useful title?', '"Batch 12 audio items 12_300–12_340 play silence"', '"Problem"', '"Help!!!"', '"Audio"', why='Specific.'),
                      q('You find personal data in a dataset you\'re labelling. You…', 'report it immediately with item IDs', 'label it and move on', 'post it in a group', 'delete the dataset',
                        why='Escalate safely.'),
                      q('Why include steps to reproduce?', 'So the team can see and fix the problem', 'To make it longer', 'Tradition', 'No reason', why='Actionable.')]),
    steps=['Confirm the problem.', 'Collect IDs and steps.', 'Write expected vs actual.', 'State impact.', 'Submit in the official channel.'],
    mistakes=['Vague reports', 'Pasting confidential data', 'Not reporting at all'], quality='Engineers or leads can fix the issue from your report alone.',
    options=['Report it', 'Ignore it', 'Fix it yourself silently'],
    practice_rows=[('Audio clips in a batch are all silent.', 'Report it'), ('A dataset row contains someone\'s BVN.', 'Report it'),
                   ('A typo in the guideline\'s example changes the meaning of a rule.', 'Report it')],
    assessment_rows=[('The platform\'s submit button fails every 10th item.', 'Report it'), ('Two guideline rules contradict each other.', 'Report it'),
                     ('You notice another contributor\'s labels are systematically wrong.', 'Report it')],
    guidelines=['Choose the professional action.'],
    report={'label': 'Write an issue report for "audio items 12_300–12_340 are silent"', 'min_words': 30},
    project_brief=project('Issue report pack', 'Write 3 full issue reports (data, tool, guideline) for realistic problems you encountered in these skills or invent plausible ones.',
                          ['3 reports with title, location, expected vs actual, steps, impact, suggested fix'], ['Actionable, safe reports'],
                          ['Issue reporting'], hours=1),
)

PLATFORMS = _work_skill(
    'working-with-annotation-platforms', 'Working With Annotation Platforms', icon='ri-layout-line', tags=['annotation'],
    tagline='Get productive fast on Label Studio-style annotation tools.',
    description='How annotation platforms work — projects, tasks, labels, shortcuts, review queues and exports — using common open tools as reference.',
    core=lesson('Inside an annotation platform', 'Navigate and work efficiently in annotation tools.',
                ['Most annotation platforms (open tools like Label Studio, or a client\'s own) share the same pieces: a project with a labelling '
                 'interface, a task queue, keyboard shortcuts for labels, a skip/flag button, a review queue where QA checks your work, and '
                 'export formats (JSON, CSV).',
                 'Productivity comes from shortcuts and a steady rhythm; quality comes from reading each item fully. Use the platform\'s flag '
                 'feature instead of side channels for item-level problems.'],
                points=['Learn label shortcuts early.', 'Use skip/flag as the guideline says.', 'Review queues show your QA feedback — read it.',
                        'Exports are usually JSON or CSV.'],
                quiz=[q('An item is broken (audio won\'t load). Use…', 'the platform\'s flag/skip feature', 'a random label', 'WhatsApp', 'nothing', why='Item-level issue.'),
                      q('Where do you see QA feedback on your work?', 'The review queue / feedback view', 'Nowhere', 'Your email spam folder', 'Social media', why='Platform feature.'),
                      q('A common export format for labels is…', 'JSON', 'MP3', 'PNG', 'DOCX', why='Structured data.')]),
    steps=['Read the project instructions in the tool.', 'Learn shortcuts.', 'Label with a steady rhythm.', 'Flag problem items.', 'Check feedback regularly.'],
    mistakes=['Ignoring shortcuts', 'Labelling broken items', 'Never reading feedback'], quality='Fast, accurate, and responsive to feedback.',
    options=['Use the flag/skip feature', 'Label it anyway', 'Check the review queue', 'Use keyboard shortcuts'],
    practice_rows=[('Audio for an item won\'t play.', 'Use the flag/skip feature'), ('You want to see why QA rejected three of your items.', 'Check the review queue'),
                   ('You want to label faster without losing accuracy.', 'Use keyboard shortcuts')],
    assessment_rows=[('The text in an item is in a language not covered by the project.', 'Use the flag/skip feature'),
                     ('Your accuracy score dropped and you want to know why.', 'Check the review queue'),
                     ('You\'re clicking through 10 label buttons for every item.', 'Use keyboard shortcuts')],
    guidelines=['Choose the best platform action.'],
    project_brief=project('Set up a mini annotation project', 'Install or use a free annotation tool (e.g. Label Studio) and set up a 20-item project for one task from these skills.',
                          ['Screenshots of your labelling interface (your own data only)', 'Label config or setup notes', 'Exported results (JSON/CSV)'],
                          ['Working setup', 'Correct export', 'Clear notes'], ['Annotation platforms'], hours=2),
)

REQUIREMENTS = _work_skill(
    'meeting-project-requirements', 'Meeting Project Requirements', icon='ri-list-check-2',
    tagline='Deliver exactly what was asked — format, scope, quality and deadline.',
    description='Read a project brief, extract its requirements, check your delivery against them, and avoid the common reasons work is rejected.',
    core=lesson('From brief to accepted delivery', 'Turn a brief into a checklist and meet it.',
                ['Work is rejected more often for not meeting requirements than for poor skill: wrong file format, wrong naming, missing fields, '
                 'over or under the requested amount, or late delivery. Before starting, turn the brief into a checklist: format, naming, quantity, '
                 'quality threshold, deadline, and delivery method.',
                 'Before delivering, check every item on the list. If a requirement can\'t be met, say so early and agree an alternative.'],
                points=['Brief → checklist before starting.', 'Check format, naming, quantity, quality, deadline.', 'Verify before delivering.',
                        'Can\'t meet one? Say so early.'],
                quiz=[q('The brief asks for WAV files; you have MP3. You…', 'convert to WAV or agree an exception before delivering', 'send MP3', 'send nothing', 'rename .mp3 to .wav',
                        why='Meet the format.'),
                      q('First step on receiving a brief?', 'Turn it into a requirements checklist', 'Start immediately', 'Ask for payment', 'Ignore the details', why='Plan.'),
                      q('You realise you can only deliver 80 of 100 items by the deadline. You…', 'tell the lead now and agree a plan', 'deliver 80 silently', 'pad with low-quality items',
                        'say nothing', why='Early communication.')]),
    steps=['Extract requirements into a checklist.', 'Clarify anything ambiguous.', 'Do the work.', 'Check every requirement.', 'Deliver as specified.'],
    mistakes=['Wrong format or naming', 'Silent shortfalls', 'Late delivery'], quality='Deliveries are accepted first time.',
    options=['Meets requirements', 'Does not meet requirements'],
    practice_rows=[('Brief: 50 WAV files named YO_001–YO_050. Delivered: 50 WAV files named YO_001–YO_050.', 'Meets requirements'),
                   ('Brief: CSV with columns id,text,label. Delivered: Excel file with columns text,label.', 'Does not meet requirements'),
                   ('Brief: deliver by Friday 5pm. Delivered: Saturday morning, no notice.', 'Does not meet requirements')],
    assessment_rows=[('Brief: 100 labelled items, accuracy ≥ 95%. Delivered: 100 items, QA accuracy 97%.', 'Meets requirements'),
                     ('Brief: transcripts with timestamps. Delivered: transcripts without timestamps.', 'Does not meet requirements'),
                     ('Brief: 16 kHz mono WAV. Delivered: 16 kHz mono WAV, correct names.', 'Meets requirements'),
                     ('Brief: 200 items. Delivered: 150 items, with an agreed extension for the rest.', 'Meets requirements')],
    guidelines=['Judge each delivery against its brief. Agreed changes count as part of the requirements.'],
    project_brief=project('Requirements checklist + delivery', 'Take one completed project from another ALL skill, write its requirements checklist from the brief, and audit your own delivery against it.',
                          ['Requirements checklist', 'Audit: each requirement met/not met with evidence', 'What you would fix before delivering to a client'],
                          ['Complete checklist', 'Honest audit'], ['Meeting project requirements'], hours=1),
)

SKILLS = [GUIDELINES, NDA, PRIVACY, REMOTE, TASKS, TIME, COMMS, ISSUES, PLATFORMS, REQUIREMENTS]
