# Candidate proof of source-corrected WOWII Conjecture 160

This repository contains an AI-assisted candidate proof of the
source-corrected statement of Written on the Wall II Graph Conjecture 160.
It is published for independent mathematical review and possible Lean
formalization. It is not a claim that the result has been accepted by the
Formal Conjectures maintainers or that historical priority has been
established.

## Statement

For a finite nontrivial connected simple graph \(G\), let:

- \(L_s(G)\) be the maximum number of leaves in a spanning tree of \(G\);
- \(\lambda(v)=\alpha(G[N(v)])\);
- \(T(v)\) be the number of triangles containing \(v\);
- \(\chi_{C_4}(G)=1\) when \(G\) contains no 4-cycle as a subgraph, and
  \(0\) otherwise.

The source-corrected conjecture is

\[
L_s(G)\ge \max_v\lambda(v)+\max_vT(v)\,\chi_{C_4}(G).
\]

The 4-cycle need not be induced.

## Contents

- [Proof (PDF)](proof/WOWII_Conjecture_160_proof.pdf)
- [Proof (Markdown)](proof/WOWII_Conjecture_160_proof.md)
- [Proof (LaTeX source)](proof/WOWII_Conjecture_160_proof.tex)
- [Constructive verifier](verification/verify_wowii160.py)
- [Recorded verification output](verification/verification_output.txt)

## Verification

The verifier implements the proof's construction rather than optimizing
\(L_s\). It has been rerun independently against NetworkX 3.6.1 and passed:

- all 995 connected unlabeled graphs of orders 2 through 7 in the NetworkX
  graph atlas;
- 4,997 deterministic random connected graphs of orders up to 20.

To reproduce:

```bash
python3 -m pip install -r requirements.txt
python3 verification/verify_wowii160.py \
  --random-samples 5000 \
  --max-order 20 \
  --seed 160
```

The computational audit supports the construction but is not a substitute
for independent proof review.

## Formal Conjectures context

The statement currently on the Formal Conjectures main branch uses a count of
induced 4-cycles. That is not the historical invariant proved here. The
source correction is tracked in:

- [Issue #4423](https://github.com/google-deepmind/formal-conjectures/issues/4423)
- [Pull request #4443](https://github.com/google-deepmind/formal-conjectures/pull/4443)

This proof should be evaluated against the corrected binary \(C_4\)-free
characteristic proposed there.

## Disclosure

OpenAI models assisted with proof search, case analysis, computational
verification, and preparation of the write-up. All claims should receive
normal independent mathematical and formal review.
