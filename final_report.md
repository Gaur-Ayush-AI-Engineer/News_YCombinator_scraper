# Hacker News Final Output

## 1. Shadcn/UI now defaults to Base UI instead of Radix

- HN: https://news.ycombinator.com/item?id=48791328
- External: https://ui.shadcn.com/docs/changelog

### Summary

shadcn/ui is updating its defaults: Base UI will be the starting component library instead of Radix. The post explains that Radix powers shadcn/ui since its 2023 launch, but Base UI has reached stability (v1.6.0, millions of weekly downloads) and is now the chosen default for new projects, docs, and shadcn/create scaffolding. Radix is not deprecated—both libraries will continue to receive updates and new components, and existing apps don’t need migration unless a user explicitly wants to switch. For those who choose to migrate, shadcn offers a “skill” for incremental, component-by-component migration with reports in .migration and clean git history, avoiding fragile codemods by understanding project-specific customizations.

#### Top 5 Positive Comments

1. Great news. I've found that no UI library comes close to shadcn's quality. It even looks incredible when building desktop apps. We used it to build DB Pro [1] and the DB Pro website, and everyone compliments us on our design. I see it becoming the defacto choice for UIs especially when building with agents. [1] https://dbpro.app

2. Ticking up a version number is all fine and good until it requires a dependency upgrade you aren’t ready for. If for example you wanted to upgrade MUI from 4 to 5, you’d find react 17 wasn’t supported. And if you weren’t ready or able to upgrade react, then you’d just be stuck using a UI library going more out of date by the day. With shadcn / the copy paste format, you’ll almost never see that happen. The button sha...

3. Love love love mantine.

4. Oh, I know exactly what you mean. I use plannotator with claude a lot and have much better time, since I asked for a specific styleguide. I used "CD era MSDN reference and Raymond Chen blogging style" as a starting prompt for the styleguide and my work ability to digest AI plans raised a lot. Couldn't recommend it more. Humble, insightful and respecting the reader

5. Correct. Nothing else comes close.

#### Top 5 Negative Comments

1. Because it means that they think I'm stupid. They think it's not worth investing human attention to write it, so why am I expected to invest my attention to read it? If it's written as SEO spam, why link it here? If it's written to be read by humans, do they think we're stupid?

2. Martine just straight up sucks. Vendoring your components gives you the best of both worlds. You get a full component library but retain the ability to modify them as you want. Your AI agent claim doesn't make any sense either. When upgrading normally your component just gets rewritten on disk. When switching from radix to base ui, a more comprehensive approach is needed.

3. now there is an upgrade ai agent for something that should just be ticking up a version number. If a component as basic as a button or a list view ever requires an “upgrade”, something is fundamentally wrong to begin with. HTML5, ARIA, etc. aren’t cutting edge technologies that the ecosystem still needs time to figure out. This should be pull once and forget.

4. I'm not a shadcn user, and so as with any project I'm not familiar with, I'm looking to see if if it's interesting to me. If the post is thoughtful and clear and I like the sense I get of their perspective on programming, then great, tell me more. No guarantees but maybe the writer is someone whose software I'd like to use. Claude doesn't tell me anything except that the writer used Claude. It's the same as with too...

5. Imagine building a brand new component library to replace your already quite successful component library and still making it React-only.

## 2. If you're a button, you have one job

- HN: https://news.ycombinator.com/item?id=48790689
- External: https://unsung.aresluna.org/if-youre-a-button-you-have-one-job/

### Summary

The post uses a simple “rotate image” UI to argue that button-like controls have one job: act reliably no matter how quickly users tap. On iPhone, rapid repeated taps are buffered so the final result returns to the starting orientation (a no-op), while on Nothing Phone/Android the device gives haptic/audio feedback and then ignores taps if an earlier rotation animation is still running. The author connects this to accessibility and “situational disability,” noting that many people temporarily find themselves effectively disabled in fast or inconvenient interaction scenarios (e.g., rotating lots of photos). The takeaway is a design rule: don’t block or force users to wait for animations to finish; instead buffer, interrupt, or accelerate/stoppage the animation so input is always honored.

#### Top 5 Positive Comments

1. It shouldn't buffer them like the author describes. It should execute the button’s function immediately when pressed. This might mean to cancel the current animation and jump ahead, or it might mean to speed it up by the appropriate factor so it takes the same amount of time as it does for one button press. Either way is massively preferable to a button that swallows my input.

2. It shouldn't buffer them like the author describes. It should execute the button’s function immediately when pressed. This might mean to cancel the current animation and jump ahead, or it might mean to speed it up by the appropriate factor so it takes the same amount of time as it does for one button press. Either way is massively preferable to a button that swallows my input.

3. The color change of the button shows you succeeded in pushing it. If you don't do this instantly most people are conditioned to try again. This is especially valuable for people with reduced motor control. It is completely independent of whether that push is a useful input given the current state of the software. Obviously when well written software knows it can't accept the input it should have disabled the button,...

4. Even in unstable or high latency I like the buffering. I’m thinking of a remote shell, where you want to type a command blindly, and see it appear seconds later, because keys got buffered in the Internet pipes. Without buffering it would feel awful, having to wait a full roundtrip per keystroke

5. I totally agree, even not going as far as a Parkinson case, if you already so old and not too old persons use phones and touch screens, you will see that very often it is complicated for them to click on the small button at the right place and to have the feeling that "they have clicked". So, for me, on the argument of about accessibility, the Nothing Phone behavior will work a lot better I think. In their mind they...

#### Top 5 Negative Comments

1. Eliminating these animations is indeed a massive win. Overuse of animations is a terrible thing that has made iOS far worse over the years. I long for the days of yore, when the loading screenshot had a chance of being accurate. These days, when loading something like the health app I get a series of three different screens, rather than just landing at the destination it knew o wanted to start at. It is idiocy of the...

2. I'm sure it just my personal preference but I hate animations. Most often they do little other than slow an application down i.e. the code of the application could finish the task almost instantaneously but for the sake of appearance, they make it take longer to finish. I would much prefer no animations in applications. If the animation is there to disguise some actual slow response, just let me wait, give me jarring...

3. This is literally the type of thing that caused the THERAC-25 disaster ( https://en.wikipedia.org/wiki/Therac-25 ). Experienced users hitting keys faster than the app could process them, resulting in safety features being inadvertantly bypassed.

4. People often forget that animations serve purely a supportive role and do not exist for the purpose of having animations. They are there to mask loading times and ease from one state into the other. That's why we have them. This knowledge eventually got lost (figuratively speaking) and now we have code that needs to wait on the animation to finish. Another amazing example of cargo culting.

5. Bad programming. People who have experience with embedded programming knows that reading out a button usually means denouncing. At the speed a microcontroller can read out a button it will change it's state multiple times per press because of contact bounce. Meaning when a user presses a button the program sees off, on, off, off, on, on, off, on, on, on, on, on, on, etc. Now if you just naively read out the current s...

## 3. Show HN: KiCad in the Browser

- HN: https://news.ycombinator.com/item?id=48793542
- External: https://demo.pcbjam.com/

### Summary

The post introduces an early-access alpha of PCBJam, which runs KiCad in the browser. Users can open example PCB designs or load their own KiCad projects directly in the demo. It requires no installation and does not upload files to a server. The linked page focuses on trying KiCad functionality interactively through the web demo.

#### Top 5 Positive Comments

1. Happy to answer any questions & feel free to reach out ( email in my profile )!

2. I like all the utility you have already built in. My selfish suggestion would be to add support to populate the part numbers for all the components from LCSC's database. JLCPCB wants these numbers in order to assemble a PCB. (Currently I use a JLCPCB plug-in to do this in KiCAD.)

3. thanks! one thing we did not port is the plugin system: it's quite hard to run python on the web ( AFAIK pyodide is not enough here ) and I've heard that it will be deprecated in the next version. The KiCad editor's state is accessible from the web app, we'll do some kind of plugin system like Figma's or just implement these functions as an overlay. We'll see, thanks for the tip!

#### Top 5 Negative Comments

_No comments available._

## 4. Claude Design System Prompt

- HN: https://news.ycombinator.com/item?id=48792399
- External: https://github.com/Trystan-SA/claude-design-system-prompt

### Summary

The GitHub project “Claude Design System Prompt” provides an open-source, MIT-licensed system prompt and 14-skill library derived from Anthropic’s Claude Design approach. It’s meant to turn an LLM into an opinionated, accessibility-aware, “AI-slop”-resistant design collaborator by rejecting generic SaaS-template aesthetics and enforcing principles like content discipline, visual hierarchy/rhythm, typography/color systems, and WCAG-friendly interaction patterns. The repository includes structured procedures for discovery, wireframing, prototype/deck generation, design-system extraction (tokens/components), and multiple review passes (accessibility, AI-trope detection, hierarchy, interaction states, and final polish), with skills designed to chain in typical workflows. It also offers variants for Claude and OpenAI Codex and includes guidance for calibrating prompt behavior to different model tendencies.

#### Top 5 Positive Comments

1. I've been using Claude Design to make animated SVGs, and I've learned a thing or two about its limits and how to get around them. One thing I've learned is that you have to ask it to first come up with a robust way to define the geometry and then apply that to an SVG. Without that first step, it just guesses at where everything should be that isn't directly connected with a node, and it is hilariously bad. But with t...

2. This is pretty awesome. I’ve wanted to use Claude design, but with my regular MCP servers. Side note: ironic use of an llm writing the readme.

3. They have never attempted to hide their system prompts in fact they explicitly publish them for Claude ( https://platform.claude.com/docs/en/release-notes/system-pro... ) and Claude Code they provide a proxy option which then makes it trivial to see the full requests and responses including the prompts and tool usage...

4. I trust on this: https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPI... It’s different than this one shared by the op, but Anthropic maybe updated the prompt

5. honestly, i think you can just look at the network tab and see the "content" of the skills. Same has been true for their excel addin and bunch of other things.

#### Top 5 Negative Comments

1. I'm calling BS, sorry. It looks light, and barely anything beyond surface level of what we could all could guess would be in a system prompt. This smells nothing more of a "claude give a system prompt that anthropic would use as a system prompt for claude" From what we know, there are some very specific details baked into the prompt as safety guards, where are those? Again calling BS and I'm not gonna waste more thou...

2. If this is regular output of the LLM, I'm not sure, but given that the author proclaims that this is reverse engineered, then they are not allowed to redistribute it under their own license terms. The terms of service are also pretty clear on this not being allowed, which makes it extra hard to defend (section 3.3): You may not access or use, or help another person to access or use, our Services in the following ways...

3. If you ask Claude Design itself to list the names of the skills available to it you get: Animated video Interactive prototype Make a deck Make a doc Make tweakable Claude API in prototypes Frontend design Wireframe Export as PPTX (editable) Export as PPTX (screenshots) Create design system Save as PDF Save as standalone HTML Send to Canva Handoff to Claude Code Which does not match the structure of this project at al...

4. This would be much more interesting if it detailed how the prompt/skills were reverse-engineered. As it is it seems like this could just be the output from “hey Claude write me a system prompt that works like Claude Design”.

5. Open source, MIT licensed. I don't think that is how copyright licensing works.

## 5. Introduction to Compilers and Language Design

- HN: https://news.ycombinator.com/item?id=48793454
- External: https://dthain.github.io/books/compiler/

### Summary

This page introduces a free, online compiler-construction textbook developed by Prof. Douglas Thain for a University of Notre Dame compilers class. It explains what compilers do and frames the book as a one-semester guide to building a simple compiler for a C-like language that generates working X86 or ARM assembly. The author provides downloadable chapter PDFs (with personal/academic use permitted) and discourages offline copying by directing readers to the main page for the latest version. It also links to a GitHub repository of code resources (scanners/parsers, project starter code, and test cases) and includes an errata process for reporting typos and mistakes.

#### Top 5 Positive Comments

_No comments available._

#### Top 5 Negative Comments

_No comments available._

## 6. Trust your compiler: Modern C++

- HN: https://news.ycombinator.com/item?id=48746933
- External: https://categorica.io/blog/2026.06.29_trust_your_compiler/

### Summary

The post argues that many long-standing “performance wisdom” in C++ is outdated because modern CPUs and optimizing compilers already recognize and optimize common patterns. It walks through examples—like Quake III’s fast inverse square root trick, bit-twiddling/popcount, matrix row-pointer indirection, and using const& reflexively—showing that “obvious” modern C++ often performs as well or better while producing clearer code and more reliable optimization. Benchmarks with Clang/GCC at high optimization levels suggest that clever, intent-obscuring tricks can even hinder vectorization/inlining or rely on assumptions (e.g., for floating-point fast-math). The overall takeaway is to trust the compiler and express intent using modern language/library features (e.g., std::popcount, contiguous layouts, and correct passing/forwarding semantics).

#### Top 5 Positive Comments

_No comments available._

#### Top 5 Negative Comments

1. Are you a fool? Another name for compilers: invisible backdoor injectors. The more complex is the syntax the more it is likely to happen... I let you guess how the "sane" syntax from c++ and similar (LOL) does fit here...

2. I’ve seen some terrible horrid nonsense from them and even the best compilers don’t use a third of the opcodes our modern CPUs boast of. Nobody understands the big compilers any more either, they’re all too huge. And soon AI will be “improving” hem too. You want to see a beautiful compiler? Look at Plan 9’s compiler suite. A man could understand and even build on that.

3. Trust the compiler - sure - but we can't change the whole program by using -ffast-math, unfortunately, so that particular one is out.

4. Virtual vs static polymorphism std::visit over std::variant<A, B, C> is lowered to a switch over the active alternative. In this case, layout is probably doing more work than the dispatch mechanism itself. Very likely because last time I checked visit lowers to a virtual call.

5. I really dislike the complexity of modern C++ language specs, but does it obscure much detail about FP ops? TL;DR: A vast majority of the programmers I've worked with don't understand the nuances of FP in general , nor the various extents of IEEE-754 support in different programming languages. So for important numerical programming, I think clarity regarding the FP operations being performed can be crucial. I'm just...

## 7. Fast Software, the Best Software (2019)

- HN: https://news.ycombinator.com/item?id=48792008
- External: https://craigmod.com/essays/fast_software/

### Summary

The essay argues that software speed—both in responsiveness and in interface “lightness”—is a crucial but often undervalued marker of engineering quality and overall usability. Using personal examples like nvALT (instant startup and search-driven flow), the author connects fast interaction to trust, reduced friction, and maintaining creative “flow” rather than breaking it with lag. They contrast this with slower or increasingly “bloated” software over time (e.g., parts of Adobe’s Lightroom/Photoshop, and Google Maps’ gradual accumulation of sluggish animations and UI complexity), claiming that slowness can signal deeper engineering problems and erode confidence. The piece concludes that the best software inches toward the physical directness of tools like typewriters, and that speed shows up not only in performance metrics but in intuitiveness and even the clarity of microcopy and UI behavior.

#### Top 5 Positive Comments

1. I fully agree. I loathe slow software. I hate bloat. I love fast software. As a developer, I'm completely, even irrationally, obsessed with speed, performance optimization, and profiling. I wish more developers felt the same way.

2. I run headless Alpine Linux (a minimal distro) in my homelab and it’s fast AF. The lag in Windows Explorer is sad when something like cd folder/folder is instant in Linux.

3. Google Maps has gotten so slow When it comes to navigating (except public transit), hiking, and route building, Organic Maps[1] is very good. OSM data and offline-first is the way forward for detailed and _fast_ map experience. For cycling route building I have to mention BRouter[2], which allows you to write a custom cost function that is used to tweak your route preferences. [1]: https://organicmaps.app/ [2]: https...

4. Simple tasks being barely fast enough alone is not fast enough, as they could unexpectedly slow down to a halt if you run a moderately heavy load alongside them. Speed enables more features and also simpler architectures and algorithms, since you can rely more on brute force in higher-level code.

5. There are dozens of us! Dozens!

#### Top 5 Negative Comments

1. I really don't understand how you can even create software that feels as bad to use as Windows Explorer. It's like it's barely attached to reality. There's this weird floaty delay in everything. You copy a file, or did you? You're not sure. It hasn't updated yet. Oh, now the copy dialog appears with this progress bar that isn't showing progress. The dialog just sits there. Is something happening? I don't know. Many s...

2. Faster at doing nothing?

3. Fast and efficient software varies depending on the local context, but for me, I think I'd be fine with something slower as long as it's convenient enough. After all, once it passes a certain threshold, I can barely even notice the speed difference anyway. I wonder what OP's thinks of IDEs like VSCode. Would they see it as heavy and not great because it's Electron-based? But I find IDEs convenient.

4. Honestly, I'm in partially disagree camp. What matters is how much time it saves. A good WYSIWYG editor will run circles around the fastest text editor. Even if WYSIWYG is a bit slower to open. It would be preferable for software to be more focused and faster over time, but that doesn't attract people to it.

5. No way I wanna chat with my oven

## 8. Pandoc Lua Filters

- HN: https://news.ycombinator.com/item?id=48773079
- External: https://pandoc.org/lua-filters.html

### Summary

The post introduces pandoc’s Lua filter system, which lets you modify Pandoc’s AST between parsing and writing. It contrasts Lua filters with “traditional” JSON-based filters, noting that Lua avoids stdin/stdout JSON marshaling overhead and doesn’t depend on external interpreters or AST-manipulation libraries—Lua 5.4 and the pandoc filter library are embedded in Pandoc starting with v2.0. It explains how to write and run filters (saving a Lua file and using `--lua-filter`), the expected return values for element handlers, and how Pandoc traverses the document (typewise by default, with options like topdown). The article also covers advanced features like filtering on ordered sequences of inlines/blocks, controlling traversal order/early exit, access to global context variables (FORMAT, version info, etc.), and the `pandoc` Lua module for creating AST elements and using helper functions (walk, read, pipe, mediabag, utilities).

#### Top 5 Positive Comments

1. We use it for seven years and it still runs fine when we update Pandoc - we usually always update things. I don’t remember anything about the docs, so not sure what changed.

2. I've always wondered if pandoc can be made reactive. Say markdown to Pandoc AST. If one changes something, a quick update to the AST would happen incrementally. Now with all these llm I might actually see if it can be done.

3. With a tagline of "a universal document converter" it is almost a guarantee to become a complicated program but how much of it is being used for any single conversion? Two more examples: Rclone is "bloated" but it needs to be in order to fulfill its purpose. ZFS is "bloated" because it combines volumes and filesystems but breaking the Unix philosophy also enables a different kind of synergy and simplicity elsewhere.

#### Top 5 Negative Comments

1. A universal document converter is expected to expand via adding support for additional formats---that's okay (same for your other examples). I'm much more worried about the widening scope of the project.

2. Is there anyone feeling that Pandoc is ever increasingly bloated? I have used Lua filters a decade ago [1] and the current documentation is nothing like my memories. I'm not even sure that how much of Lua scripts remain compatible across different Pandoc versions. [1] https://github.com/mearie/mearie.github.io/blob/source/res/w...

## 9. Knowledge Should Not Be Gated

- HN: https://news.ycombinator.com/item?id=48792195
- External: https://www.formaly.io/blog/knowledge-should-not-be-gated

### Summary

The post argues that recent AI “knowledge” approaches (chunking documents, embeddings, vector databases, RAG/graph-RAG, and SDK pipelines) often make a company’s knowledge unreadable and effectively locked behind tooling, forcing every team to rebuild the same context-assembly machinery. Instead, it claims the simplest, scalable pattern is to keep knowledge in plain Markdown files (like AGENTS.md/CLAUDE.md and wiki-style linked notes) so models can read and update it directly, avoiding repeated retrieval and “format walls.” It highlights Google Cloud’s Open Knowledge Format (OKF) as a vendor-neutral standard that formalizes this LLM-wiki approach into portable bundles of Markdown concepts with minimal YAML frontmatter and normal links. The takeaway is that boring, interoperable file-based formats—not complex databases or SDK gating—are what make knowledge flow across humans, tools, and agents.

#### Top 5 Positive Comments

1. Information wants to be free! I remember when that was the rallying cry of hackers. I miss those days.

2. Most corporations likely have zero data retention agreements with LLM providers, at least for API usage. (Sure, you could be sceptical on whether the LLM provider is upholding that, but I personally do trust them. The trust betrayal if ZDR wasn't actually ZDR would be too great and commercially damaging for them to lie.)

3. because corporations are using providers with ZDR in the contract. If OAI or any of the cloud providers violate this they're getting sued to oblivion.

4. Secifically in Google AI Overview I always see links to sites where the information is sourced from. Or at least some of the sites, if the same info is sourced from 100 pages then it only shows 2 or 3, maybe the ones with the biggest PageRanks.

5. now that any software/knowledge is copyable given sufficient cash and AIs, gating knowledge migth be the only thing that protects your business. otherwise you do not have business.

#### Top 5 Negative Comments

1. The problem is that there is an enormous, nearly unignorable incentive to work around it. So they will. As the customer base becomes more and more corporate (which it will), they end up with disproportionately more customers whose experiences cannot be used to train the model to make it better for those customers. Either way, corporate customers cannot leach off the training from consumers handing over their personal...

2. Sdks/libs, especially open source sdks, were never about gated knowledge. They were about the providing company making it as easy as possible for you to integrate. You would not need to know the idiosyncrasies behind api retries, paging, rate limits, auth flow, and on and on. The third party developers needed a resource, they call a method and get it. Open source libraries especially are about pooling knowledge, not...

3. Yep, that’s true But those links are Googled after the model started to answer, they are not the links to the training data Imagine an artificial “librarian” that read all the books and spits hallucinated quotes for you But doesn’t let you enter the library, open a single book or even see the sources for those hallucinated quotes But instead Googles some sources based on hallucinations after generating them ;-) It’s...

4. It seems beyond naive, rather malicious, to upload any useful private data to SaaS LLMs. Like, you are letting them data mine your business. Why are corporations not panicing over this?

5. Yep, knowledge should not be gated: Imagine Google search without any links or sources named This is the “modern” AI chatbot: It never mentions the training data it used, in fact has no idea what it used (often FB, Reddit and partisan websites) Update: I added the reply about after the fact Googling chatbots do - it’s different

## 10. Jellyfish can heal wounds in minutes. Scientists want their secrets

- HN: https://news.ycombinator.com/item?id=48789712
- External: https://www.mbl.edu/news/jellyfish-can-heal-wounds-minutes-scientists-want-their-secrets

### Summary

A researcher at the Marine Biological Laboratory, Jocelyn Malamy, describes how the jellyfish species Clytia hemisphaerica can close wounds extremely fast—small ones within minutes and larger ones within an hour—without forming scar tissue. Because Clytia medusae are transparent and lack an immune-system inflammatory response, scientists can directly observe epithelial cells “stitching” and migrating to repair damage in real time, and many of the underlying mechanisms appear conserved with other animals, including mammals. In a new paper, Malamy argues that Clytia epithelial wound healing is driven by two coordinated actin-based structures in sequence: lamellipodia that crawl across the basement membrane, followed by an actomyosin cable that contracts and helps pull cells over basement-membrane damage and expel debris. She also proposes that when wounds are too large for individual cell edges to meet, the entire epithelial sheet lifts and migrates collectively, then closes. The next research goal is to understand how the basement membrane itself is repaired, a process still unclear in any system.

#### Top 5 Positive Comments

1. The article is pretty explicit that the interesting part is that some of the underlying epithelial repair mechanisms appear to be conserved across animals, including mammals

2. What I like about this work is that the jellyfish may be less important as a source of some magical "regeneration gene" and more useful as a system where you can actually see the basic mechanics clearly

3. Hell, any research lab would implore you to make such challenge. Imagine all the things we'd missed out on if we always acted towards some certain goal(s), probably half the stuff we have today wouldn't have been invented (yet?).

4. Simpler tissue makes it easier to see the core mechanics without blood vessels, inflammation and a lot of other processes happening at the same time

5. The medusa, the free-swimming form most people picture when they hear the term jellyfish, is only one stage of the animal’s life cycle. We tend to think of the flower—or the jellyfish—as the organism, but these are actually reproductive units. I'll never look at jellyfish the same.

#### Top 5 Negative Comments

1. Agreed. I always hated the 'two part', 'payoff'-based drama of titles like these, even before the LLM era. If it was lazy before (it was), it now comes off as 'one-click' lazy. Sadly, The Guardian has become infested with this style lately.

2. Doctors hate them.

3. The title seems like clickbait for a super medical cream.

4. Novo Nordisk might challenge the idea that application follows directly from research objectives

5. 9 out of 10 doctors…
