import streamlit as st

st.set_page_config(
    page_title="生徒評価シート作成",
    page_icon="📝",
    layout="wide",
)

# =========================================================
# デザイン
# =========================================================
st.markdown("""
<style>
    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1 {
        font-size: 2rem !important;
        margin-bottom: 0.2rem !important;
    }

    h3 {
        margin-top: 0.7rem !important;
        margin-bottom: 0.5rem !important;
    }

    .main-title {
        padding: 1.2rem 1.4rem;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        margin-bottom: 1.4rem;
    }

    .main-title h2 {
        margin: 0;
        font-size: 1.7rem;
    }

    .main-title p {
        margin: 0.35rem 0 0 0;
        opacity: 0.7;
    }

    .section-label {
        font-size: 1.05rem;
        font-weight: 700;
        margin-top: 0.4rem;
        margin-bottom: 0.2rem;
    }

    div[data-testid="stTextArea"] textarea {
        line-height: 1.7;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# 基本データ
# =========================================================

FLOW = {
    "英語": [
        "① 宿題の確認",
        "② 宿題の解説",
        "③ 単語テスト（宿題で単語を出した場合のみ）",
        "④ 使用テキストを用いた先取り学習",
        "⑤ 宿題の提示",
    ],
    "数学": [
        "① 宿題の確認",
        "② 宿題の解説",
        "③ 使用テキストを用いた先取り学習",
        "④ 宿題の提示",
    ],
}

GOALS = [
    "定期テストで高得点を目指す",
    "定期テストで平均点以上を目指す",
    "学校内容の基礎を身につける",
]

TEXTBOOKS = {
    "小学生": [
        "エフォート",
        "ほーぷ",
        "コア",
    ],
    "中学生": [
        "iワーク",
        "Sirius",
    ],
    "高校生": [
        "学校のテキスト",
    ],
}


# =========================================================
# 評価項目
# A = とても良い
# B = 良い
# C = 普通
# D = 課題あり
# =========================================================

OPTIONS = {

    "理解力": {
        "A：理解が早く、自分で整理できる":
            "理解が早く、授業内容を自分で整理しながら進める力がついています。",

        "B：説明後は安定して理解できる":
            "説明を聞いた後は内容をしっかり理解でき、基本問題にも安定して取り組めています。",

        "C：確認しながら進めると理解できる":
            "確認を行いながら進めることで理解できており、できる問題も少しずつ増えています。",

        "D：理解に時間がかかることが多い":
            "難しい内容でも投げ出さずに取り組めており、一つずつ確認しながら理解を深めています。",
    },


    "記憶定着（復習）": {
        "A：以前の内容もよく覚えている":
            "以前に学習した内容もしっかり定着しており、新しい問題にも活用できています。",

        "B：覚えている内容が多い":
            "以前の内容も比較的よく覚えており、必要な知識を使いながら問題に取り組めています。",

        "C：復習すると内容を思い出せる":
            "復習を行うことで以前の内容を思い出すことができ、そこから問題に取り組めています。",

        "D：時間が空くと忘れやすい":
            "一度学習した内容でも時間が空くと忘れることがあるため、繰り返し確認しながら定着を進めています。",
    },


    "応用・混合への対応": {
        "A：応用問題にも対応できる":
            "基本問題だけでなく、形が変わった問題や応用問題にも対応できています。",

        "B：基本問題は安定して解ける":
            "基本問題は安定して解けており、応用問題にも少しずつ対応できるようになっています。",

        "C：応用問題は確認しながら解ける":
            "基本的な内容は理解できており、応用問題では確認を行いながら取り組めています。",

        "D：応用・混合問題で迷うことが多い":
            "基本内容を確認しながら進めていますが、応用問題や複数単元が混ざる問題では迷う場面が見られます。",
    },


    "宿題": {
        "A：毎回安定して取り組めている":
            "宿題にも毎回安定して取り組めており、学習習慣がしっかり身についています。",

        "B：概ね取り組めている":
            "宿題にも概ね取り組めており、継続して学習することができています。",

        "C：取り組みに少しムラがある":
            "宿題には取り組めていますが、日によって量に差があるため、より安定して続けられるようにしていきたいです。",

        "D：未実施・残ることが多い":
            "宿題が残ることもありますが、授業内ではできるところから取り組もうとする姿勢が見られます。",
    },


    "授業態度": {
        "A：集中して自分から取り組める":
            "授業中の集中が安定しており、自分から問題に取り組む姿勢が見られます。",

        "B：概ね集中して取り組める":
            "授業中も概ね集中しており、前向きに学習へ取り組めています。",

        "C：声かけがあると集中できる":
            "集中に波はありますが、声かけを行うことで学習に戻り、取り組むことができています。",

        "D：集中が切れることが多い":
            "集中が切れてしまう場面もありますが、声かけを行いながら少しずつ学習時間を伸ばしています。",
    },


    "単語": {
        "A：よく覚えられている":
            "単語もよく覚えられており、文法や読解でも活用できています。",

        "B：概ね覚えられている":
            "単語も概ね覚えられており、少しずつ語彙が増えています。",

        "C：覚えている単語にばらつきがある":
            "覚えられている単語も増えていますが、まだ定着にばらつきがあります。",

        "D：単語暗記に苦戦している":
            "単語はまだ覚えるのに苦戦する場面があるため、繰り返し確認しながら定着を進めています。",
    },
}


# =========================================================
# 生徒の個性
# =========================================================

STYLES = {
    "コツコツ型":
        "一つひとつの内容を丁寧に積み重ねながら取り組めるところが良い点です。",

    "慎重型":
        "すぐに答えを出すのではなく、自分で確認しながら慎重に進められています。",

    "自発型":
        "分かった内容は自分から次の問題へ進もうとする姿勢が見られます。",

    "会話しながら理解する型":
        "やり取りをしながら考えを整理すると理解が深まりやすく、積極的に授業へ参加できています。",

    "声かけで伸びる型":
        "声かけやヒントをきっかけに集中力が高まり、そこから自分で進められる場面が増えています。",

    "波はあるが前向き型":
        "日によって集中に波はありますが、授業では前向きに取り組もうとする姿勢が見られます。",

    "粘り強い型":
        "すぐに答えが出ない問題でも、諦めずに考え続けられるところが良い点です。",
}


# =========================================================
# メッセージ
# =========================================================

PARENT_MSG = (
    "宿題の取り組みに少し波が見られるため、"
    "ご家庭でも取り組む時間について声をかけていただけると助かります。"
)

STAFF_MSG = (
    "宿題ができていない日があれば、"
    "授業前後に取り組み状況について少し声をかけてもらえると助かります。"
)


# =========================================================
# 関数
# =========================================================

def select_option(label, index=1):
    choices = list(OPTIONS[label].keys())
    choice = st.selectbox(label, choices, index=index)
    return choice, OPTIONS[label][choice]


def build_plan(goal, homework_choice, retention_choice, application_choice):

    if "高得点" in goal:
        first = (
            "授業内で解き方だけでなく考え方まで整理し、"
            "間違えた問題は理由を確認した上で解き直します。"
        )

    elif "平均点" in goal:
        first = (
            "基本問題で取りこぼしが出ないよう、"
            "授業内で理解を確認しながら苦手な部分を早めに修正します。"
        )

    else:
        first = (
            "基本事項を一つずつ確認しながら、"
            "自力で解ける問題を少しずつ増やしていきます。"
        )

    if retention_choice.startswith("A"):
        review = (
            "現在の定着を維持するため、"
            "授業のはじめに短い確認問題を取り入れます。"
        )

    elif retention_choice.startswith("B"):
        review = (
            "以前の内容も定期的に確認し、"
            "忘れかけている部分をその都度復習します。"
        )

    elif retention_choice.startswith("C"):
        review = (
            "授業のはじめに短い復習を取り入れ、"
            "前回内容を思い出してから新しい内容へ進みます。"
        )

    else:
        review = (
            "毎回の授業で以前の内容を少しずつ取り入れ、"
            "繰り返し確認することで定着を進めます。"
        )

    if application_choice.startswith("A"):
        application = (
            "今後はさらに幅広い問題に触れ、"
            "安定して得点できる力を伸ばしていきます。"
        )

    elif application_choice.startswith("B"):
        application = (
            "基本問題に加えて少し形を変えた問題にも取り組み、"
            "応用力を伸ばしていきます。"
        )

    elif application_choice.startswith("C"):
        application = (
            "基本問題を確認した後に応用問題にも取り組み、"
            "自分で解き方を選べるよう練習します。"
        )

    else:
        application = (
            "まず基本問題を確実にした上で、"
            "似た問題から少しずつ応用・混合問題へ広げていきます。"
        )

    if homework_choice.startswith("A"):
        homework = (
            "宿題は現在のペースを続け、"
            "分からなかった問題は次回の授業で確認します。"
        )

    elif homework_choice.startswith("B"):
        homework = (
            "宿題は今の取り組みを継続しながら、"
            "抜けが出ないよう学習ペースを整えていきます。"
        )

    elif homework_choice.startswith("C"):
        homework = (
            "宿題は無理のない量から確実に取り組み、"
            "毎回続ける習慣を整えていきます。"
        )

    else:
        homework = (
            "宿題は量を確認しながら取り組みやすい形に調整し、"
            "まずは毎回取り組む習慣を作っていきます。"
        )

    return " ".join([first, review, application, homework])


def build_report(
    subject,
    grade,
    textbooks,
    goal,
    praise,
    issue,
    plan,
    homework_choice,
):

    textbook_text = "、".join(textbooks) if textbooks else "未選択"

    report = [
        f"【科目】{subject}",
        "",
        "【授業の流れ】",
        *FLOW[subject],
        "",
        "【学年区分】",
        grade,
        "",
        "【使用テキスト】",
        textbook_text,
        "",
        "【目標】",
        goal,
        "",
        "【頑張ったこと・褒めポイント】",
        praise,
        "",
        "【目標達成のための課題】",
        issue,
        "",
        "【課題克服のための具体的な計画】",
        plan,
    ]

    if homework_choice.startswith(("C", "D")):
        report += [
            "",
            "【保護者様にお伝えしたいこと】",
            PARENT_MSG,
            "",
            "【社員に伝えておきたいこと】",
            STAFF_MSG,
        ]

    return "\n".join(report)


# =========================================================
# 画面
# =========================================================

st.markdown("""
<div class="main-title">
    <h2>📝 生徒評価シート作成システム</h2>
    <p>授業での様子を選択すると、保護者・社員共有用の評価文を自動作成します。</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([0.95, 1.05], gap="large")


# =========================================================
# 左：入力
# =========================================================

with left:

    st.subheader("① 基本情報")

    subject = st.radio(
        "科目",
        ["英語", "数学"],
        horizontal=True,
    )

    grade = st.radio(
        "学年区分",
        ["小学生", "中学生", "高校生"],
        horizontal=True,
    )

    textbooks = st.multiselect(
        "使用テキスト",
        TEXTBOOKS[grade],
        default=TEXTBOOKS[grade][:1],
        help="複数使用している場合は複数選択できます。",
    )

    goal = st.selectbox(
        "目標",
        GOALS,
    )

    st.divider()

    st.subheader("② 学習状況")

    understanding_choice, understanding = select_option(
        "理解力"
    )

    retention_choice, retention = select_option(
        "記憶定着（復習）"
    )

    application_choice, application = select_option(
        "応用・混合への対応"
    )

    homework_choice, homework = select_option(
        "宿題"
    )

    attitude_choice, attitude = select_option(
        "授業態度"
    )

    if subject == "英語":
        vocab_choice, vocab = select_option(
            "単語"
        )
    else:
        vocab_choice = ""
        vocab = ""

    st.divider()

    st.subheader("③ 生徒の特徴")

    style_choice = st.selectbox(
        "学習スタイル",
        list(STYLES.keys()),
    )

    style = STYLES[style_choice]

    st.divider()

    st.subheader("④ 補足")

    episode = st.text_area(
        "具体的なエピソード",
        placeholder="例：最近は自分から途中式を書くようになった。",
        height=90,
    )

    result = st.text_area(
        "成果・変化",
        placeholder="例：前回のテストより計算ミスが減った。",
        height=90,
    )


# =========================================================
# 文章生成
# =========================================================

praise_parts = [
    understanding,
    style,
    attitude,
    homework,
]

if vocab:
    praise_parts.append(vocab)

if episode.strip():
    praise_parts.append(episode.strip())

if result.strip():
    praise_parts.append(result.strip())

praise = " ".join(praise_parts)


issue_parts = [
    retention,
    application,
]

if subject == "英語":

    if vocab_choice.startswith("C"):
        issue_parts.append(
            "単語は覚えているものと定着していないものに差があるため、"
            "継続して確認していく必要があります。"
        )

    elif vocab_choice.startswith("D"):
        issue_parts.append(
            "単語の定着が今後の文法・読解にも関わるため、"
            "優先して繰り返し取り組んでいきたいです。"
        )

issue = " ".join(issue_parts)


plan = build_plan(
    goal,
    homework_choice,
    retention_choice,
    application_choice,
)


report = build_report(
    subject,
    grade,
    textbooks,
    goal,
    praise,
    issue,
    plan,
    homework_choice,
)


# =========================================================
# 右：完成文
# =========================================================

with right:

    st.subheader("完成した評価文")

    st.caption(
        "内容を確認し、必要に応じて直接修正してから使用してください。"
    )

    edited_report = st.text_area(
        "評価文",
        value=report,
        height=760,
        label_visibility="collapsed",
    )

    st.download_button(
        "📄 評価文をテキストで保存",
        data=edited_report,
        file_name="生徒評価シート.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.info(
        "A＝とても良い ／ B＝良い ／ C＝標準的 ／ D＝今後の課題あり"
    )

