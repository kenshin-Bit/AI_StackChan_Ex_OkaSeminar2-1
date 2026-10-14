from pathlib import Path
import json, re, hashlib

root=Path(__file__).resolve().parent
sources=['original.md','oka.md','matsuda.md','comparison.md']
before={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in sources}
data=json.loads((root/'comparison_data.json').read_text(encoding='utf-8'))
base=(root/'original.md').read_text(encoding='utf-8-sig').splitlines()
oka_ids={1,2,3,4,8,9,12,13,14,15,18,19,21,22,23,24,28,31,32,33,34,36,37,38,46,47,66,102,104}
parts=[]; cursor=0
for r in data:
    a,b=r['start']-1,r['end']
    assert '\n'.join(base[a:b]) == r['original']
    parts.extend(base[cursor:a])
    selected=r['oka'] if int(r['id'][1:]) in oka_ids else r['matsuda']
    parts.extend(selected.split('\n') if selected else [])
    cursor=b
parts.extend(base[cursor:])
text='\n'.join(parts)+'\n'

def replace(old,new,count=1):
    global text
    assert text.count(old)==count, (old,text.count(old),count)
    text=text.replace(old,new)

# C02 takes precedence over the SD-related parts of C05 and C07.
text='\n'.join(line for line in text.split('\n') if not line.startswith(('| microSDカード |','| SDカードリーダー |')))
replace('| **microSDカードの差し込み口（顔の下面）** | 設定ファイルを入れるカードを挿します |',
        '| **microSDカードの差し込み口（顔の下面）** | 今回は使いません（設定は本体の中に直接書き込みます） |')
# C07 calls the reset location the underside of the face; C09 supplies its operation.
replace('底面のリセットボタン','顔の下面のリセットボタン',2)
replace('| **側面のボタン** | 電源のオン/オフ |','| **電源ボタン（左側面）** | 電源のオン/オフ |')
replace('側面のボタンを**短く押す**','左側面の電源ボタンを**短く押す**')
replace('側面のボタンを**長く押す**','左側面の電源ボタンを**長く押す**')

# Retain the classroom Wi-Fi policy while adopting the direct-write workflow.
replace('| 学校・展示会場で | ログイン画面が出て使えない | **問題なく使える** |',
        '| 学校・展示会場で | MSU Wi-Fiはログイン画面が出て使えない | **問題なく使える** |')
replace('## 5-2. 自分のスマホのテザリングを使うべき理由',
        '## 5-2. 自分のスマホのテザリングを使うべき理由\n\n授業中と、授業と同じWi-Fiを用意するデモ会場では、授業が提供するWi-Fiを使えます。以下は、自分で別の場所でも使う場合の説明です。')
replace('## 5-3. 専用のネットワーク名（SSID）を決めておくと、もっと楽になる',
        '## 5-3. 専用のネットワーク名（SSID）を決めておくと、もっと楽になる\n\n以下は、スマホのテザリングを使う場合の工夫です。授業が提供するWi-Fiを使う場合は、そのSSIDとパスワードを設定してください。')
replace('大学のWi-Fiは、つなぐとブラウザでログイン画面が出るタイプ',
        '大学のMSU Wi-Fiは、つなぐとブラウザでログイン画面が出るタイプ')
replace('設定ファイルを書き換える→本体に書き込み直す→戻す',
        '設定ファイルを書き換える→本体に書き込み直す')
replace('3. 開いて、`********` のうち**3か所だけ**書き換える',
        '3. 開いて、`********` のうち**3か所だけ**書き換える\n\n授業で提供するWi-FiのSSIDとパスワードは、Moodle一番上の「一般」トピックに掲載しています。授業中はその値を使い、テザリングを使う場合は自分のスマホの値を使ってください。')
replace('  ssid: "********"        ← テザリングのネットワーク名',
        '  ssid: "********"        # 授業Wi-Fiまたはテザリングのネットワーク名')
replace('  password: "********"    ← テザリングのパスワード',
        '  password: "********"    # 使用するWi-Fiのパスワード')
replace('  aiservice: "********"   ← 第4章で取得したAPIキー',
        '  aiservice: "********"   # 第4章で取得したAPIキー')
replace('| `ssid` | スマホのテザリングのネットワーク名 |',
        '| `ssid` | 授業Wi-Fiまたはスマホのテザリングのネットワーク名 |')
replace('| `password` | テザリングのパスワード |',
        '| `password` | 使用するWi-Fiのパスワード |')
# References that are part of the adopted workflow.
replace('| 6 | **1回目のビルド**（時間がかかります） | 第9章 9-1 | ビルドが成功した |',
        '| 6 | **1回目のビルド**（時間がかかります） | 第9章 9-1 | ビルドが成功した |')
replace('| 14 | 人に見せる準備・発表の用意 | 第6章 | — |',
        '| 14 | 人に見せる準備・発表の用意 | 第16章 | — |')
replace('第18章・第18章の用語集','第18章の用語集')
replace('| ② | スマホのテザリングを準備 | 5分 | |',
        '| ② | 授業Wi-Fiまたはスマホのテザリングを準備 | 5分 | |')
replace('| 3 | Wi-Fi（テザリング）の準備 | 第5章 | スマホ経由でネットに接続できる（ただし、授業中は別途Wi-Fiを提供する予定です） |',
        '| 3 | Wi-Fiの準備 | 第5章 | 授業Wi-Fiまたはスマホのテザリングでネットに接続できる |')

# C12: keep the reported figures without assigning the measurement to an unconfirmed stage.
notice=('> **【要確認：松田君】初期設定・初回ビルドの実測値について**\n'
        '> 改訂前の記録には「12分40秒・約800MB」とありますが、**拡張機能（PlatformIO）の初期設定と初回ビルドの、どちらを測った値かは未確認**です。\n'
        '> **松田君に対象工程の確認が必要です。** 確認が取れるまで、各工程の確定した所要時間・ダウンロード量としては扱わないでください。')
replace('初回のビルドでは、**部品が自動で約800MBダウンロードされます**（実測12分40秒）。',
        '初回のビルドでは、**必要な部品が自動でダウンロードされます。**\n\n'+notice)
replace('> **⑤は約800MBのダウンロードです**（実測12分40秒）。**2回目からは30秒**で終わります。',
        '> **⑤の初回ビルドには時間がかかります。** 2回目からは数十秒〜1分ほどが目安です。\n> **【要確認：松田君】「12分40秒・約800MB」の対象工程は未確認です。授業の進め方の注記を参照してください。**')
replace('| ⑤ | **1回目のビルド**（部品の自動取得） | **15分** | **★待つだけだが長い** |',
        '| ⑤ | **1回目のビルド**（部品の自動取得） | **約15分（暫定。下の要確認注記を参照）** | **★待つだけだが長い** |')
old=('6. 初回は裏で必要な部品を自動ダウンロードします。**15分ほどかかります**（気長に待ってください）\n\n'
     '> **⚠️ 初回だけ、とても時間がかかります。**\n'
     '> **実測で12分40秒、ダウンロード量は約800MB**でした（1台だけ・空いている回線での値）。\n'
     '> **複数の班が同時にやると、回線を分け合うのでさらに伸びます。**\n>\n'
     '> 画面が止まって見えても**失敗ではありません。** 最後に `[SUCCESS]` が出るまで待ってください。\n'
     '> **2回目からは30秒ほどで終わります。**')
replace(old,'6. 初回は裏で必要な部品を自動ダウンロードします。完了するまで気長に待ってください。\n\n'
        '> **⚠️ 初回だけ、時間がかかります。** 複数の班が同時にやると、回線を分け合うのでさらに伸びます。\n\n'+notice+'\n\n'
        '> `[SUCCESS]` によるビルド完了の確認は、第9章で行います。')
replace('| ② | **プログラム** | 初回は約15分、2回目からは約1分 |',
        '| ② | **プログラム** | 初回は約15分（暫定。下の要確認注記を参照）、2回目からは約1分 |')
replace('初回のプログラムは**15分ほど**かかります（実測12分40秒）。2回目以降は1分ほどです。',
        '初回のプログラムのビルド・書き込みは**約15分を暫定の目安**としてください。2回目以降は1分ほどです。\n\n'+notice)
# The schedule requires a separate first build before preparing settings.
replace('## 9-2. 書き込む（2段階）',
        '### 初回ビルドだけを先に行う場合（授業6回目）\n\n'
        'PowerShellで次を実行します。これはプログラムを作る作業だけで、本体への書き込みは行いません。\n\n'
        '```powershell\n& "$env:USERPROFILE\\.platformio\\penv\\Scripts\\pio.exe" run -e m5stack-cores3-realtime -d "C:\\stackchan\\firmware"\n```\n\n'
        '最後に `[SUCCESS]` と出れば、ビルド成功です。設定ファイルは第8章で準備し、初めて本体に書き込むときは、次の①と②を両方行ってください。\n\n'
        '## 9-2. 書き込む（2段階）')
# C27 applies to an agent with file access, distinct from the chat guidance.
replace('設定ファイルはパソコンの中にあるので、**CodexやClaudeなどのAIに、直接書いてもらえます。**\n自分で一から書かなくても大丈夫です。',
        'ここでは、**作業フォルダへのアクセスを許可し、ファイルを編集できるAI環境**（CodexやClaudeなど）を使います。\n'
        'その環境なら、設定ファイルをAIに直接書いてもらえます。自分で一から書かなくても大丈夫です。\n'
        '冒頭で説明した、マニュアルを添付して質問するだけのチャットとは使い方が異なります。')
# Apply the adopted classroom network policy to later operational instructions as well.
replace('| テザリングがつながるか | 画面が「じゅんび中」のままでないか |',
        '| 授業Wi-Fiまたはテザリングがつながるか | 画面が「じゅんび中」のままでないか |')
replace('| 「じゅんび中」から進まない | スマホのテザリングがONか確認 |',
        '| 「じゅんび中」から進まない | 使用するWi-Fiを確認。授業Wi-Fiならルータ、テザリングならスマホの共有がONか確認 |')
replace('| 「ネットが切断」と出る | 同上。スマホの画面を一度点ける |',
        '| 「ネットが切断」と出る | 使用するWi-Fiを確認。テザリングならスマホの画面を一度点ける |')
replace('スマホのテザリングが切れている | **テザリングを戻せば、10秒ごとに自動でつなぎ直します。**',
        'Wi-Fi（授業Wi-Fiまたはテザリング）が切れている | **Wi-Fiを戻せば、10秒ごとに自動でつなぎ直します。**')
replace('| `Successfully connected to Wi-Fi` | ○ テザリング接続に成功 |',
        '| `Successfully connected to Wi-Fi` | ○ Wi-Fi接続に成功 |')
replace('| `Start Smart Config` | × Wi-Fiにつながっていない。テザリング・設定ファイル・①を確認 |',
        '| `Start Smart Config` | × Wi-Fiにつながっていない。授業Wi-Fiまたはテザリング・設定ファイル・①を確認 |')
replace('| 「ネットが切断」と出る | テザリングがOFF／設定が違う |',
        '| 「ネットが切断」と出る | Wi-Fi（授業Wi-Fiまたはテザリング）が使えない／設定が違う |')

# C32: collapse redundant separators, including around the added appendix.
while re.search(r'\n---\n\s*\n---\n',text):
    text=re.sub(r'\n---\n\s*\n---\n','\n---\n',text)
out=root/'merged.md'
assert not out.exists(), 'Do not overwrite an existing merged manual.'
out.write_text(text,encoding='utf-8')
assert before=={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in sources}
assert text.count('```')%2==0
assert text.count('# 第8章')==1
assert 'Copy-to-SD' not in text and '/yaml/' not in text and '/app/AiStackChanEx/' not in text
assert '底面のリセットボタン' not in text
assert text.count('【要確認：松田君】')==4
print(f'Created {out}: {len(text.splitlines())} lines; sources unchanged; 4 C12 notices.')
