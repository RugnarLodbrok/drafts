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


def main():
    print(find_substring(s="barfoothebarfoobarman", words=["foo", "bar"]))
    print(find_substring(s="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", words=["a", "a", "a", "a", "a", "a", "a", "a"]))
    print(find_substring(s="barfoothebarfoobarman", words=[]))
    print(find_substring("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]))


if __name__ == '__main__':
    main()
