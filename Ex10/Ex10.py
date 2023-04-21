class TestShortPhrase:

    def test_check_len(self):
        phrase = input("Напишите фразу короче 15 символов: ")
        assert len(phrase) < 15, "Фраза больше 15 символов"