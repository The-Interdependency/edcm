# EDCM mathematical reference

Version: 0.1.0

Date: 2026-08-02

Status: complete compiled reference for the mathematics currently declared or
implemented in this repository; not a joint UCNS–EDCM canon selection

## Authority and scope

This document is the human-readable copy of the current Energy–Dissonance
Circuit Model mathematics. Its scope is exact:

- `edcm/measurement/` is the maintained implementation authority for the
  frozen baseline candidate `edcm-measurement-v1`;
- `edcm/ucns_objects.py` is the implemented EDCM signed-axis construction
  layer, not formal UCNS geometry;
- `edcm/edcmucns/` is the implemented v0.3.1 EDCM architecture layer; its
  historical “design canon” label does not override the current pre-canon
  status in `CANON.md` or make its local carriers formal UCNS geometry;
- `edcm/ucns_edcm_experiments*.py` contains noncanonical joint experiment
  candidates;
- `edcm/goal_vector_experiment.py` contains the controlled goal-vector
  candidate;
- `edcm/measurement/canon/data/*_v1.json` supplies frozen marker data, not
  empirically validated universal language laws;
- `CANON.md` governs epistemic status and the proof/measurement firewall.

The Interdependent Way textbook is a normative and explanatory artifact. It
may publish a source-pinned copy of this reference, but it does not redefine
EDCM mathematics. If a copied equation disagrees with the exact EDCM source
identified above, the copy has drifted.

The repository and source distribution include this file. The runtime wheel
remains code-focused; installed-wheel behavior is defined by the owning source
modules and packaged frozen data.

“Complete” here means that every mathematical surface presently declared or
implemented by EDCM is indexed below, including its unresolved boundaries. It
does not mean the model is empirically validated, mathematically final, or
joint canon.

## Status vocabulary

| Status | Meaning |
|---|---|
| implemented baseline candidate | Executed by `edcm/measurement/` and preserved by integrity gates |
| implemented EDCM construction | Executed by EDCM, but not formal UCNS geometry |
| experiment candidate | Versioned, executable, and falsifiable; no canon selection |
| represented evidence | Exact source or structural observation retained without an EDCM measurement claim |
| `NA` | Required evidence, context, geometry, or authority is unavailable; never numeric zero |
| hmmm | An unresolved constraint carried forward rather than guessed |

The baseline's numeric functions may return `0` for a measured zero or no
marker hit inside their declared domain. Missing adapters, absent evidence,
disabled axes, and unavailable geometry are represented outside that numeric
domain as typed `NA`.

## 1. Transcript and round domain

Let a transcript be an ordered sequence of turns

$$
T=(u_1,u_2,\ldots,u_m),\qquad
u_i=(a_i,x_i),
$$

where $a_i$ is the speaker identifier and $x_i$ is the exact turn text.
Turn order and multiplicity are load-bearing.

The maintained parser supports two round partitions:

- `cycle`: the first observed speaker is the anchor; a new round begins when
  that speaker regains the floor after at least one other speaker has spoken;
- `pairs`: consecutive pairs of turns form rounds, with a final singleton
  permitted.

For round $t$, let $y_t$ be the single space-joined text of its turns and let
$B_t=(b_{t,1},\ldots,b_{t,n_t})$ be the lowercase token sequence produced by
the baseline tokenizer. Let $A_t=B_{t-1}$ when a previous round exists and the
empty sequence otherwise.

The rule-based parser separately classifies frozen-canon “bone” tokens and
unmatched “flesh” tokens. Bone counts are audit continuity data; the current
behavioral metric vector is computed from round text, token statistics,
markers, and prior-round context rather than from a bones-only operator.

## 2. Common operators and text statistics

### Clamp

$$
\operatorname{clamp}(z)=\min(1,\max(0,z)).
$$

### Type–token ratio and repetition

For token sequence $B$ with $n=|B|$ and vocabulary $V(B)$:

$$
\operatorname{TTR}(B)=
\begin{cases}
0,&n=0,\\
\dfrac{|V(B)|}{n},&n>0,
\end{cases}
$$

$$
\operatorname{Rep}(B)=1-\operatorname{TTR}(B).
$$

Consequently, the historical baseline returns `1` for repetition on an empty
token sequence through `1 - TTR`; normal round computation does not emit an
empty parsed round.

### Shannon entropy

For empirical token probabilities $p_v$:

$$
H(B)=-\sum_{v\in V(B)}p_v\log_2 p_v,
$$

with $H(\varnothing)=0$.

### Repeated n-gram density

Let $G_n(B)$ be the ordered list of all length-$n$ n-grams, and $f(g)$ the
frequency of $g$ in that list:

$$
\operatorname{RepN}_n(B)=
\begin{cases}
0,&|G_n(B)|=0,\\
\dfrac{\sum_{g:f(g)>1}(f(g)-1)}{|G_n(B)|},&\text{otherwise}.
\end{cases}
$$

The maintained baseline uses $n=3$.

### Pattern density

For a regular-expression marker pattern $r$ and raw text $x$:

$$
\rho_r(x)=
\begin{cases}
0,&|x|=0,\\
1000\dfrac{\#\operatorname{matches}(r,x)}{|x|},&|x|>0.
\end{cases}
$$

Matches follow Python `re.findall` behavior; despite an older docstring, the
implementation does not add lookahead to make arbitrary patterns overlap.

### Novelty

$$
\operatorname{Nov}(B\mid A)=
\begin{cases}
0,&|B|=0,\\
\dfrac{\sum_{b\in B}\mathbf 1[b\notin V(A)]}{|B|},&|B|>0.
\end{cases}
$$

Token occurrences, not only unique types, contribute to the numerator.

### Bag-of-words cosine similarity

Let $c_A$ and $c_B$ be aligned count vectors over $V(A)\cup V(B)$:

$$
\operatorname{cos}(A,B)=
\begin{cases}
0,&A=\varnothing\ \text{or}\ B=\varnothing,\\
\dfrac{c_A\cdot c_B}{\|c_A\|_2\|c_B\|_2},&\text{otherwise}.
\end{cases}
$$

### Jaccard similarity

$$
J(X,Y)=
\begin{cases}
0,&X\cup Y=\varnothing,\\
\dfrac{|X\cap Y|}{|X\cup Y|},&\text{otherwise}.
\end{cases}
$$

### Correction fidelity

For original response $A$, new response $B$, and correction/target $C$:

$$
\operatorname{CF}(A,B,C)
=0.5J(V(C),V(B))+0.5\left(1-\operatorname{cos}(A,B)\right).
$$

### Per-100 normalization

$$
\operatorname{per100}(z,B)=
\begin{cases}
0,&|B|=0,\\
100z/|B|,&|B|>0.
\end{cases}
$$

## 3. Maintained baseline vector

For each round, the baseline emits

$$
M_t=(C_t,R_t,F_t,E_t,D_t,N_t,I_t,O_t,L_t,P_t,\kappa_t).
$$

Except for $O_t\in[-1,1]$, the metric components and state are clamped to
$[0,1]$.

Let $h_X(y_t)$ be the number of matches from the first frozen marker category
for metric $X\in\{C,R,I\}$. With $n_t=|B_t|$:

$$
C_t=\operatorname{clamp}\left(
\frac{h_C(y_t)}{\max(1,n_t/10)}\right),
$$

$$
R_t=\operatorname{clamp}\left(
\frac{h_R(y_t)}{\max(1,n_t/10)}\right),
$$

$$
I_t=\operatorname{clamp}\left(
\frac{h_I(y_t)}{\max(1,n_t/10)}\right).
$$

### Fixation

$$
F_t=\operatorname{clamp}\left(
0.30\operatorname{Rep}(B_t)
+0.30\operatorname{RepN}_3(B_t)
+0.40(1-\operatorname{Nov}(B_t\mid A_t))
\right).
$$

### Loop risk used by escalation

$$
R_{\mathrm{loop},t}=\operatorname{clamp}\left(
0.50\operatorname{Rep}(B_t)
+0.30\operatorname{RepN}_3(B_t)
+0.20\operatorname{cos}(A_t,B_t)
\right).
$$

### Escalation

For the first round, the loop term is explicitly set to zero. Otherwise:

$$
E_t=\operatorname{clamp}(0.60R_t+0.40R_{\mathrm{loop},t}).
$$

### Deflection

$$
D_t=
\begin{cases}
0,&t=1,\\
\operatorname{clamp}(1-\operatorname{cos}(B_t,A_t)),&t>1.
\end{cases}
$$

This is a lexical proxy, not full semantic deflection.

### Noise

Let $\widehat H_t=\operatorname{clamp}(H(B_t)/10)$:

$$
N_t=\operatorname{clamp}\left(
0.60\operatorname{Rep}(B_t)+0.40(1-\widehat H_t)
\right).
$$

### Confidence polarity

Let $o_t$ and $u_t$ be overconfidence and under-confidence marker hits:

$$
O_t=
\begin{cases}
0,&o_t+u_t=0,\\
2\dfrac{o_t}{o_t+u_t}-1,&o_t+u_t>0.
\end{cases}
$$

Positive is overconfident, negative is under-confident. This baseline zero is
a within-domain no-hit value; it must not be reused as typed absence.

### Coherence loss

The implementation supplies a first-round novelty default of $0.5$:

$$
L_t=\operatorname{clamp}\left(
0.50\operatorname{Rep}(B_t)+0.50(1-\nu_t)
\right),
$$

where

$$
\nu_t=
\begin{cases}
0.5,&t=1,\\
\operatorname{Nov}(B_t\mid A_t),&t>1.
\end{cases}
$$

### Progress proxy

Let

$$
g_t=
\begin{cases}
0.5,&H(B_{t-1})=0,\\
\operatorname{clamp}\left(
\dfrac{H(B_t)-H(B_{t-1})}{\max(H(B_{t-1}),10^{-9})}
\right),&H(B_{t-1})>0.
\end{cases}
$$

Then

$$
P_t=\operatorname{clamp}(0.60\nu_t+0.40g_t).
$$

$P$ is the baseline's health-oriented component. It is a lexical proxy, not
an externally validated measure of beneficial progress.

## 4. Dissonance and circuit recurrence

The baseline's round dissonance energy is the unweighted mean

$$
\mathcal E_t
=\operatorname{clamp}\left(
\frac{C_t+R_t+F_t+E_t+N_t+I_t+L_t}{7}
\right).
$$

$D_t$, $O_t$, $P_t$, and $\kappa_t$ do not enter this mean. The term “energy”
denotes a dimensionless model quantity; it is not measured in joules and does
not establish a physical-energy claim.

With persistence $\alpha=0.85$ and maximum resolution rate
$\delta_{\max}=0.30$ by default:

$$
g_t=\delta_{\max}\max(0,1-\mathcal E_t),
$$

$$
\delta_t=\min(\delta_{\max},g_t),
$$

$$
\kappa_t=\operatorname{clamp}\left(
\alpha\kappa_{t-1}+\mathcal E_t-\delta_t
\right),\qquad \kappa_0=0.
$$

Because $\mathcal E_t\in[0,1]$, the current implementation has
$\delta_t=g_t$. The public `energy_step` returns $(\mathcal E_t,\kappa_t)$;
the accepted legacy `prev_energy` argument is ignored.

## 5. Auxiliary risk proxies

These are implemented functions but are not all invoked by the default
round-vector path.

### Broken return

$$
R_{\mathrm{broken}}(A,B,C)=\operatorname{clamp}\left(
0.55\operatorname{cos}(A,B)+0.45(1-J(V(C),V(B)))
\right).
$$

### Escalation or shutdown risk

For refusal density $\rho_R$ and hedge density $\rho_H$, both measured per
1,000 characters:

$$
R_{\mathrm{esc}}=\operatorname{clamp}\left(
0.45R_{\mathrm{broken}}+0.35\frac{\rho_R}{5}
+0.20\frac{\rho_H}{5}
\right).
$$

### Stagnation

For caller-supplied gain $G\in[0,1]$:

$$
R_{\mathrm{stag}}=\operatorname{clamp}\left(
0.45\frac{\rho_R}{5}
+0.35(1-\operatorname{Nov}(B\mid A))
+0.20(1-G)
\right).
$$

### Fixation and loop

$R_{\mathrm{fix}}$ is exactly the $F_t$ equation in section 3.
$R_{\mathrm{loop}}$ is the loop equation used by $E_t$.

These values are bounded behavioral proxies. Their names do not establish
diagnosis, intention, morality, consciousness, or external truth.

## 6. Agent-facing projections

The implemented Layer-3 vector is

$$
A_t=(CM_t,DA_t,DRIFT_t,DVG_t,INT_t,TBF_t)\in[0,1]^6.
$$

The exact linear projections are

$$
CM_t=\operatorname{clamp}(0.50C_t+0.50I_t),
$$

$$
DA_t=\operatorname{clamp}(0.40\kappa_t+0.40E_t+0.20R_t),
$$

$$
DRIFT_t=\operatorname{clamp}(0.50L_t+0.50(1-P_t)),
$$

$$
DVG_t=\operatorname{clamp}(0.50D_t+0.50N_t),
$$

$$
INT_t=\operatorname{clamp}(0.50E_t+0.50F_t).
$$

### Turn-balance Gini

Let $x_1\le\cdots\le x_n$ be total token counts by speaker in the round and
$S=\sum_i x_i$. For $n\le1$ or $S=0$, $TBF_t=0$. Otherwise:

$$
G=\frac{2\sum_{i=1}^{n}ix_i}{nS}-\frac{n+1}{n},
$$

$$
TBF_t=\operatorname{clamp}\left(\frac{G}{(n-1)/n}\right).
$$

Higher $TBF$ means greater token-share imbalance. “Fairness” here names this
specific distributional proxy; it does not measure social or substantive
fairness.

## 7. Alerts and risk crosswalk

Alerts fire only when the metric is strictly greater than its threshold:

| Alert | Metric | Threshold |
|---|---:|---:|
| `ALERT_CM_HIGH` | $CM$ | 0.70 |
| `ALERT_DA_RISING` | $DA$ | 0.60 |
| `ALERT_DRIFT` | $DRIFT$ | 0.50 |
| `ALERT_DVG_HIGH` | $DVG$ | 0.60 |
| `ALERT_INT_HIGH` | $INT$ | 0.70 |
| `ALERT_TBF_SKEW` | $TBF$ | 0.40 |

The implemented nonnumeric crosswalk is:

| Risk | Associated alerts |
|---|---|
| $R_{\mathrm{fix}}$ | `ALERT_INT_HIGH`, `ALERT_DRIFT` |
| $R_{\mathrm{esc}}$ | `ALERT_DA_RISING`, `ALERT_CM_HIGH` |
| $R_{\mathrm{stag}}$ | `ALERT_DRIFT`, `ALERT_DA_RISING` |
| $R_{\mathrm{loop}}$ | `ALERT_INT_HIGH` |

Thresholds and crosswalks are version-1 candidate policy, not empirically
selected universal constants.

## 8. Matrix identity and present duplication

`edcm/measurement/metrics/matrix.py` declares `MATRIX_VERSION = "1.0"`, the
Layer-0-to-Layer-1 weight dictionary, projections, thresholds, and crosswalk.
The runtime formulas for the Layer-1 metrics remain hardcoded in
`compute.py`; the matrix itself states that it is documentation-shaped rather
than the runtime source of those calculations. This document therefore records
the executed `compute.py` equations above and treats the matrix as a
versioned intended mirror.

For any matrix dictionary $Q$, `freeze(Q)` computes

$$
\operatorname{id}(Q)=
\operatorname{SHA256}(\operatorname{canonicalJSON}(Q))[0:16],
$$

then attaches that hexadecimal prefix as `_sha256`. `diff` reports every
changed `(metric, primitive)` coefficient pair.

hmmm: the declared matrix and the executed Layer-1 equations still have two
maintenance locations. Making the matrix the runtime source requires a
separate versioned migration and equivalence tests.

## 9. Signed-ternary EDCM construction

An enabled metric axis is

$$
X=(s,m),\qquad s\in\{-1,0,+1\},\quad m\in[0,1].
$$

Typed absence is

$$
X=NA\iff enabled=false\land s=null\land m=null.
$$

Therefore

$$
NA\ne(0,0).
$$

The implemented grains are token, turn, round, session, and archive.

### Constraint field

Let a `ConstraintField` contain raised-field count $r\ge0$, contact direction
$c$, contact magnitude $m_c$, resolution state $z$, and resolution magnitude
$m_z$. Presence is

$$
present\iff r>0.
$$

If $r=0$, contact, resolution, $R$, $D$, $I$, and resistance-$L$ readouts are
all `NA`.

Contact direction is mapped as

$$
toward\mapsto+1,\qquad against\mapsto-1,\qquad away\mapsto0.
$$

Resolution is mapped as

$$
closed\mapsto+1,\qquad open\mapsto-1,\qquad unresolved\mapsto0.
$$

For a present field, the behavioral readout signs are:

| Contact | $R$ refusal/resistance | $D$ deflection/return | $L_{resistance}$ |
|---|---:|---:|---:|
| `against` | +1 | 0 | +1 |
| `toward` | -1 | -1 | -1 |
| `away` | 0 | +1 | 0 |
| omitted | 0 | 0 | 0 |

Each receives magnitude $\operatorname{clamp}(m_c)$. The $I$ readout uses the
resolution sign and magnitude $\operatorname{clamp}(m_z)$.

### Field motion

For axis reads $q_1,\ldots,q_n$, let

$$
\bar q=\frac1n\sum_i q_i.
$$

A present `FieldMotion` emits

$$
s=\operatorname{sign}(\bar q),\qquad
m=\min(1,|\bar q|).
$$

An empty read list on a present motion emits $(0,0)$; an absent motion emits
`NA`. The three right-angle readouts are:

- recurrence reads $\rightarrow F$ fixation/release;
- intensity reads $\rightarrow E$ escalation/de-escalation;
- scope reads $\rightarrow O_{scope}$ expansion/contraction.

All three share the same ordered transition parent
`previous_field_hash->current_field_hash` while preserving distinct metric
identities. The field and transition hashes are deterministic content
identifiers, not formal UCNS objects or signed authentication.

The exact `ConstraintField` content identity is the first 16 hexadecimal
characters of SHA-256 over the UTF-8 pipe-joined sequence

$$
(schema\_id,grain,raised\_field\_count,contact,contact\_magnitude,
resolution,resolution\_magnitude,witness).
$$

The field reader retains `previous_field_hash->current_field_hash` and appends
`#` plus the first 16 hexadecimal characters of SHA-256 over Python `repr` of
the motion-presence flag and the three exact read tuples. This is a
runtime-language identity contract, not a portable canonical-JSON signature.

The axis registry also names $C,R,D,I,F,E,O_{scope},O_{confidence},L_{load},
L_{loss},L_{resistance},N,P,\kappa$ and the six projections. Registration does
not make an axis canonical.

## 10. Implemented v0.3.1 architecture layer

`edcm/edcmucns/` implements the v0.3.1 identity and composition architecture.
Its source docstrings preserve the historical label “ratified as architecture
(frozen design canon).” Under the repository-wide status authority in
`CANON.md`, that label is scoped to this implemented architecture: it is not a
joint UCNS–EDCM canon selection, formal UCNS geometry, or empirical
measurement validation.

The architecture declares the measurement dependency

$$
M_{EDCM}=\operatorname{readout}
\left(G_{carrier},\Pi_{provenance},payloads,field\_state,policy\_manifest\right).
$$

`G_carrier` here is the EDCM-local `Window` construction described below. The
implementation does not construct or validate the six-field formal UCNS
object reproduced by the earlier design handoff.

### Manifest and family gauge

The exact v0.3.1 family-to-prime gauge is

$$
P\mapsto3,\qquad K\mapsto5,\qquad Q\mapsto7,\qquad
T\mapsto13,\qquad S\mapsto29.
$$

`PolicyManifest` requires this exact gauge and the residue-rule identity
`non_origin_residue_v031`. Its canonical JSON contains the gauge and seven
policy-version fields. The manifest identity is

$$
h_{manifest}=\operatorname{SHA256}(\operatorname{UTF8}(J_{manifest})).
$$

The polarity, bone-emission, payload-governance, lens-readout, and
training-update version strings are architecture identifiers. The contact
predicate remains explicitly `v031-frontier-unimplemented`; the strings do
not establish that the named empirical policies are validated.

The ordered readout-bearing witness fields are `family`, `ordinal_m_f`,
`residue_r_f`, `turn_id`, `speaker_or_source`, `surface_form`, `role`,
`constraint_governance`, and `payload_attachment`. A witness hash is SHA-256
over their sorted-key compact JSON object; an ordered bundle hash is SHA-256
over the compact JSON array of those objects. Decorative witness fields never
enter either identity. The bundle order is chronological and readout-bearing.

### Non-origin residue and anchors

For one-based ordinal $m\ge1$ and family prime $p\ge2$:

$$
r(m,p)=1+((m-1)\bmod(p-1)),
$$

$$
\theta_{bone}(m,p)=\frac{r(m,p)}{p}
$$

as an exact fraction of a turn in $[0,1)$. Bone residues therefore cycle
through $1,\ldots,p-1$ and never land at the origin. An origin anchor has

$$
\theta=0,\qquad face=0,\qquad lattice\_n=1,
$$

and carries no family, ordinal, or residue metadata. Bone faces are exactly
$-1$ or $+1$.

An explicitly caller-constructed cadence fixture uses

$$
\theta_{cadence}(m,n)=\frac{m\bmod n}{n}.
$$

Cadence admission from transcript text is not implemented. The source also
retains an exact `hmmm`: when $m\bmod n=0$, the cadence helper returns the
datum angle even though non-origin `Anchor` validation rejects that collision.

### Mass, carriers, shares, and field load

For a window $W$ with host anchors $A(W)$, bone anchors $B(W)$, cadence
anchors $C(W)$, and payloads $P(W)$:

$$
L_{geo}(W)=|A(W)|,
\qquad
L_{op}(W)=|B(W)|.
$$

The implemented carrier functions are least common multiples over their
declared scopes, with the empty least common multiple equal to one:

$$
n_{host}(W)=\operatorname{lcm}\{a.lattice\_n:a\in A(W)\},
$$

$$
n_{family}(W)=\operatorname{lcm}\{a.lattice\_n:a\in B(W)\},
$$

$$
n_{cadence}(W)=\operatorname{lcm}\{a.lattice\_n:a\in C(W)\},
$$

$$
n_{payload}(W)=\operatorname{lcm}\{p.reduced\_carrier:p\in P(W)\}.
$$

Only $n_{family}$ carries the architecture's active-family factor claim.
Payload carriers do not automatically enter $n_{host}$.

For family $f$, the operator share is

$$
share_f(W)=
\begin{cases}
\text{absent from the returned map},&L_{op}(W)=0,\\
\dfrac{|\{a\in B(W):a.family=f\}|}{L_{op}(W)},&L_{op}(W)>0.
\end{cases}
$$

Shares after chronological append are derived from summed counts, never by
averaging the two input share maps.

Field load remains separate from both masses:

$$
\lambda_{field}(W)=
\begin{cases}
NA,&TOK(W)\le0,\\
\dfrac{raised\_field\_count(W)}{TOK(W)},&TOK(W)>0.
\end{cases}
$$

The Python value for this typed absence is `None`, not numeric zero.

### Turn and payload absence

The implemented turn sum type is

$$
OperatorTurn=Present(Window)\mid AbsentOperatorGeometry(ContentLensEvent).
$$

A no-bone turn emits `AbsentOperatorGeometry`. Its operator-presence readout
is `NA`; a present turn emits $(+1,1)$. A no-bone turn is neither the geometric
unit nor numeric zero and remains available to the content layer.

For payload $p$:

$$
p.reduced\_carrier=
\begin{cases}
1,&p.status=closed,\\
p.carrier\_n,&p.status=open.
\end{cases}
$$

Its content identity is SHA-256 over the exact UTF-8 string

$$
payload\_id\;|\;carrier\_n\;|\;status\;|\;tension\;|\;content.
$$

This delimiter-based identity is the implemented contract; it is not silently
re-described as canonical JSON.

The architecture-only kappa ledger is

$$
\kappa_{balance}(W)=
\sum_{p\in P(W):p.status\ne closed}p.tension.
$$

A nonzero balance emits a `kappa_leak` diagnostic. This placeholder is not the
maintained baseline circuit recurrence in section 4 and makes no empirical
stored-tension claim.

### Chronological append and reserved interaction product

For windows sealed under the same manifest, `SeqAppend` is exact tuple
concatenation of anchors, witnesses, payloads, and field-chain entries, with
token and raised-field counts added:

$$
L(A\boxplus B)=L(A)+L(B),
\qquad
F(A\boxplus B)=F(A)\mathbin{\|}F(B).
$$

Appending windows with different manifest hashes raises `EpochBreakError`.
The reserved interaction product returns a non-window signature with

$$
L(A\boxtimes B)=L(A)L(B).
$$

The current implementation does not implement the earlier handoff's payload
product, XOR face product, mirror construction, or external zero/unit algebra.
Those equations therefore must not be reconstructed by a publication
consumer as current EDCM implementation.

### Exact implemented equivalence

The local carrier-equivalence predicate is

$$
A\equiv_{carrier}B
\iff
n_{host}(A)=n_{host}(B)
\land
sort\{(\theta_a,face_a):a\in A\}
=sort\{(\theta_b,face_b):b\in B\}.
$$

It ignores witnesses, payloads, and manifest identity. It compares sorted
angle-face pairs rather than chronological anchor order. Chronological
testimony order remains readout-bearing in the ordered witness-bundle hash.
The module preserves this split as `hmmm`; a website must not silently replace
it with a stronger ordered UCNS equivalence claim.

EDCM measurement equivalence first requires carrier equivalence and equal
manifest hashes. It then applies one closed readout scope:

| Scope | Additional exact comparison |
|---|---|
| `operator_scope` | ordered readout-bearing witness-bundle hash |
| `payload_scope` | sorted `(content_hash, reduced_carrier)` tuples |
| `cadence_scope` | cadence carrier plus ordered cadence `(lattice_n, ordinal, theta)` tuples |
| `field_scope` | exact field-chain tuple |
| `bridge_scope` | no additional identity comparison; validator diagnostics remain observational |

The `bridge_scope` diagnostic vocabulary remains unresolved and growing. No
runtime scope-registration surface exists; extending the registry requires a
manifest revision and epoch break.

### Validation, polarity, and epochs

`witness_geometry_consistent` checks origin constraints, nonzero bone phases,
one-to-one bone/witness pairing, exact gauge and residue agreement, stable NFC
canonicalization of turn/source ids, and existing payload targets. A mismatch
emits a Bridge diagnostic rather than an alternate reading.

`gauge_audit` considers bone faces only. No differences passes; a difference
at every paired face is reported as `gauge_mismatch`; a partial difference or
different face-sequence length is `measurement_divergence`. This is a
diagnostic classification, not proof of empirical equivalence.

The window identity used in epoch chains hashes, in order:

- serialized anchor role, family, lattice, ordinal, angle, and face values;
- the ordered witness-bundle hash;
- sorted payload content hashes;
- the exact field-chain tuple; and
- the manifest hash.

The five components are pipe-joined before SHA-256. Anchor records are
semicolon-joined; payload content hashes are sorted then comma-joined; field
chain entries retain their exact order. These identities detect implementation
drift but do not authenticate a producer.

A manifest rotation seals the old segment and records old manifest, new
manifest, and optional boundary-window identities before opening the new
segment. Cross-epoch comparison emits `cross_epoch_lens`; it is not a raw
delta. Adoption of `non_origin_residue_v031` is itself recorded as an epoch
break.

### v0.3.1 unresolved boundary

The following remain non-operational `NotImplementedError` surfaces with
named falsifiers: contact convergence, residual-primality / $DA_{geom}$
correlation, and cadence admission from transcript text. Corpus parallel-run
conclusions and operating-state empirical validity also remain frontier.

Additional source-level `hmmm` boundaries remain visible:

- `constraint_governance` is an opaque readout-bearing string;
- the cadence origin collision described above is unresolved;
- `bridge_scope` compares manifest/carrier identity while its diagnostic
  vocabulary is still growing;
- the kappa ledger reads open-payload tension only;
- bone emission from raw text is outside this encoder and is identified only
  by the manifest's upstream emission-policy version; and
- v0.3.1 carrier equivalence sorts angle-face pairs while witness identity
  retains chronology.

## 11. Controlled goal-vector candidate

For a declared goal with $d$ components, each available component state is
`toward` $(+1,1)$ or `away` $(-1,1)$. An unavailable component is `NA`; a turn
that makes no claim about a component is `no-claim`. Both unavailable states
carry null sign and magnitude rather than numeric zero.

Let $T_t$, $A_t$, and $U_t$ be the counts of toward, away, and `NA` component
states after turn $t$, so $T_t+A_t+U_t=d$. The declared-loss scalar projection
is

$$
q_t=\frac{T_t-A_t}{d},\qquad q_0=0.
$$

The complete component state remains authority-bearing evidence. $q_t$ is not
sufficient to reconstruct which components produced the value.

Motion is

$$
\Delta q_t=q_t-q_{t-1}.
$$

For a sequence $z_1,\ldots,z_n$, the candidate uses population variance

$$
\operatorname{Var}(z)=\frac1n\sum_{i=1}^{n}(z_i-\bar z)^2,
\qquad
\bar z=\frac1n\sum_{i=1}^{n}z_i.
$$

Thus

$$
V_{motion}=\operatorname{Var}(\Delta q_1,\ldots,\Delta q_n),
$$

$$
V_{trajectory}=\operatorname{Var}(q_1,\ldots,q_n).
$$

A terminal state is `candidate-complete` exactly when all $d$ components are
toward and the contradiction ledger has no active entry. Formal completion
remains `NA`.

Contradiction status is procedural over declared fixture claims:

- a claim opposing the prior component sign creates a contradiction;
- it is `resolved` only when that opposing claim is explicitly declared a
  revision;
- otherwise it remains `active`;
- no claim about dishonesty, intention, diagnosis, morality, consciousness,
  or external truth follows.

The sealed v0.1.0 fixture produced:

| Case | $q_n$ | $V_{motion}$ | $V_{trajectory}$ | Active contradictions |
|---|---:|---:|---:|---:|
| contradiction resolved | $1$ | $1/8$ | $5/32$ | 0 |
| contradiction active after reordering | $1/2$ | $9/64$ | $11/256$ | 1 |

This is controlled candidate-measured evidence: eight supported findings, zero
falsified findings, and no canon selection.

## 12. Initial joint experiment candidate

The historical v0.1 experiment also retains a transparent, noncanonical
sequence candidate. For each turn $i$, phrase-hit signals
$c_i,r_i,z_i\in[0,1]$ represent constraint, refusal, and resolution; $p_i=1$
when the normalized turn has appeared earlier in the same case and $0$
otherwise.

$$
pressure_i=0.35c_i+0.35r_i+0.20p_i,
$$

$$
release_i=0.55z_i,
$$

$$
\tau_i=\operatorname{clamp}(0.72\tau_{i-1}+pressure_i-release_i),
\qquad \tau_0=0.
$$

The reported constraint, refusal, resolution, and repetition pressures are
their arithmetic means over turns. Final tension is $\tau_n$.

Three support assignments were tested:

$$
\mu_{unit}=1,
$$

$$
\mu_{token}=\max(1,\operatorname{tokenCount}),
$$

$$
\mu_{pressure}=1+c_i+r_i+z_i+p_i.
$$

The experiment exposes all three UCNS product-character candidates
(`cell-support-geometric-mean`, `cell-support-maximum`,
`cell-support-minimum`) and all three faithful-breadth candidates
(`cell-log-support`, `cell-detail`, `retained-presence`) under each support
assignment. Their definitions and authority belong to the experiment-pinned
UCNS producer; EDCM records their readouts and comparisons without adopting a
winner.

Ordered-sequence, unordered-multiset, and set projections are compared. A
projection is incompatible for a named EDCM readout only when it declares two
cases equivalent while that readout materially differs under the declared
comparison policy. This is scoped falsification, not universal rejection.

### v0.2 occurrence, coverage, and latency candidate

Unlike v0.1, v0.2 does not clamp phrase occurrences to one. For turn $i$, let
$c_i$ be total constraint-phrase occurrences, $f_i$ the number of distinct
constraint phrase families hit, $r_i$ refusal occurrences, $z_i$ resolution
occurrences, and $p_i$ the repeated-turn indicator.

$$
pressure_i=0.30c_i+0.55r_i+0.20p_i,
$$

$$
release_i=0.65z_i,
$$

$$
\tau_i=\max(0,0.78\tau_{i-1}+pressure_i-release_i),
\qquad \tau_0=0.
$$

The candidate records occurrence totals, family-hit totals, refusal rate,
terminal tension, peak tension, and tension area

$$
Area=\sum_{i=1}^{n}\tau_i.
$$

If first pressure occurs at zero-based event index $j$ and the first resolution
observed once pressure has occurred is at $k$, resolution latency is $k-j$.
It is `-1` when either event
is absent. If pressure occurs but resolution does not, the comparison horizon
is $n+1$ rather than `-1`.

Its support assignments are

$$
\mu_{unit}=1,
\qquad
\mu_{token}=\max(1,\operatorname{tokenCount}),
$$

$$
\mu_{occurrence}=1+c_i+r_i+z_i+p_i,
$$

$$
\mu_{dissonance}=1+c_i+r_i+p_i.
$$

### v0.3 assertion and local-scope candidate

v0.3 emits an ordered event sequence from nonoverlapping phrase spans.
Each event retains kind, family, speaker, source position, polarity, quotation,
hypothetical, conditional, attribution, retraction, ownership, and active
flags. The implemented active predicate for a mention is

$$
active=\neg negated\land\neg quoted\land\neg hypothetical\land\neg retracted.
$$

Attribution and conditionality remain separately counted; they do not by
themselves make the event inactive. An owned refusal additionally requires a
refusal event, first-person `I` evidence, and neither quotation nor attribution.

Let $a_i$ be active pressure after event $i$. An active constraint or refusal
increments pressure by one; a repair event resets it to zero:

$$
a_i=
\begin{cases}
0,&event_i=repair,\\
a_{i-1}+1,&event_i\text{ is an active constraint or refusal},\\
a_{i-1},&\text{otherwise}.
\end{cases}
$$

The candidate reports $a_n$, $\max_i a_i$, $\sum_i a_i$, exact event counts,
and the index distance from first active pressure to first later repair, or
`-1` if either is absent.

For event complexity

$$
k_i=\mathbf1[negated]+\mathbf1[quoted]+\mathbf1[hypothetical]
+\mathbf1[conditional]+\mathbf1[attributed]+\mathbf1[retracted],
$$

the support policies are

$$
\mu_{mention}=1,
$$

$$
\mu_{scope}=1+k_i,
$$

$$
\mu_{active}=1+2\mathbf1[event_i\text{ is an active constraint or refusal}].
$$

These are deterministic synthetic-scope rules, not a general semantic parser.

### v0.4 discourse-graph candidate

v0.4 is a finite, bounded graph-state experiment. A case contains ordered
discourse nodes, positive reference expressions, and declared relations.
Candidate resolvers select targets by explicit label or ordinal, nearest
compatible prior node, nearest same-speaker prior node, all compatible family
nodes, or every ambiguity-preserving singleton alternative. Only nodes earlier
than the reference are eligible. Ambiguity expansion is capped at 32 generated
interpretations and then deduplicated by exact interpretation digest.

The node-state transition is

$$
\operatorname{transition}(s,r)=
\begin{cases}
retracted,&r\in\{retracts,repairs\},\\
suspended,&r=suspends,\\
active,&r\in\{resumes,activates\},\\
inactive\_condition,&r=deactivates,\\
s,&\text{otherwise}.
\end{cases}
$$

A `contradicts` edge increments the target's contradiction count without
changing its state. A reference with no selected target remains positive
unresolved-reference evidence.

Across admissible interpretations, the readout reports the number of
alternatives, number of distinct state signatures minus one, minima and maxima
of active/suspended/retracted/contradiction/unresolved/edge counts, declared
target hits and misses, per-node active/retracted bounds, and per-speaker active
bounds. Minima encode what holds across every retained interpretation; maxima
encode what occurs in at least one retained interpretation.

Graph support is:

$$
\mu_{node-reference}=\mu_{node-edge}=1
$$

for nodes, while `state-detail` uses

$$
\mu_{node,state}=1+\mathbf1[active]+\mathbf1[contradictions>0],
$$

$$
\mu_{reference,state}=1+\mathbf1[unresolved].
$$

Each retained graph or quote edge has support one under `node-edge` and
`state-detail`. Exact ordered labeled, labeled multigraph, unlabeled
multigraph, flat node multiset, and active-state summary views explicitly list
their information losses.

The v0.2–v0.4 complete executable definitions and sealed results remain
versioned in `edcm/ucns_edcm_experiments_v2.py` through
`edcm/ucns_edcm_experiments_v4.py` and `experiments/results/`. None replaces
the maintained baseline equations or selects joint canon.

## 13. Exact UCNS observation boundary

The current profile supplies exact ordered word-gonol observations with one
unit of support per speaker turn. It retains exact Unicode source values,
carrier assignments, SPACE boundaries, multiplicity, and turn order.

It does not currently supply an EDCM equation for:

- formal Möbius coordinates;
- word-to-turn-to-dialogue higher-gonol composition;
- lawful scalar projection into EDCM axes;
- formal completion;
- measurement validity.

Those quantities are `NA`, not zero. A UCNS observation digest establishes
deterministic content identity under its schema; it is not signed producer
authentication and transfers no theorem or proof status into EDCM.

## 14. Booking-outcome holdout calibration

For each admitted MultiWOZ booking outcome event, the candidate score is the
maintained terminal progress proxy $s=P_{terminal}\in[0,1]$ over context turns
strictly preceding the labelled response. Source dialogue-act labels are
targets only:

$$
y=\begin{cases}
1 & \text{for Booking-Book},\\
0 & \text{for Booking-NoBook}.
\end{cases}
$$

On development events only, scores are standardized using population moments

$$
z=\frac{s-\mu_{dev}}{\sigma_{dev}},
$$

and the candidate probability is a two-parameter Platt map

$$
\hat p(y=1\mid s)=\frac{1}{1+\exp[-(a+bz)]}.
$$

The sealed v0.1.0 fit uses a slope ridge of $10^{-6}$ and deterministic Newton
updates. Validation chooses one probability threshold $\theta$ by maximum
balanced accuracy, with ties resolved first by proximity to $0.5$ and then by
the lower threshold. Development and validation freeze $(\mu_{dev},
\sigma_{dev},a,b,\theta)$ before test evaluation.

For confusion counts $TP,FP,FN,TN$,

$$
\operatorname{sensitivity}=\frac{TP}{TP+FN},\qquad
\operatorname{specificity}=\frac{TN}{TN+FP},
$$

$$
\operatorname{balanced\ accuracy}
=\frac{\operatorname{sensitivity}+\operatorname{specificity}}{2}.
$$

Probability error is reported as

$$
\operatorname{Brier}=\frac1n\sum_{i=1}^{n}(\hat p_i-y_i)^2
$$

and ten-bin expected calibration error

$$
\operatorname{ECE}_{10}
=\sum_{j=1}^{10}\frac{|B_j|}{n}
\left|\operatorname{mean}_{i\in B_j}(\hat p_i)
-\operatorname{mean}_{i\in B_j}(y_i)\right|.
$$

Sensitivity and specificity receive 95% Wilson intervals. Balanced accuracy,
Brier score, and ECE receive deterministic 2,000-replicate percentile
intervals resampling whole dialogue clusters with seed `20260802`.

The sealed test values are $TP=249$, $FP=56$, $FN=281$, and $TN=75$.
Sensitivity is $0.4698$, specificity $0.5725$, and balanced accuracy $0.5212$;
the cluster interval for balanced accuracy is $[0.4656,0.5739]$. The
sensitivity hypothesis is falsified. These equations and fitted values belong
only to candidate `edcm.maintained-terminal-progress/0.1.0`; they are not a
canonical baseline change or production threshold.

## 15. Identity and reproducibility mathematics

EDCM evidence records use canonical JSON bytes

$$
J(x)=\operatorname{UTF8}(\operatorname{JSON}(x;
sort\_keys=true,separators=(\texttt{,},\texttt{:}),ensure\_ascii=false)).
$$

Content identity is

$$
d(x)=\operatorname{SHA256}(J(x)).
$$

For a self-digesting report, `report_digest` is removed before computing
$d(x)$ and then attached to the report. The immutable evidence file also has a
SHA-256 over its exact serialized bytes. These identities detect drift; they
do not prove truth, authorship, or empirical validity.

For `edcm.shared-stack-result/1.2.0`, `epoch_identity` is $d(x)$ over the
METAPAT canon/provenance digests, UCNS profile identity/scope/source/options,
EDCM manifest hash, and selected semantic-authority, UCNS-profile, and
measurement implementations. `result_identity` is $d(x)$ over that epoch
identity plus source evidence, the complete UCNS profile observation, EDCM
readouts, factorization evidence, and status evidence. Geometry absence remains
a typed compartment and does not become a fabricated geometry identity.

## 16. What is not yet mathematics

The following are deliberately not filled with convenient equations:

- an empirically calibrated mapping from language to every EDCM axis;
- a validated threshold or coefficient selection procedure;
- a canonical global objective or optimization function;
- a numeric `hmmm` penalty or hidden uncertainty scalar;
- METAPAT semantic labels converted directly into measured values;
- formal UCNS geometry or completion inferred from observation identity;
- real-dialogue goal authority inferred by the model;
- physical-energy units or conservation claims;
- diagnosis, intention, morality, consciousness, or external truth.

`hmmm` is a boundary object carrying unresolved constraints and provenance. It
is not silently mapped to zero, averaged away, or inserted as an unvalidated
term in an objective function.

## Usage guidance

For the maintained baseline:

```bash
python -m edcm.integrity
python -m pytest -q
```

For the controlled goal-vector candidate:

```bash
python -m edcm.goal_vector_experiment \
  --ucns-source-root /path/to/ucns-at-a98c9e6c69804a8a08d0786b1d8b450bb2c49a97 \
  --output /tmp/goal-vector.json
```

For the externally labelled booking-outcome holdout:

```bash
python -m edcm.corpora.multiwoz21_booking_holdout \
  --archive /path/to/MULTIWOZ2.1.zip \
  --edcm-repository-root /path/to/edcm \
  --edcm-commit "$(git -C /path/to/edcm rev-parse HEAD)" \
  --output /tmp/multiwoz-booking-holdout.json \
  --receipt /tmp/multiwoz-booking-holdout-complete.json
```

When changing any equation, coefficient, threshold, state domain, tokenizer,
marker source, round boundary, or projection:

1. change the owning source and its tests;
2. update this reference in the same change;
3. version any changed candidate or evidence schema;
4. preserve old sealed reports unchanged;
5. rerun integrity, metadata, complete tests, build, and wheel checks;
6. record falsified and unresolved consequences rather than rewriting them.

A textbook or website copy must cite the EDCM repository path and exact commit
from which it was copied and must label itself non-authoritative.

## hmmm

The maintained baseline now has one complete mathematical reference and one
bounded externally labelled calibration, but its coefficients remain candidate
policy and the Layer-1 matrix still duplicates runtime equations. Independent
human task-success adjudication, formal higher-gonol composition, signed
producer records, externally hidden holdout custody, and the first joint canon
decision remain unresolved.
