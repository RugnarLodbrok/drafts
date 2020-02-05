"""
https://leetcode.com/problems/substring-with-concatenation-of-all-words/

You are given a string, s, and a list of words, words, that are all of the same length.
Find all starting indices of substring(s) in s that is a concatenation of each word in
words exactly once and without any intervening characters.


Example 1:

Input:
  s = "barfoothefoobarman",
  words = ["foo", "bar"]
Output: [0, 9]
Explanation: Substrings starting at index 0 and 9 are "barfoo" and "foobar" respectively.
The output order does not matter, returning [9, 0] is fine too.


Example 2:

Input:
  s = "wordgoodgoodgoodbestword",
  words = ["word", "good", "best", "word"]
Output: []

"""
import re
from collections import defaultdict
from typing import List


def find_substring(s: str, words: List[str]) -> List[int]:  # 21 us
    """
    fastest so far
    """
    ret = []
    if not words:
        return ret
    total_w_len = sum(map(len, words))
    ww = defaultdict(int)
    for w in words:
        ww[w] += 1

    def recur(i, cnt):  # pass i instead of cut string to avoid copying memory
        if not cnt:
            return True
        for w, c in ww.items():
            if not c:
                continue
            if s[i:].startswith(w):  # still we copy here :(
                ww[w] -= 1
                if recur(i + len(w), cnt - 1):
                    ww[w] += 1
                    return True
                ww[w] += 1
        return False

    for i, c in enumerate(s):
        if total_w_len + i > len(s):
            break
        if recur(i, len(words)):
            ret.append(i)
    return ret


def find_substring_re(s: str, words: List[str]) -> List[int]:  # 33 us
    """
    non-recursive, based on regex
    """
    ret = []
    if not words:
        return ret
    total_w_len = sum(map(len, words))
    ww = defaultdict(int)
    for w in words:
        ww[w] += 1

    def recur(i):  # pass i instead of cut string to avoid copying memory
        words = {**ww}
        while True:
            words_pattern = "|".join(w for w, c in words.items() if c)
            if not words_pattern:
                return True
            match = re.match(fr"^.{{{i}}}({words_pattern})", s)
            if not match:
                return False
            w = match.group(1)
            words[w] -= 1
            i += len(w)

    for m in re.finditer("(" + "|".join(ww) + ")", s):
        i = m.start()
        if total_w_len + i > len(s):
            break
        if recur(i):
            ret.append(i)
    return ret


def find_substring_non_recur(s: str, words: List[str]) -> List[int]:  # 60us
    """
    the slowest but doesnt fail when len(words) > python stack size
    """
    ret = []
    if not words:
        return ret
    ww = defaultdict(int)
    for w in words:
        ww[w] += 1
    ww = [dict(word=w, count=c) for w, c in ww.items()]
    total_w_len = sum(map(len, words))

    def non_recur(i, cnt):
        stack = [{"i": i}]  # (j)
        ans = False
        while stack:
            if len(stack) > cnt:
                ans = True
            state = stack[-1]

            state.setdefault('j', 0)
            state.setdefault('recur', False)
            if state['recur']:
                ww[state['j']]['count'] += 1
                state['j'] += 1
            while state['j'] < len(ww):
                w = ww[state['j']]
                if not w['count']:
                    state['j'] += 1
                    continue
                if s[state['i']:].startswith(w['word']):
                    w['count'] -= 1
                    state['recur'] = True
                    stack.append(dict(i=state['i'] + len(w['word'])))
                    break
                state['j'] += 1
            else:
                stack.pop(-1)
        return ans

    cnt = len(words)
    for i, c in enumerate(s):
        if total_w_len + i > len(s):
            break
        if non_recur(i, cnt):
            ret.append(i)
    return ret


def main():
    print(find_substring_re(s="barfoothebarfoobarman", words=["foo", "bar"]))  # this was used for the benchmark
    print(find_substring_re(s="a" * 36, words=["a"] * 8))
    print(find_substring_re(s="barfoothebarfoobarman", words=[]))
    print(find_substring_re("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]))
    print(find_substring_re("a" * 100, ["a"] * 101))
    print(find_substring_re("a" * 500, ["a"] * 499))
    print(find_substring_re("a" * 5000, ["a"] * 5001))


if __name__ == '__main__':
    main()
