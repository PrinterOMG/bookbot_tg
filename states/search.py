import os

from aiogram.types import Message, InputFile, InputMedia
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from loader import dp, languages_worker, archive_worker
from keyboards.inline import get_move_keyboard, get_cancel_keyboard, get_book_buy_keyboard
from utils.csv_worker import search, create_txt_with_books, get_book


class ArchiveBookBuy(StatesGroup):
    search_input = State()
    book_input = State()


@dp.message_handler(state=ArchiveBookBuy.search_input)
async def search_input(message: Message, state: FSMContext):
    value = message.text
    main_msg = (await state.get_data("main_msg"))["main_msg"]
    search_type = (await state.get_data("type"))["type"]

    text = languages_worker.get_text_on_user_language(message.from_user.id,
                                                      "bookFile, searchError, searchTextResult, searchFileResult, bookArchiveFormat")

    result = await search(text["bookFile"], search_type, value)
    print(result)

    if result["title"]:
        books = list()
        for i in result["title"].keys():
            id = result["id"][i]
            title = result["title"][i]
            author = result["author"][i]
            genre = result["genre"][i]
            year = result["year"][i]
            price = result["price"][i]

            books.append(
                text["bookArchiveFormat"].format(id=id, title=title, author=author, genre=genre, year=year,
                                                 price=price))

        books = "\n".join(books)

        if len(result["title"].values()) > 10:
            filename = await create_txt_with_books(books, message.from_user.id)
            file = InputFile(filename)

            await main_msg.answer_document(file)
            main_msg = await main_msg.answer(text["searchFileResult"],
                                             reply_markup=await get_cancel_keyboard(message.from_user.id))
            os.remove(filename)
        else:
            await main_msg.edit_text(text["searchTextResult"].format(books=books),
                                     reply_markup=await get_cancel_keyboard(message.from_user.id))
    else:
        await main_msg.edit_text(text["searchError"],
                                 reply_markup=await get_move_keyboard(message.from_user.id, to="archive"))
        await message.delete()
        await state.finish()
        return

    await message.delete()
    await state.update_data(main_msg=main_msg, books=result)
    await ArchiveBookBuy.book_input.set()


@dp.message_handler(state=ArchiveBookBuy.book_input)
async def book_input(message: Message, state: FSMContext):
    book_id = message.text
    books = (await state.get_data("books"))["books"]
    main_msg = (await state.get_data("main_msg"))["main_msg"]

    text = languages_worker.get_text_on_user_language(message.from_user.id,
                                                      "bookFile, bookInputError, bookBuyMenu, bookArchiveFormat")

    if not book_id.isdigit() or (int(book_id) not in books["id"].values()):
        await main_msg.edit_text(text["bookInputError"],
                                 reply_markup=await get_move_keyboard(message.from_user.id, to="archive"))
    else:
        book_id = int(book_id)
        book = await get_book(text["bookFile"], book_id)
        print(book)

        book_str = text["bookArchiveFormat"].format(id=book_id, title=book["title"],
                                                    genre=book["genre"],
                                                    author=book["author"], year=book["year"],
                                                    price=book["price"])

        await main_msg.edit_text(text["bookBuyMenu"].format(book=book_str),
                                 reply_markup=await get_book_buy_keyboard(message.from_user.id, book_id))

        is_book = archive_worker.is_book_in_base(book_id)
        if not is_book:
            archive_worker.add_book(book)

        archive_worker.update_appeal(book_id)

    await state.finish()
    await message.delete()
