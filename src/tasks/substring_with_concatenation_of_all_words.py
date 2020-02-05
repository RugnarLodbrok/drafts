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

from typing import List


def find_substring(s: str, words: List[str]) -> List[int]:
    def recur(i, words):
        if not words:
            return True
        for j, w in enumerate(words):
            if s[i:].startswith(w):
                words2 = words[:]
                words2.pop(j)
                if recur(i + len(w), words2):
                    return True
        return False

    ret = []
    for i, c in enumerate(s):
        if recur(i, words):
            ret.append(i)
    return ret


def main():
    print(find_substring(s="barfoothebarfoobarman", words=["foo", "bar"]))


if __name__ == '__main__':
    main()
