#set page(width: 158mm, height: auto, margin: 5pt)
#set text(font: "Libertinus Serif", size: 10pt)
#let op(label, body) = block(width: 100%, height: 65pt, stroke: 0.8pt, inset: 5pt)[
  #align(center)[#label #v(5pt) #body]
]
#align(center)[*One item job, weight $w_t$*]
#v(8pt)
#grid(columns: (1fr, 12pt, 1fr, 12pt, 1fr, 12pt, 1fr, 12pt, 1fr), align: center+horizon,
  op($O_1$, [$M_1: C$]), [$arrow.r$],
  op($O_2$, [$M_1: w_t$ #linebreak()or $M_2: L$]), [$arrow.r$],
  op($O_3$, [$M_2: 1$]), [$arrow.r$],
  op($O_4$, [$M_2: L$ #linebreak()or $M_3: w_t$]), [$arrow.r$],
  op($O_5$, [$M_3: C$]))
#v(10pt)
#align(center)[
  $O_2 arrow M_1$ and $O_4 arrow M_2$: add $w_t$ to $A$ #linebreak()
  $O_2 arrow M_2$ and $O_4 arrow M_3$: add $w_t$ to $B$
]
