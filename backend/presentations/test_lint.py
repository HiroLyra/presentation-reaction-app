# reviewdogテスト用ファイル
import os
import sys

def unused_function():
    x = 1
    y = 2
    # xは使われていない
    return y


# 長すぎる行（Flake8は1行79文字まで）
very_long_variable_name_that_exceeds_the_line_length_limit = "This is a very long string that will definitely exceed the recommended line length"
