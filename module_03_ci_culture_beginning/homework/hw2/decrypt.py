import sys
import unittest


def decrypt(encryption: str) -> str:
    result: list = []
    dots: int = 0
    for symbol in encryption:
        if symbol != '.':
            result.append(symbol)
            dots = 0
            continue

        dots += 1
        if dots == 2 and result:
            result.pop()
            dots = 0

    return ''.join(result)


class TestDecrypt(unittest.TestCase):
    def test_no_dots(self):
        self.assertEqual(decrypt("абра-кадабра."), "абра-кадабра")

    def test_two_dots(self):
        self.assertEqual(decrypt("абраа..-кадабра"), "абра-кадабра")

    def test_two_dots_at_start(self):
        self.assertEqual(decrypt("абраа..-.кадабра"), "абра-кадабра")

    def test_dots_and_dash(self):
        self.assertEqual(decrypt("абра--..кадабра"), "абра-кадабра")

    def test_three_dots(self):
        self.assertEqual(decrypt("абрау...-кадабра"), "абра-кадабра")

    def test_only_dots(self):
        self.assertEqual(decrypt("абра........"), "")
        self.assertEqual(decrypt("."), "")
        self.assertEqual(decrypt("1......................."), "")

    def test_edge_cases(self):
        self.assertEqual(decrypt("абр......a."), "a")
        self.assertEqual(decrypt("1..2.3"), "23")


if __name__ == '__main__':
    data: str = sys.stdin.read()
    decryption: str = decrypt(data)
    print(decryption)
