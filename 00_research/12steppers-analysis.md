# 12Steppers.org — Comprehensive Deep-Dive Analysis & Knowledge Base
### Product Analysis for Web Application Development

---

## 1. Application Overview

**What it is:** 12Steppers.org is a free, content-driven informational website that provides educational resources, printable worksheets, and a glossary for individuals participating in any of 30+ twelve-step recovery programs.

**Core offer:** Free printable 12-step worksheets with guided self-reflection questions, paired with an extensive educational resource library covering every major 12-step fellowship.

The site's primary deliverable is a downloadable PDF worksheet (available in PDF, DOCX, ODT, XLSX, CSV, and RTF formats) containing guided questions for all 12 steps of recovery. The worksheet is designed to complement—not replace—work done with a sponsor and a fellowship group. Beyond the worksheets, 12Steppers.org functions as a comprehensive encyclopedia of 12-step programs, covering over 30 fellowships across five categories: substance abuse, food-related addictions, friends & family programs, lifestyle & behavioral programs, and sex/love/relationship programs. The site also provides a glossary of recovery terminology, online meeting directories, meeting topic ideas, and articles on sponsorship, safety, program effectiveness, and spiritual principles.

**How it works — Current User Journey:**

1. **Discovery:** A user (typically a newcomer or someone returning to step work) finds the site via search, often looking for "12 step worksheet" or a specific step's questions.
2. **Orientation:** The homepage introduces 12-step programs broadly with navigation into specific fellowships or directly into the 12 steps.
3. **Step Education:** Each step has a dedicated article page explaining the step's purpose, spiritual principles, and practical application (12 individual pages, one per step).
4. **Worksheet Access:** From the "12 Step Worksheet" nav link, users can view an overview of all 12 steps with questions inline on the webpage, or download the complete worksheet as a PDF/DOCX/ODT/XLSX/CSV/RTF.
5. **Step 4 Deep-Dive:** Step 4 has its own dedicated, more detailed worksheet page with expanded inventory questions (the "moral inventory" step is traditionally the most writing-intensive).
6. **Supplementary Resources:** Users can access a gratitude worksheet (7 exercises, downloadable PDF), meeting topic ideas, a glossary, and an online meeting directory.
7. **Ongoing Reference:** Users return to individual step pages or resource articles as they progress through their program.

**Business model:** The site appears to operate as a free, ad-supported resource. It runs on WordPress and displays advertising. There is no subscription tier, no paywall, no premium content, and no user accounts. Revenue likely comes from display advertising, and potentially affiliate partnerships with treatment centers or recovery services. The site invites community contributions through a "Write For Us" page.

---

## 2. Target Market & Users

**Primary audience: People actively working a 12-step program.**

These are individuals who have committed to recovery through a 12-step fellowship—most commonly AA (Alcoholics Anonymous) or NA (Narcotics Anonymous)—and are either beginning their step work for the first time or cycling back through the steps. Demographics skew across all ages, though research suggests the bulk of AA members are 30–60 years old. They range from newly sober individuals to those with years of sobriety doing repeat step work. Their goals are to have a structured way to process each step's introspective questions, something to write on or fill in, and a resource to complement what their sponsor guides them through. Their pain points include feeling overwhelmed by the abstract nature of some steps, not knowing where to start, and wanting a tangible document they can hold in their hands or fill out between meetings.

**Secondary audiences:**

- **Sponsors** looking for a worksheet to give to sponsees as a structured tool for guiding step work conversations.
- **Newcomers exploring recovery** who haven't yet committed to a specific program and want to understand the 12-step landscape (which programs exist, how they work, what to expect at meetings).
- **Friends and family members** of addicts seeking to understand 12-step programs, or looking for their own programs (Al-Anon, Nar-Anon, ACA, etc.).
- **Therapists, counselors, and treatment professionals** who may use or recommend the worksheets as supplementary tools in clinical settings.
- **Members of less common 12-step programs** (Debtors Anonymous, Emotions Anonymous, Workaholics Anonymous, etc.) who have fewer mainstream resources available.

**User context — What triggers someone to seek this out?**

The primary trigger is being told by a sponsor, a meeting, or a treatment program to "work the steps." This is an actionable directive that requires introspection, writing, and self-assessment, but the user often doesn't know how to begin. They search for worksheets, guides, or questions to structure the process. Secondary triggers include: receiving a court mandate to attend 12-step meetings, leaving a treatment facility and needing aftercare support, experiencing a relapse and restarting step work, or being newly sober and curious about the program structure. The motivation to take action stems from a combination of personal desperation (life has become unmanageable), external pressure (family, legal system, employer), and hope (observing others who have found recovery through the program).

---

## 3. Problem & Value Proposition

**Core problem solved:** People in 12-step programs need structured, guided prompts to do the deep introspective work each step requires, but the steps themselves are described abstractly in program literature, leaving many members unsure how to translate principles into concrete personal reflection.

The traditional 12-step program texts (AA's Big Book, NA's Basic Text, etc.) describe the principles of each step, but they don't provide a worksheet format with specific questions to answer. A sponsor guides the process verbally, but many members benefit from having written prompts they can work through independently between meetings. Without this structure, members may procrastinate on step work, feel intimidated by the scope of self-examination required, or produce superficial responses that don't lead to meaningful growth.

**Value proposition:** 12Steppers.org provides free, downloadable, program-agnostic worksheets with thoughtfully crafted questions for every step, designed to complement sponsor guidance and make the abstract personal.

**Unique differentiators of 12Steppers.org content:**

- **Program-agnostic framing:** The worksheets use the word "addiction" broadly rather than being specific to alcohol, drugs, or any single fellowship. This makes them usable across all 30+ supported programs.
- **Educational scaffolding:** Each step's section includes three pedagogical components: (1) "Focus of step" — what the step is about and why the questions are structured as they are, (2) the questions themselves, and (3) "How this step helps us recover" — connecting the introspective work to recovery outcomes.
- **Balanced tone:** The worksheet explicitly warns against both self-aggrandizement and self-loathing, encouraging measured, honest reflection.
- **Multiple format availability:** PDF, DOCX, ODT, XLSX, CSV, RTF — accommodating different user preferences and accessibility needs.
- **Completely free and reprintable:** The content is explicitly offered for free reprinting with attribution, making it accessible to sponsors, meeting groups, and treatment centers.

---

## 4. Complete Worksheet Content Inventory

This section documents every question from the 12Steppers.org worksheet, organized by step, including the pedagogical framing. This is the core content that would be converted into interactive forms in your web application.

### Step 1 — Admitting Powerlessness
**Theme:** Acknowledging that addiction has defeated us and our attempts to function have failed.
**Spiritual Principle:** Honesty

**Questions (19 total):**

1. How did you discover your addiction? Why did you enjoy it initially?
2. How did you feel when you had not engaged in an addictive behavior for a while?
3. List all the types of behavior of which your addiction consisted. Which did you do most often and why?
4. Did your addiction damage your most important personal relations? How did it do so?
5. Does your addiction isolate you from other people? Is it an internal feeling of isolation, or have the people in your life noticed it too?
6. Were there any feelings that led to bouts of engagement in addictive behavior? Were you trying to mask them? How did your behavior alter or influence those feelings?
7. What is the most regrettable outcome of your addiction?
8. How did your addiction affect your finances? How did you rationalize your spending? Did you have to hide the damage from other people?
9. How did you try to hide your addictive behavior from other people? Did it work?
10. Did you suffer any illnesses or maladies, either physical or mental, because of your addiction? What were they? How did you deal with them?
11. Did you ever do something you truly did not want to do (without being forced), knowing that you did not want it? Was it related to your addiction? How did it feel?
12. Did you ever put yourself in danger because of your addiction? How did you manage the situation? Did you put yourself in danger again or did you learn from the first time?
13. What is the most embarrassing situation that emerged in your life as a result of your addiction?
14. Did you ever manipulate other people to satisfy your addiction? How did you rationalize it?
15. In what period in your life did you feel you had the least control? Was it related to your addiction? What did it feel like?
16. How much time did you spend on your addiction, both when things were at their worst and normally? How did this influence the rest of your life?
17. Did you ever truly betray another person because of your addiction? How did you rationalize it?
18. Did your addiction affect your career? What lengths did you go to hide your behavior at work? Did it work?
19. When did you realize you were an addict? Did you feel like your life was unmanageable at that moment? In what way?

**Recovery outcome:** Taking stock of how life became unmanageable and how previous attempts to manage addiction failed. Admitting failure to prepare for a better path.

---

### Step 2 — Coming to Believe (Restoration of Hope)
**Theme:** Trusting that a greater power can lead to recovery. Probing spirituality and willingness to let go.
**Spiritual Principle:** Hope

**Questions (11 total):**

1. Do you believe that there is an order to the universe or are events random?
2. What was the attitude towards spirituality in your childhood home?
3. How do you feel about the spiritual tradition you grew up in? Did it contribute to your addiction or provide you any aid or comfort?
4. Do you ever attend religious services or rites of any kind? Why or why not?
5. What role does spirituality currently play in your life?
6. Do you wish spirituality played a larger role in your life? If so, why doesn't it?
7. Do you ever feel anger at a Higher Power? Why do you feel it? Is it justified?
8. Have you ever prayed to a Higher Power in moments of distress? Why? How did it make you feel?
9. Have you ever made a deal or bargain with a Higher Power? Did you keep to it? Why?
10. Does your Higher Power have characteristics? If so, what are they?
11. Did you ever feel like someone in your family had authority over you and abused it? How does that make you feel about the concept of a Higher Power?

**Recovery outcome:** Focusing on current vision of a Higher Power, understanding why you view it as you do, and beginning to consider what role it will play in your future.

---

### Step 3 — Turning It Over (Surrender)
**Theme:** Understanding and managing the process of giving control to a Higher Power.
**Spiritual Principle:** Faith / Surrender

**Questions (9 total):**

1. Do you fear a loss of control or do you welcome the possibility of someone or something making decisions for you?
2. Did you lose control of your life due to a lack of rational judgment or a lack of emotional control?
3. Does your Higher Power have a plan for you, or does this power leave you with free will?
4. How do you maintain the presence of your Higher Power in your daily life? Do you believe recovery requires more of an effort than you are currently making? If so, why?
5. Do you ever pray? How does prayer make you feel? Does it matter why you pray?
6. Have you ever truly trusted anyone? Was this trust betrayed? How easy is it for you to trust now?
7. Do you feel like your life has meaning? Has anything you have done in the past made you feel like your life was meaningful? Why?
8. Are there things that are easy for me to surrender? Are other things very difficult to surrender? Why and what is the difference?
9. What is the most problematic habit or part of me which I have not yet fully surrendered?

**Recovery outcome:** Insight into the process of surrender and beginning to understand the role of a Higher Power in the new path.

---

### Step 4 — Moral Inventory (Self-Assessment)
**Theme:** Taking fair stock of who we are — deficiencies and strengths — without extremes of self-aggrandizement or self-loathing.
**Spiritual Principle:** Courage

**Questions (18 total):**

1. Has anyone hurt you deeply by judging or outing your addictive behavior? Do you feel anger at this person?
2. When you think of the person you hurt most through your addiction, how do you feel about yourself?
3. Do you ever get mad at random? At what? Why?
4. Have you ever tried to get revenge on a person? Why? What was the result?
5. Do you ever feel self-loathing? What triggers it?
6. Do you suffer from a lack of confidence or overconfidence? If so, do you ever veer from one extreme to another? Why?
7. What form of behavior do you find most aggravating in others? Do you ever behave that way?
8. When people hurt you, do they apologize? Would you prefer that they did? Do you apologize for hurting others?
9. Do you have character traits which you associate with addiction? Are they purely negative or have you also used them for beneficial purposes?
10. If you had a chance to do-over one incident in your life, what would it be? Why?
11. What is the best trait you inherited from your parents and what is the worst?
12. Think about your worst traits. Do you think you were born with them or were they shaped by your environment?
13. Do you blame anyone else for your addiction? Is that justified?
14. Have you ever experienced trauma? Was your addiction a coping mechanism?
15. Look at the most important decisions of your life. Do your good decisions have anything in common? What about your bad ones?
16. Do you feel responsible for the damage you caused because of your addiction? Why?
17. Have you ever done something you are so ashamed of, that you have told no one or almost no one about it? Why have you avoided sharing it?
18. Do you think you judge yourself too harshly or too leniently?

**Recovery outcome:** A fair and searching look at personality, understanding that character flaws can also be channeled positively.

**Note:** Step 4 also has a dedicated, separate expanded worksheet on the site specifically for the moral inventory process. This is the most writing-intensive step in the traditional 12-step framework.

---

### Step 5 — Admitting Wrongs (Sharing with Others)
**Theme:** Developing honest and genuine relationships by sharing insights about flaws with others.
**Spiritual Principle:** Integrity

**Questions (8 total):**

1. Have you lost an important relationship due to your addiction? Does that make it difficult to discuss it with other people?
2. Has anyone pleasantly surprised you by always being there for you? How has that influenced your recovery?
3. Some people have practiced "tough love" with you during your addiction and recovery. Others have taken a softer approach. Which helped you more?
4. What have you learned from your sponsor? What would you change about them?
5. Do you fear sharing your fifth step with another individual? What is the worst thing that can happen?
6. When you share your fifth step with your Higher Power, what do you feel? Do you get a sense of the response of your Higher Power to your efforts?
7. Once you have shared, write down what the experience was like. Were your fears overblown? Are you glad you did this?
8. Do you feel ready to share with other people, or are you happy to leave it as is?

**Recovery outcome:** Understanding wrongs and seeing what others think of behavior, preparing to work towards removal of defects.

---

### Step 6 — Becoming Ready (Defect Awareness)
**Theme:** Embracing humility and becoming ready to have a Higher Power remove character defects.
**Spiritual Principle:** Willingness

**Questions (12 total):**

1. Have you ever been misleading in your prayers and interactions with your Higher Power? Do you believe your power forgives you?
2. When I am uncomfortable with what I am feeling, what steps do I take to change it? Are they healthy?
3. What can you do to improve yourself? Think of practical habits, which would improve your life if you followed through on them.
4. What destructive habits do I keep repeating? If they are destructive, why do I repeat them?
5. Do you still engage in activity that is harmful to yourself and others? How could you stop?
6. Do you contribute to the well-being of your community? Could you do more? If so, what are practical steps you can take weekly to do so?
7. Do you consider yourself a dishonest person? Has working the steps made you a more honest person?
8. Are you an envious person? Has working the steps made you more grateful?
9. Do you take responsibility for your actions? Has working the steps made you a more accountable person?
10. List the five most significant defects of character you possess. How have they harmed you and others?
11. Are there any actionable steps you can take to alleviate the implications of those defects?
12. Do you cling to any of those flaws? If so why?

**Recovery outcome:** Understanding flaws and how they persist. Preparing to ask for their removal.

---

### Step 7 — Humbly Asking (Removal of Shortcomings)
**Theme:** Practicing humility learned in previous steps, trusting the Higher Power to remove shortcomings.
**Spiritual Principle:** Humility

**Questions (11 total):**

1. How would you feel if you no longer had those characteristics? Would you be happier or would you feel like you have lost part of your identity?
2. Write a letter to your Higher Power asking for the removal of these traits. Make sure not to bargain or plead, but rather show a readiness to grow.
3. Do you believe your shortcomings can come back? In what situations is this most likely to occur?
4. Do you ever lose hope in the process of recovery? When does that occur and why? Can you do anything to avoid it?
5. What are you most grateful for? Who do you credit with these elements in your life? Do you show enough gratitude?
6. Do you spend enough time with loved ones? If not, how can you change your habits to change that?
7. When do you feel most hopeful? How can you bring those situations into your day-to-day life?
8. What have you lost due to your addiction? Should you try and reintroduce those elements into your life? What would that look like?
9. If your Higher Power were to remove your defects, what would your life look like? Are your expectations realistic?
10. Have you ever been truly happy? If so, do you think that happiness can be recaptured?
11. Have you improved the world around you? If not, how can you? If you have, could you do more?

**Recovery outcome:** Greater humility regarding personal ability to remove shortcomings, better understanding of the Higher Power's role, and a clearer vision of a better life.

---

### Step 8 — Making a List (People Harmed)
**Theme:** Creating a comprehensive, honest list of people harmed. Overcoming emotional barriers to including the right people.
**Spiritual Principle:** Willingness / Justice

**Questions (9 total):**

1. What are the most important relationships you destroyed or damaged because of your addictive behaviors?
2. Do you owe anyone an apology for your non-addiction related behavior? Should they be on your list?
3. Have you pictured making amends to anyone over the years? Who was it? What did it look like?
4. Who do you most fear making amends to? Do you look forward to making amends to anyone?
5. Will I be harming the person or others further by making amends?
6. What is your absolute worst fear regarding making amends? How likely is that to occur? What are your best expectations? How likely are they?
7. How can I let go of these expectations and realize I am powerless over the response?
8. How is making amends different from just saying you are sorry?
9. Now make that list. Try to include everyone you have hurt due to your addictive behavior. For each write how your behavior affected their lives as individuals. Only then write how it influenced your relationship.

**Recovery outcome:** A workable list of people to make amends to.

**Note:** Question 9 is a structured list-building exercise — this would be a dynamic, repeatable form element in a web application (name + impact description + relationship impact).

---

### Step 9 — Making Amends (Direct Action)
**Theme:** Making amends the right way and for the proper reasons, avoiding ulterior motives.
**Spiritual Principle:** Discipline / Forgiveness

**Questions (13 total):**

1. Have you already made amends to anyone? What did they consist of? Were they sufficient? What did you learn from them?
2. Am I genuine in making my amends, or do I have hidden motives, such as to gain acceptance or love from someone else, or to prove them wrong and me right?
3. Am I trying to make the individuals on the list guilty? If so, why?
4. Do you feel anger towards anyone on the list? If so, write a letter expressing all your reasons for anger. DO NOT SEND IT.
5. Figure out with your sponsor how to get rid of that anger. What mechanisms did you use? Did they work?
6. Write an apology and/or statement of amends for each individual you believe deserves one. DO NOT SEND IT.
7. Design a list of actionable amends to each person on your list.
8. Show the written apologies to your sponsor. Your sponsor should now tell you if they sound sincere, or if an ulterior motive shows through. Write down your sponsors' comments.
9. Try to roleplay at least one process of amends making with your sponsor. Now you should be ready to make amends.
10. What happened in your first few attempts? What did you learn from them? How can you improve in the future?
11. Did you have a desire to defend yourself? How did you deal with it?
12. How has this process affected your relationship with others?
13. Did you realize you have to make further amends? To whom? Write a list.

**Recovery outcome:** Making amends for wrongs committed, learning how to make amends in the future. The list is described as a "living breathing" document.

**Note:** Multiple questions here involve writing separate documents (letters, apology statements, actionable amends lists) — in a web application, these would be sub-forms or linked documents within the step.

---

### Step 10 — Continued Inventory (Daily Practice)
**Theme:** Transitioning from addressing the past to bringing recovery into daily life. Ongoing self-assessment.
**Spiritual Principle:** Perseverance

**Questions (8 total):**

1. At the end of every day, ask yourself, what did I do today that helped me obtain serenity and peace of mind? What failed to do so? What can I learn from this?
2. Taking inventory requires time for reflection. How do you make time for that daily?
3. Do you still have triggers and behaviors you fear will cause a relapse? What are they? How can you guard against them?
4. Have I been resentful, self-serving or dishonest today?
5. What did you learn from the process of making amends which you can apply to your day-to-day life? How will you immediately make amends for, and acknowledge new wrongs?
6. Is there sanity in my life now? If so, what does that entail and how can I maintain it? If not, what steps can I take to restore sanity in my life?
7. How can I be critical and honest about my behavior, not only in retrospect but also while events are still unfolding?
8. Am I resting on my laurels or am I still fighting just as hard for my recovery?

**Recovery outcome:** No longer just addressing past wrongs but improving ongoing daily life.

**Note:** Step 10 is inherently a *recurring* step. Questions 1 and 4 are designed to be answered daily. A web application should support repeatable daily journal entries tied to this step.

---

### Step 11 — Conscious Contact (Spiritual Relationship)
**Theme:** Building and maintaining a close relationship with a Higher Power.
**Spiritual Principle:** Spiritual Awareness

**Questions (10 total):**

1. How has your belief in a Higher Power changed since you started working the steps?
2. How would you explain these beliefs to an atheist?
3. What do you believe happens after death?
4. How do I understand the difference between religion and spirituality? Do I have both in my life? Do I need both?
5. How often do I pray? How does prayer make you feel? What role does it play in your life?
6. When I pray do I make demands or petition my Higher Power? Do I express enough gratitude? Do I pray for others or only for myself?
7. Do I meditate? Why or why not? If you do, what role does it play in your life?
8. Do you feel connected to anything when you meditate? Are you listening to anything?
9. Has your perception of self been altered by your relationship with a Higher Power? How has it changed?
10. Do you always remember you are not in control? How do you remind yourself of that?

**Recovery outcome:** A more secure and healthy relationship with a Higher Power.

**Note:** Like Step 10, Step 11 has an ongoing daily practice component (morning and nighttime prayer/meditation routines). A web application should support daily check-ins tied to this step.

---

### Step 12 — Carrying the Message (Service & Practice)
**Theme:** Passing on the benefits of recovery to others, practicing principles in all affairs.
**Spiritual Principle:** Service

**Questions (8 total):**

1. How do you use your positive relationship with a Higher Power to make the world better for others?
2. Have you reached out to a recovering addict or an addict still in pain? If so, describe the situation and how it affected you. If not, why not?
3. What kind of support would you have liked to receive when you started the program? How can you use these insights to help those still suffering from addiction?
4. How did you handle conflict when you were an addict? Has working the steps changed that? If so, how?
5. Do you believe your life is now solid enough to maintain long-term recovery? If so, how can I build on this? If not, what do I need to do to get there?
6. How do you plan to be of service to the fellowship and other addicts? How will you work that into your daily life?
7. Do you think you are ready to be a sponsor? If so, when did you feel you were ready? If not, what do you think you need to work on to get to that stage?
8. Having understood the principles of recovery, what does it mean to "practice these principles in all my affairs?"

**Recovery outcome:** Completion of the 12 steps, with the understanding that recovery is a lifestyle, not an endpoint. Users may find it necessary to work the steps again.

---

## 5. Additional Worksheet Content

### Gratitude Worksheet (7 Exercises)
The site offers a separate, free printable gratitude worksheet containing 7 exercises specifically designed for 12-step program participants. Gratitude practice is a core component of ongoing recovery, particularly relevant to Steps 7, 10, and 11.

### Step 4 Dedicated Worksheet
Step 4 has its own expanded worksheet page beyond the main worksheet. This reflects the traditional emphasis on Step 4 as the most intensive written exercise in the 12-step process — the "searching and fearless moral inventory." In traditional AA practice, this often involves structured tables for resentments, fears, sex conduct, and harms done.

---

## 6. Site Architecture & Content Map

### Navigation Structure
```
├── 12 Step Programs (30+ fellowship pages across 5 categories)
│   ├── Substance Abuse (AA, CA, CMA, HA, MA, NA, NicA, PA)
│   ├── Food-Related (FAA, FA, OA)
│   ├── Friends & Family (ACA/ACOA, Al-Anon, Co-Anon, Gam-Anon, FA, Nar-Anon)
│   ├── Lifestyle & Behavioral (CLA, CoDA, DA, EA, GA, SIA, RA, UA, WA)
│   └── Sex, Love & Relationships (COSLAA, SA, SAA, SCA, SLAA, SRA)
├── 12 Steps (12 individual step pages + overview)
├── Resources
│   ├── Articles (Sponsorship, Safety, Program Effectiveness, etc.)
│   ├── 12 Step Meetings info
│   ├── 12 Traditions
│   └── Program-specific resources (AA, NA, SA, etc.)
├── 12 Step Worksheet (main worksheet with all 12 steps)
├── Step 4 Worksheet (dedicated expanded worksheet)
├── Online Meeting List (directory of virtual meetings)
└── 12 Step Terms (glossary)
```

### Content Volume
- **12 individual step pages** with in-depth educational content
- **30+ fellowship pages** with program-specific information
- **20+ resource articles** covering topics like sponsorship, safety, program effectiveness, spiritual principles, AA slogans, meeting types, and more
- **1 comprehensive worksheet** (PDF, 12 pages, ~130 questions total across all steps)
- **1 dedicated Step 4 worksheet** (expanded moral inventory)
- **1 gratitude worksheet** (7 exercises)
- **1 glossary** of 12-step terminology
- **1 online meeting directory**

---

## 7. Competitive Landscape

### Direct Competitors (Digital 12-Step Worksheet/Recovery Apps)

**1. 12 Step Toolkit App (12steptoolkit.com)**
- **Platform:** Android, iOS, Mac, Web
- **Users:** 450,000+ members, 11,000+ in-app sponsors, 15,000+ positive reviews
- **Key features:** Sobriety calculator, Step 4 & 5 inventory tool (resentment/fear/sex/harms format), Step 8 & 9 amends tool, Step 10 spot-check inventory, Step 11 nighttime & morning inventory tools, notes & gratitude lists, instant messaging, sponsorship management tools, AA literature and prayers, Big Book stories, hourly motivational notifications
- **Business model:** Free with ads; paid subscription removes ads and unlocks premium features
- **Strengths:** Largest community, comprehensive tool coverage across key steps, built-in sponsor/sponsee relationship management
- **Weakness:** AA-specific (not program-agnostic), ad-supported free tier may feel inappropriate for recovery context

**2. OpenRecovery (Huxley Technologies)**
- **Platform:** Android, iOS
- **Key features:** Kai AI Recovery Assistant with voice chat, guided step work with real-time AI feedback, conversational inventories with shareable summaries, accountability partner integration, milestone/daycount tracking, video tutorials, customizable accountability reports
- **Programs supported:** 25+ programs including AA, NA, GA, OA, SLAA, SAA, DA, MA, CA, Al-Anon, ACA, CoDA, and more. Also supports SMART Recovery and CBT methodologies
- **Business model:** Free base; premium subscription with 14-day trial for unlimited AI features and analytics
- **Strengths:** AI-powered (most modern approach), broadest program support, voice interaction, combines 12-step with SMART Recovery and CBT
- **Weakness:** AI reliance may feel impersonal to traditionalists, newer product with smaller community

**3. Recovery Box**
- **Features:** Nightly reminders, note-taking, sponsor/sponsee connections via instant messenger, spiritual tools, AA program worksheets and accountability tools
- **Business model:** $39.99/year or $15.99/quarterly for unlimited ad-free access
- **Strengths:** Complete AA program coverage, affordability
- **Weakness:** More limited feature set compared to newer competitors

**4. 12Step.org Tools**
- **Type:** Web-based (not an app)
- **Features:** Custom worksheets generated by addiction type and step number, self-reflection tools
- **Business model:** Free
- **Strengths:** Customizable to specific addictions, similar philosophy to 12steppers.org
- **Weakness:** Not interactive, no account system, no progress tracking

**5. 12 Steps AA Companion (App Bundle)**
- **Features:** Big Book reader with search, sobriety calculator, notes, AA contacts database, recovery speaker recordings (1,000+ tracks, 100+ hours)
- **Business model:** App bundle with monthly/quarterly premium subscription for full audio access ($3.99/mo or $6.99/quarter)
- **Strengths:** Most comprehensive audio content, Big Book reference tool
- **Weakness:** AA-only, primarily literature/audio focused rather than step work

### Adjacent Competitors (Sobriety/Recovery Apps without Step Work Focus)

- **SoberTool:** CBT-based thinking adjustment for sobriety
- **Sobriety Counter:** Quit-slowly mode, 64 sobriety badges, health improvement tracking
- **I Am Sober:** Community-based sobriety tracking with daily pledges
- **Loosid:** Social network for sober people (non-anonymous)

### Competitive Gap Analysis — Opportunity for Your Application

| Feature | 12Steppers.org | 12 Step Toolkit | OpenRecovery | **Your App (Opportunity)** |
|---------|---------------|-----------------|--------------|---------------------------|
| Account/login system | ❌ | ✅ | ✅ | ✅ |
| Save progress | ❌ | ✅ | ✅ | ✅ |
| Interactive form-based step work | ❌ | Partial (Steps 4,8,10,11) | AI-guided | ✅ All 12 steps |
| Program-agnostic | ✅ | ❌ (AA only) | ✅ | ✅ |
| Web-based (no install) | ✅ (static) | ✅ | ❌ (app only) | ✅ |
| Guided questions per step | ✅ (print) | Partial | AI-generated | ✅ Pre-written + expandable |
| Progress dashboard | ❌ | ✅ | ✅ | ✅ |
| Daily inventory (Step 10) | ❌ | ✅ | ✅ | ✅ |
| Gratitude tracking | ❌ (print) | ✅ | ❌ | ✅ |
| Database persistence | ❌ | ✅ | ✅ | ✅ |
| Sponsor sharing/review | ❌ | ✅ | ✅ | Possible |
| Free/Open content | ✅ | Freemium | Freemium | Your choice |
| AI assistance | ❌ | ❌ | ✅ (Kai) | Possible |

**Key differentiator opportunity:** No existing product combines (1) the complete 12Steppers.org question set for all 12 steps, (2) interactive web-based forms, (3) program-agnostic design, and (4) persistent database-backed progress tracking in a single web application. The closest competitors are either app-only, AA-specific, or only cover select steps with inventory tools.

---

## 8. Feature Specification for Web Application

Based on the analysis above, here is a detailed feature map for converting 12Steppers.org worksheets into an interactive web application.

### Core Features

**8.1 User Account System**
- Email/password registration
- Anonymous option (recovery culture values anonymity — consider allowing pseudonymous accounts)
- Profile: sobriety date, primary fellowship, sponsor info (optional)
- Data encryption at rest (sensitive personal disclosures)

**8.2 Step Work Module (12 Interactive Forms)**
For each of the 12 steps:
- Step overview (focus, spiritual principle, why it matters)
- Interactive form with all questions from the 12Steppers.org worksheet
- Text area fields for each question with auto-save
- Ability to mark a step as "In Progress," "Complete," or "Revisiting"
- Timestamp tracking for when each answer was written/edited
- Ability to revisit and revise answers (recovery is iterative)

**8.3 Progress Dashboard**
- Visual progress indicator showing completion status across all 12 steps
- Current step highlighted
- Percentage complete per step (questions answered / total)
- Timeline view showing when step work was done
- Sobriety date counter/calculator

**8.4 Daily Practice Module (Steps 10 & 11)**
- Step 10 daily inventory: recurring form with daily prompts (questions 1 and 4 from Step 10)
- Step 11 morning and nighttime check-in prompts
- Calendar view of daily entries
- Streak tracking for consistent daily practice

**8.5 Amends Management (Steps 8 & 9)**
- Dynamic list builder for Step 8 (add people, describe harm, describe relationship impact)
- Per-person amends tracking for Step 9 (status: not started, letter drafted, amends made, ongoing)
- Private letter/journal space for anger letters (Step 9, Q4) and apology drafts (Step 9, Q6)
- Notes field for sponsor feedback (Step 9, Q8)

**8.6 Gratitude Journal**
- Daily gratitude entries (based on the 7-exercise gratitude worksheet)
- Historical view of gratitude entries
- Tied to Step 7 and ongoing practice

**8.7 Character Defects Tracker (Step 6)**
- List builder for the "five most significant defects of character" (Step 6, Q10)
- Action plan field for each defect (Step 6, Q11)
- Check-in mechanism for tracking progress on defects over time

### Extended Features

**8.8 Multiple Program Support**
- Allow users to select which 12-step fellowship they belong to
- Language/terminology can be subtly customized per program (e.g., "alcohol" vs "substance" vs "behavior")
- Support for working the steps in multiple programs simultaneously

**8.9 Export/Print**
- Export completed step work as PDF (recreating the worksheet format with answers filled in)
- Print individual steps or the complete set
- Share with sponsor (generate a read-only link or export)

**8.10 Educational Content**
- "Focus of step" and "How this step helps us recover" text displayed alongside each form
- Links to relevant articles and resources
- Glossary of terms accessible throughout

**8.11 Privacy & Security**
- End-to-end encryption for stored answers
- No social features visible by default (recovery content is deeply personal)
- Option to completely delete account and all data
- HIPAA-awareness (while not a healthcare app, users will disclose health-related information)

---

## 9. Question Type Analysis for Form Design

Understanding the nature of each question helps determine appropriate form field types:

| Question Type | Count | Example | Recommended Form Element |
|---------------|-------|---------|--------------------------|
| Open-ended reflective | ~85 | "How did you discover your addiction?" | Large textarea (300+ chars) |
| Yes/No + elaborate | ~25 | "Do you ever pray? How does it make you feel?" | Toggle + conditional textarea |
| List-building | ~8 | "List all types of behavior..." / "Make that list" | Dynamic repeating rows |
| Letter writing | ~3 | "Write a letter to your Higher Power" | Rich text editor / large textarea |
| Action planning | ~5 | "Design a list of actionable amends" | Structured task list |
| Daily recurring | ~4 | "At the end of every day, ask yourself..." | Daily journal entry form |
| Ranking/rating | ~2 | "List the five most significant defects" | Ordered list builder |

**Total unique questions across all 12 steps: ~130**

---

## 10. Content Licensing & Legal Considerations

The 12Steppers.org worksheet includes an explicit statement: the content "may be reprinted" with credit to 12steppers.org and "may not be sold for profit." This has important implications:

- **You may use the question structure and pedagogical framing as inspiration**, but you should create original questions and content for your commercial application.
- The 12 steps themselves are derived from AA's program and are widely considered public domain in their general form, though specific wordings from AA's Big Book are copyrighted by AA World Services, Inc.
- **Recommendation:** Create original guided questions inspired by the 12Steppers.org approach, tailored specifically for your interactive format. Consult a lawyer regarding any IP considerations, especially if you plan to monetize.

---

## 11. Summary Statistics

| Metric | Value |
|--------|-------|
| Total steps covered | 12 |
| Total worksheet questions | ~130 |
| Questions per step (average) | ~11 |
| Most question-heavy step | Step 1 (19 questions) |
| Least question-heavy step | Step 5 (8 questions) |
| Steps with daily/recurring components | Steps 10, 11, 12 |
| Steps with list-building exercises | Steps 4, 6, 8, 9 |
| Steps with letter-writing exercises | Steps 7, 9 |
| Downloadable formats offered | 6 (PDF, DOCX, ODT, XLSX, CSV, RTF) |
| 12-step programs covered by site | 30+ |
| Separate worksheets offered | 3 (Main 12-Step, Step 4, Gratitude) |

---

*Document prepared as a living knowledge base for the development of an interactive 12-step recovery web application. Last updated: February 2026.*
