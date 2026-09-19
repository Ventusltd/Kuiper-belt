# MEASURED — the estate's true line count, 19 September 2026

The first honest denominator this project has had. Every number here came from a command that can
fail, over the 66 repositories under `Documents/GitHub` at their current HEAD.

| quantity | value |
|---|---|
| repositories | 66 |
| tracked paths | 41,710 |
| distinct blobs | 19,304 |
| text blobs | 17,835 |
| binary blobs | 1,469 |
| **total text lines** | **25,335,587** |

Method: `git ls-tree -r -l HEAD` per repository for the blob set, then one `git cat-file --batch`
pass per repository over the blobs not already seen, counting newlines and adding one where a file
does not end in a newline. A blob containing a NUL byte in its first 8,000 is counted as binary and
excluded from the line total. Distinct blobs only, so identical content in many places is counted
once, exactly as the Kuiper belt counts bodies.

Index written to `data/blob-lines.tsv`, one row per text blob as `sha<TAB>lines`, 17,835 rows,
sha256 `11a9aa789ca4def10dd6a884228f72731ecdf0b0a1e9dfd3ed8f1425aaa3f4b6`. That file is the whole index SPEC-INFINITE calls for: a global ordinal maps to a
line by prefix sum over it, in both directions, and no coordinate is ever stored.

## What this settles

**67,108,864 is not the estate's line count and never was.** It is 2^26, the particle count of the
`spiral_vs_stack` benchmark, which measured what the renderer can place (21.03 s spiral against
26.89 s stack) using particles generated from a seed that stood for nothing. Quoting it as a line
count would be the same error as reporting the wafer's dust total for the Kuiper belt.

**The real figure is 25,335,587**, and it is 378 times the 250,174 lines the wafer currently draws.
So the wafer shows **0.99 per cent** of the estate's text. That is the gap SPEC-INFINITE exists to
close, and it is closeable: the renderer is already proven well beyond 25 million.

## What is still not measured

- **Authored lines**, from `git log --numstat` additions across all history. A different and more
  meaningful number than lines currently present, and not yet taken.
- **Lines in deleted history**, which the belt's blob-depth view does not reach.
- Whether any of the 17,835 text blobs are generated rather than written. One repository alone
  averages 329 kB per blob, so a large share of those 25 million lines is data, not authorship.
  Until that is split out, **do not describe 25,335,587 as lines of code.** It is lines of text.

## Authored lines — measured 2026-09-19T04:00:03+01:00

| quantity | value |
|---|---|
| lines **added** by commits, all branches | **57,820,668** |
| lines deleted | 11,253,909 |
| net | 46,566,759 |
| commits | 9,887 |
| repositories | 66 |

Method: `git log --all --numstat --format=%H` per repository, summing the added and deleted columns.
Written to `data/authored.tsv` as `repo<TAB>added<TAB>deleted<TAB>commits`, sha256
`95bb5320eba34fc3ceed124d6ac04be70170702b2d23f88296e544c424468d71`.

**This is the number change detection should key on**, because it counts what entered the estate
rather than what happens to be present. Re-run `tools/count_lines.py` and diff `data/counts.json`
against the previous run: any change in `authored_added` is new work, and every figure carries the
command and the timestamp that produced it.

## The four numbers, so they are never conflated again

| number | value | what it is |
|---|---|---|
| **wafer dust** | 250,174 | numbered lines with issued keys, what the wafer draws today |
| **lines at HEAD** | 25,335,587 | text in distinct blobs currently present |
| **lines authored** | 57,820,668 | added by commits across all history |
| **content in history** | 8.75 GB / 45,082 blobs | every blob ever stored; line count not yet taken |
| benchmark, not a count | 67,108,864 | 2^26 particles placed in 21.03 s. **Not a line count.** |

The wafer therefore draws **0.43 per cent** of what has been authored.

Three of those four are measured. The fourth, lines across all stored history, needs one pass over
8.75 GB and is the remaining job: `python tools/count_lines.py --depth history`.
