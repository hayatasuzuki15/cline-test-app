#!/bin/bash
# テスト実行スクリプト

# 仮想環境が有効化されていることを確認
if [ -z "$VIRTUAL_ENV" ]; then
    echo "仮想環境を有効化してください"
    exit 1
fi

# プロジェクトのルートディレクトリに移動
cd "$(dirname "$0")"

# PYTHONPATHを設定
export PYTHONPATH=.

# テストの実行
pytest tests/clock_in_test/test_clock_in.py -v
