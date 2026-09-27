# Script — "The unit is a token, not a word"

**Course:** INFO 7375 · Week 1 · **Concept source:** `chapters/01-randomness-and-first-prompts.md` §"One question, asked over and over"
**Target runtime:** ~3:25 (assignment window 2–4 min)
**Narration:** Kokoro `af_bella`, local, synthetic — disclosed on screen and in SOURCES.md
**Revision 2** — rewritten after the real Claude response came back **correct**.

Every number spoken comes from `evidence/*.txt`, raw stdout of the scripts beside them.

> **Framing note.** Rev 1 assumed the model would fail. It did not. The claim
> "a language model cannot do it" was cut as overstated. The video now asks the
> harder and more honest question: it got it right — using what?

---

## B00 — Cold open: the question (~13s)

> How many r's are in the word strawberry?
> Three. And you got that by looking at the letters, one at a time, until you ran out.
> Hold on to that, because the machine cannot do the thing you just did.

**Visual:** `strawberry` large; the three r's illuminate one at a time; counter 1, 2, 3.

---

## B01 — The real answer: correct (~19s)

> So I asked Claude.
> It said there are three r's in strawberry. That is the right answer.
> Which makes this more interesting, not less. The question is what it used to get there.

**Visual:** verbatim transcript card, exactly as received, with interface, model name and date.
**Evidence:** `evidence/claude_response.md`
**Blocked:** date / interface / model still missing — card cannot render until supplied.

---

## B02 — What the model actually receives (~16s)

> Before the model sees anything, the text is cut into tokens — fragments from a fixed vocabulary.
> Each fragment is replaced by a single integer. That row of integers is the whole input.

**Visual:** the prompt dissolving from characters into a row of integers.

---

## B03 — The real split of the real prompt (~26s)

> This is the actual tokenizer output for the question I asked. Eight tokens.
> How. Many. Space r. Apostrophe s. Space are. Space in. Space strawberry. Question mark.
> Look at the seventh. The entire word arrives as one token. One integer. Seventy-three thousand seven hundred.
> The letter r is sitting right there in the question as its own separate token. The word it asks about is a single opaque number.

**Visual:** 8 labelled boxes, real ids `[4438, 1690, 436, 596, 527, 304, 73700, 30]`; box 7 enlarges.
**Evidence:** `evidence/prompt_tokens_demo.txt`, cl100k_base.

---

## B04 — In isolation it splits three ways (~22s)

> Strip the leading space and the same word breaks into three pieces instead. s-t-r. a-w. berry.
> The r's do not land one per piece. One inside "str". None in "aw". Two inside "berry".
> The seams fall where the vocabulary says, not where the letters are.

**Visual:** `str | aw | berry`, ids `496, 675, 15717`; r's at positions 2, 7, 8; tally 1 / 0 / 2.
**Evidence:** `evidence/token_split_demo.txt`, cl100k_base.

---

## B05 — Two vocabularies, two different seams (~20s)

> And those seams belong to the vocabulary, not to the word.
> One vocabulary cuts it s-t-r, a-w, berry. Another cuts the same ten letters s-t, r-a-w, berry.
> Same word, same spelling, different pieces.

**Visual:** cl100k `str|aw|berry` stacked over o200k `st|raw|berry`, seams sliding.
**Evidence:** `evidence/token_split_demo.txt`, both encodings.

---

## B06 — The id is a label, not a description (~22s)

> You might think the number itself carries the spelling. It does not.
> Seventy-three thousand seven hundred is strawberry. One less is the word Smoking. One more is C-M-P.
> And "straw" on its own is thirty-one thousand one hundred and seven — a completely unrelated number, even though it is the first five letters.
> The id is a name tag. It is not a description.

**Visual:** id ladder 73697–73703 with real decoded strings; then ` straw` = 31107 vs ` strawberry` = 73700.
**Evidence:** `evidence/id_is_arbitrary_demo.txt`.

---

## B07 — Constructed illustration (~18s)

> This picture is a constructed illustration, not tokenizer output.
> The tokens are one row. The letters are another. Counting happens on the bottom row.
> The model is handed the top one.

**Visual:** ON-SCREEN LABEL "CONSTRUCTED ILLUSTRATION — not tokenizer output". Token row above,
ten letter cells below, dotted guides that deliberately fail to align.

---

## B08 — The mechanism, stated precisely (~26s)

> So here is what actually happened when Claude answered correctly.
> To count the r's it had to know that token seventy-three thousand seven hundred is spelled s-t-r-a-w-b-e-r-r-y.
> That spelling is not in the integer. It is something the model learned about that token during training.
> It did not read the letters. It recalled them. The answer was right — but it came from memory of the token, not from inspection of the word.

**Visual:** `73700` alone → arrow to spelling, arrow labelled "learned, not given".

---

## B09 — What this does NOT establish (~24s)

> One limit, and it is a real one.
> These splits are OpenAI's tokenizers, because Anthropic does not publish Claude's.
> So this does not establish how Claude splits this word, and it does not prove that tokenization explains this particular answer. The answer was correct; I have not shown what produced it.
> It shows the mechanism exists and where to look. It does not close the case.

**Visual:** two-column card — what this shows / what it does not establish.

---

## B10 — Close (~13s)

> The unit is a token, not a word.
> Run the script in this folder on your own name, and see how many pieces you are.

**Visual:** end card, slug, rebuild command, synthetic-narration disclosure.
