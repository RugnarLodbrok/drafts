"""
https://leetcode.com/problems/interleaving-string/

Given s1, s2, s3, find whether s3 is formed by the interleaving of s1 and s2.

Example 1:

Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
Output: true
Example 2:

Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
Output: false
"""


def interleaving_naive(s1, s2, s3):
    len1 = len(s1)
    len2 = len(s2)
    len3 = len(s3)

    def recur(i, j, k):
        while k < len3:
            if i < len1 and j < len2 and s1[i] == s2[j]:
                if s1[i] != s3[k]:
                    return False
                return recur(i + 1, j, k + 1) or recur(i, j + 1, k + 1)

            elif i < len1 and s1[i] == s3[k]:
                k += 1
                i += 1
                continue

            elif j < len2 and s2[j] == s3[k]:
                k += 1
                j += 1
                continue
            else:
                return False

        return (i == len1) and (j == len2) and (k == len3)

    return recur(0, 0, 0)


if __name__ == '__main__':
    interleaving = interleaving_naive
    print(interleaving(s1="aabcc", s2="dbbca", s3="aadbbcbcac"))
    print(interleaving(s1="aabcc", s2="dbbca", s3="aadbbbaccc"))
    # print(interleaving(*[
    #     "bbbbbabbbbabaababaaaabbababbaaabbabbaaabaaaaababbbababbbbbabbbbababbabaabababbbaabababababbbaaababaa",
    #     "babaaaabbababbbabbbbaabaabbaabbbbaabaaabaababaaaabaaabbaaabaaaabaabaabbbbbbbbbbbabaaabbababbabbabaab",
    #     "babbbabbbaaabbababbbbababaabbabaabaaabbbbabbbaaabbbaaaaabbbbaabbaaabababbaaaaaabababbababaababbababbbababbbbaaaabaabbabbaaaaabbabbaaaabbbaabaaabaababaababbaaabbbbbabbbbaabbabaabbbbabaaabbababbabbabbab"]))
