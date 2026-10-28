# スタックチャン演習：PC安全対策マニュアル（学生用・Windows最終版）

最終版：2026-10-27。WindowsでVS Code・Git・PlatformIOを使う学生向けです。
この文書だけで、PCの更新、接続検査、完了報告まで進められます。  
Macの学生は別途配布するMac版安全対策マニュアルを参照して進めて下さい。MacやLinuxの学生は、以下のWindows用コマンドを流用してはいけません。

## 1．最初に読むこと

### 1-1．今回必要なこと

開発ツールが偽の接続先を信用しないように、証明書に関係する部品を更新し、通信を検査します。
教員側で、スタックチャン本体への修正版の書き込みと動作テストを済ませています。
ただし、教員のPCでの対策は、学生のPCには自動では引き継がれません。

開発で使うPCは1台ずつ、このマニュアルの手順を実施します。2人1組でも、両方のPCを使うなら両方が対象です。  
同じPCでも別のユーザーアカウントや別のPython環境を使う場合はアカウント毎や環境毎にそれぞれ確認が必要です。

### 1-2．対策が済まないうちにしてもよい作業／してはいけない作業

| 作業 | 扱い |
|---|---|
| コード・性格設定の編集、ローカル保存、資料閲覧・レポート | してよい |
| この文書で指定する更新と公開先の接続検査 | 必ずすべて実施する |
| 通常のGit送受信、部品追加、Build・Upload・Upload Filesystem | **このマニュアルの手順7が完了するまでは不可**；手順7まで完了したら可 |
| スタックチャン本体のオンライン音声対話 | **自分のスタックチャン本体に教員配布の修正版（2026年10月25日以降の版）を入れるまでは不可**；修正版が入っていることを確認したら可；**修正版を入れるためにはそれに先立って手順7まで完了している必要** |

ビルドはコードを本体用プログラムに変換する処理ですが、不足部品を自動取得する場合があるため、**修正版のビルドに先立ってPCの対策**が必須です。  
この文書はPCの安全対策を完結させる文書です。本体の初期設定や新規導入を一から行う教科書ではありません。

### 1-3．困ったときの共通ルール

エラーや判断できない表示が出たら、そこで止めてAIや教員に相談します。  
通信エラーを無視する設定（-k、--insecure、--trusted-host、sslVerify false等）に変更してはいけません。  
platformio.iniのライブラリ版・ボード・書き込み速度・SPIFFS指定は変更しません。  
pio pkg update、.pioの削除、Python環境の削除・入れ直しで解決しようとしてはいけません。

### 1-4．準備と対象範囲

インターネットに接続し、既存の授業用プロジェクトを使います。まだツール未導入なら教員に相談します。  
PlatformIO以外にConda・Node.js・WSL・Docker・別のPython等を使っている人は、その名前も教員へ知らせます。  
この文書の対策だけでPC上の全アプリを確認済みとは扱いません。

各コード枠を順にコピーしてEnterで実行します。画面にあるPS C:\...>などの入力欄の印はコピーしません。  
PowerShellとVS Codeのターミナルを使い分ける箇所は、本文の指示に従ってください。

## 2．Windows・ブラウザ・VS Codeを更新する

1. 作業中のファイルを保存する。
2. 「設定」→「Windows Update」→「更新プログラムのチェック」で通常の更新を適用する。
3. 求められたら再起動する。
4. Chromeの画面右上の「3点メニュー」→「ヘルプ」→「Google Chromeについて」、またはEdgeの「ヘルプとフィードバック」→「Microsoft Edgeについて」で更新し、ブラウザを再起動する。
5. VS Codeの画面左下隅の「設定アイコン（歯車）」をクリック→更新確認（Check for Updates...）をクリック→利用可能な更新はないというメッセ―ジが出たらOKを押して完了；自動的に更新が始まったら更新完了を待つ→更新完了したら、VS Codeを再起動する。

学校管理PCで更新できない場合は管理者へ依頼します。ここだけではGit・Pythonの対策は完了しません。

## 3．Git for Windowsを更新する

1. VS Code、Git Bash、GitHub Desktopなど、Gitを使うアプリを閉じる。
2. 更新したブラウザで [Gitの公式ダウンロードページ](https://git-scm.com/install/windows) から最新版をダウンロード。通常のIntel/AMDの64ビットPCでは「Git-2.56.0.3-64-bit.exe」（←今回の問題に対応した版はこれ；これ以降の版もOK）を取得する。ARMのPCはARM64版。
3. ダウンロードしたファイルを実行し、既存設定を引き継いで更新する。アンインストールは不要。
4. 新しくPowerShellを開き、次を実行する。

~~~powershell
git --version
where.exe git
~~~

合格：git version 2.56.0.windows.3、または後継の修正版。
古い版が出る、複数の別のGitが見つかる場合は未確認として教員に相談します。  
**GitHub Desktop等に同梱される別のGit**は、この更新だけで対策済みとは扱いません。**そのアプリも公式更新**し、授業では確認済みのGitを使います。  
**GitHub Desktopの更新方法**：画面上部のメニューから「Help」をクリック→「About GitHub Desktop」をクリック→「Check for Updates」をクリック

## 4．PlatformIOが使うPythonを調べる

VS Code画面左端のPlatformIOアイコン（蟻アイコン）をクリック→画面左側のQuick Access→Miscellaneous→PlatformIO Core CLIを開きます。
見つからなければCtrl+Shift+Pで「PlatformIO: Open PlatformIO Core CLI」を検索します。
開いたターミナルに下記をコピー＆ペーストして、Enterキーを押して実行します。

~~~text
pio system info
~~~

「Python」の版と「Python Executable」のパス（場所）を控えます。ビルドはしません。
Python Executableは、例えば C:\Users\ユーザー名\.platformio\penv\Scripts\python.exe です。
この例ではなく、自分のPCに表示されたパスを控えて使います。

Pythonが3.11以上なら続けます。3.10以下、コマンドが動かない、パスが見つからない場合は止めて教員に相談します。

## 5．そのPythonのpip・certifiを対策する

スタートメニューから通常のPowerShellを開きます。管理者権限は不要。
ここから同じPowerShell画面で進めます。閉じた場合は変数設定をやり直します。
下記をPowerShellにコピー＆ペーストします。

~~~powershell
$pioPython = Read-Host "Python Executableのパスを引用符なしで貼り付けてEnter"
& $pioPython --version
& $pioPython -m pip --version
~~~

入力待ちになったら、手順4の Python Executableのパス を貼り付けてEnterを押します。
pipは部品を取得する道具、certifiは接続先確認用の証明書一覧です。

### 5-1．pipが26.2.2未満の場合だけ更新

26.2.2以上なら、この長いコマンドは飛ばして5-2へ進みます。新しいpipを古い版へ戻さないためです。
26.2.2未満なら、次を丸ごとコピーして実行します。末尾のSHA-256で取得ファイルの一致を確認するコマンドになっています。

~~~powershell
& $pioPython -m pip install "pip @ https://files.pythonhosted.org/packages/3f/06/3e4420302363fbb71be3c7f35ce042f54bfca330e3e66b3a2e3c4cca579f/pip-26.2.2-py3-none-any.whl#sha256=fd7f4dfa8190e014013b9f08f3e973f4e4c26ffd179a204895533a7254813a70"
~~~

正常にインストールが終了したら次に進みます。エラーならここで止め教員に相談します。ハッシュ不一致を無視したり、--trusted-host等を追加したりしてはいけません。

### 5-2．certifiを更新・結果確認

pipの26.2.2以上への更新成功を確認してから（元々26.2.2以上だった場合はそのままで）下記を実行します。

~~~powershell
& $pioPython -m pip install --upgrade "certifi>=2026.10.19"
& $pioPython -m pip --version
& $pioPython -c "import certifi; print(certifi.__version__)"
~~~

合格：pipが26.2.2以上、certifiが2026.10.19以上。  
失敗時は最後の数行を教員に相談します。Python環境を削除・再作成したり、pio pkg updateを実行したりしてはいけません。  
別のPythonも授業で使う場合は、その実行ファイルを$pioPythonに指定して手順5以降を繰り返します。

## 6．正常接続と証明書の拒否を確認する

公開サイトへの検査です。APIキー・パスワード・トークンは不要です。
問題の証明書を使う代表的な2経路を検査します。全攻撃の網羅試験ではありません。
名前解決失敗・時間切れは「未確認」で、証明書拒否の合格とは区別します。

### 6-1．Windows付属curl

まず、下記を実行します。

~~~powershell
& "$env:WINDIR\System32\curl.exe" -I https://github.com/
~~~

HTTP/2 200などのHTTP応答が返ることを確認します。続けて次の2つを実行します。

~~~powershell
& "$env:WINDIR\System32\curl.exe" https://dv-g3b-emudhra.we-have-a-problem.com/
& "$env:WINDIR\System32\curl.exe" https://dv-g3b-aaa-emudhra.we-have-a-problem.com/
~~~

この2つは、証明書の理由で失敗するのが合格です。
例：CERT_E_REVOKED、certificate revoked、証明書チェーンを信頼できない旨のエラー。  
ページ本文を取得できた場合は止めます。-k、--insecure、--ssl-no-revokeは使いません。

### 6-2．実際に使うGit

エクスプローラーで、firmwareの一つ上のプロジェクトフォルダーを開き、アドレス欄のパスをコピーします。続いて、下記を実行し、途中で指示にしたがってコピーしたパスを貼り付けます。

~~~powershell
$projectRoot = Read-Host "プロジェクトのルートのパスを引用符なしで貼り付けてEnter"
Set-Location -LiteralPath $projectRoot
git ls-remote https://github.com/git/git.git HEAD
~~~

通常接続では長い英数字とHEADの表示が合格です。ログインを求められたら入力せず教員に相談します。  
続けて次を実行します。

~~~powershell
git ls-remote https://dv-g3b-emudhra.we-have-a-problem.com/ HEAD
git ls-remote https://dv-g3b-aaa-emudhra.we-have-a-problem.com/ HEAD
~~~

この2つは証明書エラーで失敗するのが合格です。  
repository not foundやHTTP 404だけなら、証明書を拒否した証拠ではありません。未確認として止めます。

### 6-3．PlatformIOのPythonが使う通信

以下を一塊で同じPowerShellへコピーします。実際に使うrequestsで検査します。

~~~powershell
@'
import requests
urls = [
    ('https://github.com/', False),
    ('https://dv-g3b-emudhra.we-have-a-problem.com/', True),
    ('https://dv-g3b-aaa-emudhra.we-have-a-problem.com/', True),
]
passed = 0
for url, must_reject in urls:
    try:
        r = requests.get(url, timeout=20, allow_redirects=False)
    except requests.exceptions.SSLError as exc:
        detail = str(exc).lower()
        ok = must_reject and 'certificate verify failed' in detail.replace('_', ' ')
        result = 'certificate rejected' if ok else 'other TLS error: not confirmed'
    except requests.exceptions.RequestException:
        ok = False
        result = 'network error: not confirmed'
    else:
        ok = not must_reject and 200 <= r.status_code < 400
        result = 'HTTP ' + str(r.status_code)
        r.close()
    print(('PASS' if ok else 'STOP'), url, result)
    passed += int(ok)
raise SystemExit(0 if passed == len(urls) else 1)
'@ | & $pioPython -
~~~

合格：3行ともPASS。  
STOPやrequestsが見つからない等のエラーなら未確認です。
検証を無効にせず教員に相談します。

## 7．確認結果を記録して教員へ報告する

### 7-1．完了チェック

- [ ] Windows・ブラウザ・VS Codeを更新した。
- [ ] 授業で実際に使うGitが修正版である。
- [ ] PlatformIOのPythonの場所と版を確認した。
- [ ] pipが26.2.2以上、certifiが2026.10.19以上。
- [ ] Windows curlで、通常接続成功と問題の2経路の証明書拒否を確認した。
- [ ] Gitでも、通常接続成功と問題の2経路の証明書拒否を確認した。
- [ ] PlatformIOのPythonの検査が3行ともPASS。
- [ ] 別の開発環境を使う場合、教員に伝えてあり、未確認のまま使っていない。

未確認・STOP・時間切れが残る場合は、対策完了とはせず教員に相談します。  
この検査は今回の証明書問題の代表的な経路の確認です。あらゆる攻撃に対する安全保証ではありません。

### 7-2．報告する内容（コピーして記入）

~~~text
PCの呼び名：
Windowsの版：
Gitの版：
PlatformIOのPythonの版：
pipの版：
certifiの版：
Windows curl：通常接続OK／問題の2経路拒否OK／未確認
Git：通常接続OK／問題の2経路拒否OK／未確認
PlatformIO Python：3行PASS／STOP／未確認
ほかに使う開発環境：なし／あり（名前）
教員配布の本体ファームウェア修正版：受け取り済み／未受領
自分の本体：修正版書き込み済み／旧版／不明
困っている点：
~~~

パス中の自分の名前は伏せて構いません。秘密設定・APIキー・パスワード・生のシリアルログは提出しません。

## 8．授業の作業を再開する条件

### 8-1．PCでの作業

手順7が完了したPCを用いて、確認済みのGit・PlatformIOで授業の作業を再開します。  
別PCへ移る場合は、そのPCでもこのマニュアルの安全対策手順を実施します。

### 8-2．本体のファームウェア修正版について

教員側での本体書き込み・動作テストは成功しています。これは学生の本体にも自動で反映されたという意味ではありません。  
教員から配布された修正版の授業用プロジェクトを使います。配布元や、自分が加えた変更がある場合の自分のPCへの取り込み方などについては、[スタックチャン AI会話マニュアル_授業版.md](https://github.com/okana2ki/AI_StackChan_Ex_OkaSeminar2/blob/main/%E3%82%B9%E3%82%BF%E3%83%83%E3%82%AF%E3%83%81%E3%83%A3%E3%83%B3%20AI%E4%BC%9A%E8%A9%B1%E3%83%9E%E3%83%8B%E3%83%A5%E3%82%A2%E3%83%AB_%E6%8E%88%E6%A5%AD%E7%89%88.md#%E7%AC%AC7%E7%AB%A0%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%A0%E3%81%AE%E5%85%A5%E6%89%8B%E3%81%A8%E9%85%8D%E7%BD%AE) や [GitHub_Desktop_学生用手順書.md](https://github.com/okana2ki/AI_StackChan_Ex_OkaSeminar2/blob/main/GitHub_Desktop_%E5%AD%A6%E7%94%9F%E7%94%A8%E6%89%8B%E9%A0%86%E6%9B%B8.md) を参照。不明な点がある場合は、何も考えずに既存ファイルを上書きするのではなく、AIや教員に相談します。

同じPowerShellで、手順6-2のプロジェクトフォルダーにいることを確認して次を実行すると、プログラムの修正箇所を確認できます。

~~~powershell
Select-String -LiteralPath firmware/src/llm/Gemini/GeminiLive.cpp -Pattern 'webSocket.beginSslWithCA'
Select-String -LiteralPath firmware/src/rootCA/rootCAgoogleGemini.h -Pattern 'SHA-256'
~~~

pull origin操作をして修正版を自分のPCに取り込む前に上記を実行すると、何も表示されませんが、修正版を取り込んだ後で上記を実行すると、
一つ目にCA指定の接続呼び出し、二つ目にGTS Root R1〜R4の4つの指紋が表示されることが確認できます。
ファイルがない、表示が違う場合は、教員に相談します。
この文字列確認だけで配布物の真正性や本体の動作を証明するものではありません。

各自のPCの安全対策完了だけでは、スタックチャン本体内のプログラムは変わりません。
通常の授業の書き込み操作で修正版を本体に反映します。  
今回の安全対策はプログラムの修正です。設定を変えない場合は、Upload Filesystemを実行する必要はありません。これは既存設定を上書きする操作になります。

再開条件は「各自のPCの安全対策確認」と「自分の本体に安全対策修正版ファームウェアが入っていること」の両方です。
教員側の動作テスト成功と、各自の実機での不正証明書拒否の専用検査は別です。この文書は後者の実施済みを意味しません。

今回の安全対策の修正は、プログラムの修正およびそれに伴うマニュアルの追加修正を含みますが、[GitHub_Desktop_学生用手順書.md](https://github.com/okana2ki/AI_StackChan_Ex_OkaSeminar2/blob/main/GitHub_Desktop_%E5%AD%A6%E7%94%9F%E7%94%A8%E6%89%8B%E9%A0%86%E6%9B%B8.md) の4章に記載の Pull origin 操作により、プログラムの更新とマニュアルの更新の両方を自分のパソコンに取り込むことができます。

## 9．よくあるつまずき

| 表示・状況 | 対応 |
|---|---|
| Pythonやpioが見つからない | 手順4のPlatformIO Core CLIとPython Executableを確認。推測のパスを使わない |
| PowerShellを閉じてしまった | 手順5の$pioPython設定をやり直し、必要なら手順6-2の場所設定もやり直す |
| 更新したのにGitが古い | 新しくPowerShellを開き、where.exe gitの結果を教員に伝える |
| 検査サイトが時間切れ | 証明書を拒否した証拠にならないため未確認。ネットワークを確認して再検査 |
| Gitの検査で404・repository not found | TLS接続後のエラーなので、証明書拒否の合格にしない |
| requestsが見つからない、Python検査にSTOP | Pythonの選択と環境を教員に相談；検証を無効にしない |
| Python 3.10以下 | 手順を止め、サポート中のPythonを使う環境への移行を教員と相談 |
| 本体が返事をしない | Wi-Fi・時刻・Gemini無料枠を確認 |

## 根拠資料と更新について（2026-10-27確認）

本文に必要なコマンド・判定はすべて記載しています。以下は根拠を確認したい場合の資料です。

- [Git for Windows：今回の修正版](https://github.com/git-for-windows/git/releases/tag/v2.56.0.windows.3)
- [Python公式：pip・certifiとハッシュ付き更新](https://discuss.python.org/t/information-for-python-users-regarding-emudhra-emsign-ca-certificate-security-incident/109576)
- [接続検査の提供元](https://emudhra.we-have-a-problem.com/)
- [PlatformIOの環境情報](https://docs.platformio.org/en/latest/core/userguide/system/cmd_info.html)

Python公式はPython本体の修正版（3.11.18、3.12.16、3.13.18、3.14.10、3.15.2）も案内しています。  
本文のpip・certifiの更新と接続検査は、使用中のダウンロード環境の確認です。Python本体や別環境まで更新したことにはなりません。  
Python本体の更新・PlatformIO環境の移行は、固定された授業環境を壊さないようAIや教員と相談しながら進める必要があります。学生が自己判断で環境を作り直すのは避けて下さい。
