"""Row → Panel object builders."""

from __future__ import annotations

import ast
import numpy as np

import pandas as pd
import panel as pn

from ..config import (
    FILTER_GROUPS,
    TOPIC_COLS,
    TOPIC_OPTIONS,
    TOPIC_QUESTIONS,
)
from .components import card_styles, description
from .tokens import ACCENT, FIRST_COL_BOLD_CSS, GROUP_COLORS, TABLE_CSS, TEXT



# ── Psychometric scale item texts ─────────────────────────────────────────

MAES_ITEMS = [
    "A simultaneous equation",
    "Work with decimals",
    "Determine the degrees of a missing angle",
    "An algebra problem",
    "A problem in trigonometry",
    "Calculate values of area and volume",
    "Sketch a curve",
    "Work with fractions",
    "Determine the value of a missing side length",
]

AMAS_ITEMS = [
    "Having to use the tables in the back of a math book.",
    "Thinking about an upcoming math test 1 day before.",
    "Watching a teacher work an algebraic equation on the blackboard.",
    "Taking an examination in a math course.",
    "Being given a homework assignment of many difficult problems that is due the next class meeting.",
    "Listening to a lecture in math class.",
    "Listening to another student explain a math formula.",
    "Being given a 'pop' quiz in math class.",
    "Starting a new chapter in a math book.",
]

MSEAQ_ITEMS = [
    # 1-7: Self-efficacy
    "I believe I am the kind of person who is good at mathematics.",
    "I believe I am the type of person who can do mathematics.",
    "I believe I can learn well in a mathematics course.",
    "I feel that I will be able to do well in future mathematics courses.",
    "I believe I can understand the content in a mathematics course.",
    "I believe I can get an 'A' when I am in a mathematics course.",
    "I believe I can do the mathematics in a mathematics course.",
    # 8-28: Anxiety
    "I worry that I will not be able to do well on mathematics tests.",
    "I get tense when I prepare for a mathematics test.",
    "I get nervous when taking a mathematics test.",
    "I worry that I will not be able to get an 'A' in my mathematics course.",
    "I worry that I will not be able to get a good grade in my mathematics course.",
    "I feel confident when taking a mathematics test.",
    "I believe I can do well on a mathematics test.",
    "Working on mathematics homework is stressful for me.",
    "I get nervous when I have to use mathematics outside of school.",
    "I feel confident when using mathematics outside of school.",
    "I worry that I will not be able to use mathematics in my future career when needed.",
    "I worry I will not be able to understand the mathematics.",
    "I worry that I will not be able to learn well in my mathematics course.",
    "I feel stressed when listening to mathematics instructors in class.",
    "I believe I will be able to use mathematics in my future career when needed.",
    "I worry that I do not know enough mathematics to do well in future mathematics courses.",
    "I am afraid to give an incorrect answer during my mathematics class.",
    "I feel confident enough to ask questions in my mathematics class.",
    "I get nervous when asking questions in class.",
    "I believe I can complete all of the assignments in a mathematics course.",
    "I worry that I will not be able to complete every assignment in a mathematics course.",
]


def _make_scale_table(items, col_prefix, row, start=1):
    scale_rows = []
    has_data = False
    for i, item_text in enumerate(items, start=start):
        rating_col = f"rating_{col_prefix}_{i}"
        why_col    = f"why_{col_prefix}_{i}"
        score = str(row[rating_col]) if rating_col in row and pd.notna(row[rating_col]) else "—"
        why   = str(row[why_col])    if why_col    in row and pd.notna(row[why_col])    else "—"
        if score != "—" or why != "—":
            has_data = True
        scale_rows.append({
            "Item":        f"{col_prefix.upper()}-{i}",
            "Statement":   item_text,
            "Explanation": why,
            "Score":       score,
        })
    if not has_data:
        return pn.pane.Markdown(
            "_⚠️ No data available for this persona on this scale._",
            sizing_mode="stretch_width",
        )
    return pn.widgets.Tabulator(
        pd.DataFrame(scale_rows),
        sizing_mode="stretch_width",
        show_index=False,
        theme="default",
        pagination=None,
        layout="fit_columns",
        disabled=True,
        stylesheets=[TABLE_CSS, FIRST_COL_BOLD_CSS],
        configuration={
            "columnDefaults": {"headerWordWrap": True, "headerSort": False},
            "columns": [
                {"field": "Item",        "widthGrow": 1},
                {"field": "Statement",   "widthGrow": 4, "formatter": "textarea"},
                {"field": "Explanation", "widthGrow": 4, "formatter": "textarea"},
                {"field": "Score",       "widthGrow": 1, "hozAlign": "left"},
            ],
        },
    )


def build_psy_scales(row):
    # Active scale tracker
    active = pn.widgets.RadioButtonGroup(
        options=[
            "Self-Efficacy MAES",
            "Self-Efficacy MSEAQ",
            "Anxiety AMAS",
            "Anxiety MSEAQ",
        ],
        value="Self-Efficacy MAES",
        button_type="primary",
        sizing_mode="stretch_width",
        stylesheets=[
            f"""
            :host {{ display:flex !important; }}
            :host .bk-btn-group {{
                display:flex !important; gap:8px !important; width:100%;
            }}
            :host .bk-btn {{
                flex:1 1 auto; margin:0 !important;
                border-radius:8px !important;
                border:1px solid {ACCENT} !important;
                font-weight:600 !important;
                background:#ffffff !important; color:{ACCENT} !important;
            }}
            :host .bk-btn.bk-active {{
                background:{ACCENT} !important; color:#ffffff !important;
            }}
            """
        ],
    )

    # Pre-build all 4 tables
    tables = {
        "Self-Efficacy MAES":  _make_scale_table(MAES_ITEMS,       "maes",  row, start=1),
        "Self-Efficacy MSEAQ": _make_scale_table(MSEAQ_ITEMS[:7],  "mseaq", row, start=1),
        "Anxiety AMAS":        _make_scale_table(AMAS_ITEMS,       "amas",  row, start=1),
        "Anxiety MSEAQ":       _make_scale_table(MSEAQ_ITEMS[7:],  "mseaq", row, start=8),
    }

    content = pn.Column(tables["Self-Efficacy MAES"], sizing_mode="stretch_width")

    def _on_switch(event):
        content.objects = [tables[event.new]]

    active.param.watch(_on_switch, "value")

    return pn.Column(
        description(
            "**Psychometric Scales** — MAES (math self-efficacy, 9 items), "
            "AMAS (math anxiety, 9 items), MSEAQ self-efficacy (items 1–7) "
            "and anxiety (items 8–28). Ratings on a 1–5 Likert scale."
        ),
        active,
        content,
        sizing_mode="stretch_width",
        styles=card_styles(),
    )




MSESR_QUESTIONS = [
    "In a certain triangle, the shortest side is 6 inches. The longest side is twice as long as the shortest side, and the third side is 3.4 inches shorter than the longest side. What is the sum of the three sides in inches?",
    "About how many times larger than 614,360 is 30,668,000?",
    "There are three numbers. The second is twice the first and the first is one-third of the other number. Their sum is 48. Find the largest number.",
    "Five points are on a line. T is next to G. K is next to H. C is next to T. H is next to G. Determine the positions of the points along the line.",
    "If y = 9 + x/5, find x when y = 10.",
    "A baseball player got two hits for three times at bat. This could be represented by 2/3. Which decimal most closely represents this?",
    "If P = M + N, which of the following will be true? (a) N = P − M  (b) P − N = M  (c) N + M = P.",
    "The hands of a clock form an obtuse angle at ____ o'clock.",
    "Bridget buys a packet containing 9-cent and 13-cent stamps for $2.65. If there are 25 stamps in the packet, how many are 13-cent stamps?",
    "On a certain map, 7/8 inch represents 200 miles. How far apart are two towns whose distance apart on the map is 3 half inches?",
    "Fred's bill for some household supplies was $13.64. If he paid for the items with a $20 bill, how much change should he receive?",
    "Some people suggest that the following formula be used to determine the average weight for boys between the ages of 1 and 7: W = 17 + 5A, where W is weight in pounds and A is age in years. According to this formula, for each year older a boy gets, should his weight become more or less, and by how much?",
    "Five spelling tests are to be given to Mary's class. Each test has a value of 25 points. Mary's average for the first four tests is 15. What is the highest possible average she can have on all five tests?",
    "Compute: 3 4/5 − 1/2.",
    "In an auditorium, the chairs are usually arranged so that there are x rows and y seats in a row. For a popular speaker, an extra row is added and an extra seat is added to every row. Multiply (x + 1)(y + 1).",
    "A ferris wheel measures 80 feet in circumference. The distance on the circle between two of the seats is 10 feet. Find the measure in degrees of the central angle whose rays support the two seats.",
    "Set up the problem needed to find the number in the expression 'six less than twice 4 5/6'.",
    "Two triangles are similar. The corresponding sides are proportional and AC / BD = XZ / YZ. If AC = 1.7, BC = 2, and XZ = 5.1, find YZ.",
]

MSESR_CORRECT_ANSWERS = {
    1: "C", 2: "C", 3: "D", 4: "A", 5: "C",
    6: "D", 7: "E", 8: "D", 9: "C", 10: "D",
    11: "C", 12: "D", 13: "C", 14: "B", 15: "C",
    16: "D", 17: "B", 18: "E",
}

def build_quizzes(row):
    quiz_rows = []
    for i in range(1, 19):
        chosen     = str(row[f"chosen_option_{i}"])    if f"chosen_option_{i}"    in row and pd.notna(row[f"chosen_option_{i}"])    else "—"
        reasoning  = str(row[f"reasoning_{i}"])        if f"reasoning_{i}"        in row and pd.notna(row[f"reasoning_{i}"])        else "—"
        confidence = str(row[f"confidence_score_{i}"]) if f"confidence_score_{i}" in row and pd.notna(row[f"confidence_score_{i}"]) else "—"
        correct    = MSESR_CORRECT_ANSWERS[i]
        result     = "✅" if chosen == correct else "❌"
        quiz_rows.append({
            "Q":          i,
            "Question":   MSESR_QUESTIONS[i - 1],
            "Chosen":     chosen,
            "Correct":    correct,
            "Result":     result,
            "Confidence": confidence,
            "Reasoning":  reasoning,
        })

    table = pn.widgets.Tabulator(
        pd.DataFrame(quiz_rows),
        sizing_mode="stretch_width",
        show_index=False,
        theme="default",
        pagination=None,
        layout="fit_columns",
        disabled=True,
        stylesheets=[TABLE_CSS, FIRST_COL_BOLD_CSS],
        configuration={
            "columnDefaults": {"headerWordWrap": True, "headerSort": False},
            "columns": [
                {"field": "Q",          "widthGrow": 1,  "hozAlign": "left"},
                {"field": "Question",   "widthGrow": 4,  "formatter": "textarea"},
                {"field": "Chosen",     "widthGrow": 1},
                {"field": "Correct",    "widthGrow": 1},
                {"field": "Result",     "widthGrow": 1},
                {"field": "Confidence", "widthGrow": 1,  "hozAlign": "left"},
                {"field": "Reasoning",  "widthGrow": 4,  "formatter": "textarea"},
            ],
        },
    )
    return pn.Column(
        description(
            "**Problem Solving (MSESR)** — 18 multiple-choice math problems. "
            "Each row shows the question, the persona's chosen answer, the correct answer, "
            "whether it was correct, the confidence rating (1–5), and the free-text reasoning."
        ),
        table,
        sizing_mode="stretch_width",
        styles=card_styles(),
    )

def render_persona_card(row):
    """Render the header card summarising one persona's traits."""
    if row is None:
        return ""

    def has(c):
        return c in row and pd.notna(row[c]) and str(row[c]).strip() not in ("nan", "")

    def li(c):
        return f'<li style="margin:3px 0;"><b>{c.replace("_", " ").title()}:</b> {row[c]}</li>'

    meta = "  ·  ".join(
        f"<b>{c.replace('_', ' ').title()}:</b> {row[c]}"
        for c in FILTER_GROUPS["LLMs / Modality"]
        if has(c)
    )
    columns = ""
    for group, color in GROUP_COLORS.items():
        items = "".join(li(c) for c in FILTER_GROUPS[group] if has(c))
        # Group title: bumped from .72rem to .88rem so the bold (700) actually
        # reads as bold — at the previous size the uppercase + colored text
        # looked thin despite the weight setting.
        columns += (
            '<div style="flex:1 1 200px;min-width:200px;">'
            f'<div style="font-size:.84rem;font-weight:800;text-transform:uppercase;'
            f"letter-spacing:.5px;color:{color};border-bottom:2px solid {color};"
            f'padding-bottom:4px;margin-bottom:8px;">{group}</div>'
            f'<ul style="margin:0;padding-left:18px;list-style:disc;color:{TEXT};">{items}</ul>'
            "</div>"
        )
    return (
        '<div style="display:flex;gap:14px;align-items:center;margin-bottom:12px;">'
        '<div style="font-size:2.4rem;line-height:1;">👤</div>'
        f'<div style="font-size:.95rem;color:{TEXT};">{meta}</div></div>'
        f'<div style="display:flex;gap:28px;flex-wrap:wrap;">{columns}</div>'
    )


def build_topics(row):
    rows = []
    for name in TOPIC_OPTIONS:
        tcol = TOPIC_COLS[name]
        text = str(row[tcol]) if tcol in row and pd.notna(row[tcol]) else "—"
        rows.append(
            {"Topic": name, "Question": TOPIC_QUESTIONS[name], "Response": text}
        )
    table = pn.widgets.Tabulator(
        pd.DataFrame(rows),
        sizing_mode="stretch_width",
        show_index=False,
        theme="default",
        pagination=None,
        layout="fit_columns",
        disabled=True,
        stylesheets=[TABLE_CSS, FIRST_COL_BOLD_CSS],
        configuration={
            "columnDefaults": {"headerWordWrap": True, "headerSort": False},
            "columns": [
                {"field": "Topic", "widthGrow": 1, "formatter": "textarea"},
                {"field": "Question", "widthGrow": 2, "formatter": "textarea"},
                {"field": "Response", "widthGrow": 4, "formatter": "textarea"},
            ],
        },
    )
    return pn.Column(
        description(
            "**Topic Responses** — Six open-ended mental-health questions (family "
            "support, medications, professional help, stigma, AI psychologists, OCD "
            "symptoms), each answered in a short first-person reply (~50–80 words) "
            "shaped by the persona's traits."
        ),
        table,
        sizing_mode="stretch_width",
        styles=card_styles(),
    )



def build_networks(row):
    active = pn.widgets.RadioButtonGroup(
        options=["Edge List", "Valence"],
        value="Edge List",
        button_type="primary",
        sizing_mode="stretch_width",
        stylesheets=[
            f"""
            :host {{ display:flex !important; }}
            :host .bk-btn-group {{
                display:flex !important; gap:8px !important; width:100%;
            }}
            :host .bk-btn {{
                flex:1 1 auto; margin:0 !important;
                border-radius:8px !important;
                border:1px solid {ACCENT} !important;
                font-weight:600 !important;
                background:#ffffff !important; color:{ACCENT} !important;
            }}
            :host .bk-btn.bk-active {{
                background:{ACCENT} !important; color:#ffffff !important;
            }}
            """
        ],
    )

    # ── Edge List ─────────────────────────────────────────────────────────
    def build_edge_table():
        raw = row["edges"] if "edges" in row else None
        edges = []
        if isinstance(raw, (list, tuple, np.ndarray)) and len(raw) > 0:
            edges = [(str(e[0]), str(e[1])) for e in raw]

        if not edges:
            return pn.pane.Markdown("_No edge list available._")

        lines = "\n".join(f"- **{e[0]}** - {e[1]}" for e in edges)
        return pn.pane.Markdown(lines, sizing_mode="stretch_width")
        
    


# ── Valence ───────────────────────────────────────────────────────────
    def build_valence_table():
        def as_list(name):
            v = row[name] if name in row else None
            if v is None or (isinstance(v, float) and pd.isna(v)):
                return []
            return list(v)

        # Pair every word in `edges` with its valence: edge i = [cue, assoc],
        # cue_valences[i] is the cue's valence, assoc_valences[i] the assoc's.
        # `seen` = {word: valence}, keeping the first occurrence of each word.
        seen = {}
        for pair, cv, av in zip(as_list("edges"),
                                as_list("cue_valences"),
                                as_list("assoc_valences")):
            for word, val in ((str(pair[0]), cv), (str(pair[1]), av)):
                if word not in seen and pd.notna(val):
                    seen[word] = val

        if not seen:
            return pn.pane.Markdown("_No valence data available._")

        # Group words by valence
        groups = {1: [], 0: [], -1: []}
        for w, v in seen.items():
            groups.setdefault(int(v), []).append(w)

        # Split each group over two columns (first half / second half)
        def two_cols(words):
            half = (len(words) + 1) // 2
            return words[:half], words[half:]

        pos1, pos2 = two_cols(groups.get(1, []))
        neu1, neu2 = two_cols(groups.get(0, []))
        neg1, neg2 = two_cols(groups.get(-1, []))

        # Pad all columns to the same length
        n = max(len(pos1), len(neu1), len(neg1), 1)
        pad = lambda L: L + [""] * (n - len(L))

        df_v = pd.DataFrame({
            "pos_1": pad(pos1), "pos_2": pad(pos2),
            "neu_1": pad(neu1), "neu_2": pad(neu2),
            "neg_1": pad(neg1), "neg_2": pad(neg2),
        })

        # COL_BG = {
        #     "pos_1": "#f3eafe", "pos_2": "#f3eafe",   # very light purple
        #     "neu_1": "#ededed", "neu_2": "#ededed",   # light gray
        #     "neg_1": "#fdecea", "neg_2": "#fdecea",   # light red
        # }
        COL_BG = {
            "pos_1": "#648FFF", "pos_2": "#648FFF",   # darker purple
            "neu_1": "#ededed", "neu_2": "#ededed",   # light gray
            "neg_1": "#f1948a", "neg_2": "#f1948a",   # darker red
        }

        tab = pn.widgets.Tabulator(
            df_v,
            titles={
                "pos_1": "Positive", "pos_2": "Positive",
                "neu_1": "Neutral",  "neu_2": "Neutral",
                "neg_1": "Negative", "neg_2": "Negative",
            },
            sizing_mode="stretch_width",
            show_index=False,
            theme="default",
            pagination=None,
            layout="fit_columns",
            disabled=True,
            stylesheets=[TABLE_CSS],
        )
        tab.style.apply(
            lambda col: [
                f"background-color: {COL_BG[col.name]}" if v != "" else ""
                for v in col
            ],
            axis=0,
        )
        return tab

    tables = {
        "Edge List": build_edge_table(),
        "Valence":   build_valence_table(),
    }

    content = pn.Column(tables["Edge List"], sizing_mode="stretch_width")

    def _on_switch(event):
        content.objects = [tables[event.new]]

    active.param.watch(_on_switch, "value")

    return pn.Column(
        description(
            "**Behavioral forma mentis networks** — Semantic association network built "
            "from cue words. Edge List shows all word pairs of the behavioral forma mentis networks"
            "belong to the selected persona; "
            "Valence shows sentiment polarity of each node in the network."
        ),
        active,
        content,
        sizing_mode="stretch_width",
        styles=card_styles(),
    )


BUILDERS = {
    "Topics":      build_topics,
    "Psy. Scales": build_psy_scales,
    "Networks":    build_networks,
    "Quizzes":     build_quizzes,
}



