"""Seed data for the Video Production & Motion Design 30-Day Skill Class."""

SKILL = {
    "slug": "video-production-motion-design",
    "name": "Video Production & Motion Design",
    "tagline": "Shoot, edit, and animate video content that brands and creators actually pay for.",
    "description": "Video production and motion design covers the full pipeline from a script idea to a finished, exportable video — shooting or sourcing footage, editing with pacing and sound, and adding basic motion graphics. Video is now the dominant content format for brands, creators, and businesses across Africa, and skilled editors are hired for everything from Instagram reels to full ad campaigns. This track builds you from a phone-shot first video to a polished piece ready for a client reel.",
    "level": "beginner",
    "estimated_hours": 65,
    "course_title": "30-Day Video Production & Motion Design Career Track",
    "course_description": "After finishing all 30 days, a student can plan a shoot, film or source usable footage, edit a video with proper pacing and sound design, add simple motion graphics and captions, and export a finished piece suitable for a portfolio or client delivery.",
    "final_project": {
        "title": "Produce a Portfolio-Ready Short Video or Motion Piece",
        "description": "Script, shoot (or storyboard and animate), edit, and export a finished short video or motion piece — between 30 seconds and 3 minutes — suitable for a portfolio reel or an actual client. Choose a realistic brief: a product ad, a brand story reel, an explainer, or a short narrative piece, for a real or realistic client. The final deliverable must include a written script or storyboard, edited footage or animation with sound design and at least one motion graphic element (lower third, title card, or animated text), and a final exported video file ready to share. Present it with a one-paragraph creative brief explaining the goal, audience, and your key creative choices, exactly as you would to a client.",
        "difficulty": "advanced",
        "estimated_hours": 12,
        "skills_demonstrated": ["scripting", "shooting/storyboarding", "video editing", "pacing", "sound design", "motion graphics", "color and export", "client presentation"],
        "rubric": [
            {"name": "Script/storyboard and planning quality", "max_points": 20},
            {"name": "Editing craft — pacing, cuts, and story flow", "max_points": 30},
            {"name": "Visual and sound production quality", "max_points": 25},
            {"name": "Motion graphics and final polish/export", "max_points": 25}
        ]
    },
    "days": [
        {
            "day_number": 1,
            "week_number": 1,
            "week_title": "Foundations of Video Storytelling",
            "title": "Why Every Great Video Starts With a One-Sentence Story Goal",
            "learning_objective": "By the end of this class, you will be able to write a one-sentence story goal that defines what a video must make its viewer feel or do.",
            "duration_minutes": 25,
            "content_html": "<p>Before touching a camera or editing app, every professional video starts with one question answered clearly: what should the viewer feel or do after watching this? Skipping this step is why so many beginner videos feel directionless even when the shots look nice.</p><h2>The One-Sentence Story Goal</h2><p>A story goal names the viewer's emotion or action at the end: \"I want the viewer to feel FOMO and tap the link to book a table\" or \"I want the viewer to trust this brand enough to follow the page.\" Every shot, cut, and piece of music should serve that one sentence.</p><h2>Worked Example</h2><p>Brief: \"Make a video for a new food delivery app.\" Weak goal: \"Show the app is good.\" Strong goal: <strong>\"I want the viewer to feel the relief of not cooking after a long day, and download the app before they close Instagram.\"</strong> This single sentence now tells you to open with a tired-after-work scene, not a screenshot of the app's menu.</p><ul><li>Write your story goal before writing a script or picking up a camera</li><li>A story goal names both an emotion AND an action</li><li>If a shot doesn't serve the story goal, cut it — even if it looks nice</li></ul>",
            "key_concepts": ["story goal", "viewer emotion", "purposeful editing", "pre-production thinking"],
            "practical_exercise": {
                "title": "Write Three Story Goals",
                "instructions": "Choose three different types of video (a product ad, a brand story, and a tutorial) for any brand or idea of your choice. For each, write one clear story goal sentence naming the target emotion and the target viewer action. Submit all three story goals."
            },
            "quiz": [
                {"question": "What should a story goal define?", "options": ["The camera brand to use", "The emotion and action a viewer should have after watching", "The exact runtime in seconds", "The video's file format"], "correct_index": 1, "explanation": "A story goal names the target emotional response and desired action, guiding every creative decision that follows."},
                {"question": "When should the story goal be written?", "options": ["After the final edit is exported", "Before scripting or shooting begins", "Only if the client asks for it", "It is optional and rarely useful"], "correct_index": 1, "explanation": "Writing the story goal first ensures every subsequent decision — shots, pacing, music — serves a clear purpose."},
                {"question": "What should happen to a nice-looking shot that doesn't serve the story goal?", "options": ["It should always be included regardless", "It should generally be cut, even if visually appealing", "It should replace the story goal", "It should be shown twice"], "correct_index": 1, "explanation": "Shots that don't serve the defined story goal weaken focus and should usually be cut, no matter how good they look alone."}
            ],
            "resources": []
        },
        {
            "day_number": 2,
            "week_number": 1,
            "week_title": "Foundations of Video Storytelling",
            "title": "Shot Types and What Each One Tells the Viewer",
            "learning_objective": "By the end of this class, you will be able to identify and plan wide, medium, and close-up shots for a specific storytelling purpose.",
            "duration_minutes": 25,
            "content_html": "<p>A video made entirely of one shot type — usually medium shots of someone talking — feels flat no matter how good the content is. Understanding what each shot type communicates lets you plan footage that keeps a viewer engaged, using just a phone camera.</p><h2>The Three Core Shot Types</h2><p>Wide shot: establishes location and context — \"where are we?\" Medium shot: shows a person from the waist up, the default for dialogue or talking-head content. Close-up: shows emotion or important detail — a face, a product, hands doing something specific.</p><h2>Worked Example: Shooting a Skincare Product Video</h2><p>Wide shot: the bathroom shelf where the product sits, establishing everyday context. Medium shot: a person picking up the product, showing natural use. Close-up: <strong>the product being applied to skin, and a close-up of the person's satisfied expression.</strong> This three-shot sequence alone can carry an entire 15-second ad without feeling repetitive.</p><ul><li>Every scene should mix at least two shot types to avoid visual monotony</li><li>Close-ups do the emotional heavy lifting — use them for reactions and key details</li><li>Wide shots are best at the start of a scene, to orient the viewer before going closer</li></ul>",
            "key_concepts": ["wide shot", "medium shot", "close-up", "shot variety"],
            "practical_exercise": {
                "title": "Plan a Three-Shot Sequence",
                "instructions": "Choose any simple everyday action (making tea, tying a shoe, opening a laptop). Write a shot list of exactly three shots — one wide, one medium, one close-up — describing what each shot shows and why. Submit the shot list."
            },
            "quiz": [
                {"question": "What does a wide shot typically establish?", "options": ["A character's emotion", "The location and context of a scene", "The exact dialogue being spoken", "The video's color grade"], "correct_index": 1, "explanation": "Wide shots orient the viewer by showing where the scene is taking place."},
                {"question": "Which shot type is best for showing emotional reactions or important detail?", "options": ["Wide shot", "Close-up", "Aerial shot", "Establishing shot"], "correct_index": 1, "explanation": "Close-ups isolate faces or details, making them the most effective for conveying emotion or important specifics."},
                {"question": "Why should a scene mix at least two shot types?", "options": ["To meet a legal video requirement", "To avoid visual monotony and keep viewers engaged", "Mixing shot types is never recommended", "It only matters for feature films"], "correct_index": 1, "explanation": "Varying shot types keeps the viewer visually engaged rather than watching one static framing for too long."}
            ],
            "resources": []
        },
        {
            "day_number": 3,
            "week_number": 1,
            "week_title": "Foundations of Video Storytelling",
            "title": "Getting Clean Footage With Just a Phone — Light, Stability, Sound",
            "learning_objective": "By the end of this class, you will be able to shoot a stable, well-lit, clear-audio clip using only a smartphone.",
            "duration_minutes": 30,
            "content_html": "<p>You don't need expensive gear to produce usable video — most professional-looking phone footage comes down to three fundamentals: light, stability, and audio. Get these right and even a basic phone camera looks professional; get them wrong and no editing can fully save the footage.</p><h2>The Three Fundamentals</h2><p>Light: face a window or light source — never shoot with the light source behind your subject (backlighting creates a silhouette). Stability: brace your arms against your body, or use a cheap tripod/stack of books — handheld shake is the #1 sign of amateur footage. Audio: get the microphone close to the sound source; phone mics struggle with distance and background noise.</p><h2>Worked Example: A Simple Home Setup</h2><p>Position your subject facing a window during daytime (free, even lighting). Prop the phone against a stack of books at chest height instead of holding it. <strong>If recording speech, use wired earphones with a mic, held near the mouth, instead of relying on the phone's built-in mic from a distance.</strong> This basic setup alone produces footage that looks far more professional than handheld, backlit, distant-mic footage.</p><ul><li>Natural window light is the most reliable free lighting source available</li><li>Any stabilization (tripod, books, wall) beats handheld shooting</li><li>Audio quality affects perceived professionalism more than most beginners expect</li></ul>",
            "key_concepts": ["natural lighting", "backlighting", "camera stability", "audio proximity"],
            "practical_exercise": {
                "title": "Shoot a 15-Second Stable, Well-Lit Clip",
                "instructions": "Using only a smartphone, shoot a 15-second clip of any subject applying the three fundamentals: face a light source (not backlit), stabilize the camera (no handheld shake), and record clear audio if there's speech. Write a short note describing your setup (light source, stabilization method, mic position) alongside your description of the shot."
            },
            "quiz": [
                {"question": "What problem does backlighting cause?", "options": ["It makes colors too bright", "It creates a silhouette effect that obscures the subject's face", "It has no effect on footage", "It only affects audio quality"], "correct_index": 1, "explanation": "When the light source is behind the subject, the camera exposes for the background, turning the subject into a dark silhouette."},
                {"question": "What is the most common sign of amateur, unstable footage?", "options": ["Handheld camera shake", "Too much light", "Correct audio levels", "Using a wide shot"], "correct_index": 0, "explanation": "Uncontrolled handheld movement is one of the clearest visual signs of unpolished footage."},
                {"question": "Why is microphone proximity important for phone audio recording?", "options": ["Phone mics work equally well at any distance", "Phone mics struggle with distance and pick up more background noise farther away", "Distance has no effect on audio clarity", "Closer mics always distort sound"], "correct_index": 1, "explanation": "Built-in phone mics are much more sensitive to distance and ambient noise, so keeping the mic close improves clarity significantly."}
            ],
            "resources": []
        },
        {
            "day_number": 4,
            "week_number": 1,
            "week_title": "Foundations of Video Storytelling",
            "title": "Setting Up Your First Editing Timeline",
            "learning_objective": "By the end of this class, you will be able to import footage into an editing app and assemble a basic sequence of clips on a timeline.",
            "duration_minutes": 30,
            "content_html": "<p>Editing is where a pile of raw clips becomes an actual story. Today's job is purely mechanical: understanding how a timeline works, so every later lesson on pacing and effects has a foundation to build on. Free tools like CapCut and DaVinci Resolve are industry-relevant and used by working professionals, not just beginners.</p><h2>Understanding the Timeline</h2><p>A timeline is built from tracks stacked vertically (video on top, audio below) and time moving left to right. Clips are placed end to end (a 'cut') or overlapped (a transition). The playhead shows your current position; scrubbing moves through the footage without playing it.</p><h2>Worked Example: A First Rough Assembly</h2><p>Import 5 clips. Arrange them on the timeline in story order (not necessarily the order you filmed them). Trim each clip's start and end to remove dead air or shaky moments — <strong>a 10-second raw clip might become a clean 3-second cut in the final sequence.</strong> This rough assembly, even unpolished, is the essential first pass every editor does before refining pacing or adding effects.</p><ul><li>Video and audio tracks stack vertically; time flows left to right</li><li>Always do a rough assembly cut first — refine pacing and effects only after the story order is locked</li><li>Trimming dead space at the start/end of every clip is the single highest-impact first edit</li></ul>",
            "key_concepts": ["editing timeline", "rough assembly", "trimming", "tracks and playhead"],
            "practical_exercise": {
                "title": "Assemble a Rough Cut",
                "instructions": "Using any editing app (CapCut, DaVinci Resolve, or similar), import at least 4 short clips (your own footage or stock/phone clips) and assemble them into a rough cut on the timeline, trimming each clip's dead space at the start and end. Export or screen-record the resulting timeline/sequence and describe your trim decisions in one paragraph."
            },
            "quiz": [
                {"question": "In a typical editing timeline, how are video and audio organized?", "options": ["Randomly placed anywhere", "Stacked vertically in tracks, with time moving left to right", "Audio always comes before video chronologically", "There is no fixed structure"], "correct_index": 1, "explanation": "Standard timelines stack tracks vertically (video, audio) while time progresses horizontally from left to right."},
                {"question": "What is a 'rough assembly' in editing?", "options": ["The final polished export", "The first pass of arranging clips in story order before refining pacing/effects", "A type of video transition", "A color grading technique"], "correct_index": 1, "explanation": "A rough assembly is the initial, unpolished arrangement of clips in the correct story order, done before finer editing work."},
                {"question": "What is often the highest-impact first edit to make on raw footage?", "options": ["Adding music immediately", "Trimming dead space at the start and end of each clip", "Applying color grading first", "Adding text overlays before anything else"], "correct_index": 1, "explanation": "Removing dead space tightens pacing immediately and is typically the first, most impactful trimming step."}
            ],
            "resources": [{"label": "CapCut", "url": "https://www.capcut.com"}]
        },
        {
            "day_number": 5,
            "week_number": 1,
            "week_title": "Foundations of Video Storytelling",
            "title": "Cutting on Action and Basic Pacing Rhythm",
            "learning_objective": "By the end of this class, you will be able to apply the 'cut on action' technique to make a transition between two clips feel seamless.",
            "duration_minutes": 25,
            "content_html": "<p>The difference between an edit that feels invisible and one that feels jarring often comes down to a single technique: cutting on action. This is one of the most-used tricks in professional editing, and it's simple enough to apply from your very first project.</p><h2>What Cutting on Action Means</h2><p>Instead of cutting between two static shots, cut in the middle of a movement — a hand reaching for a door, a person starting to sit down. The viewer's brain focuses on the motion and barely registers the shot change, making the cut feel smooth and natural.</p><h2>Worked Example</h2><p>Bad cut: Shot A shows a person standing still. Shot B shows the same person already seated. This feels like a jump — jarring and amateurish. Good cut: <strong>Shot A shows the person beginning to bend their knees to sit; cut to Shot B mid-motion, showing them continuing to sit down from a slightly different angle.</strong> The motion continuity hides the cut almost entirely.</p><ul><li>Cutting on action works because the brain is distracted by motion during the cut point</li><li>Always shoot a little extra footage before and after an action, so you have material to cut on</li><li>Pacing rhythm — fast cuts for energy, slow holds for emotion — should match your Day 1 story goal</li></ul>",
            "key_concepts": ["cut on action", "seamless transitions", "pacing rhythm", "match cut"],
            "practical_exercise": {
                "title": "Edit a Cut-on-Action Sequence",
                "instructions": "Shoot or use existing footage of a simple physical action broken into two clips (e.g. someone starting to open a door, then the door open). Edit them together using the cut-on-action technique so the transition feels seamless. Submit the edited clip or a description of exactly where you placed the cut point and why."
            },
            "quiz": [
                {"question": "What is 'cutting on action'?", "options": ["Cutting only between static shots", "Cutting in the middle of a movement so the transition feels seamless", "Removing all action scenes from a video", "A technique only used in action movies"], "correct_index": 1, "explanation": "Cutting mid-movement distracts the viewer's brain with motion, making the shot change nearly invisible."},
                {"question": "Why does cutting on action feel smoother than cutting between static shots?", "options": ["It uses more colorful footage", "The viewer's attention is focused on the motion, masking the cut", "It is technically not a real cut", "Static shots are always jarring regardless of cut placement"], "correct_index": 1, "explanation": "Motion during a cut naturally draws viewer attention away from the transition itself, making it feel continuous."},
                {"question": "Why should you shoot extra footage before and after an action?", "options": ["It is unnecessary and wastes storage", "It gives you material to find the right cut-on-action point later", "Extra footage automatically improves lighting", "It replaces the need for editing entirely"], "correct_index": 1, "explanation": "Having buffer footage around an action gives the editor flexibility to find the ideal seamless cut point in post-production."}
            ],
            "resources": []
        },
        {
            "day_number": 6,
            "week_number": 2,
            "week_title": "Sound, Color, and Text",
            "title": "Sound Design Basics — Music, SFX, and Levels That Don't Clash",
            "learning_objective": "By the end of this class, you will be able to layer background music and dialogue audio with balanced levels so neither overpowers the other.",
            "duration_minutes": 25,
            "content_html": "<p>Viewers forgive rough visuals more than they forgive bad audio — muddy sound or music that drowns out dialogue makes a video feel unwatchable within seconds. Sound design is one of the most underrated skills separating amateur from professional-feeling video.</p><h2>Layering Audio Without Clashing</h2><p>Dialogue/voiceover should always sit as the loudest, clearest layer. Background music should sit noticeably lower — a common professional technique called 'ducking' automatically lowers music volume whenever speech is present. Sound effects (SFX) add texture (a click, a whoosh on a transition) but should never compete with dialogue.</p><h2>Worked Example: Balancing a Voiceover Video</h2><p>Voiceover track: kept at a strong, clear volume throughout. Background music: brought in at roughly 15-20% of the voiceover's volume during speech, then raised to full volume during silent visual moments. <strong>A whoosh SFX added on a text transition, kept brief and subtle, adds polish without distracting from the message.</strong></p><ul><li>Dialogue clarity is non-negotiable — always prioritize it over background music volume</li><li>Ducking (lowering music under speech) is a simple, learnable technique in most editing apps</li><li>Use SFX sparingly — overused sound effects quickly feel amateurish and distracting</li></ul>",
            "key_concepts": ["audio ducking", "dialogue priority", "sound effects", "audio levels"],
            "practical_exercise": {
                "title": "Layer and Balance Three Audio Elements",
                "instructions": "Take a clip with dialogue or voiceover (yours or existing footage). Add a background music track and at least one sound effect. Adjust levels so the dialogue remains clearly audible throughout, with music ducked lower during speech. Submit the edited clip or a written description of your exact volume levels for each layer."
            },
            "quiz": [
                {"question": "What is 'ducking' in audio editing?", "options": ["Removing all background music", "Automatically lowering music volume when dialogue is present", "Increasing sound effects volume", "A technique only used in music videos"], "correct_index": 1, "explanation": "Ducking automatically reduces background music levels during speech so dialogue remains clear and prioritized."},
                {"question": "Which audio element should generally be the loudest, clearest layer?", "options": ["Background music", "Sound effects", "Dialogue or voiceover", "Ambient room noise"], "correct_index": 2, "explanation": "Dialogue clarity is essential for viewer comprehension, so it should take priority over music and effects."},
                {"question": "What happens when sound effects are overused in a video?", "options": ["The video automatically feels more professional", "It quickly starts to feel amateurish and distracting", "It has no impact on viewer perception", "It always improves audience retention"], "correct_index": 1, "explanation": "Excessive or unnecessary SFX draws attention away from the content and tends to read as unpolished, not enhancing."}
            ],
            "resources": [{"label": "Adobe Premiere Pro", "url": "https://www.adobe.com/products/premiere.html"}]
        },
        {
            "day_number": 7,
            "week_number": 2,
            "week_title": "Sound, Color, and Text",
            "title": "Basic Color Correction — Making Footage Look Consistent",
            "learning_objective": "By the end of this class, you will be able to apply basic exposure and white balance correction to make two differently-lit clips look visually consistent.",
            "duration_minutes": 25,
            "content_html": "<p>Footage shot at different times or locations often looks inconsistent — one clip too warm, another too dark. Color correction (different from stylistic color grading) is the essential first step of fixing this, and it's a skill every working editor uses on nearly every project.</p><h2>Correction vs Grading</h2><p>Color correction: fixing technical problems — exposure (too dark/bright) and white balance (too orange/too blue), so footage looks natural and consistent. Color grading: an optional creative style layered on TOP of correction (cinematic teal-and-orange, warm nostalgic tones, etc). Correction must always come first.</p><h2>Worked Example: Matching Two Clips</h2><p>Clip A was shot near a window (cooler, bluish tone). Clip B was shot under a yellow room bulb (warmer, orange tone). Correction: adjust Clip B's white balance cooler to match Clip A's neutral tone, and adjust exposure so both clips have similar brightness. <strong>Once both clips look neutrally consistent, THEN you could apply the same creative grade to both for a unified stylistic look.</strong></p><ul><li>Fix exposure and white balance before applying any creative color style</li><li>Consistency across clips matters more to viewers than any single clip looking 'perfect'</li><li>Most free editing apps (CapCut, DaVinci Resolve) include basic exposure/white balance sliders</li></ul>",
            "key_concepts": ["color correction", "white balance", "exposure", "color grading vs correction"],
            "practical_exercise": {
                "title": "Correct Two Mismatched Clips",
                "instructions": "Find or shoot two clips taken in different lighting conditions (different rooms, times of day). Using any editing app, adjust exposure and white balance on each so they look visually consistent with each other when placed side by side or back to back. Submit before/after screenshots or a description of the specific adjustments made."
            },
            "quiz": [
                {"question": "What is the difference between color correction and color grading?", "options": ["They are the same thing", "Correction fixes technical issues; grading applies a creative style, and correction comes first", "Grading always comes before correction", "Correction is only for black-and-white footage"], "correct_index": 1, "explanation": "Correction fixes fundamental technical issues like exposure and white balance; grading is a creative style applied afterward."},
                {"question": "What does white balance correction fix?", "options": ["Audio levels", "Whether footage looks too orange or too blue/cool", "Video resolution", "Frame rate mismatches"], "correct_index": 1, "explanation": "White balance correction adjusts the color temperature of footage so whites and neutral tones look natural, not overly warm or cool."},
                {"question": "Why does visual consistency across clips matter more than any single clip looking perfect?", "options": ["It doesn't matter to viewers at all", "Inconsistent lighting/color between clips is jarring and breaks immersion", "Only the first clip in a video matters", "Consistency only matters for feature films"], "correct_index": 1, "explanation": "Viewers notice jumps in color and brightness between clips, so overall consistency is more important than any single perfect shot."}
            ],
            "resources": [{"label": "Adobe Premiere Pro", "url": "https://www.adobe.com/products/premiere.html"}]
        },
        {
            "day_number": 8,
            "week_number": 2,
            "week_title": "Sound, Color, and Text",
            "title": "Captions and On-Screen Text That People Actually Read",
            "learning_objective": "By the end of this class, you will be able to add readable, well-timed captions and text overlays to a short video clip.",
            "duration_minutes": 25,
            "content_html": "<p>Most social video is watched with the sound off — captions aren't optional anymore, they're often how the majority of your audience consumes the content at all. Readable, well-timed text is now a core, expected editing skill.</p><h2>Rules for Readable On-Screen Text</h2><p>Keep captions short — 1-2 lines max, synced tightly to speech. Use high-contrast text (white text with a dark outline/background works on almost any footage). Never let text sit in the same spot as important visual action; keep it in a consistent safe zone (usually lower or upper third).</p><h2>Worked Example: Captioning a Talking-Head Clip</h2><p>Bad: a full paragraph of text appearing all at once, small font, low contrast against a busy background. Good: <strong>short caption chunks (\"Most people quit\" / \"in the first 30 days\") appearing in sync with speech, bold white text with a subtle black outline, positioned in the lower third.</strong> This keeps text legible on any device and any background.</p><ul><li>Sound-off viewing is now the majority use case for social video — captions are essential, not optional</li><li>Break long sentences into short caption chunks synced to natural speech pauses</li><li>Auto-caption tools (built into CapCut and similar apps) are industry-standard starting points — always proofread and correct them</li></ul>",
            "key_concepts": ["captions", "on-screen text", "safe zones", "sound-off viewing"],
            "practical_exercise": {
                "title": "Caption a Short Talking Clip",
                "instructions": "Take a short clip (yours or existing) with speech. Add synced captions broken into short, readable chunks, using high-contrast text positioned in a consistent safe zone. If using an auto-caption tool, proofread and correct any errors. Submit the captioned clip or a screenshot sequence showing the captions in place."
            },
            "quiz": [
                {"question": "Why are captions now considered essential rather than optional for social video?", "options": ["They are required by law in most countries", "Most social video is watched with the sound off", "Captions replace the need for good audio entirely", "They are only used for accessibility, nothing else"], "correct_index": 1, "explanation": "Since a majority of viewers watch social video without sound, captions are often the only way the message is received at all."},
                {"question": "What makes on-screen text easy to read across different backgrounds?", "options": ["Small font size with low contrast", "High-contrast text, such as white with a dark outline", "Placing text randomly across the frame", "Using the same color as the background"], "correct_index": 1, "explanation": "High-contrast styling (like white text with a dark outline) keeps captions legible regardless of what's happening in the background footage."},
                {"question": "What should always be done with auto-generated captions before publishing?", "options": ["Nothing, they are always perfectly accurate", "They should be proofread and corrected", "They should be deleted and never used", "They only need review for videos under 10 seconds"], "correct_index": 1, "explanation": "Auto-caption tools are a useful starting point but frequently contain errors that need human review and correction."}
            ],
            "resources": [{"label": "CapCut", "url": "https://www.capcut.com"}]
        },
        {
            "day_number": 9,
            "week_number": 2,
            "week_title": "Sound, Color, and Text",
            "title": "Transitions — When to Use Them and When to Just Cut",
            "learning_objective": "By the end of this class, you will be able to choose an appropriate transition style for a given scene change and justify the choice.",
            "duration_minutes": 25,
            "content_html": "<p>New editors often overuse flashy transitions, thinking more effects mean more professional work. In reality, professional editors default to a simple hard cut most of the time, and reach for a special transition only when it serves the story.</p><h2>Matching Transition to Story Purpose</h2><p>Hard cut: the default, invisible, works for most scene changes. Cross dissolve (fade between two clips): signals time passing or a soft emotional shift. Whip pan / fast zoom: signals energy or a fast change in location, common in social content. Fade to black: signals a clear ending or a major tonal shift.</p><h2>Worked Example</h2><p>A video showing a morning routine: hard cuts between each small action (brushing teeth, making tea) keep energy tight. A dissolve is used once, showing the transition from morning at home to arriving at school hours later — <strong>signaling time passing without needing an on-screen clock or caption.</strong> A whip-pan transition adds energy to a fast montage of getting dressed.</p><ul><li>Default to hard cuts; a transition should be a deliberate choice, not a default habit</li><li>Match the transition's feeling to what's happening in the story at that moment</li><li>Using 5 different flashy transition styles in one short video usually reads as amateur, not creative</li></ul>",
            "key_concepts": ["hard cut", "cross dissolve", "whip pan", "transition purpose"],
            "practical_exercise": {
                "title": "Justify Three Transition Choices",
                "instructions": "Plan a short video with three distinct scene changes (can be hypothetical or based on real footage). For each scene change, specify which transition type you would use (hard cut, dissolve, whip pan, or fade to black) and write one sentence justifying why that transition fits the story moment. Submit the three transition choices and justifications."
            },
            "quiz": [
                {"question": "What is the default, most commonly used transition in professional editing?", "options": ["A spinning 3D cube transition", "The hard cut", "A slow fade to white", "A glitch transition"], "correct_index": 1, "explanation": "Hard cuts are the invisible default used for most scene changes; flashy transitions are reserved for specific purposes."},
                {"question": "What does a cross dissolve typically signal to a viewer?", "options": ["High energy and fast action", "The passing of time or a soft emotional shift", "The end of the entire video", "A change of camera brand"], "correct_index": 1, "explanation": "A dissolve gently blends two shots, commonly used to suggest time passing or a subtle emotional transition."},
                {"question": "Why is overusing many different flashy transitions in one short video usually a mistake?", "options": ["It is always technically impossible", "It typically reads as amateur rather than professional or creative", "Flashy transitions are illegal on social platforms", "It has no impact on viewer perception"], "correct_index": 1, "explanation": "Overusing varied flashy transitions is a common beginner habit that tends to distract from the story rather than enhance it."}
            ],
            "resources": []
        },
        {
            "day_number": 10,
            "week_number": 2,
            "week_title": "Sound, Color, and Text",
            "title": "Exporting Correctly for Different Platforms",
            "learning_objective": "By the end of this class, you will be able to export a finished video with the correct aspect ratio, resolution, and format for a specific platform.",
            "duration_minutes": 25,
            "content_html": "<p>A brilliantly edited video with the wrong export settings looks broken the moment it's published — cropped awkwardly, blurry, or rejected by the platform. Export settings are a small technical detail with a big visible impact, and clients expect editors to get this right without being told.</p><h2>Platform-Specific Export Basics</h2><p>Vertical (9:16, e.g. 1080x1920): Instagram Reels, TikTok, YouTube Shorts, WhatsApp Status. Square (1:1, 1080x1080): Instagram feed posts (still common). Horizontal (16:9, 1920x1080): YouTube, most website embeds, TV/projector presentations. Match your shooting orientation to your intended platform whenever possible.</p><h2>Worked Example: Exporting One Video for Two Platforms</h2><p>A brand story video shot in 16:9 needs to go on both YouTube (horizontal, no change needed) and Instagram Reels (vertical). <strong>Rather than just squeezing/stretching the footage, reframe key shots for the vertical crop, repositioning subjects and text so nothing important gets cut off at the edges.</strong> Export settings: H.264 codec, MP4 format, and platform-recommended bitrate are safe universal defaults.</p><ul><li>Never stretch footage to fit a different aspect ratio — reframe or crop deliberately instead</li><li>MP4 (H.264 codec) is the safest universal export format across nearly all platforms</li><li>Always preview the exported file before sending to a client or publishing</li></ul>",
            "key_concepts": ["aspect ratio", "export settings", "platform formatting", "reframing for vertical"],
            "practical_exercise": {
                "title": "Export the Same Clip for Two Aspect Ratios",
                "instructions": "Take any short edited clip. Export it once in 16:9 horizontal format and once reframed (not stretched) for 9:16 vertical format, repositioning key subjects/text so nothing important is cropped out. Submit both exported versions or screenshots comparing the two framings."
            },
            "quiz": [
                {"question": "What aspect ratio is standard for Instagram Reels and TikTok?", "options": ["16:9 horizontal", "1:1 square", "9:16 vertical", "4:3"], "correct_index": 2, "explanation": "Reels, TikTok, and YouTube Shorts are all designed for the 9:16 vertical format."},
                {"question": "What is the correct way to adapt horizontal footage for a vertical platform?", "options": ["Stretch the footage to fill the vertical frame", "Reframe or crop deliberately to keep key subjects in view", "It cannot be adapted at all", "Simply add black bars with no other changes"], "correct_index": 1, "explanation": "Stretching distorts the image; deliberate reframing preserves visual quality and keeps important content visible."},
                {"question": "What is a safe, universal export format for most platforms?", "options": ["A proprietary raw camera file", "MP4 with the H.264 codec", "An uncompressed BMP sequence", "A PowerPoint file"], "correct_index": 1, "explanation": "MP4 with H.264 encoding is widely compatible across nearly all major social and web platforms."}
            ],
            "resources": [{"label": "CapCut", "url": "https://www.capcut.com"}]
        },
        {
            "day_number": 11,
            "week_number": 3,
            "week_title": "Intermediate Editing and Motion Graphics",
            "title": "Scripting a Short Video From Hook to Payoff",
            "learning_objective": "By the end of this class, you will be able to write a full short-video script with a timed hook, body, and payoff structure.",
            "duration_minutes": 25,
            "content_html": "<p>Editing quality can't save a video with no clear script structure — viewers drop off within the first 3 seconds if there's no hook, and unclear structure loses them even if they stay. Scripting is where the video's success is decided before any footage is shot.</p><h2>The Hook-Body-Payoff Structure</h2><p>Hook (0-3 seconds): a bold statement, question, or visual surprise that stops the scroll. Body: the value or story delivered clearly and efficiently. Payoff: the resolution — a punchline, a result reveal, or a clear CTA.</p><h2>Worked Example: 30-Second Product Script</h2><p>Hook (0-3s): \"I wasted ₦50,000 before I found this.\" Body (3-22s): show the specific problem, then the product solving it, with 2-3 quick supporting shots. Payoff (22-30s): <strong>\"Now I never run out mid-month — link in bio.\"</strong> paired with a clear final product shot and on-screen CTA text.</p><ul><li>Write the exact timing next to each script section — this trains pacing discipline early</li><li>The hook must work even with sound off, since many viewers scroll on mute</li><li>Every script should end with one clear payoff, not a vague trail-off</li></ul>",
            "key_concepts": ["video script", "hook-body-payoff", "scroll-stopping hook", "timed structure"],
            "practical_exercise": {
                "title": "Write a Timed 30-Second Script",
                "instructions": "Choose a product, service, or idea. Write a full 30-second video script broken into hook (0-3s), body (3-22s), and payoff (22-30s) sections, including both spoken/voiceover lines and a brief description of the visuals for each section. Submit the timed script."
            },
            "quiz": [
                {"question": "Why is the hook (first 0-3 seconds) so critical in a short video script?", "options": ["It has no real impact on viewer retention", "Viewers commonly drop off within the first few seconds without a strong hook", "The hook is only important for long-form videos", "It should always be the longest section"], "correct_index": 1, "explanation": "Social video viewers decide within seconds whether to keep watching, making the hook the single highest-leverage part of the script."},
                {"question": "Why must a hook work even with the sound off?", "options": ["Sound is never used in video", "Many viewers scroll and watch content muted by default", "Hooks are always purely visual by definition", "It doesn't need to work without sound"], "correct_index": 1, "explanation": "Since a large portion of viewers watch on mute, a hook relying only on audio risks losing them immediately."},
                {"question": "What should a script's payoff section deliver?", "options": ["A vague, open-ended trail-off", "A clear resolution — a result, punchline, or CTA", "Another hook to restart the video", "Nothing; payoffs are optional"], "correct_index": 1, "explanation": "A strong payoff gives the viewer clear closure or a next action, rather than leaving the video feeling unfinished."}
            ],
            "resources": []
        },
        {
            "day_number": 12,
            "week_number": 3,
            "week_title": "Intermediate Editing and Motion Graphics",
            "title": "Introduction to Keyframes — Animating Text and Objects",
            "learning_objective": "By the end of this class, you will be able to use keyframes to animate a text element's position or opacity over time.",
            "duration_minutes": 30,
            "content_html": "<p>Keyframes are the foundation of all motion graphics — from a simple text fade-in to complex animated logos. Understanding this one concept unlocks the ability to animate almost anything inside an editing or motion app.</p><h2>How Keyframes Work</h2><p>A keyframe marks a specific value (position, size, opacity, rotation) at a specific point in time. Set two keyframes with different values, and the software automatically calculates the smooth animation between them — this is called 'interpolation.'</p><h2>Worked Example: Animating a Text Fade-In and Slide</h2><p>Keyframe 1 (at 0 seconds): text opacity = 0%, position = 20px below its final spot. Keyframe 2 (at 0.5 seconds): text opacity = 100%, position = final spot. <strong>The software automatically animates the text fading in while sliding up into place over that half-second — this exact technique is used in nearly every lower-third title you see on professional video.</strong></p><ul><li>Two keyframes minimum are needed to create any animation — one alone does nothing</li><li>Keep simple animations short (0.3-0.6 seconds) so they feel snappy, not sluggish</li><li>Most editing apps (CapCut, Premiere, DaVinci Resolve, After Effects) all use this same keyframe logic</li></ul>",
            "key_concepts": ["keyframes", "interpolation", "animation timing", "opacity and position animation"],
            "practical_exercise": {
                "title": "Animate a Text Fade-and-Slide",
                "instructions": "Using any editing app that supports keyframes, create a text element and animate it fading in while sliding into position over 0.3-0.6 seconds using two keyframes. Submit a screen recording or exported clip of the animation, plus a note on the exact keyframe values you set."
            },
            "quiz": [
                {"question": "What is a keyframe?", "options": ["A type of video transition", "A marker that sets a specific value at a specific point in time for animation", "The first frame of any video", "A sound effect trigger"], "correct_index": 1, "explanation": "A keyframe records a property's value at a moment in time; the software interpolates between keyframes to create motion."},
                {"question": "How many keyframes are minimally needed to create an animation?", "options": ["One", "Two", "Ten", "Zero"], "correct_index": 1, "explanation": "At least two keyframes with different values are required so the software has something to interpolate between."},
                {"question": "What is 'interpolation' in the context of keyframe animation?", "options": ["Manually drawing every frame", "The software automatically calculating the smooth transition between keyframe values", "A type of audio effect", "Removing keyframes from a timeline"], "correct_index": 1, "explanation": "Interpolation is the automatic calculation of in-between values, producing smooth motion between two keyframes."}
            ],
            "resources": [{"label": "Adobe Premiere Pro", "url": "https://www.adobe.com/products/premiere.html"}]
        },
        {
            "day_number": 13,
            "week_number": 3,
            "week_title": "Intermediate Editing and Motion Graphics",
            "title": "Building a Lower Third and Title Card Template",
            "learning_objective": "By the end of this class, you will be able to design and animate a reusable lower-third graphic with a name and title.",
            "duration_minutes": 30,
            "content_html": "<p>Lower thirds (name/title graphics at the bottom of the screen) and title cards are staples of interview content, brand videos, and explainer videos. Editors who can build clean, reusable templates save huge amounts of time on every future project.</p><h2>Anatomy of a Good Lower Third</h2><p>A simple, effective lower third has: a background shape (a bar or box, often brand-colored), primary text (name, bold and larger), secondary text (title/role, smaller), and a subtle entrance/exit animation using keyframes from Day 12.</p><h2>Worked Example: Interview Lower Third</h2><p>Background: a solid brand-color bar, semi-transparent, positioned in the lower-left third of the frame. Primary text: \"Amaka Chukwu\" in bold white. Secondary text: <strong>\"Founder, Lagos Skincare Co.\"</strong> in a smaller, lighter weight beneath it. Animation: slides in from the left over 0.4 seconds, holds for the duration of the speaker's segment, then slides out.</p><ul><li>Keep lower thirds legible — high contrast text against the background bar is essential</li><li>Build it once as a reusable template — swap only the text for future videos to save time</li><li>Standard on-screen duration is long enough to read twice comfortably, not just a flash</li></ul>",
            "key_concepts": ["lower third design", "title card", "reusable template", "text hierarchy"],
            "practical_exercise": {
                "title": "Design and Animate a Lower Third",
                "instructions": "Using any editing or design app, build a lower-third graphic with a background bar, a primary name text, and a secondary title text, and animate it sliding or fading in and out. Use a realistic name and title relevant to your final project brand. Submit the exported clip or screen recording of the lower third in action."
            },
            "quiz": [
                {"question": "What are the two main text elements of a typical lower third?", "options": ["A hashtag and an emoji", "Primary text (name) and secondary text (title/role)", "Only a company logo", "A full paragraph of biography"], "correct_index": 1, "explanation": "A standard lower third pairs a bold primary name with a smaller secondary title or role description."},
                {"question": "Why should a lower third be built as a reusable template?", "options": ["Templates cannot be reused across projects", "It saves significant time on future videos by only swapping the text", "Reusable templates are against industry standards", "It has no practical benefit"], "correct_index": 1, "explanation": "A well-built template lets an editor quickly reuse the same design across many projects, just updating the text content."},
                {"question": "What is essential for a lower third's readability?", "options": ["Low contrast between text and background", "High contrast between the text and its background bar", "Using the smallest possible font", "Removing any background shape"], "correct_index": 1, "explanation": "High contrast ensures the text remains legible against varying video footage behind it."}
            ],
            "resources": []
        },
        {
            "day_number": 14,
            "week_number": 3,
            "week_title": "Intermediate Editing and Motion Graphics",
            "title": "Case Study: Deconstructing a Viral Short-Form Video",
            "learning_objective": "By the end of this class, you will be able to analyze a short-form video and identify the specific editing, pacing, and hook choices that drove its performance.",
            "duration_minutes": 25,
            "content_html": "<p>Studying videos that actually performed well — critically, not just as a viewer — trains your editing instincts faster than tutorials alone. Professional editors constantly reverse-engineer what's working right now, because trends and platform behavior shift quickly.</p><h2>A Framework for Deconstructing Video</h2><p>For any well-performing short video, ask: What was the hook in the first 3 seconds? How fast are the cuts (average shot length)? What text/captions appear and when? What's the audio doing (trending sound, original voiceover, music-only)? What's the payoff or CTA at the end?</p><h2>Worked Example: Deconstructing a Trending Cooking Reel</h2><p>Hook: an extreme close-up of a sizzling pan with bold text \"You're cooking jollof rice wrong.\" Cut speed: very fast, roughly one cut every 1-2 seconds, matching a trending upbeat sound. Captions: short, punchy phrases synced to key moments, not full sentences. <strong>Payoff: the final plated dish shown in a satisfying slow-motion close-up, with the CTA \"Save this before your next cook.\"</strong></p><ul><li>Fast cut speed is now standard on most short-form platforms — note the average shot length in successful videos</li><li>Studying trending audio use reveals current platform norms, which shift every few months</li><li>Look specifically at HOW the hook is delivered — visually, textually, or both</li></ul>",
            "key_concepts": ["video deconstruction", "shot length analysis", "trending audio", "case study analysis"],
            "practical_exercise": {
                "title": "Deconstruct a Real Short-Form Video",
                "instructions": "Find one real short-form video (Reels, TikTok, or YouTube Shorts) that you believe performed well. Write an analysis covering: the hook, the approximate cut speed/average shot length, the caption style, the audio choice, and the payoff/CTA. Submit the analysis along with a description or link reference to the video studied."
            },
            "quiz": [
                {"question": "What is a useful metric to note when analyzing a fast-paced short-form video?", "options": ["The video's file size", "The average shot length (how fast the cuts are)", "The number of comments only", "The video codec used"], "correct_index": 1, "explanation": "Average shot length reveals the pacing rhythm that's currently resonating with audiences on a given platform."},
                {"question": "Why is studying trending audio use valuable for editors?", "options": ["It has no practical value", "It reveals current platform norms, which shift frequently", "Audio trends never change", "It only matters for music videos"], "correct_index": 1, "explanation": "Platform audio trends shift often, and studying current usage helps editors stay relevant to what's currently resonating."},
                {"question": "What should you specifically look at when studying a video's hook?", "options": ["Only the video's total length", "How the hook is delivered — visually, textually, or both", "The video's upload date only", "The number of hashtags used"], "correct_index": 1, "explanation": "Understanding whether a hook relies on visuals, text, or a combination reveals techniques you can apply to your own scripts."}
            ],
            "resources": []
        },
        {
            "day_number": 15,
            "week_number": 3,
            "week_title": "Intermediate Editing and Motion Graphics",
            "title": "Working With Stock Footage and Music Legally",
            "learning_objective": "By the end of this class, you will be able to source stock footage and music from properly licensed sources and correctly attribute or license them.",
            "duration_minutes": 25,
            "content_html": "<p>Using copyrighted music or footage without a license can get a video muted, taken down, or land a freelancer in legal trouble with a client. Knowing where to legally source stock assets is a basic professional requirement, not an optional extra.</p><h2>Understanding Licensing Types</h2><p>Royalty-free: pay once (or free), use many times without ongoing fees — but still check the specific license terms. Creative Commons: free to use, but often requires attribution (crediting the creator) — terms vary by license type. Platform-licensed music (e.g. built into CapCut or TikTok): usually fine within that specific platform, but often NOT licensed for use elsewhere, like YouTube or a client's website.</p><h2>Worked Example: Sourcing Music for a Client Video</h2><p>A client video destined for YouTube and their website needs music. Using a trending TikTok sound would likely trigger a copyright claim outside TikTok. <strong>Instead, source music from a royalty-free library and confirm the specific license covers commercial client use, not just personal projects.</strong> Save the license confirmation/receipt for the client's records.</p><ul><li>Always check whether a license covers commercial use, not just personal or educational use</li><li>Platform-native sounds/music rarely transfer legally to other platforms</li><li>When in doubt, keep license proof/receipts for any client-facing project</li></ul>",
            "key_concepts": ["royalty-free licensing", "Creative Commons", "commercial use rights", "copyright claims"],
            "practical_exercise": {
                "title": "Source and Document a Licensed Asset",
                "instructions": "Find one piece of royalty-free or Creative Commons music or stock footage online that you could legally use in a client video. Write a short note documenting the source, the license type, whether it covers commercial use, and any attribution requirements. Submit your documentation note."
            },
            "quiz": [
                {"question": "Why is using a trending platform-native sound risky for a video posted elsewhere?", "options": ["It is always completely safe everywhere", "Platform-licensed sounds are often not licensed for use outside that specific platform", "Trending sounds are always royalty-free everywhere", "It has no legal implications"], "correct_index": 1, "explanation": "Music licensed within one platform's ecosystem frequently isn't cleared for use on other platforms or client websites."},
                {"question": "What should you always check about a royalty-free license before using it in client work?", "options": ["The file format only", "Whether the license actually covers commercial use", "The song's release date", "Nothing needs to be checked"], "correct_index": 1, "explanation": "Some 'free' licenses only permit personal or non-commercial use, so commercial coverage must be explicitly confirmed."},
                {"question": "What does a Creative Commons license often require in exchange for free use?", "options": ["A large payment", "Attribution (crediting the original creator)", "Nothing is ever required", "Exclusive rights transfer to the user"], "correct_index": 1, "explanation": "Many Creative Commons licenses require crediting the original creator as a condition of free use."}
            ],
            "resources": []
        },
        {
            "day_number": 16,
            "week_number": 4,
            "week_title": "Portfolio-Quality Production",
            "title": "Directing a Simple Talking-Head Interview Setup",
            "learning_objective": "By the end of this class, you will be able to plan and execute a basic interview shoot with proper framing, eyeline, and multi-angle coverage.",
            "duration_minutes": 30,
            "content_html": "<p>Talking-head interviews are among the most requested video formats for brands, testimonials, and personal branding content — and a poorly directed one is instantly noticeable, regardless of what's said. A few deliberate choices make the difference.</p><h2>Framing and Eyeline Basics</h2><p>Rule of thirds: position the subject's eyes roughly one-third down from the top of the frame, not dead center. Eyeline: have the subject look slightly off-camera at the interviewer, not directly into the lens (unless a direct-to-camera style is intentional). Coverage: capture at least two angles (a main medium shot, plus a closer reaction shot) to give the editor cutting options.</p><h2>Worked Example: A Two-Camera-Feel Setup With One Camera</h2><p>Since most beginners have only one camera, shoot the full interview once in a medium shot. Then, if time allows, re-ask 1-2 key questions and reshoot just those answers in a tighter close-up. <strong>In editing, cutting between the 'two angles' from these two passes creates the impression of a multi-camera shoot, hiding jump cuts and adding visual variety.</strong></p><ul><li>Off-center eye placement using the rule of thirds looks more intentional and professional</li><li>Avoid direct-lens eye contact unless deliberately going for a direct-address style</li><li>Simulating multi-angle coverage with a single camera is a real, widely used low-budget technique</li></ul>",
            "key_concepts": ["rule of thirds", "eyeline", "interview coverage", "single-camera multi-angle technique"],
            "practical_exercise": {
                "title": "Shoot a Two-Pass Interview Segment",
                "instructions": "Record a short interview or talking-head segment (yourself or a willing subject) answering one question, framed using the rule of thirds with correct eyeline. Then reshoot the same answer in a closer angle. Edit the two passes together to simulate multi-camera coverage. Submit the edited clip or a written description of your framing and edit choices."
            },
            "quiz": [
                {"question": "According to the rule of thirds for interview framing, where should the subject's eyes be positioned?", "options": ["Dead center of the frame", "Roughly one-third down from the top of the frame", "At the very bottom edge", "It doesn't matter"], "correct_index": 1, "explanation": "Positioning the eyes about one-third from the top is a standard framing guideline that looks more intentional than dead-center placement."},
                {"question": "In a typical interview, where should the subject usually look?", "options": ["Directly into the lens at all times", "Slightly off-camera toward the interviewer, unless direct address is intended", "Away from the camera entirely", "It never matters where they look"], "correct_index": 1, "explanation": "A slight off-camera eyeline toward an interviewer is the standard, natural-feeling interview convention."},
                {"question": "How can a single-camera shoot simulate multi-angle coverage?", "options": ["It cannot be simulated with one camera", "By reshooting key answers from a different angle and cutting between the two passes", "By using two different microphones", "By adding a filter effect only"], "correct_index": 1, "explanation": "Reshooting key moments from a second angle and cutting between the two takes creates the impression of multi-camera coverage."}
            ],
            "resources": []
        },
        {
            "day_number": 17,
            "week_number": 4,
            "week_title": "Portfolio-Quality Production",
            "title": "Editing an Ad — Persuasive Structure for Commercial Video",
            "learning_objective": "By the end of this class, you will be able to edit a 15-30 second commercial video following a proven persuasive structure.",
            "duration_minutes": 30,
            "content_html": "<p>A commercial ad has a job different from entertainment content: it must persuade within a very tight time window. Editors who understand ad structure are far more valuable to businesses than those who can only cut nice-looking montages.</p><h2>The Problem-Solution-Proof-CTA Ad Structure</h2><p>Problem (0-5s): show the pain point visually or through voiceover. Solution (5-15s): introduce the product/service as the fix. Proof (15-22s): a quick testimonial, result, or demonstration that builds trust. CTA (22-30s): a clear, single next action.</p><h2>Worked Example: 25-Second App Ad Edit</h2><p>Problem (0-5s): quick cuts of someone frustrated, manually tracking expenses in a notebook. Solution (5-14s): the app being opened, showing the automated feature solving that exact frustration. Proof (14-20s): <strong>a quick on-screen stat, \"Users save 3 hours a week,\" paired with a brief satisfied-customer clip.</strong> CTA (20-25s): app icon and download button animation with voiceover \"Download free today.\"</p><ul><li>Every second of a commercial should map to one of these four structural beats — don't pad with unrelated pretty shots</li><li>Proof (testimonials, stats, before/afters) builds trust faster than more product footage alone</li><li>End on the CTA, always — never let a commercial trail off without a clear final ask</li></ul>",
            "key_concepts": ["ad structure", "problem-solution-proof-CTA", "commercial editing", "persuasive pacing"],
            "practical_exercise": {
                "title": "Edit a 25-Second Structured Ad",
                "instructions": "Using footage of your choice (real or stock/phone clips), edit a 20-30 second commercial-style video following the problem-solution-proof-CTA structure. Label which seconds of your final edit correspond to each of the four beats. Submit the edited video or a shot-by-shot breakdown with timing."
            },
            "quiz": [
                {"question": "What are the four beats of the problem-solution-proof-CTA ad structure?", "options": ["Intro, middle, climax, credits", "Problem, solution, proof, call-to-action", "Hook, body, twist, ending", "Title, content, outro, thanks"], "correct_index": 1, "explanation": "This proven commercial structure moves from the pain point through the solution, supporting proof, and a clear final action."},
                {"question": "What does the 'proof' section of a commercial typically provide?", "options": ["More footage of the product logo", "Trust-building evidence like a testimonial or a result stat", "An extended problem restatement", "Nothing, it can be skipped"], "correct_index": 1, "explanation": "Proof — testimonials, statistics, or demonstrations — builds viewer trust more effectively than repeated product shots alone."},
                {"question": "Why should a commercial always end on a clear CTA?", "options": ["CTAs are optional in commercial video", "Trailing off without a clear next action reduces the ad's persuasive effectiveness", "The CTA should always come first, not last", "It has no impact on ad performance"], "correct_index": 1, "explanation": "A strong ad needs a definitive closing action to convert viewer interest into a concrete next step."}
            ],
            "resources": []
        },
        {
            "day_number": 18,
            "week_number": 4,
            "week_title": "Portfolio-Quality Production",
            "title": "Simple Motion Graphics — Animated Titles and Icon Reveals",
            "learning_objective": "By the end of this class, you will be able to create an animated title sequence and an icon reveal using layered keyframe animation.",
            "duration_minutes": 30,
            "content_html": "<p>Motion graphics — animated titles, icons, and shapes — elevate a video from 'edited footage' to a polished, branded piece. You don't need After Effects mastery to add real value here; layered keyframe animation (from Day 12) covers most client needs.</p><h2>Layering Multiple Animated Elements</h2><p>A title sequence typically layers: a background shape animating in first, then title text animating in second (slightly delayed), then a subtitle or tagline animating in last. This staggered timing ('offset') makes multi-element animations feel choreographed rather than everything appearing at once.</p><h2>Worked Example: Brand Intro Title Sequence</h2><p>0.0s: background color bar slides in from the left. 0.2s (offset): main title text \"LAGOS SKINCARE CO.\" fades and scales in. 0.4s (offset): <strong>tagline \"Glow that lasts\" fades in beneath it.</strong> All elements then hold for 2 seconds before animating out in reverse order. This staggered approach is standard in professional title sequences and intros.</p><ul><li>Stagger multiple elements' entrance timing — simultaneous entrances feel flat and less polished</li><li>Reversing the entrance order on exit (last-in, first-out) creates a satisfying symmetrical feel</li><li>Keep total animation time short (1-3 seconds) so it doesn't slow down the video's pacing</li></ul>",
            "key_concepts": ["motion graphics", "staggered animation", "title sequence", "layered keyframes"],
            "practical_exercise": {
                "title": "Build a Staggered Title Sequence",
                "instructions": "Using any editing or motion app, create a title sequence with at least three elements (a background shape, a main title, and a subtitle/tagline) that animate in with staggered timing, hold briefly, then animate out. Use your final project brand's name and tagline. Submit the exported clip or screen recording."
            },
            "quiz": [
                {"question": "What does staggering the entrance timing of multiple animated elements achieve?", "options": ["It makes the animation feel choreographed rather than flat", "It has no visible effect", "It is only relevant for feature films", "It slows down rendering time only"], "correct_index": 0, "explanation": "Offsetting when each element appears creates a more polished, intentional-feeling sequence than everything appearing at once."},
                {"question": "What is a common professional technique for animating elements OUT of frame?", "options": ["Always using the exact same order as the entrance", "Reversing the entrance order (last-in, first-out)", "Elements should never animate out, only in", "Randomizing the exit order each time"], "correct_index": 1, "explanation": "A last-in, first-out exit order creates a satisfying, symmetrical feel that mirrors the entrance sequence."},
                {"question": "Why should a title sequence's total animation time stay short (1-3 seconds)?", "options": ["Longer animations are always better", "A long animation can slow down the video's overall pacing", "There is a strict platform-enforced time limit", "Short animations are technically impossible to render"], "correct_index": 1, "explanation": "Keeping intro animations brief maintains good pacing and avoids losing viewer attention before the main content starts."}
            ],
            "resources": []
        },
        {
            "day_number": 19,
            "week_number": 4,
            "week_title": "Portfolio-Quality Production",
            "title": "Editing to Music — Syncing Cuts to a Beat",
            "learning_objective": "By the end of this class, you will be able to edit a sequence of clips so that cut points land on the beat of a chosen music track.",
            "duration_minutes": 25,
            "content_html": "<p>Beat-synced editing — cutting exactly on musical beats — is a technique that instantly makes montages, product videos, and hype reels feel more satisfying and professional. It's one of the most requested styles for brand and event recap videos.</p><h2>Finding and Marking the Beat</h2><p>Most editing apps let you add markers on the timeline. Play the music and tap a marker key on each beat (or every other beat for a slower-feeling cut rhythm). Then align your clip cuts to land exactly on those markers.</p><h2>Worked Example: A 15-Second Beat-Synced Montage</h2><p>Track chosen: an upbeat instrumental with a clear, consistent beat. Markers placed on every beat for the first 8 seconds (faster cuts, high energy opening), then every OTHER beat for the remaining 7 seconds (slightly slower rhythm as the montage settles). <strong>Each clip's cut point is trimmed to land exactly on its assigned marker, not just close to it.</strong></p><ul><li>Precision matters — even a cut that's a few frames off the beat feels noticeably wrong</li><li>Varying beat density (every beat vs every other beat) creates intentional pacing changes within one montage</li><li>Choose music with a clear, consistent beat for your first attempts — complex rhythms are harder to sync to</li></ul>",
            "key_concepts": ["beat-synced editing", "timeline markers", "montage pacing", "cut precision"],
            "practical_exercise": {
                "title": "Edit a Beat-Synced Montage",
                "instructions": "Choose a piece of music with a clear beat. Using at least 5 short clips, edit them together so the cuts land precisely on the beat for at least 10 seconds of montage. Submit the edited clip or a written breakdown of your marker placements and corresponding cut points."
            },
            "quiz": [
                {"question": "What is beat-synced editing?", "options": ["Editing without any music at all", "Aligning cut points precisely with the beats of a music track", "Randomly placing cuts throughout a video", "Only used for slow, emotional videos"], "correct_index": 1, "explanation": "Beat-synced editing deliberately times cuts to land exactly on musical beats, creating a satisfying rhythmic effect."},
                {"question": "Why does precision matter so much in beat-synced editing?", "options": ["Precision doesn't matter at all", "Even a cut a few frames off the beat feels noticeably wrong to viewers", "Only the first cut needs to be precise", "Precision only matters for professional film releases"], "correct_index": 1, "explanation": "Human perception is very sensitive to rhythm, so even small timing misalignments are noticeable and feel off."},
                {"question": "What can varying beat density (every beat vs. every other beat) achieve within one montage?", "options": ["It has no creative purpose", "Intentional pacing changes, like starting fast and settling into a slower rhythm", "It always signals a mistake in editing", "It only works with silent footage"], "correct_index": 1, "explanation": "Deliberately changing how often cuts land on beats lets an editor shape energy and pacing across a montage."}
            ],
            "resources": []
        },
        {
            "day_number": 20,
            "week_number": 4,
            "week_title": "Portfolio-Quality Production",
            "title": "Reading Basic Video Analytics to Improve Your Next Edit",
            "learning_objective": "By the end of this class, you will be able to interpret retention and watch-time data from a video and translate it into one specific editing change.",
            "duration_minutes": 25,
            "content_html": "<p>Editors who never look at how their videos actually performed keep repeating the same mistakes. You don't need to be a data analyst — but understanding basic retention data lets you diagnose exactly where a video loses viewers and fix that specific point.</p><h2>Reading a Retention Graph</h2><p>Most platforms show a retention graph — the percentage of viewers still watching at each point in the video. A steep early drop usually signals a weak hook. A drop at a specific mid-video point usually signals a slow or confusing section. A graph that holds steady suggests good pacing throughout.</p><h2>Worked Example: Diagnosing a Retention Graph</h2><p>A video's retention graph shows 100% at 0 seconds, dropping sharply to 40% by 3 seconds, then holding fairly steady after that. Diagnosis: <strong>the hook failed to hold attention, but the body content that DID get watched held viewers reasonably well.</strong> The fix is not to change the whole video — it's specifically to rewrite and re-test the first 3 seconds.</p><ul><li>Match each retention drop to the specific timestamp and section of the video it reflects</li><li>A steep early drop = hook problem. A mid-video drop = pacing or clarity problem in that specific section</li><li>Always form one specific hypothesis for what to change next, not a vague 'make it more engaging'</li></ul>",
            "key_concepts": ["retention graph", "watch time", "hook diagnosis", "data-driven editing"],
            "practical_exercise": {
                "title": "Diagnose a Retention Scenario",
                "instructions": "You are given this scenario: a video's retention graph holds at 90% for the first 10 seconds, then drops sharply to 35% between seconds 10-15, then stays flat afterward. Write a short diagnosis of what likely happened at seconds 10-15, and propose one specific editing change to fix it. Submit your written diagnosis and proposed fix."
            },
            "quiz": [
                {"question": "What does a steep drop in viewer retention within the first few seconds usually indicate?", "options": ["The video's title was too long", "A weak or ineffective hook", "The video was too high resolution", "Nothing meaningful can be concluded"], "correct_index": 1, "explanation": "An early sharp retention drop typically points to a hook that failed to capture or hold viewer attention."},
                {"question": "What does a retention drop at a specific mid-video timestamp usually suggest?", "options": ["A pacing or clarity problem in that specific section", "The video is too short overall", "The music was too loud throughout", "It always means the video should be deleted"], "correct_index": 0, "explanation": "A localized drop points to a specific section that lost viewers, often due to slow pacing or confusing content at that point."},
                {"question": "What is the recommended response after diagnosing a retention issue?", "options": ["Vaguely deciding to 'make the next video more engaging'", "Forming one specific hypothesis for what to change based on the data", "Ignoring retention data entirely going forward", "Re-uploading the exact same video"], "correct_index": 1, "explanation": "A specific, testable hypothesis derived directly from the data leads to real improvement, unlike vague resolutions."}
            ],
            "resources": []
        },
        {
            "day_number": 21,
            "week_number": 5,
            "week_title": "Advanced Craft and Client-Ready Skills",
            "title": "Advanced Pacing — Building Tension and Rhythm Across a Full Edit",
            "learning_objective": "By the end of this class, you will be able to plan pacing changes across a full video timeline to build and release tension deliberately.",
            "duration_minutes": 30,
            "content_html": "<p>Beginner edits often use one pacing speed throughout — either all fast cuts or all slow holds. Advanced editors deliberately vary pacing across the full video to build tension, then release it, mirroring how music or storytelling builds toward a climax.</p><h2>Mapping Pacing Across a Timeline</h2><p>Slow opening: longer holds, establishing calm or normalcy. Building middle: gradually shortening cut lengths, increasing tension or energy. Climax: the fastest cuts or the single longest, most impactful hold — whichever suits the story goal. Release: a slower, resolving final beat.</p><h2>Worked Example: A Brand Story Video Pacing Map</h2><p>0-10s: slow, single long shots showing the founder's daily struggle (calm, contemplative pacing). 10-25s: cuts gradually shorten as the story builds toward the moment of change (rising energy). 25-30s: <strong>a single sustained shot of the product/result, held deliberately long, releasing the built-up tension with a moment of payoff stillness.</strong></p><ul><li>Pacing itself tells a story — audiences feel rising tension from shortening cuts, even without realizing why</li><li>A held shot after a fast sequence reads as a deliberate emotional beat, not a mistake</li><li>Map pacing changes on paper before editing — it's easier to plan than to discover by trial and error</li></ul>",
            "key_concepts": ["pacing map", "tension and release", "rhythm across an edit", "climax pacing"],
            "practical_exercise": {
                "title": "Map and Apply a Pacing Arc",
                "instructions": "Choose or shoot footage for a 30-45 second sequence. Write a pacing map dividing the timeline into slow opening, building middle, climax, and release sections, noting the approximate cut length for each. Edit the footage to follow this pacing map. Submit the edited clip alongside your written pacing map."
            },
            "quiz": [
                {"question": "What is a common beginner pacing mistake?", "options": ["Varying pacing too much throughout a video", "Using one single pacing speed throughout the entire edit", "Using too many different shot types", "Adding too much music"], "correct_index": 1, "explanation": "Beginners often use uniform pacing (all fast or all slow) rather than deliberately building and releasing tension."},
                {"question": "What does a gradually shortening cut length across a sequence typically signal to viewers?", "options": ["A technical editing error", "Rising tension or building energy", "The video is ending soon regardless of content", "Nothing, viewers don't perceive pacing"], "correct_index": 1, "explanation": "Progressively faster cuts are widely felt as building energy or tension, even without the viewer consciously noticing why."},
                {"question": "Why is it useful to map pacing on paper before editing?", "options": ["It has no practical benefit", "It's easier to plan deliberate pacing changes than to discover them through trial and error", "Paper planning is required by industry standard", "It replaces the need for a script entirely"], "correct_index": 1, "explanation": "Planning the pacing arc in advance helps an editor make deliberate, story-serving choices rather than arbitrary ones during editing."}
            ],
            "resources": []
        },
        {
            "day_number": 22,
            "week_number": 5,
            "week_title": "Advanced Craft and Client-Ready Skills",
            "title": "Working With Talent and Getting Natural Performances on Camera",
            "learning_objective": "By the end of this class, you will be able to direct a non-professional on-camera subject to deliver a natural, relaxed performance.",
            "duration_minutes": 25,
            "content_html": "<p>Most people freeze up or become stiff and unnatural in front of a camera — including small business owners, employees, and everyday people you'll often be filming as a freelance or in-house video creator. Directing natural performances from non-actors is a real, learnable skill.</p><h2>Techniques for Natural On-Camera Performances</h2><p>Have a real conversation before rolling — nerves drop once someone feels like they're just talking to a person, not performing. Ask questions rather than handing over a script to read word-for-word — natural speech patterns beat stiff recitation. Do multiple takes; the 2nd or 3rd take is often more relaxed than the 1st.</p><h2>Worked Example: Filming a Nervous Business Owner Testimonial</h2><p>Instead of asking them to read a prepared statement, ask a conversational question: \"What was the moment you knew this business idea would work?\" and film their natural, unscripted answer. <strong>If the first answer feels stiff, say \"That was great, let's just try it once more, more casually\" — reframing it as low-stakes, not a retake due to failure.</strong></p><ul><li>Scripted word-for-word delivery from non-actors almost always sounds unnatural on camera</li><li>Conversational questions produce more authentic, usable soundbites than reading prompts</li><li>Frame additional takes positively — subjects relax more when they don't feel they're being corrected</li></ul>",
            "key_concepts": ["directing talent", "natural performance", "conversational interviewing", "on-camera nerves"],
            "practical_exercise": {
                "title": "Direct and Film a Natural Testimonial",
                "instructions": "Find a willing subject (friend, family member, classmate). Instead of giving them a script, ask them 2-3 conversational questions about a topic they know well and film their natural answers. Do at least two takes of one question, reframing the second take positively. Submit the footage or a written reflection on what changed between takes."
            },
            "quiz": [
                {"question": "Why does handing a non-actor a script to read word-for-word often produce weak footage?", "options": ["Scripts always improve on-camera delivery", "Scripted, word-for-word delivery from non-actors usually sounds stiff and unnatural", "It is illegal to use scripts with non-actors", "Scripts have no effect on performance quality"], "correct_index": 1, "explanation": "Non-actors reading prepared lines typically sound stiff, whereas natural conversational answers feel more authentic."},
                {"question": "What is an effective way to get more natural answers from a nervous subject?", "options": ["Demanding a perfect take on the first try", "Asking conversational questions instead of a scripted read", "Filming only one take regardless of quality", "Telling them exactly what words to say"], "correct_index": 1, "explanation": "Conversational questions invite natural speech patterns rather than the stiffness of memorized or read lines."},
                {"question": "Why should additional takes be framed positively rather than as corrections?", "options": ["It has no effect on the subject's comfort", "Subjects tend to relax more and perform better when they don't feel they're being criticized", "Framing takes positively is dishonest and should be avoided", "Only professional actors need positive framing"], "correct_index": 1, "explanation": "Positive framing reduces performance anxiety, helping non-professional subjects give more relaxed, natural takes."}
            ],
            "resources": []
        },
        {
            "day_number": 23,
            "week_number": 5,
            "week_title": "Advanced Craft and Client-Ready Skills",
            "title": "Ethical Editing — Manipulation, Misleading Cuts, and Disclosure",
            "learning_objective": "By the end of this class, you will be able to identify editing choices that mislead viewers and apply an ethical alternative that preserves persuasive impact.",
            "duration_minutes": 25,
            "content_html": "<p>Editing has real power to shape what viewers believe happened — cutting out context, exaggerating results, or implying an outcome that wasn't real. Clients sometimes push for misleading edits; knowing the line, and pushing back professionally, protects both viewers and your professional reputation.</p><h2>Where Persuasive Editing Crosses Into Misleading</h2><p>Ethical: highlighting genuine strong moments, honest before/after framing, clear disclosure of sponsored content. Misleading: fabricated before/after results, cutting testimonials out of context to imply something untrue, undisclosed paid promotion presented as an organic opinion.</p><h2>Worked Example: A Before/After Product Video</h2><p>Misleading version: using different lighting/angles between the 'before' and 'after' shots to exaggerate a difference that isn't real. Ethical version: <strong>identical lighting, angle, and conditions for both shots, letting a genuine difference speak for itself — still persuasive, but honest.</strong> If the results aren't dramatic, that's a signal to change the marketing angle, not to fake the footage.</p><ul><li>Match shooting conditions exactly for any before/after comparison to keep it honest</li><li>Sponsored or paid content must be clearly disclosed to viewers, not hidden</li><li>You can, and should, push back professionally if a client requests a misleading edit</li></ul>",
            "key_concepts": ["ethical editing", "misleading before/after", "sponsored disclosure", "editing integrity"],
            "practical_exercise": {
                "title": "Identify and Fix a Misleading Edit",
                "instructions": "Describe one realistic example of a misleading editing technique (a fabricated before/after, an out-of-context cut, or undisclosed sponsorship) as a bad example. Then describe the ethical alternative that achieves a similar persuasive goal honestly. Submit both descriptions with a one-sentence explanation of what made the first one misleading."
            },
            "quiz": [
                {"question": "What makes a before/after comparison video misleading?", "options": ["Using the exact same lighting and angle for both shots", "Using different lighting/angles to exaggerate a difference that isn't genuinely real", "Showing a genuine, unedited difference", "Including a timestamp on each shot"], "correct_index": 1, "explanation": "Deliberately changing shooting conditions between before/after shots to exaggerate results is a classic misleading editing technique."},
                {"question": "What is required when creating sponsored or paid promotional content?", "options": ["Nothing, disclosure is optional", "Clear disclosure to viewers that the content is sponsored", "Sponsored content must always be hidden", "Disclosure is only needed for videos over 5 minutes"], "correct_index": 1, "explanation": "Ethical practice and platform/legal requirements call for clear, visible disclosure of paid or sponsored content."},
                {"question": "What should an editor do if a client requests a misleading edit?", "options": ["Comply without question to keep the client happy", "Push back professionally, since misleading edits harm viewers and reputation", "Immediately quit the industry", "Misleading edits are never actually a problem"], "correct_index": 1, "explanation": "Ethical editors are expected to push back professionally against requests that would mislead or deceive viewers."}
            ],
            "resources": []
        },
        {
            "day_number": 24,
            "week_number": 5,
            "week_title": "Advanced Craft and Client-Ready Skills",
            "title": "Pitching Your Video Services — A Reel That Gets You Hired",
            "learning_objective": "By the end of this class, you will be able to plan a 60-90 second demo reel structure that showcases range and leads with your strongest work.",
            "duration_minutes": 25,
            "content_html": "<p>Nobody hires a video editor based on a resume alone — a demo reel is the primary way editors and videographers get hired, whether for freelance gigs or in-house roles. A poorly structured reel, even with good individual clips, fails to land the job.</p><h2>Structuring a Demo Reel</h2><p>Open with your single strongest, most impressive 3-5 seconds — reel viewers, like social viewers, decide fast whether to keep watching. Follow with a range of work types (a commercial cut, a motion graphics moment, an interview edit) to show versatility. Keep the whole reel under 90 seconds — reviewers rarely watch longer reels in full.</p><h2>Worked Example: A 75-Second Reel Structure</h2><p>0-5s: your single best, most eye-catching cut or motion graphic moment, no explanation needed. 5-35s: a full mini-sequence from a commercial-style edit, showing pacing and sound design skill. 35-55s: <strong>a motion graphics moment (title sequence or lower third) to show that specific skill distinctly.</strong> 55-75s: a closing sequence, often set to a strong music beat-drop, ending on your name/logo card.</p><ul><li>Lead with your best work — never save your strongest clip for the end of a reel</li><li>Show range deliberately — different clip types signal versatility to a potential employer or client</li><li>Keep total reel length under 90 seconds; longer reels lose reviewer attention</li></ul>",
            "key_concepts": ["demo reel structure", "showcasing range", "leading with strength", "reel length"],
            "practical_exercise": {
                "title": "Outline Your Demo Reel Structure",
                "instructions": "Using the clips and pieces you've created so far in this course, plan a 60-90 second demo reel outline. List the order of clips, the approximate timestamp for each, and a one-sentence note on what skill each clip demonstrates. Submit the full reel outline."
            },
            "quiz": [
                {"question": "What should typically open a demo reel?", "options": ["Your weakest clip, to build up gradually", "Your single strongest, most impressive moment", "A long introduction explaining your background", "A blank title card only"], "correct_index": 1, "explanation": "Since reviewers decide quickly whether to keep watching, leading with your strongest work maximizes impact immediately."},
                {"question": "Why should a demo reel include a range of different clip types?", "options": ["Range has no real value to reviewers", "It signals versatility across different skills to a potential employer or client", "Reels should only ever show one skill", "Variety makes reels harder to watch"], "correct_index": 1, "explanation": "Showing different types of work (commercial, motion graphics, interview editing) demonstrates broader capability to hiring reviewers."},
                {"question": "What is a recommended maximum length for a demo reel?", "options": ["10 minutes", "Under 90 seconds", "There is no length that matters", "At least 5 minutes"], "correct_index": 1, "explanation": "Reviewers often don't watch long reels in full, so keeping it under 90 seconds respects their limited attention."}
            ],
            "resources": []
        },
        {
            "day_number": 25,
            "week_number": 5,
            "week_title": "Advanced Craft and Client-Ready Skills",
            "title": "Pricing and Scoping Your First Video Editing Gigs",
            "learning_objective": "By the end of this class, you will be able to scope a small video editing project into specific deliverables and set a defensible price for it.",
            "duration_minutes": 25,
            "content_html": "<p>New video freelancers often underprice their time dramatically, not accounting for how long editing, revisions, and rendering actually take. Learning to scope and price projects protects your time and turns video skills into sustainable income.</p><h2>Scoping Before Pricing</h2><p>A price should always attach to specific deliverables: number of finished videos, approximate length, number of revision rounds, and turnaround time. \"I'll edit your videos\" is not a scope. \"2 videos, up to 60 seconds each, 1 round of revisions, delivered in 5 business days\" is a scope you can price and defend.</p><h2>Worked Example: Scoping a Small Package</h2><p>Vague (bad): \"I'll edit your content for ₦20,000.\" Scoped (good): <strong>\"Package: 3 short-form videos (up to 60 seconds each), including captions and basic motion graphics (lower third + title card). Includes 1 round of revisions per video. Delivery: 6 business days. Price: ₦45,000.\"</strong> The scoped version protects the editor from scope creep and endless unpaid re-edits.</p><ul><li>Always state a specific number of revision rounds included per video</li><li>Factor in real time costs: shooting/sourcing, editing, motion graphics, rendering, and export all take time</li><li>Research a few similar freelance editors' public rates before setting your own</li></ul>",
            "key_concepts": ["project scoping", "pricing packages", "revision limits", "turnaround time"],
            "practical_exercise": {
                "title": "Scope and Price a Sample Video Package",
                "instructions": "Design one small video editing service package you could realistically offer today (e.g. short-form social videos, a talking-head interview edit, a product ad edit). Define exactly what's included, how many revision rounds, the turnaround time, and a specific price in naira. Submit the full package description as you would send it to a potential client."
            },
            "quiz": [
                {"question": "Why is 'I'll edit your videos' considered a poor project scope?", "options": ["It is too specific", "It doesn't define concrete deliverables, length, revisions, or timeline", "It always guarantees client satisfaction", "It includes too much detail"], "correct_index": 1, "explanation": "A usable scope must specify exact deliverables and limits; vague language invites scope creep and disputes."},
                {"question": "What real time costs should a video editor factor into their pricing?", "options": ["Only the time spent filming", "Shooting/sourcing, editing, motion graphics, and rendering/export time", "Nothing beyond the final export", "Only the client meeting time"], "correct_index": 1, "explanation": "The full production pipeline — from sourcing footage through final export — takes real time that should be reflected in pricing."},
                {"question": "Why should a video package specify a limited number of revision rounds per video?", "options": ["Revisions should always be unlimited", "Unlimited revisions erode a freelancer's effective earnings on a project", "Revisions are illegal to offer", "It has no effect on project profitability"], "correct_index": 1, "explanation": "Without stated limits, clients can request endless re-edits, significantly reducing the freelancer's effective hourly rate."}
            ],
            "resources": []
        },
        {
            "day_number": 26,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "What Hiring Managers and Clients Actually Look for in a Video Reel",
            "learning_objective": "By the end of this class, you will be able to evaluate your own demo reel against the criteria a hiring manager or client typically uses before submitting it.",
            "duration_minutes": 25,
            "content_html": "<p>A technically impressive reel can still fail to get you hired if it doesn't match what the reviewer actually needs to see. Understanding what a hiring manager or client scans for changes how you select and present your work.</p><h2>What Reviewers Actually Scan For</h2><p>1. Does the reel match the type of work they need (don't lead with music videos for a corporate brand role)? 2. Is there evidence of storytelling/pacing judgment, not just flashy effects? 3. Is the audio mix clean throughout — bad audio in a reel is an instant red flag? 4. Is there a mix of skills shown (editing, sound, motion graphics), not just one repeated trick?</p><h2>Worked Example: Framing a Reel for a Specific Role</h2><p>Applying for a social media content role at a Nigerian fintech startup: lead the reel with short-form, fast-paced, caption-heavy content rather than long-form documentary-style edits, even if the documentary work is technically stronger. <strong>Add a one-line note before the reel: \"Reel curated for short-form social content — additional long-form work available on request.\"</strong> This shows self-awareness of what's relevant to the specific role.</p><ul><li>Curate your reel's content order and selection specifically for each application or pitch, not one-size-fits-all</li><li>Clean audio throughout a reel is non-negotiable — a single bad-audio clip can undercut the whole reel</li><li>Show range across editing, sound, and motion graphics rather than only your favorite single skill</li></ul>",
            "key_concepts": ["reel curation for role", "audio quality standard", "showing skill range", "reviewer expectations"],
            "practical_exercise": {
                "title": "Curate Your Reel for a Specific Role",
                "instructions": "Imagine a specific job or client type you'd want to work with (e.g. a fintech startup's social content, a wedding videography client, an ad agency). Using your reel outline from Day 24, revise the order and selection of clips to specifically match what that role/client would want to see first. Submit the revised outline plus a one-sentence note on why you reordered it."
            },
            "quiz": [
                {"question": "Why should a reel's clip order be curated differently for different applications?", "options": ["Reel order never matters to reviewers", "Different roles/clients want to see different types of work led with first", "Reels should always be identical regardless of audience", "Curation only matters for long-form reels"], "correct_index": 1, "explanation": "Matching the lead content to what a specific reviewer cares about increases the reel's relevance and impact."},
                {"question": "Why is clean audio throughout a reel considered non-negotiable?", "options": ["Audio quality doesn't affect reel perception", "A single bad-audio clip can undercut trust in the whole reel", "Reels are typically watched with sound off", "Only video quality matters to reviewers"], "correct_index": 1, "explanation": "Since audio quality reflects overall production competence, even one bad-audio moment can damage the reel's credibility."},
                {"question": "What does showing a mix of skills (editing, sound, motion graphics) in a reel demonstrate?", "options": ["Nothing useful to a reviewer", "Range and versatility beyond a single repeated trick", "That the editor is unfocused", "It is discouraged in professional reels"], "correct_index": 1, "explanation": "Demonstrating multiple distinct skills shows broader capability, which is valuable to most hiring managers and clients."}
            ],
            "resources": []
        },
        {
            "day_number": 27,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "Answering 'Walk Me Through Your Edit' in a Video Interview",
            "learning_objective": "By the end of this class, you will be able to articulate your personal editing process clearly enough to answer a common interview question.",
            "duration_minutes": 25,
            "content_html": "<p>\"Walk me through your process for editing a project\" is one of the most common questions in video editing interviews and client discovery calls. Interviewers want to know you have a repeatable, professional workflow — not just that you can produce a good final result occasionally.</p><h2>A Process You Can Actually Describe</h2><p>A strong answer moves through clear stages: 1) understand the story goal and audience (Day 1), 2) organize and review all footage before editing, 3) build a rough assembly cut, 4) refine pacing and add sound design, 5) add motion graphics/text, 6) color correct and export for the target platform.</p><h2>Worked Example: A Sample Interview Answer</h2><p>\"I start by making sure I understand exactly what the video needs to accomplish and for who. Then I review all the footage before touching the timeline, so I know what I'm working with. I build a rough cut first, focused purely on story order, before worrying about polish. After that, I refine pacing, layer in sound design, then add any motion graphics. <strong>For example, on a recent product ad, that review-first step caught a much stronger clip buried in the raw footage that I would have missed if I'd started editing immediately.</strong>\"</p><ul><li>Always end your answer with one specific example — abstract process descriptions alone sound rehearsed</li><li>Mentioning that you review all footage before editing signals discipline, a trait interviewers specifically value</li><li>Practice saying your process answer out loud — interviews are spoken, not written</li></ul>",
            "key_concepts": ["interview process answer", "editing workflow", "job interview prep", "specific example"],
            "practical_exercise": {
                "title": "Write and Practice Your Process Answer",
                "instructions": "Write a 100-150 word answer to the interview question 'Walk me through how you'd approach editing a new client's video project.' Structure it in clear stages and end with one specific example from your work in this course. Then read it aloud at least once and note any part that felt awkward to say. Submit the written answer plus your note on what you'd adjust."
            },
            "quiz": [
                {"question": "What are interviewers really testing with the 'walk me through your edit' question?", "options": ["Whether you memorized software shortcuts", "Whether you have a repeatable, professional workflow", "Your typing speed", "Whether you own expensive equipment"], "correct_index": 1, "explanation": "This question probes for a structured, repeatable editing process, which signals reliability on real client projects."},
                {"question": "Why should reviewing all footage happen before starting the rough assembly cut?", "options": ["It wastes time and should be skipped", "It ensures the editor knows what material is available and can find hidden strong moments", "Footage review is only necessary for long documentaries", "It has no impact on the final edit quality"], "correct_index": 1, "explanation": "Reviewing footage first prevents missing strong clips and helps make more informed editing decisions from the start."},
                {"question": "Why should a process answer end with a specific example?", "options": ["Abstract answers alone can sound rehearsed and unconvincing", "Examples are never necessary in interviews", "It is required to mention specific software brands", "It shortens the overall answer significantly"], "correct_index": 0, "explanation": "A concrete example grounds the abstract process description and makes the answer more credible and memorable to an interviewer."}
            ],
            "resources": []
        },
        {
            "day_number": 28,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "Selecting and Sequencing Your Best Work for a Portfolio",
            "learning_objective": "By the end of this class, you will be able to select and order 3-5 pieces of your own video work into a coherent portfolio sequence.",
            "duration_minutes": 25,
            "content_html": "<p>The order and selection of pieces in a video portfolio tells its own story before a reviewer watches a single clip in full. A scattered, unordered portfolio makes reviewers work harder to see your range and skill — and busy hiring managers or clients often won't do that work.</p><h2>A Simple Portfolio Sequencing Logic</h2><p>Lead with your strongest, most relevant full piece — first impressions dominate attention. Follow with pieces that show range (a different format each time: commercial ad, interview edit, motion graphics piece). Close with a piece that shows technical range or a specific niche skill, if you have one.</p><h2>Worked Example: A 4-Piece Sequence</h2><p>1. Commercial-style ad edit (strongest, most relevant to target roles). 2. Interview/talking-head edit (shows range into a different format). 3. Motion graphics piece or title sequence (shows a distinct technical skill). 4. <strong>A beat-synced montage (shows rhythm and music-editing sensibility, a specific and valued niche skill).</strong> This sequence tells a story: strong editor, format-flexible, technically skilled — three things reviewers specifically look for.</p><ul><li>Never bury your best piece in the middle or end — lead with it</li><li>3-5 well-chosen pieces beat 10 mediocre or repetitive ones</li><li>Include at least one piece that shows a specific, distinct technical skill (motion graphics, beat-sync, color grading)</li></ul>",
            "key_concepts": ["portfolio sequencing", "leading with strength", "showing range", "niche technical skill"],
            "practical_exercise": {
                "title": "Sequence Your Portfolio Pieces",
                "instructions": "Review all the pieces you've created so far in this course. Select 3-5 of your strongest and most varied pieces, and write out the order you would present them in a portfolio, with a one-sentence justification for the order (why that piece leads, what range or specific skill each subsequent piece shows). Submit your sequence and justifications."
            },
            "quiz": [
                {"question": "Which piece should typically lead a video portfolio?", "options": ["The oldest piece you've made", "Your strongest, most relevant full piece", "A random selection", "Your shortest clip"], "correct_index": 1, "explanation": "Leading with your strongest, most relevant work makes the best first impression, which matters most to busy reviewers."},
                {"question": "Why should a portfolio include at least one piece showing a specific niche technical skill?", "options": ["Niche skills have no value in a portfolio", "It differentiates you and shows depth beyond general editing ability", "It is required by every job application", "It replaces the need for other pieces"], "correct_index": 1, "explanation": "Showcasing a distinct technical skill (like beat-syncing or motion graphics) demonstrates specialized value beyond general competence."},
                {"question": "Is a portfolio of 10 similar pieces generally stronger than 3-5 varied, strong ones?", "options": ["Yes, more pieces is always better", "No, 3-5 well-chosen varied pieces typically beat many repetitive ones", "Quantity and variety don't matter", "Only the total runtime matters"], "correct_index": 1, "explanation": "A curated, varied selection demonstrates range and quality more effectively than a large number of similar pieces."}
            ],
            "resources": []
        },
        {
            "day_number": 29,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "Handling Client Feedback and Revision Requests Like a Professional",
            "learning_objective": "By the end of this class, you will be able to respond to critical client feedback on an edit with a specific, non-defensive revision plan.",
            "duration_minutes": 25,
            "content_html": "<p>Every video editor gets tough feedback — \"this doesn't feel right\" or \"can you make it more exciting?\" How you respond to that moment matters as much to a client's decision to keep working with you as the quality of your original edit. This is a skill hiring managers explicitly probe for in interviews.</p><h2>The Non-Defensive Revision Response</h2><p>Step 1: acknowledge the feedback specifically, without arguing or over-explaining your original choices. Step 2: ask one clarifying question if the feedback is vague (\"more exciting\" could mean pacing, music, or visuals). Step 3: propose a specific, concrete change, not just \"I'll fix it.\"</p><h2>Worked Example: Responding to Vague Feedback</h2><p>Client feedback: \"Can you make it feel more exciting?\" Weak response: \"Sure, I'll make it better\" (no clarity gained). Strong response: <strong>\"Got it — is that more about the pacing feeling too slow, the music not hitting hard enough, or something visual? In the meantime, I'll try tightening the cuts in the middle section and testing a higher-energy track, since that's my read on what might be flat right now.\"</strong> This response gets clarity AND shows immediate proactive action.</p><ul><li>Never respond defensively, even when you believe your original edit was the right call</li><li>Vague feedback ('more exciting', 'doesn't feel right') needs one clarifying question before a blind re-edit</li><li>Always pair a clarifying question with a proposed concrete next step, showing initiative</li></ul>",
            "key_concepts": ["feedback handling", "non-defensive response", "clarifying questions", "client relationships"],
            "practical_exercise": {
                "title": "Respond to a Difficult Feedback Scenario",
                "instructions": "You receive this feedback from a client on a video you edited: 'It's good but something feels off about the pacing, I can't explain it.' Write your full response, including one clarifying question and one specific proposed revision direction. Submit your written response."
            },
            "quiz": [
                {"question": "What is the first step in responding to critical client feedback professionally?", "options": ["Arguing why your original edit was correct", "Acknowledging the feedback specifically without being defensive", "Ignoring the feedback and resubmitting the same edit", "Ending the working relationship immediately"], "correct_index": 1, "explanation": "Specific, non-defensive acknowledgment shows professionalism and keeps the working relationship constructive."},
                {"question": "What should an editor do when feedback is vague, like 'make it more exciting'?", "options": ["Guess randomly and hope for the best", "Ask one clarifying question to get more specific direction", "Refuse to revise until the client edits it themselves", "Immediately end the project"], "correct_index": 1, "explanation": "A clarifying question turns vague feedback into something actionable, avoiding wasted revision effort."},
                {"question": "Why is pairing a clarifying question with a proposed next step effective?", "options": ["It shows initiative while still seeking necessary clarity", "It is unnecessary since questions alone are enough", "Clients dislike proposed next steps", "It slows down the revision process unnecessarily"], "correct_index": 0, "explanation": "Combining a question with a concrete proposed action demonstrates proactive professionalism, not just passive waiting."}
            ],
            "resources": []
        },
        {
            "day_number": 30,
            "week_number": 6,
            "week_title": "Career-Ready Portfolio and Interview Prep",
            "title": "Launching Your Final Video Project — From Script to Export",
            "learning_objective": "By the end of this class, you will be able to plan and begin execution of your full final video project, from concept and script through the first edited pass.",
            "duration_minutes": 35,
            "content_html": "<p>Today you begin the final project: scripting, shooting/storyboarding, editing, and exporting a finished short video or motion piece — between 30 seconds and 3 minutes — suitable for a portfolio reel or an actual client. This is the single asset that proves everything you've learned over the last 29 days, and the piece you'll actually show to clients or employers.</p><h2>How to Approach the Final Project</h2><p>Start by choosing your brief (product ad, brand story, explainer, or short narrative) and writing your story goal (Day 1) and full script (Day 11). Plan your shot list (Day 2) and shoot or source your footage applying the light/stability/sound fundamentals (Day 3). Build a rough assembly cut first (Day 4), then refine pacing (Day 5, Day 21), sound design (Day 6), color (Day 7), captions/text (Day 8), and at least one motion graphic element (Day 12, 13, or 18).</p><h2>A Realistic Execution Plan</h2><p>Session 1: finalize brief, write story goal and script, plan shot list. Session 2: shoot or source all footage. Session 3: build the rough assembly cut and refine pacing. <strong>Session 4: add sound design, color correction, captions, and your motion graphic element, then export in the correct format for your intended platform, and write your one-paragraph creative brief explaining your goal, audience, and key creative choices.</strong></p><ul><li>Every choice should trace back to your Day 1 story goal — keep it visible while editing</li><li>Quality over length: a tight, well-paced 45-second piece beats a rushed 3-minute one</li><li>Treat this exactly like a real client delivery — review your export on the actual target platform format before calling it done</li></ul>",
            "key_concepts": ["final project planning", "script-to-export pipeline", "creative brief", "portfolio delivery"],
            "practical_exercise": {
                "title": "Start Your Final Project",
                "instructions": "This IS the start of your final project. Choose your brief (product ad, brand story, explainer, or narrative) and write your story goal and full script. Plan your shot list. Begin shooting or sourcing footage, or building your storyboard if animating. Submit your chosen brief, story goal, script, and shot list/storyboard as the beginning of your final project submission."
            },
            "quiz": [
                {"question": "What is the final project for this course?", "options": ["A single still photograph", "A scripted, shot/edited, and exported short video or motion piece with sound and motion graphics", "A written essay only", "A resume only"], "correct_index": 1, "explanation": "The final project is a complete short video or motion piece taken from script through final export, ready for a portfolio or client."},
                {"question": "Why should every editing choice in the final project trace back to the Day 1 story goal?", "options": ["The story goal is not relevant to final production", "It ensures every shot, cut, and effect serves a clear, unified purpose", "Story goals are only used in scripting, not editing", "It has no impact on final quality"], "correct_index": 1, "explanation": "Keeping the story goal central throughout production ensures cohesive, purposeful creative decisions rather than random or unrelated choices."},
                {"question": "According to the suggested execution plan, what should happen in the final session of work?", "options": ["Only writing the script", "Adding sound design, color correction, captions, motion graphics, exporting, and writing the creative brief", "Only shooting footage", "Choosing which quiz questions to answer"], "correct_index": 1, "explanation": "The plan reserves the final stage for finishing touches, correct export, and the client-facing creative brief that presents the work professionally."}
            ],
            "resources": []
        }
    ]
}
