"""Seed all 12 steps and their original guided questions.

All questions are ORIGINAL content written for PS01 (Powerful Silence).
They are inspired by common 12-step themes but are not copied from any source.
"""

from django.core.management.base import BaseCommand

from steps.models import Question, Step

# Each step is a dict with metadata + a list of questions.
# Questions are tuples of (number, text, help_text, question_type).
STEPS_DATA = [
    # ─────────────────────────────────────────────────────
    # STEP 1 — Admitting Powerlessness
    # ─────────────────────────────────────────────────────
    {
        "number": 1,
        "title": "Admitting Powerlessness",
        "description": (
            "We admitted we were powerless over alcohol — "
            "that our lives had become unmanageable."
        ),
        "focus": (
            "This step asks you to honestly examine how addiction took hold "
            "of your life and the ways it made daily living unmanageable. "
            "The goal is not self-punishment but clear-eyed honesty about "
            "what happened and why you are here."
        ),
        "recovery_outcome": (
            "By honestly examining how addiction overpowered your best "
            "intentions, you lay the foundation for change. Admitting the "
            "problem is the first act of courage on the path to recovery."
        ),
        "spiritual_principle": "Honesty",
        "is_recurring": False,
        "questions": [
            (1, "Looking back, what were the earliest signs that your relationship with alcohol was different from other people's?",
             "Think about when drinking shifted from social to something you needed.", "text"),
            (2, "What did alcohol initially give you that you felt you couldn't get any other way?",
             "Consider emotional relief, confidence, escape, belonging.", "text"),
            (3, "Describe a time when you told yourself you would stop or cut back, but couldn't follow through. What happened?",
             "", "text"),
            (4, "How has your drinking affected the people closest to you? Be specific about relationships that were damaged.",
             "", "text"),
            (5, "In what ways has alcohol created a sense of isolation in your life?",
             "This could be physical withdrawal from others or an internal feeling of being apart.", "text"),
            (6, "What emotions or situations most reliably triggered you to drink? Were you aware of these patterns at the time?",
             "", "text"),
            (7, "What is one consequence of your drinking that still causes you pain when you think about it?",
             "", "text"),
            (8, "How did alcohol affect your financial situation? Did you hide the cost from anyone?",
             "", "text"),
            (9, "Describe the lengths you went to in order to conceal your drinking. How much energy did that secrecy consume?",
             "", "text"),
            (10, "Has your drinking caused you any physical or mental health problems? What were they?",
              "", "yesno"),
            (11, "Can you recall a time when you did something while drinking that deeply contradicted your own values?",
              "", "text"),
            (12, "Did you ever put yourself or someone else in danger because of alcohol? What happened?",
              "", "yesno"),
            (13, "What situation related to your drinking causes you the most embarrassment or shame?",
              "Remember: shame thrives in secrecy. Writing it down begins to loosen its grip.", "text"),
            (14, "Did you ever manipulate or use other people in order to keep drinking? How did you justify it to yourself?",
              "", "text"),
            (15, "During what period of your life did you feel the most out of control? What was that like day to day?",
              "", "text"),
            (16, "How much of your daily time and mental energy was consumed by drinking — planning it, doing it, recovering from it?",
              "", "text"),
            (17, "Did your drinking harm your work or career? What efforts did you make to keep it hidden professionally?",
              "", "text"),
            (18, "When did you first seriously consider that you might be an alcoholic? What was happening at that moment?",
              "", "text"),
            (19, "In what specific ways has your life become unmanageable? List the areas where things have broken down.",
              "Consider: relationships, health, work, finances, self-respect, legal issues.", "list"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 2 — Coming to Believe
    # ─────────────────────────────────────────────────────
    {
        "number": 2,
        "title": "Coming to Believe",
        "description": (
            "Came to believe that a Power greater than ourselves "
            "could restore us to sanity."
        ),
        "focus": (
            "Step 2 invites you to open your mind to the possibility that "
            "something beyond your own willpower can help you recover. "
            "This is not about adopting a specific religion — it is about "
            "finding hope that change is possible."
        ),
        "recovery_outcome": (
            "You begin to develop a personal understanding of a Higher Power "
            "and recognize that you do not have to face recovery alone. "
            "Hope replaces despair."
        ),
        "spiritual_principle": "Hope",
        "is_recurring": False,
        "questions": [
            (1, "Do you sense that there is some kind of order or purpose in the universe, or does everything feel random to you?",
             "There is no wrong answer. Be honest about where you stand today.", "text"),
            (2, "What role did spirituality or religion play in the home where you grew up?",
             "", "text"),
            (3, "How do you feel about whatever spiritual tradition you were raised in? Did it help you, harm you, or leave you indifferent?",
             "", "text"),
            (4, "Do you currently attend any religious or spiritual gatherings? Why or why not?",
             "", "text"),
            (5, "What role, if any, does spirituality play in your life right now?",
             "", "text"),
            (6, "Do you wish you had a stronger connection to something greater than yourself? What holds you back?",
             "", "text"),
            (7, "Have you ever felt angry at God or a Higher Power? What caused that anger?",
             "", "yesno"),
            (8, "Can you recall a moment of crisis when you found yourself praying or reaching out to something beyond yourself? What was that like?",
             "", "text"),
            (9, "If you were to describe your Higher Power to someone, what would you say? What qualities would it have?",
             "Your Higher Power can be anything — God, nature, the fellowship, the universe, love.", "text"),
            (10, "Has anyone in your life ever held power over you and misused it? How does that experience affect your ability to trust a Higher Power?",
              "", "text"),
            (11, "What would 'being restored to sanity' actually look like in your daily life?",
              "Think concretely about what sane, healthy living would mean for you.", "text"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 3 — Turning It Over
    # ─────────────────────────────────────────────────────
    {
        "number": 3,
        "title": "Turning It Over",
        "description": (
            "Made a decision to turn our will and our lives over to the "
            "care of God as we understood Him."
        ),
        "focus": (
            "Step 3 is about making a conscious decision to let go of the "
            "illusion of total control and to trust that your Higher Power "
            "can guide your recovery. It does not demand perfection — only "
            "willingness."
        ),
        "recovery_outcome": (
            "You gain insight into what surrender actually means in daily "
            "practice and begin to understand that letting go is not weakness "
            "but a profound act of faith."
        ),
        "spiritual_principle": "Faith",
        "is_recurring": False,
        "questions": [
            (1, "Does the idea of surrendering control frighten you, or does part of you welcome it? Explain.",
             "", "text"),
            (2, "When your life became unmanageable, was it because of poor thinking, overwhelming emotions, or both?",
             "", "text"),
            (3, "Do you believe your Higher Power has a specific plan for you, or does it simply provide strength and guidance? How does either view affect your recovery?",
             "", "text"),
            (4, "What does your daily practice of connecting with your Higher Power look like? Do you feel it is enough?",
             "This could be prayer, meditation, quiet reflection, time in nature — anything meaningful.", "text"),
            (5, "How does prayer or meditation make you feel? Do you feel heard?",
             "", "text"),
            (6, "Has your ability to trust been damaged by past experiences? Who or what broke your trust, and how does it affect you now?",
             "", "text"),
            (7, "When in your life have you felt a genuine sense of purpose or meaning? What was happening at those times?",
             "", "text"),
            (8, "What parts of your life are you willing to surrender? What parts feel impossible to let go of? What accounts for the difference?",
             "", "text"),
            (9, "What is the one habit, fear, or resentment you are most reluctant to turn over to your Higher Power? Why?",
             "", "text"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 4 — Moral Inventory
    # ─────────────────────────────────────────────────────
    {
        "number": 4,
        "title": "Moral Inventory",
        "description": (
            "Made a searching and fearless moral inventory of ourselves."
        ),
        "focus": (
            "Step 4 is a thorough, honest self-examination. The goal is not "
            "to beat yourself up, but to see yourself clearly — both your "
            "defects and your strengths. Avoid the extremes of self-loathing "
            "and self-glorification. Aim for the truth."
        ),
        "recovery_outcome": (
            "A candid and balanced portrait of who you are — your patterns, "
            "resentments, fears, and also your positive qualities. This "
            "inventory becomes the raw material for growth."
        ),
        "spiritual_principle": "Courage",
        "is_recurring": False,
        "questions": [
            (1, "Is there someone who exposed or confronted your addiction in a way that felt deeply hurtful? Do you still carry resentment toward them?",
             "", "text"),
            (2, "When you think of the person your drinking hurt most, what do you feel about yourself?",
             "", "text"),
            (3, "Do you experience sudden anger without an obvious cause? What patterns can you identify?",
             "", "text"),
            (4, "Have you ever sought revenge against someone? What happened, and how did it affect you afterward?",
             "", "text"),
            (5, "Do you experience self-loathing? What situations or memories trigger it most intensely?",
             "", "text"),
            (6, "Do you swing between extremes of low confidence and overconfidence? When does each show up?",
             "", "text"),
            (7, "What behavior in other people irritates you the most? Have you ever recognized that same behavior in yourself?",
             "", "text"),
            (8, "When someone wrongs you, do you expect an apology? Are you quick to apologize when you wrong others?",
             "", "text"),
            (9, "List the character traits you most associate with your addiction. Are any of them also useful in positive contexts?",
             "For example, stubbornness can also be persistence.", "list"),
            (10, "If you could go back and change one moment in your life, what would it be and why?",
              "", "text"),
            (11, "What is the best quality you inherited or learned from each parent? What is the most damaging?",
              "", "text"),
            (12, "Do you believe your worst traits are something you were born with, or were they shaped by your experiences?",
              "", "text"),
            (13, "Do you hold anyone else responsible for your addiction? Is there any truth to that, and does it matter?",
              "", "text"),
            (14, "Have you experienced trauma in your life? Did your drinking serve as a way to cope with it?",
              "You do not need to describe the trauma in detail if you are not ready.", "yesno"),
            (15, "Look at the biggest decisions you've made. What do your good decisions have in common? Your worst ones?",
              "", "text"),
            (16, "Do you accept responsibility for the harm caused by your drinking, or do you still make excuses? Be honest.",
              "", "text"),
            (17, "Is there something you have done that you are so ashamed of you have never told anyone? Why have you kept it hidden?",
              "This is private step work. No one sees this unless you choose to share it.", "text"),
            (18, "Overall, do you tend to judge yourself too harshly, or do you let yourself off too easy?",
              "", "text"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 5 — Admitting Wrongs
    # ─────────────────────────────────────────────────────
    {
        "number": 5,
        "title": "Admitting Wrongs",
        "description": (
            "Admitted to God, to ourselves, and to another human being "
            "the exact nature of our wrongs."
        ),
        "focus": (
            "Step 5 moves from private self-examination to sharing what "
            "you've found with your Higher Power and another person. "
            "This is where honesty becomes relational — and where healing "
            "deepens through connection."
        ),
        "recovery_outcome": (
            "By speaking your truth aloud to someone you trust, the weight "
            "of secrecy and shame begins to lift. You gain perspective on "
            "your inventory that you cannot get alone."
        ),
        "spiritual_principle": "Integrity",
        "is_recurring": False,
        "questions": [
            (1, "Has your addiction cost you a relationship that was important to you? Does that loss make it harder to open up to others now?",
             "", "text"),
            (2, "Has anyone surprised you by standing by you through your worst moments? How has their steadiness affected your recovery?",
             "", "text"),
            (3, "Some people in your life have used tough love; others have been gentle. Which approach has helped you more, and why?",
             "", "text"),
            (4, "What have you learned from your sponsor or a trusted mentor? Is there anything about their approach you would change?",
             "", "text"),
            (5, "What is your greatest fear about sharing your Step 4 inventory with another person? What is the worst thing that could realistically happen?",
             "", "text"),
            (6, "When you share your wrongs with your Higher Power, what do you feel? Do you sense any kind of response?",
             "", "text"),
            (7, "After completing your Fifth Step sharing, describe the experience. Were your fears justified? How do you feel now?",
             "Complete this question after your Fifth Step conversation.", "text"),
            (8, "Do you feel ready to share more openly with others in your life, or do you want to take it slowly? What feels right?",
             "", "text"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 6 — Becoming Ready
    # ─────────────────────────────────────────────────────
    {
        "number": 6,
        "title": "Becoming Ready",
        "description": (
            "Were entirely ready to have God remove all these "
            "defects of character."
        ),
        "focus": (
            "Step 6 is about becoming truly willing to change. It asks you "
            "to identify your character defects clearly and to examine why "
            "you might be clinging to them — even when they cause harm."
        ),
        "recovery_outcome": (
            "You develop a clear understanding of the flaws that hold you "
            "back and build genuine willingness to have them removed. "
            "Readiness is itself the work of this step."
        ),
        "spiritual_principle": "Willingness",
        "is_recurring": False,
        "questions": [
            (1, "Have you ever been less than fully honest in your prayers or conversations with your Higher Power? Do you believe you are forgiven?",
             "", "text"),
            (2, "When you feel emotionally uncomfortable, what do you instinctively do to change the feeling? Are those responses healthy?",
             "", "text"),
            (3, "What practical habits could you adopt that would genuinely improve your daily life? Be specific.",
             "", "text"),
            (4, "What destructive patterns do you keep repeating even though you know they harm you? Why do you think you return to them?",
             "", "text"),
            (5, "Are there behaviors you continue that are harmful to yourself or others? What concrete steps could you take to stop?",
             "", "text"),
            (6, "Do you contribute to the well-being of your community in any way? What more could you do?",
             "Think about your neighborhood, fellowship, family, workplace.", "text"),
            (7, "Do you consider yourself a dishonest person? Has working the steps so far changed your relationship with honesty?",
             "", "text"),
            (8, "Are you prone to envy? Has the recovery process made you more grateful for what you have?",
             "", "yesno"),
            (9, "Do you take genuine responsibility for your actions, or do you still find ways to deflect? How has this changed?",
             "", "text"),
            (10, "List the five most significant character defects you possess. For each, describe how it has harmed you and others.",
              "", "list"),
            (11, "For each defect listed above, what is one actionable step you could take to reduce its impact?",
              "", "action"),
            (12, "Are you attached to any of your defects? Do any of them feel like a core part of who you are? Why?",
              "", "text"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 7 — Humbly Asking
    # ─────────────────────────────────────────────────────
    {
        "number": 7,
        "title": "Humbly Asking",
        "description": (
            "Humbly asked Him to remove our shortcomings."
        ),
        "focus": (
            "Step 7 calls you to practice the humility you have been "
            "developing and to genuinely ask your Higher Power for help "
            "in removing your shortcomings. This is not bargaining — "
            "it is an honest request born from willingness."
        ),
        "recovery_outcome": (
            "A deeper humility about your ability to fix yourself alone, "
            "a clearer relationship with your Higher Power, and a more "
            "concrete vision of the life you are building in recovery."
        ),
        "spiritual_principle": "Humility",
        "is_recurring": False,
        "questions": [
            (1, "If your character defects were truly removed, how would you feel? Would you miss any part of them?",
             "", "text"),
            (2, "Write a letter to your Higher Power asking for help with your shortcomings. Do not bargain or plead — simply express your readiness to grow.",
             "This is a private letter between you and your Higher Power.", "letter"),
            (3, "Do you believe your shortcomings could return even after they are removed? In what situations would you be most vulnerable?",
             "", "text"),
            (4, "Are there moments when you lose hope in the recovery process? When does that tend to happen, and what can you do about it?",
             "", "text"),
            (5, "What are you most grateful for in your life right now? Do you express that gratitude enough?",
             "", "text"),
            (6, "Are you spending enough time with the people who matter most to you? If not, what could you change?",
             "", "text"),
            (7, "When do you feel most hopeful about your future? How can you create more of those moments?",
             "", "text"),
            (8, "What important things has your addiction taken from you? Should you try to rebuild any of them? What would that look like?",
             "", "text"),
            (9, "If your Higher Power removed your defects, what would a typical day look like? Are your expectations realistic?",
             "", "text"),
            (10, "Have you ever experienced genuine, deep happiness? Do you believe it can be part of your life again?",
              "", "text"),
            (11, "In what ways have you made the world around you better? How could you do more?",
              "", "text"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 8 — Making a List
    # ─────────────────────────────────────────────────────
    {
        "number": 8,
        "title": "Making a List",
        "description": (
            "Made a list of all persons we had harmed, and became "
            "willing to make amends to them all."
        ),
        "focus": (
            "Step 8 asks you to create a thorough, honest list of people "
            "you have harmed. The challenge is not just remembering names "
            "but becoming genuinely willing to face each person. This step "
            "is about preparation, not action."
        ),
        "recovery_outcome": (
            "A complete and honest list of people you have harmed, along "
            "with the willingness to make things right. This list becomes "
            "the foundation for Step 9."
        ),
        "spiritual_principle": "Justice",
        "is_recurring": False,
        "questions": [
            (1, "Which relationships in your life suffered the most damage because of your drinking? Describe what happened.",
             "", "text"),
            (2, "Are there people you owe an apology to for behavior unrelated to drinking? Should they be on your amends list too?",
             "", "text"),
            (3, "Have you ever imagined making amends to someone? Who was it, and what did you picture happening?",
             "", "text"),
            (4, "Who on your list do you most dread facing? Is there anyone you actually look forward to approaching?",
             "", "text"),
            (5, "For anyone on your list, could making amends actually cause them more harm? How will you handle those situations?",
             "Discuss these cases with your sponsor before acting.", "text"),
            (6, "What is the absolute worst outcome you can imagine from making amends? How likely is it? What is the best outcome?",
             "", "text"),
            (7, "How can you let go of expectations about how others will respond? You are powerless over their reactions.",
             "", "text"),
            (8, "What is the difference between making amends and simply apologizing? Why does the distinction matter?",
             "Amends involve changed behavior, not just words.", "text"),
            (9, "Create your list of people you have harmed. For each person, write how your behavior specifically affected their life.",
             "Be thorough. Include people you might want to skip over.", "list"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 9 — Making Amends
    # ─────────────────────────────────────────────────────
    {
        "number": 9,
        "title": "Making Amends",
        "description": (
            "Made direct amends to such people wherever possible, "
            "except when to do so would injure them or others."
        ),
        "focus": (
            "Step 9 is about taking action — making direct amends to the "
            "people on your list with sincerity and humility. The key is to "
            "approach each person without hidden motives and to accept "
            "whatever response comes."
        ),
        "recovery_outcome": (
            "Freedom from the burden of past wrongs. Amends-making teaches "
            "you how to live with integrity going forward. Your amends list "
            "is a living document that may grow as your awareness deepens."
        ),
        "spiritual_principle": "Forgiveness",
        "is_recurring": False,
        "questions": [
            (1, "Have you already attempted to make amends to anyone? What did you do, and what did you learn from the experience?",
             "", "text"),
            (2, "Examine your motives honestly: are you making amends for the right reasons, or do you have hidden goals like gaining approval or proving yourself right?",
             "", "text"),
            (3, "Are you trying to make anyone on your list feel guilty? If so, why? What would genuine amends look like instead?",
             "", "text"),
            (4, "Write a letter expressing all of your anger toward someone on your list. Get everything out. DO NOT SEND THIS LETTER.",
             "This is a therapeutic exercise to process anger before making amends.", "letter"),
            (5, "Work with your sponsor to process and release that anger. What approaches did you try? Did they help?",
             "", "text"),
            (6, "Draft an apology or statement of amends for each person who you believe deserves one. DO NOT SEND these yet — review them with your sponsor first.",
             "", "letter"),
            (7, "For each person on your list, what are specific, actionable amends you can make beyond words?",
             "Amends are about changed behavior, not just apologies.", "action"),
            (8, "Share your written amends with your sponsor. What was their feedback? Did they identify any hidden motives or insincerity?",
             "", "text"),
            (9, "If possible, practice the amends conversation with your sponsor through roleplay. What did you learn from the rehearsal?",
             "", "text"),
            (10, "Describe your first few amends experiences. What happened? What surprised you? What would you do differently?",
              "", "text"),
            (11, "During the amends process, did you feel the urge to defend yourself or justify your actions? How did you handle it?",
              "", "yesno"),
            (12, "How has making amends changed your relationships? Have any relationships been restored that you thought were lost?",
              "", "text"),
            (13, "Have you realized you need to make additional amends to people not on your original list? Who are they?",
              "", "list"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 10 — Continued Inventory
    # ─────────────────────────────────────────────────────
    {
        "number": 10,
        "title": "Continued Inventory",
        "description": (
            "Continued to take personal inventory and when we were "
            "wrong promptly admitted it."
        ),
        "focus": (
            "Step 10 shifts the focus from addressing the past to living "
            "well in the present. It asks you to practice daily self-examination "
            "and to make corrections quickly rather than letting wrongs accumulate."
        ),
        "recovery_outcome": (
            "A habit of ongoing self-awareness and prompt honesty. You learn "
            "to catch problems while they are small and to maintain the "
            "emotional sobriety that supports your physical sobriety."
        ),
        "spiritual_principle": "Perseverance",
        "is_recurring": True,
        "questions": [
            (1, "At the end of today, what did you do that contributed to your serenity and peace of mind? What disrupted it? What can you learn from both?",
             "This question is designed to be revisited daily.", "daily"),
            (2, "How do you create time each day for honest self-reflection? If you don't, what gets in the way?",
             "", "text"),
            (3, "What triggers or situations do you fear could lead to relapse? What specific safeguards do you have in place?",
             "", "text"),
            (4, "Were you resentful, self-centered, or dishonest at any point today? What happened?",
             "This question is designed to be revisited daily.", "daily"),
            (5, "What lessons from making amends can you apply to your everyday interactions? How will you address new wrongs promptly?",
             "", "text"),
            (6, "Is there sanity and stability in your life now? What does that look like, and how can you protect it? If not, what needs to change?",
             "", "text"),
            (7, "How can you practice honesty about your behavior in real time — not just in hindsight, but as events are unfolding?",
             "", "text"),
            (8, "Are you still putting the same effort into your recovery, or have you started to coast? What does sustained effort look like for you?",
             "", "text"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 11 — Conscious Contact
    # ─────────────────────────────────────────────────────
    {
        "number": 11,
        "title": "Conscious Contact",
        "description": (
            "Sought through prayer and meditation to improve our conscious "
            "contact with God as we understood Him, praying only for knowledge "
            "of His will for us and the power to carry that out."
        ),
        "focus": (
            "Step 11 is about deepening your relationship with your Higher "
            "Power through regular prayer and meditation. It encourages you "
            "to move beyond asking for things and toward seeking guidance "
            "and the strength to follow it."
        ),
        "recovery_outcome": (
            "A stronger, more secure relationship with your Higher Power "
            "and a growing ability to seek guidance rather than trying to "
            "control outcomes."
        ),
        "spiritual_principle": "Spiritual Awareness",
        "is_recurring": True,
        "questions": [
            (1, "How has your understanding of a Higher Power changed since you began working the steps?",
             "", "text"),
            (2, "If someone who didn't believe in anything asked you to explain your spiritual beliefs, what would you say?",
             "", "text"),
            (3, "What do you believe happens after death? How does that belief affect how you live today?",
             "", "text"),
            (4, "How do you distinguish between religion and spirituality? Do you need both in your life, one, or neither?",
             "", "text"),
            (5, "How often do you pray? What does prayer feel like, and what role does it play in your daily life?",
             "", "text"),
            (6, "When you pray, do you mostly ask for things, express gratitude, or seek guidance? Do you pray for others or mostly for yourself?",
             "", "text"),
            (7, "Do you practice meditation? If so, what does it do for you? If not, what has prevented you from trying?",
             "", "text"),
            (8, "When you meditate or sit in stillness, do you feel connected to anything? Are you listening for something?",
             "", "text"),
            (9, "Has your relationship with your Higher Power changed how you see yourself? In what ways?",
             "", "text"),
            (10, "How do you remind yourself that you are not in ultimate control? What practices help you stay humble?",
              "", "text"),
        ],
    },
    # ─────────────────────────────────────────────────────
    # STEP 12 — Carrying the Message
    # ─────────────────────────────────────────────────────
    {
        "number": 12,
        "title": "Carrying the Message",
        "description": (
            "Having had a spiritual awakening as the result of these steps, "
            "we tried to carry this message to alcoholics, and to practice "
            "these principles in all our affairs."
        ),
        "focus": (
            "Step 12 asks you to share the gifts of recovery with others "
            "and to live the principles of the program in every area of "
            "your life — not just in meetings or step work, but in how "
            "you treat people, handle conflict, and show up each day."
        ),
        "recovery_outcome": (
            "Recovery becomes a way of life rather than a project with an "
            "end date. You discover that helping others strengthens your "
            "own sobriety and that the steps are something you practice, "
            "not just complete."
        ),
        "spiritual_principle": "Service",
        "is_recurring": True,
        "questions": [
            (1, "How do you use your relationship with your Higher Power to be of service to others?",
             "", "text"),
            (2, "Have you reached out to someone who is still struggling with addiction? What happened, and how did it affect you?",
             "", "text"),
            (3, "What kind of support did you wish you had received when you first entered the program? How can you offer that to newcomers?",
             "", "text"),
            (4, "How did you handle conflict when you were actively drinking? How do you handle it now? What changed?",
             "", "text"),
            (5, "Do you believe your recovery is strong enough to sustain you long-term? If so, how will you keep building on it? If not, what needs more work?",
             "", "text"),
            (6, "How do you plan to be of service to your fellowship and to other alcoholics? How does that fit into your daily and weekly routine?",
             "", "action"),
            (7, "Do you feel ready to be a sponsor? If so, what prepared you? If not, what do you still need to develop?",
             "", "text"),
            (8, "What does it mean to you to 'practice these principles in all your affairs'? Give a specific example of how you do this.",
             "", "text"),
        ],
    },
]


class Command(BaseCommand):
    help = "Seed all 12 steps and their original guided questions"

    def handle(self, *args: object, **options: object) -> None:
        total_questions = 0

        for step_data in STEPS_DATA:
            questions = step_data.pop("questions")

            step, created = Step.objects.update_or_create(
                number=step_data["number"],
                defaults={**step_data, "order": step_data["number"]},
            )
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  {verb} Step {step.number}: {step.title}")

            for q_number, text, help_text, question_type in questions:
                Question.objects.update_or_create(
                    step=step,
                    number=q_number,
                    defaults={
                        "text": text,
                        "help_text": help_text,
                        "question_type": question_type,
                    },
                )
                total_questions += 1

            # Re-add questions for potential re-runs (pop removed them)
            step_data["questions"] = questions

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeeded {len(STEPS_DATA)} steps with {total_questions} questions."
            )
        )
