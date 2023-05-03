from random import choice

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from keyboards.game_kb import letters_kb, GameAction, restart

router = Router()


class Gallows:
    def __init__(self):
        self.words = ['азбука', 'телеграмм', 'пользователь', 'визитер', 'паулина', 'сабля']
        self.letters = [
            'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и',
            'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
            'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь',
            'э', 'ю', 'я'
        ]
        self.choice_letters = []
        self.lives = 10
        self.word = choice(self.words)

    def add_letter(self, letter):
        if letter in self.word:
            self.choice_letters.append(letter)
        else:
            self.lives -= 1
        self.letters.remove(letter)

    def loss(self):
        if self.lives == 0:
            return True
        return False

    def win(self):
        for letter in self.word:
            if letter not in self.choice_letters:
                return False
        return True

    def field(self):
        text_word = ''
        text_lives = ''
        field = ''
        if self.win():
            field = 'Победа!!!\nВы угадали слово: {word}'.format(
                word=self.word
            )
        elif self.loss():
            field = 'Вы проиграли(\nЗагаданное слово: {word}'.format(
                word=self.word
            )
        else:
            for _ in range(self.lives):
                text_lives += '🧡'
            for letter in self.word:
                if letter in self.choice_letters:
                    text_word += letter
                else:
                    text_word += '🟩'
            field = 'Слово: {word}\n\nЖизни: {lives}'.format(
                word=text_word,
                lives=text_lives
            )
        return field


@router.message(Command("game"))
async def cmd_game(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text='Пример простой игры "Виселица". Игры можно использовать в обучающих целях или в качестве рекламной акции'
    )
    game = Gallows()
    await message.answer(
        text=game.field(),
        reply_markup=letters_kb(game.letters)
    )
    await state.update_data(game=game)


@router.callback_query(GameAction.filter(F.action == 'restart'))
async def cmd_game(callback: CallbackQuery, state: FSMContext):
    game = Gallows()
    await callback.message.edit_text(
        text=game.field(),
        reply_markup=letters_kb(game.letters)
    )
    await state.update_data(game=game)
    await callback.answer()


@router.callback_query(GameAction.filter(F.action == 'letter'))
async def cancel_send(callback: CallbackQuery, callback_data: GameAction, state: FSMContext):
    game_data = await state.get_data()
    game: Gallows = game_data['game']

    game.add_letter(callback_data.letter)

    if game.win() or game.loss():
        await callback.message.edit_text(
            text=game.field(),
            reply_markup=restart()
        )
        await state.clear()
    else:
        await callback.message.edit_text(
            text=game.field(),
            reply_markup=letters_kb(game.letters)
        )
        await state.update_data(game=game)
    await callback.answer()



