# Hacker News Final Output

## 1. Shadcn/UI now defaults to Base UI instead of Radix

- HN: https://news.ycombinator.com/item?id=48791328
- External: https://ui.shadcn.com/docs/changelog

### Summary

shadcn/ui is changing its default component library from Radix to Base UI, starting July 2026. The post explains that while Radix remains fully supported (not deprecated), Base UI is now the recommended option because it’s stable (v1.6.0), improving quickly, and is already used for new projects created via shadcn/create and docs defaults. New projects will use Base UI automatically, with Radix available via a flag or config to keep existing CI scripts consistent. The team also offers an AI “skill” to migrate progressively component-by-component without risky codemods, producing working, typechecked code plus per-component migration reports and clean git history.

#### Top 5 Positive Comments

1. Great news. I've found that no UI library comes close to shadcn's quality. It even looks incredible when building desktop apps. We used it to build DB Pro [1] and the DB Pro website, and everyone compliments us on our design. I see it becoming the defacto choice for UIs especially when building with agents. [1] https://dbpro.app

2. I love Mantine. It’s easy to use, full featured with lots of components and helpers, and yet if you need to, you can use it headless and customise it too (I’ve never bothered though; I did add my own additional spacing/sizing options via the theme support though)

3. Base UI is more low-level, a lot less opinionated and doesn’t force you into certain layouts. This of course makes it more complex to use, but that doesn’t matter if you’re using shadcn components because they’re doing that work for you. So essentially they look and operate the same as Radix components at the shadcn level but you have low-level control later on should you need it.

4. I highly prefer a copy and paste approach. The less npm installs the better.

5. That's great. Started using Base UI early on via 9ui [0] and found the primitives very pleasant to work with, especially if one wants to compose more complex components from other Base UI components. Maybe Shad can reduce some of the dependencies they rely on now. [0] https://www.9ui.dev

#### Top 5 Negative Comments

1. Martine just straight up sucks. Vendoring your components gives you the best of both worlds. You get a full component library but retain the ability to modify them as you want. Your AI agent claim doesn't make any sense either. When upgrading normally your component just gets rewritten on disk. When switching from radix to base ui, a more comprehensive approach is needed.

2. now there is an upgrade ai agent for something that should just be ticking up a version number. If a component as basic as a button or a list view ever requires an “upgrade”, something is fundamentally wrong to begin with. HTML5, ARIA, etc. aren’t cutting edge technologies that the ecosystem still needs time to figure out. This should be pull once and forget.

3. I’m leaning towards vendoring for all my new projects. Grabbing an off-the-shelf UI library is easy in the short term, but it’s usually overcomplicated, implements things I won’t ever need, is hard to tweak if/when you want to distinguish your app from the thousand others using the same library, and when you do decide to upgrade it, all your tweaks break in subtle ways. What I think would be the best approach is buil...

4. My main gripe with Shadcn and, well, most UI libraries nowadays, is that they are reinventing the wheel for like a thousandth time. I’m trying out Ark UI on a side project. They do have some genuinely useful components, like tags input: https://ark-ui.com/docs/components/tags-input They have a tabs/“segment group” component with a nice animated active element indicator which would probably be tricky to implement: htt...

5. building your own UI library It's one more thing to maintain, and it's also difficult to push back on things. If you use off the shelf components it's much easier to say to designers and managers that a UX pattern is not available or not valid. You can point to the mature well known community owned UI library you use and make it authoritative. It's harder to do it if you build your own, suddenly each designer and dev...

## 2. If you're a button, you have one job

- HN: https://news.ycombinator.com/item?id=48790689
- External: https://unsung.aresluna.org/if-youre-a-button-you-have-one-job/

### Summary

The post argues that a simple UI control like an image-rotation button has to “do one job” reliably: handle rapid repeated taps without blocking or unpredictably changing state. Testing shows iPhones buffer/remember taps so quick multi-taps reliably result in the expected final rotation, while a Nothing Phone/Android implementation confirms each tap with haptics/sound but ignores taps during an ongoing animation. The author links this to accessibility and “situational disability,” where many people intermittently face conditions that effectively limit their ability to wait or follow animations, such as rotating lots of photos quickly. The takeaway is that interfaces should never force users to wait for animations to finish; alternative solutions include interrupting/accelerating/stopping animations on new input.

#### Top 5 Positive Comments

1. Even in unstable or high latency I like the buffering. I’m thinking of a remote shell, where you want to type a command blindly, and see it appear seconds later, because keys got buffered in the Internet pipes. Without buffering it would feel awful, having to wait a full roundtrip per keystroke

2. We like buffering of keystrokes or gestures when the system is completely reliable, exhibits reasonable latency and low jitter in its latency.

3. In the Google photos app (Pixel 10) there is no animation, the rotation just happens immediately and there's no button press to buffer.

4. This is so true. Sorry you got downvoted.

5. This still exists on modern Androids (thanks God!) Even better: they moved it from developer options to accessibility options, which means that they treat it as a normal use case now What is bad is that it still disables the animations for progress bars (the only place where the animation makes sense)

#### Top 5 Negative Comments

1. Eliminating these animations is indeed a massive win. Overuse of animations is a terrible thing that has made iOS far worse over the years. I long for the days of yore, when the loading screenshot had a chance of being accurate. These days, when loading something like the health app I get a series of three different screens, rather than just landing at the destination it knew o wanted to start at. It is idiocy of the...

2. This is literally the type of thing that caused the THERAC-25 disaster ( https://en.wikipedia.org/wiki/Therac-25 ). Experienced users hitting keys faster than the app could process them, resulting in safety features being inadvertantly bypassed.

3. It shouldn't buffer them like the author describes. It should execute the button’s function immediately when pressed. This might mean to cancel the current animation and jump ahead, or it might mean to speed it up by the appropriate factor so it takes the same amount of time as it does for one button press. Either way is massively preferable to a button that swallows my input.

4. I'm sure it just my personal preference but I hate animations. Most often they do little other than slow an application down i.e. the code of the application could finish the task almost instantaneously but for the sake of appearance, they make it take longer to finish. I would much prefer no animations in applications. If the animation is there to disguise some actual slow response, just let me wait, give me jarring...

5. I used to have a device with a physical button which, when you pressed it, would beep and add 30 seconds to the time. However, sometimes it would beep and not add 30 seconds, and sometimes it would add 30 seconds without beeping, so you always had to squint at the dim display to discover whether it had worked or not. I thought this must be a peculiarly bad design ... but since then I have lost count of the number of...

## 3. Command and Conquer Generals natively ported to macOS, iPhone, iPad using Fable

- HN: https://news.ycombinator.com/item?id=48788283
- External: https://github.com/ammaarreshi/Generals-Mac-iOS-iPad/tree/main

### Summary

The linked repository documents a native port of Command & Conquer: Generals: Zero Hour to Apple platforms (macOS on Apple Silicon, plus iPhone and iPad) including campaign, skirmish, and Generals Challenge. It emphasizes that it uses the real 2003 ARM64 engine with DirectX 8 mapped through DXVK → Vulkan → MoltenVK → Metal—no emulation—and adds RTS-appropriate touch controls. The project builds on EA’s GPLv3 source release via the existing GeneralsX macOS/Linux port, extending it with iOS/iPadOS work and engine fixes, while explicitly not distributing game assets (users must obtain their own Steam copy). The repo also provides build and packaging instructions, an engineering log and porting documentation, and notes known issues like iPad memory/session termination and occasional iOS backgrounding crashes.

#### Top 5 Positive Comments

1. EA released the Generals source under GPL v3, the GeneralsX project got it running on macOS/Linux, and I've taken it the rest of the way: native iOS and iPadOS builds of Zero Hour, plus Apple Silicon macOS. What works (all verified on a real iPad and iPhone): Campaign, Skirmish, and Generals Challenge: full missions, objectives, cutscenes, saves All audio: music, unit voices, EVA announcements, Challenge taunts, brie...

2. This is an actual dream come true

3. IMHO, this is an actual good use of what sounds like a person guiding a model to do a mass conversion. This is quite the understatement. Actually, it's probably the understatement of the year. "Pretty good, not bad, great use case". Dude. Fable fucking did what ?

4. I vibe code myself to sleep and implemented a rewrite of civ1 in Common Lisp. It works well, has all the DOS nostalgia I wanted (uses the same sprites etc.) 10/10 will continue doing this kind of shit.

5. I think the next 10 years or so are going to see a chucklefuck of games reversed thanks to LLMs, which can easily pattern match and operate on contrivedely optimized assembly and output reasonably accurate C/C++ code. I’m one of many right now using Ghidra + LLM workflow. It’s doing the thing it needs to and I’ve helped several communities revive and port their games this way. It is a huge time saver. While I’d perso...

#### Top 5 Negative Comments

1. Title is click bait. This started back in February and looking at commits, Fable did only a small part of the latest commits. 19 commits out of 2000: https://github.com/ammaarreshi/Generals-Mac-iOS-iPad/commits... And maybe it wasn't even Fable, they might have downgraded to Opus. This is the kind of frequent misinformation that makes me skeptical of Anthropic LLM claims. Whenever I compare them to GPT 5.5 on my web...

2. Completely misleading title.

3. no way fable did this. It would have stopped after the words "command and conquer" and nerfed you to opus (while also landing you on some nsa watch list)

4. If they're using the same graphical assets they're violating copyright. Even if it's a reimagining of said assets it's probably still grounds for takedown.

5. Pretty much a clickbait.

## 4. Web-based cryptography is always snake oil

- HN: https://news.ycombinator.com/item?id=48792203
- External: https://www.devever.net/~hl/webcrypto

### Summary

The post argues that “end-to-end encryption” claims made by web-based apps are effectively “snake oil” because the web platform can’t support the necessary threat model. Since the website operator distributes the client-side JavaScript, a service that claims to protect against server/operator malice cannot do so: the operator can always change the client code to bypass confidentiality, making such cryptosystems inherently incoherent/backdoored. The author further claims the main reason companies adopt this kind of crypto is legal “cryptography theatre”—using nominal E2E encryption to claim they can’t comply with warrants or subpoenas—while noting that this shield can be challenged, unwound by law, or circumvented in practice. The piece cites examples like Lavabit and the FBI–Apple case to illustrate that governments may still compel compromises or that reliance on these legal theories is unreliable.

#### Top 5 Positive Comments

1. The discussion on the proposed solution is interesting https://github.com/w3c/ServiceWorker/issues/1680

2. having E2E encryption is a marketing feature, you need it if you want to be competitive in the market, so this is another incentive to add it

3. Before reading this article, I used to believe that IT companies deeply respected users’ human rights, spending millions of dollars to build end‑to‑end encryption. But thanks to this very article, I learned that they were actually saving tens of millions in administrative litigation costs – costs they would otherwise have had to pay every month to respond to wiretap warrants. Some might call this a “cryptographic inn...

4. I think the article raises interesting questions about trust, but I am also doubtful if the definition of the “incoherent cryptosystem” is useful: The article argues that Signal is an incoherent cryptosystem, because they ship the E2E-encrypting Signal client (and could, hence, backdoor it) that should protect me, the user, against their own infrastructure snooping on me. As I understand the definition, we would not...

#### Top 5 Negative Comments

1. This entire article is... Nonsense? It categorically dismisses e2ee, without any supporting evidence whatsoever, other than the notion that a provider might push a update that doesn't encrypt messages anymore. It's on the level of "you can't trust your OS unless you wrote it yourself" -righteous sounding but utterly stupid in practice

2. As a developer, when Facebook says that WhatsApp is end-to-end encrypted, you know that it means "the default client provides encryption, by default" but you know very well that they could selectively turn it off for anyone, at any time and it may be impossible to know that they did this this unless the target was tech savvy and actively monitoring their network packets. Especially on the web, they could just serve a...

3. I never believed that the messages were truly E2E encrypted and I know for sure when WhatsApp retroactively censored a message I sent to a friend a while back, I found that super sus.

4. The entire argument is based on the definition of an “Incoherent cryptosystem”, which is too restrictive to be useful for cases that you want eg. Tor is also developed and distributed by Tor people and it is supposed to protect you against everyone, including the Tor people.

5. technically you could audit your local copy of tor source code, build it, and then never upgrade it. still this wouldn't guarantee that all the other nodes are not compromised

## 5. Apocketlypse

- HN: https://news.ycombinator.com/item?id=48792352
- External: https://0dd.company/galleries/triumph/1.html

### Summary

The article describes a creator’s “Apocketlypse” project cycle, prompted by a shift away from hobby programming as AI enters professional work, alongside nostalgia from Digimon and its grief-filled “digital pet dies” themes. Using the uxn bytecode system, the author builds a tamagotchi/digimon-inspired handheld concept where you raise an apocalypse avatar instead of a pet—feeding it by destroying hospitals, forests, and polluting sources until it evolves and ends humanity. The device includes a small set of forms tied to machine rise, plague and distrust in science, and pollution/poisoned air, each with brief epilogues. The author notes that development was the most enjoyable “computer time” in a while, highlighting the mental discipline of byte-by-byte programming, and shares plans to release the uxn source code and ROM (with advice to use a larger-scale uxn setup).

#### Top 5 Positive Comments

1. Looks super sweet! Reminds me a good bit of Plague Inc (wrt the "destroy humanity") aspect. ...And now I want an m5 stack too haha. Looks super cute.

#### Top 5 Negative Comments

_No comments available._

## 6. Pandoc Lua Filters

- HN: https://news.ycombinator.com/item?id=48773079
- External: https://pandoc.org/lua-filters.html

### Summary

Pandoc Lua Filters explains how pandoc filters can modify the document AST between parsing and writing. It contrasts traditional JSON-based filters (passed via stdin/stdout and requiring external interpreters/libraries) with pandoc 2.0+ Lua filters that run in an embedded Lua 5.4 environment and marshal AST data directly, avoiding JSON pipe overhead and environment issues. The page shows a simple filter that replaces Strong emphasis with SmallCaps, then documents the Lua filter structure (tables keyed by element types), how return values can replace, splice, or delete elements, and how traversal can be customized via typewise vs topdown walking. It also covers special list filters (Inlines and Blocks), traversal order rules, how pandoc provides useful global variables (e.g., FORMAT, PANDOC_VERSION) to filters, and the built-in pandoc Lua module for creating and manipulating AST elements.

#### Top 5 Positive Comments

1. I've always wondered if pandoc can be made reactive. Say markdown to Pandoc AST. If one changes something, a quick update to the AST would happen incrementally. Now with all these llm I might actually see if it can be done.

#### Top 5 Negative Comments

1. Is there anyone feeling that Pandoc is ever increasingly bloated? I have used Lua filters a decade ago [1] and the current documentation is nothing like my memories. I'm not even sure that how much of Lua scripts remain compatible across different Pandoc versions. [1] https://github.com/mearie/mearie.github.io/blob/source/res/w...

## 7. GPT-5.5 Codex reasoning-token clustering may be leading to degraded performance

- HN: https://news.ycombinator.com/item?id=48789428
- External: https://github.com/openai/codex/issues/30364

### Summary

The post reports an aggregate telemetry anomaly in OpenAI Codex: for the GPT-5.5 model, responses disproportionately end with exactly `reasoning_output_tokens = 516`, with additional spikes at fixed boundaries around `1034` and `1552`. The effect appears model-specific (GPT-5.5 accounts for 82% of exact-516 events despite only 19.3% of all responses) and coincides with a period (May–June 2026) where overall reasoning-token intensity drops sharply while exact-516 clustering rises. The author links this to a prior issue (#29353) where runs ending at exactly 516 reasoning tokens sometimes returned wrong answers, but they caution they are not proving hidden chain-of-thought truncation—only that telemetry suggests thresholded “reasoning-budget” behavior. They ask the Codex team to investigate internal causes (budget caps, routing/truncation/fallback/scheduler) and proposes validation queries and task replays comparing GPT-5.5 to other Codex models.

#### Top 5 Positive Comments

1. I love that Codex is open source and issues like these can surface/be addressed publicly.

2. But in that case you have nobody but yourself to blame, and you can stabilize things yourself at any time by refraining from making any changes. You won't be surprised by a provider. Honestly? That's not just valuable—it's essential.

3. Verified this locally myself. Thanks for the concrete test. I guess it's time to give Claude another try.

4. It’s not just you this is also my opinion, 5.3-codex was a fantastic model in terms of balancing output quality and cost. Cheap and efficient enough I could afford to use it on basically everything unlike 5.5 or Opus, but still pretty good, I preferred it to sonnet

5. If this really is widespread and degrading performance in 40% of the cases, then if OpenAI simultaneously fixes this bug and releases GPT 5.6 within a day or two, then the sudden boost in capability is going to blow people's hair back.

#### Top 5 Negative Comments

1. I’ve definitely experienced step jumps down in quality on an almost daily basis. I usually used xhigh. The experience of relying on codex’s outstandingly thorough coding earlier in the year has evaporated for me. I’m seeing incredibly stupid implementations intermittently, and have simply switched to Claude until openai takes the issue seriously. As far as i could tell they haven’t taken it seriously for the several...

2. this explains so much why gpt 5.5 has been so bad lately it was really puzzling why it struggled so much where when it first came out it was one shotting stuff totally amazing, i tried the prompt that will tell you if your plan is degraded: codex exec --json --skip-git-repo-check --ephemeral -s read-only --disable memories -m gpt-5.5 -c model_reasoning_effort=high "Do not use external tools. A black bag contains cand...

3. The good experience I had with GPT-5.5 before made me upgrade to Pro this month. Now I want a refund.

4. Oh this seems bad, and is fairly easy to reproduce using codex cli. You give it a puzzle prompt that it has to reason about and solve, occasionally it will seemingly short circuit and think for exactly 516 tokens, and return the wrong result. When it ends up using 6000-8000 thinking tokens it returns the correct result. Maybe some issue with adaptive thinking? Another point for local models I guess, don't have to wor...

5. i don't ever believe these issues are technical. They're business decisions to downgrade performance because to fix it means $$$$ and you arn't paying them enough.

## 8. Programmers need to start meditating now

- HN: https://news.ycombinator.com/item?id=48792080
- External: https://jacob.gold/posts/programmers-need-to-start-meditating-now/

### Summary

The post argues that programming used to naturally provide a “meditative” focus: deep flow that quiets the brain’s default mode network, reducing rumination and worry. The author claims that with modern work patterns dominated by context switching, they’ve spent far less time in flow and feel that programming no longer fulfills that calming function. They suggest programmers compensate by adopting another calming practice—e.g., deliberate meditation using apps like Calm or Waking Up—so the mind still gets a regular settling.

#### Top 5 Positive Comments

1. Meditation - «getting used to» A most elementary form of meditation, is getting used to placing your attention on a sensation and keeping it anchored there - even when other sensations or thoughts arise. Following the breath- place your awareness, your attention, on the sensation of air passing through your nostrils. Count one inbreath and outbreath cycle as «1», and count until 10 or 21. Decide before you start, how...

2. Thank you. I like the comparison of "meditation" with "sport": it is not all the same, even if there are commonalities between some disciplines. It is rare to see laypeople discuss some of the different types and which one may be best suited for a particular goal. If the goal is simply relieving stress, performing some sport outdoors —especially team sports— is probably more effective than any meditation, for most pe...

3. My favorite metaphor for programming is playing chess. Your opponent in programming is the complexity, you don't see its moves before the coding and design progress, before you make your choices/moves. You solve a problem by writing some code but that causes new problems down the line you didn't know existed before you made your choice of writing some specific code. or choosing a specific design. Chess-players too ar...

4. I noticed how relaxing and meditative programming can be. It might sound that after day job basically solving other people pronlems I sit down late at noght to just write code for hours on end. But I really enjoy it. Using LLM’s to generate the code ruins it. I have also done meditation, but I struggle to keep it up for long. I think you should really do it consistently to get majority of effects. Coding, exercising,...

5. I’m clearly much more productive now. I’m doing five things at once very effectively, switching between multiple agent sessions from morning to night. Joel Spolsky disagrees here: https://www.joelonsoftware.com/2001/02/12/human-task-switche...

#### Top 5 Negative Comments

1. I have certainly noticed my stress skyrocket in this new mode of working. I was used to getting a lot done very quickly, with intense pockets of work followed downtime. Now it feels more like a steady stream of medium stress, and there is no opportunity to stop or drop the thread. I must admit, if this is the new way of doing software development (eg: not actually programming but working with LLMs) I am not going to...

2. Yeah, same thoughts. And this industry is becoming so volatile, I'm not sure what will happen tomorrow. I mean it's highly unlikely that AI will replace developers at least in the next 10 years, but I'm not sure what will "software developer" become. Certain people love to work with details. If AI is taking away this joy, I'll rather retire as early as possible from this volatile industry.

3. “I’m doing five things at once very effectively” …sure you are buddy, sure you are… Note to self: book appointment with Optometrist ASAP to correct how far my eyes have rolled back into my head.

## 9. Megawatts by Microwave

- HN: https://news.ycombinator.com/item?id=48791591
- External: https://computer.rip/2026-07-04-microwave-and-power.html

### Summary

The article traces how U.S. federal agencies pursued major dam projects on the Columbia River—initially for irrigation, metals, navigation changes, and national defense, but increasingly for large-scale hydropower during the Great Depression. It explains the institutional rivalry between the Army Corps of Engineers and the Bureau of Reclamation, culminating in the Bonneville and Grand Coulee dams, and the resulting politics over whether government should publicly market the electricity. The Bonneville Power Administration (BPA) then built an integrated “Master Grid” transmission network across multiple states, pioneering regional grid concepts and high-voltage technologies. Because rural substations were spread out and fault response was hard, the post shifts to how the BPA also developed long-distance communications for power control—using carrier-current telephone systems, radio/telephony options, and selective calling to coordinate remote switching and monitoring.

#### Top 5 Positive Comments

1. history lesson about power transmission lines in the us

#### Top 5 Negative Comments

_No comments available._

## 10. Jellyfish can heal wounds in minutes. Scientists want their secrets

- HN: https://news.ycombinator.com/item?id=48789712
- External: https://www.mbl.edu/news/jellyfish-can-heal-wounds-minutes-scientists-want-their-secrets

### Summary

Researchers at the Marine Biological Laboratory have studied how jellyfish (Clytia hemisphaerica) heal epithelial wounds extremely fast—small injuries close within minutes, without scarring and with “embryonic-like” repair. Because the jellyfish medusae are transparent and lack an immune system that would obscure the process, scientists can watch epithelial cells stitch and migrate in real time, and they find many wound-healing mechanisms conserved with other animals, including mammals. In a new paper, Jocelyn Malamy shows that Clytia epithelial healing is coordinated by two key sequential structures: lamellipodia that “walk” across the basement membrane to cover the wound, and an actomyosin cable that contracts to help close wounds and deal with basement membrane damage or debris. She now plans to investigate how Clytia repairs the basement membrane itself, an area still poorly understood across species.

#### Top 5 Positive Comments

1. Hell, any research lab would implore you to make such challenge. Imagine all the things we'd missed out on if we always acted towards some certain goal(s), probably half the stuff we have today wouldn't have been invented (yet?).

2. The medusa, the free-swimming form most people picture when they hear the term jellyfish, is only one stage of the animal’s life cycle. We tend to think of the flower—or the jellyfish—as the organism, but these are actually reproductive units. I'll never look at jellyfish the same.

3. True jellyfish (like moon jellies, box jellyfish)are a single organism, just like you or me. Theres a single genome and one body. Portuguese man o’ war is not a single organism at all but a siphonophore, a colony of many genetically identical but specialized individual organisms called zooids, all fused together and functionally dependent on each other.

4. My memories of being a 6-7 years old, throwing blue jellyfish on each other in "jelly wars" with other kids just suddenly turned into a traumatic memory instead. Fun fact; where I grew up, we only had (at the time at least) two different types of jellyfish in the sea, blue and red ones. Easy to tell apart, one is "good", one is bad. However, now living in a very different place, suddenly what I learnt as a child is n...

5. Clytia is not just your normal jellyfish, is an organism that alternates between a jellyfish and a polyp that live in small colonies, not unlike corals but less complex and without hard calcified skeletons. Is also in the same group that has the only animals known to be potentially immortal. I'm not joking. This things exist. So the word "heal" here can mean different things than people expects. Imagine that as we gr...

#### Top 5 Negative Comments

1. Agreed. I always hated the 'two part', 'payoff'-based drama of titles like these, even before the LLM era. If it was lazy before (it was), it now comes off as 'one-click' lazy. Sadly, The Guardian has become infested with this style lately.

2. The title seems like clickbait for a super medical cream.

3. Healing their own wounds, not ours.

4. They're not even technically one organism, but colonies of independent but mostly specialized organisms. I'd be willing to bet that has something to do with the articles title

5. This is a press release from a marine research organization, so the main implication here isn't that they're doing it because it's in any way relevant to humans. They're doing it because it's a cool thing for a marine research organization to research. Yes, it's probably not gonna help humans, unless some of your friends are gelatinous blobs with no circulatory or nervous system and with a lifespan measured in months...
