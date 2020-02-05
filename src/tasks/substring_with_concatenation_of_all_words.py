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
from collections import defaultdict
from typing import List


def find_substring(s: str, words: List[str]) -> List[int]:
    ret = []
    if not words:
        return ret
    ww = defaultdict(int)
    for w in words:
        ww[w] += 1

    def recur(i, cnt):
        if not cnt:
            return True
        for w, c in ww.items():
            if not c:
                continue
            if s[i:].startswith(w):
                ww[w] -= 1
                if recur(i + len(w), cnt - 1):
                    ww[w] += 1
                    return True
                ww[w] += 1
        return False

    cnt = len(words)
    for i, c in enumerate(s):
        if recur(i, cnt):
            ret.append(i)
    return ret


def find_substring_non_recur(s: str, words: List[str]) -> List[int]:
    ret = []
    if not words:
        return ret
    ww = defaultdict(int)
    for w in words:
        ww[w] += 1
    ww = [dict(word=w, count=c) for w, c in ww.items()]

    def non_recur(i, cnt):
        stack = [{"i": i}]  # (j)

        def iteration(state):
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
                    return dict(i=state['i'] + len(w['word']))
                state['j'] += 1
            else:
                return False

        ans = False
        while stack:
            if len(stack) > cnt:
                ans = True
            state = stack[-1]
            new_state = iteration(state)
            if new_state:
                stack.append(new_state)
            else:
                stack.pop(-1)
        return ans

    cnt = len(words)
    for i, c in enumerate(s):
        if non_recur(i, cnt):
            ret.append(i)
    return ret


def main():
    print(find_substring_non_recur(s="barfoothebarfoobarman", words=["foo", "bar"]))
    print(find_substring_non_recur(s="a" * 36, words=["a"] * 8))
    print(find_substring_non_recur(s="barfoothebarfoobarman", words=[]))
    print(find_substring_non_recur("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]))
    print(find_substring_non_recur("a" * 1000, ["a"] * 1001))
    # print(find_substring_non_recur("a" * 5000, ["a"] * 5001))


if __name__ == '__main__':
    main()
