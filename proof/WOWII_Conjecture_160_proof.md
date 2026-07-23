# A proof of the source-corrected WOWII Graph Conjecture 160

## Statement

Let \(G\) be a finite nontrivial connected simple graph. Write

- \(L_s(G)\) for the maximum number of leaves in a spanning tree of \(G\);
- \(\lambda(v)=\alpha(G[N(v)])\), the independence number of the open neighborhood of \(v\);
- \(T(v)\) for the number of triangles containing \(v\);
- \(\lambda_{\max}=\max_v\lambda(v)\) and \(T_{\max}=\max_vT(v)\);
- \(\chi_{C_4}(G)=1\) when \(G\) contains no (not necessarily induced) 4-cycle, and \(0\) otherwise.

The source-corrected Conjecture 160 asserts

\[
L_s(G)\ge \lambda_{\max}+T_{\max}\chi_{C_4}(G).
\]

We prove this statement.

## Preliminary lemma: extending a subtree

**Lemma 1.** If \(H\) is a tree subgraph of a connected graph \(G\), then \(H\) is contained in a spanning tree of \(G\) with at least as many leaves as \(H\).

**Proof.** While \(H\) is not spanning, connectivity gives an edge \(uv\) with \(u\in V(H)\) and \(v\notin V(H)\). Add \(v\) and the edge \(uv\). If \(u\) was not a leaf, the new vertex \(v\) adds one leaf. If \(u\) was a leaf, \(u\) ceases to be a leaf but \(v\) becomes one, so the leaf count does not decrease. Repeating produces the required spanning tree. \(\square\)

Consequently, throughout the proof it is enough to construct an arbitrary tree subgraph having the desired number of leaves.

## Local structure in a \(C_4\)-free graph

**Lemma 2.** If \(G\) has no 4-cycle, then for every vertex \(v\), the graph \(G[N(v)]\) has maximum degree at most one.

**Proof.** If some \(a\in N(v)\) had two distinct neighbors \(b,c\in N(v)\), then

\[
b-a-c-v-b
\]

would be a 4-cycle. \(\square\)

Thus \(G[N(v)]\) is a disjoint union of edges and isolated vertices. The edges of \(G[N(v)]\) correspond one-to-one with triangles containing \(v\). If there are \(T(v)\) such edges and \(s(v)\) isolated vertices, then

\[
d(v)=2T(v)+s(v),\qquad \lambda(v)=T(v)+s(v).
\]

Hence

\[
\boxed{d(v)=\lambda(v)+T(v)}                                      \tag{1}
\]

and, in particular,

\[
\boxed{\lambda(v)\ge T(v)}.                                      \tag{2}
\]

Also, in a \(C_4\)-free graph two vertices have at most one common neighbor.

## Two-star constructions

Let \(x,y\) be vertices of a \(C_4\)-free connected graph.

1. If \(d(x,y)\ge2\), take a shortest \(x\)-\(y\) path and add every edge incident with \(x\) and every edge incident with \(y\). No internal vertex of the path other than the first or last can be a neighbor of an endpoint, by geodesicity. If \(d(x,y)=2\), the middle vertex is the only common neighbor, since a second common neighbor would make a 4-cycle. Therefore the selected edges form a tree subgraph with at least
   \[
   d(x)+d(y)-2                                                     \tag{3}
   \]
   leaves.

2. If \(x\) and \(y\) are adjacent and have no common neighbor, their two full stars form a double-star with at least
   \[
   d(x)+d(y)-2                                                     \tag{4}
   \]
   leaves.

3. If \(x\) and \(y\) are adjacent and have a common neighbor \(z\), then \(z\) is unique. Take both full stars and omit one of the two selected edges from \(z\) to \(x,y\). This is a tree subgraph with at least
   \[
   d(x)+d(y)-3                                                     \tag{5}
   \]
   leaves.

## Main proof

Choose vertices \(x,y\) such that

\[
\lambda(x)=\lambda_{\max}=:\Lambda,
\qquad
T(y)=T_{\max}=:\Tau.
\]

### Graphs containing a 4-cycle

Here \(\chi_{C_4}(G)=0\). Take a maximum independent set in \(G[N(x)]\) and join all of its vertices to \(x\). This is a star with at least \(\Lambda\) leaves. Lemma 1 gives

\[
L_s(G)\ge\Lambda,
\]

which is the required inequality.

### \(C_4\)-free graphs

Assume now that \(G\) is \(C_4\)-free. Put

\[
t_x=T(x),\qquad \lambda_y=\lambda(y).
\]

By (1),

\[
d(x)=\Lambda+t_x,
\qquad
d(y)=\lambda_y+\Tau.                                            \tag{6}
\]

If \(\Tau=0\), the full star centered at \(x\) has at least
\(d(x)=\Lambda+t_x\ge\Lambda\) leaves, so suppose \(\Tau\ge1\).

If \(x=y\), then \(t_x=\Tau\), and the full star centered at \(x\) has
\[
d(x)=\Lambda+\Tau
\]
leaves. Hence we may also suppose that \(x\ne y\).

#### Case 1: \(d(x,y)\ge2\)

If \(t_x+\lambda_y\ge2\), (3) and (6) give

\[
\begin{aligned}
L_s(G)
&\ge d(x)+d(y)-2\\
&=\Lambda+\Tau+(t_x+\lambda_y-2)\\
&\ge\Lambda+\Tau.
\end{aligned}
\]

It remains only to handle \(t_x+\lambda_y<2\). Since \(\Tau\ge1\) and (2) gives \(\lambda_y\ge\Tau\), this forces

\[
t_x=0,\qquad \lambda_y=\Tau=1.
\]

Lemma 2 then says that \(d(y)=2\), and the two neighbors of \(y\), say \(p,z\), are adjacent. Choose a shortest path from \(x\) to \(y\), so that \(p\) is the predecessor of \(y\). Take the full star at \(x\), the path from \(x\) to \(y\), and the edge \(pz\), omitting the edge \(yz\). This is a tree subgraph. It has the \(d(x)-1\) neighbors of \(x\) not used to continue the path, together with both \(y\) and \(z\), as leaves. Hence it has

\[
d(x)-1+2=d(x)+1=\Lambda+1=\Lambda+\Tau
\]

leaves.

#### Case 2: \(x\) and \(y\) are adjacent with no common neighbor

The vertex \(x\) is then an isolated vertex of \(G[N(y)]\). Since \(G[N(y)]\) also contains \(\Tau\ge1\) independent matching edges, we have

\[
\lambda_y\ge\Tau+1\ge2.
\]

Thus \(t_x+\lambda_y\ge2\), and (4) and (6) again imply

\[
L_s(G)\ge\Lambda+\Tau.
\]

#### Case 3: \(x\) and \(y\) are adjacent with a common neighbor

The common neighbor is unique, and the triangle through \(x,y\) gives \(t_x\ge1\). Since \(\Tau\) is maximal, \(t_x\le\Tau\).

If \(t_x=\Tau\), the full star centered at \(x\) has

\[
d(x)=\Lambda+t_x=\Lambda+\Tau
\]

leaves.

If \(t_x<\Tau\), then \(\Tau\ge2\). By (2), \(\lambda_y\ge\Tau\ge2\), and hence

\[
t_x+\lambda_y\ge3.
\]

Using (5) and (6),

\[
\begin{aligned}
L_s(G)
&\ge d(x)+d(y)-3\\
&=\Lambda+\Tau+(t_x+\lambda_y-3)\\
&\ge\Lambda+\Tau.
\end{aligned}
\]

All cases are complete. Therefore

\[
\boxed{L_s(G)\ge \lambda_{\max}+T_{\max}\chi_{C_4}(G)}.
\]

\(\square\)

## Verification note

The accompanying Python program implements the constructive proof: it chooses the two extremal vertices, builds the appropriate tree subgraph in each case, extends it to a spanning tree without losing leaves, and checks the claimed bound. It also exhaustively checks all 995 connected unlabeled graphs available in the NetworkX graph atlas (all connected graphs through seven vertices).
