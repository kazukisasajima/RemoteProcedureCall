# RemoteProcedureCall

## 概要

クライアントとサーバが異なるプログラミング言語で書かれていても、クライアントプログラムがサーバ上の機能を呼び出せるRPC(remote procedure call)のシステムを作成しました。<br>
このプロジェクトはコンピュータサイエンス学習サービス[Recursion](https://recursion.example.com)の課題で取り組みました。


## サーバーによるRPC関数の提供

- floor(double x): 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
- nroot(int n, int x): 方程式 rn = x における、r の値を計算する。
- reverse(string s): 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
- validAnagram(string str1, string str2): 2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
- sort(string[] strArr): 文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。


## 実行方法

- 以下のコマンドを使用して、実行できます。

```sh
python3 server.py
```
```sh
python3 client.py
```
```sh
node client.js
```
クライアント側のターミナルで1~5の数字を入力してjsonファイルを呼び出す。<br>
1~5の数字はrequest1.json~request5.jsonのファイル名に対応している。

### 注意
- 名前付きパイプ（UNIXソケット）を使用しているため、Windowsの標準的なコマンドプロンプトやPowerShellでは動作しません。
- このアプリケーションはLinuxまたはWSL（Windows Subsystem for Linux）環境で動作します。
